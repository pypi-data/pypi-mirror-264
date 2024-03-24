#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : paddle_dist.py    
@Author        : yanxiaodong
@Date          : 2022/11/29
@Description   :
"""
import io
import pickle
import traceback
from numbers import Number
from argparse import Namespace
from typing import Any, List, Optional, Tuple, Union, cast, Dict, Callable

import numpy as np

from gaea_operator.engine import PADDLE_BACKEND
from gaea_operator.plugin import (Device, Layer, Model, Optimizer, PTensor,
                                   paddle)
from gaea_operator.utils.distribution import ReduceOP
from gaea_operator.utils import setup_logger

from .base import ComputationModel

if paddle is None:
    has_paddle_native_dist_support = False
else:
    has_paddle_native_dist_support = True


class _PaddleDistModel(ComputationModel):
    """
    Private class for Paddle native distributed computation model.
    """
    available_backends = ('paddle',)

    @staticmethod
    def create_from_backend(model_type: str,
                            backend: str,
                            is_collective: Optional[bool] = True,
                            find_unused_parameters: Optional[bool] = False) -> "_PaddleDistModel":
        if backend not in _PaddleDistModel.available_backends:
            raise ValueError(f"Backend should be one of '{_PaddleDistModel.available_backends}'")

        return _PaddleDistModel(model_type=model_type,
                                backend=backend,
                                is_collective=is_collective,
                                find_unused_parameters=find_unused_parameters)

    def __init__(self,
                 is_collective: Optional[bool] = True,
                 find_unused_parameters: Optional[bool] = False,
                 **kwargs) -> None:
        super(_PaddleDistModel, self).__init__(**kwargs)
        self._local_rank = None  # type: Optional[int]

        self.is_collective = is_collective
        self.find_unused_parameters = find_unused_parameters

        if self._backend is not None:
            self._create_from_backend(self._backend)

    def _create_from_backend(self, backend: str) -> None:
        self._backend = backend

        strategy = paddle.distributed.fleet.DistributedStrategy()
        strategy.find_unused_parameters = self.find_unused_parameters

        paddle.distributed.fleet.init(is_collective=self.is_collective, strategy=strategy)
        self._local_rank = paddle.distributed.fleet.local_rank()

        self._setup_attrs()

    def _compute_nproc_per_node(self) -> int:
        node_num = paddle.distributed.fleet.node_num()
        return int(self.get_world_size() / node_num)

    @staticmethod
    def setup_spawn_params(**spawn_kwargs: Any) -> Dict:
        nproc_per_node = spawn_kwargs.get("nproc_per_node")
        if nproc_per_node is None:
            nproc_per_node = paddle.device.cuda.device_count()
        if nproc_per_node < 1:
            raise ValueError(f"Argument nproc_per_node should positive, but given {nproc_per_node}")

        join = spawn_kwargs.get("join", True)
        daemon = spawn_kwargs.get("daemon", False)
        communicate_backend = spawn_kwargs.get("communicate_backend", "NCCL")

        params = {
            "communicate_backend": communicate_backend,
            "nproc_per_node": nproc_per_node,
            "join": join,
            "daemon": daemon,
        }

        return {k: v for k, v in params.items() if v is not None}

    @staticmethod
    def _dist_worker_task_fn(
            backend: str,
            communicate_backend: str,
            model_type: str,
            fn: Callable,
            args: Namespace
    ) -> None:
        from gaea_operator.distributed.utils import _set_model

        model = _PaddleDistModel.create_from_backend(model_type, backend)
        _set_model(model)

        logger = setup_logger(__name__)
        try:
            fn(args)
        except Exception:
            logger.error(traceback.format_exc())
            for handle in logger.handlers:
                handle.close()
            exit(1)

    @staticmethod
    def spawn(
            backend: str,
            model_type: str,
            fn: Callable,
            args: Namespace,
            nproc_per_node: int = 1,
            communicate_backend: Optional[str] = "NCCL",
            **kwargs: Any,
    ) -> None:
        spawn_kwargs = {
            "join": kwargs.get("join", True),
            "daemon": kwargs.get("daemon", False),
        }

        start_processes = paddle.distributed.spawn

        start_processes(
            _PaddleDistModel._dist_worker_task_fn,
            nprocs=nproc_per_node,
            args=(
                backend,
                communicate_backend,
                model_type,
                fn,
                args,
            ),
            **spawn_kwargs,
        )

    def is_initialized(self) -> bool:
        return paddle.distributed.is_initialized()

    def get_local_rank(self) -> int:
        _local_size = self._local_rank
        if _local_size is None:
            self._local_rank = 0
        return int(self._local_rank)

    def get_world_size(self) -> int:
        _world_size = paddle.distributed.fleet.world_size()
        if _world_size is None:
            _world_size = 1
        return _world_size

    def get_rank(self) -> int:
        _rank = paddle.distributed.fleet.rank()
        if _rank is None:
            _rank = 0
        return _rank

    def get_nproc_per_node(self) -> int:
        return cast(int, self._nproc_per_node)

    def get_nnodes(self) -> int:
        return cast(int, self._nnodes)

    def get_node_rank(self) -> int:
        return cast(int, self._node)

    def device(self) -> Device:
        return paddle.set_device(paddle.get_device())

    def _number_to_tensor(self, obj: Union[Number, float], device: Union[str, Device]) -> PTensor:
        tensor = paddle.to_tensor(obj, place=device)
        return tensor

    def _tensor_to_number(self, obj: Union[List[PTensor], PTensor]) -> Union[List, Number, float]:
        if isinstance(obj, List):
            return obj
        else:
            if obj.numel() == 1:
                return obj.item()
            else:
                return obj.tolist()

    def _get_max_length(self, size: PTensor) -> int:
        size = self._do_all_reduce(size, op="MAX")
        return cast(int, size.item())

    def _encode_str(self, obj: str, device: Union[str, Device], retain: Optional[bool] = False) -> PTensor:
        _pickler = pickle.Pickler
        f = io.BytesIO()
        _pickler(f).dump(obj)
        data = np.frombuffer(f.getvalue(), dtype=np.uint8)
        obj_tensor = paddle.to_tensor(data, place=device)
        obj_tensor = paddle.cast(obj_tensor, 'int32')

        max_length = self._get_max_length(obj_tensor.numel())

        padded_x = paddle.zeros([max_length + 1], dtype='int32')
        padded_x[:len(obj_tensor)] = obj_tensor
        if retain:
            padded_x[-1] = max_length
        else:
            padded_x[-1] = len(obj_tensor)
        return padded_x

    def _decode_str(self, obj: Union[List[PTensor], PTensor]) -> Union[str, List[str]]:
        if isinstance(obj, List):
            all_string = []
            for tensor in obj:
                tensor = paddle.cast(tensor, 'uint8')
                _unpickler = pickle.Unpickler
                data = tensor.numpy()
                all_string.append(_unpickler(io.BytesIO(data[:int(data[-1])])).load())
            return all_string
        else:
            tensor = paddle.cast(obj, 'uint8')
            _unpickler = pickle.Unpickler
            data = tensor.numpy()
            return _unpickler(io.BytesIO(data[:int(data[-1])])).load()

    def _do_all_reduce(self, tensor: PTensor, op: str = "SUM") -> PTensor:
        if self.get_world_size() < 2:
            return tensor
        if op not in ReduceOP.paddle_reduce_op_map():
            raise ValueError(f"Unsupported reduction operation: '{op}'")
        reduce_op = ReduceOP.paddle_reduce_op_map()[op]
        paddle.distributed.all_reduce(tensor, reduce_op)
        return tensor

    def _do_all_gather(self, tensor: PTensor) -> List:
        if self.get_world_size() < 2:
            return [tensor]
        tensor_list = []  # type: List[PTensor]
        if isinstance(tensor, list):
            paddle.distributed.all_gather_object(tensor_list, tensor)
        else:
            paddle.distributed.all_gather(tensor_list, tensor)
        return tensor_list

    def _do_broadcast(self, tensor: PTensor, src: int) -> PTensor:
        if self.get_world_size() < 2:
            return tensor
        paddle.distributed.broadcast(tensor, src=src)
        return tensor

    def auto_model(self, model: Model) -> Tuple[str, Model]:
        assert isinstance(model, Layer), f'model should paddle.nn.Layer, but give {type(model)}'

        self._module = PADDLE_BACKEND
        model = paddle.distributed.fleet.distributed_model(model)
        return self._module, model

    def auto_optim(self, optimizer: Optimizer) -> Optimizer:
        if isinstance(optimizer, List):
            for i in range(len(optimizer)):
                optimizer[i] = paddle.distributed.fleet.distributed_optimizer(optimizer[i])
        else:
            optimizer = paddle.distributed.fleet.distributed_optimizer(optimizer)
        return optimizer

    def finalize(self) -> None:
        pass

    def barrier(self) -> None:
        if self.is_initialized():
            paddle.distributed.barrier()
