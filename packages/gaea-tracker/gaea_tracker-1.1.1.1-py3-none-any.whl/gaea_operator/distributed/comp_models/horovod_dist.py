#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : horovod_dist.py    
@Author        : yanxiaodong
@Date          : 2022/12/29
@Description   :
"""
import warnings
from numbers import Number
from typing import Any, List, Optional, Union, cast, Tuple

from gaea_operator.engine import TORCH_BACKEND
from gaea_operator.plugin import Device, TTensor, horovod, torch, Model, Optimizer, Module
from gaea_operator.utils.distribution import ReduceOP

from .base import ComputationModel

if horovod is None:
    has_hvd_dist_support = False
else:
    has_hvd_dist_support = True
    import horovod.torch as hvd


class _HorovodDistModel(ComputationModel):
    """
    Private class for `Horovod` distributed computation model.
    """
    available_backends = ('horovod',)

    @staticmethod
    def _get_hvd_rank() -> int:
        try:
            rank = hvd.rank()
        except ValueError:
            rank = -1
        return rank

    @staticmethod
    def create_from_backend(model_type: str, backend: str) -> "_HorovodDistModel":
        if backend not in _HorovodDistModel.available_backends:
            raise ValueError(f"Backend should be one of '{_HorovodDistModel.available_backends}'")

        rank = _HorovodDistModel._get_hvd_rank()
        # hvd must be not initialized
        if rank > -1:
            raise RuntimeError("Can not re-initialize Horovod if it is already initialized")
        return _HorovodDistModel(model_type=model_type, backend=backend)

    def __init__(self, **kwargs) -> None:
        super(_HorovodDistModel, self).__init__(**kwargs)
        if self._backend is not None:
            self._create_from_backend(self._backend)

    def _create_from_backend(self, backend: str) -> None:
        self._backend = backend

        hvd.init()
        self._setup_attrs()

        if torch.cuda.is_available():
            torch.cuda.set_device(self.get_local_rank())

    def _compute_nproc_per_node(self) -> int:
        return hvd.local_size()

    def is_initialized(self) -> bool:
        try:
            hvd.size()
            is_init = True
        except ValueError:
            is_init = False
        return is_init

    def get_local_rank(self) -> int:
        return hvd.local_rank()

    def get_world_size(self) -> int:
        return hvd.size()

    def get_rank(self) -> int:
        return hvd.rank()

    def get_nproc_per_node(self) -> int:
        return cast(int, self._nproc_per_node)

    def get_nnodes(self) -> int:
        return cast(int, self._nnodes)

    def get_node_rank(self) -> int:
        return cast(int, self._node)

    def device(self) -> Device:
        if torch.cuda.is_available():
            index = self.get_local_rank()
            if index < self.get_local_rank():
                warnings.warn(
                    "Current device index is less than current local rank. "
                    "Please, make sure to call torch.cuda.set_device(local_rank)."
                )
            return torch.device(f"cuda:{index}")
        return torch.device("cpu")

    def _number_to_tensor(self, obj: Union[Number, float], device: Union[str, Device]) -> TTensor:
        tensor = torch.tensor(obj, device=device)
        return tensor

    def _tensor_to_number(self, obj: Union[List[TTensor], TTensor]) -> Union[List, Number, float]:
        if isinstance(obj, List):
            return obj
        else:
            if obj.numel() == 1:
                return obj.item()
            else:
                return obj.tolist()

    def _get_max_length(self, size: TTensor) -> int:
        size = self._do_all_reduce(size, op="MAX")
        return cast(int, size.item())

    def _encode_str(self, obj: str, device: Union[str, Device], retain: Optional[bool] = False) -> TTensor:
        obj_tensor = torch.tensor(bytearray(obj, "utf-8")).to(device)

        max_length = self._get_max_length(torch.tensor([len(obj_tensor)], device=device))

        padded_x = torch.zeros(max_length + 1, device=device, dtype=torch.long)
        padded_x[:len(obj_tensor)] = obj_tensor

        if retain:
            padded_x[-1] = max_length
        else:
            padded_x[-1] = len(obj_tensor)
        return padded_x

    def _decode_str(self, obj: Union[List[TTensor], TTensor]) -> Union[str, List[str]]:
        if isinstance(obj, List):
            all_string = []
            for tensor in obj:
                all_string.append(bytearray(tensor[:tensor[-1]].tolist()).decode("utf-8"))
            return all_string
        else:
            return bytearray(obj[: obj[-1]].tolist()).decode("utf-8")

    def _do_all_reduce(self, tensor: TTensor, op: str = "SUM") -> TTensor:
        if op in ReduceOP.horovod_manual_reduce_op_map():
            op_fn = ReduceOP.horovod_manual_reduce_op_map()[op]
            return self._do_manual_all_reduce(tensor, op_fn)
        if op not in ReduceOP.horovod_reduce_op_map():
            raise ValueError(f"Unsupported reduction operation: '{op}'")
        op = ReduceOP.horovod_reduce_op_map()[op]
        return hvd.allreduce(tensor, op=op)

    def _do_manual_all_reduce(self, tensor: TTensor, op: Any) -> TTensor:
        res = self._do_all_gather(tensor)
        res = torch.stack(res, dim=0)
        reduced_res = op(res, dim=0)
        if isinstance(reduced_res, TTensor):
            return reduced_res
        # output can also torch min/max_return_type: (min/max_vals, indices)
        return reduced_res[0]

    def _do_all_gather(self, tensor: TTensor) -> List:
        if self.get_world_size() < 2:
            return [tensor]
        if tensor.ndimension() == 0:
            tensor = tensor.unsqueeze(0)
        tensor = tensor.unsqueeze(0)
        tensor = hvd.allgather(tensor)
        tensor_tuple = torch.split(tensor, split_size_or_sections=1, dim=0)
        return [tensor.squeeze(0) for tensor in tensor_tuple]

    def _do_broadcast(self, tensor: TTensor, src: int) -> TTensor:
        return hvd.broadcast(tensor, root_rank=src)

    def auto_model(self, model: Model) -> Tuple[str, Model]:
        assert isinstance(model, Module), f'model should torch.nn.Module, but give {type(model)}'

        self._module = TORCH_BACKEND

        # Put model's parameters to device if its parameters are not on the device
        device = self.device()
        if not all([p.device == device for p in model.parameters()]):
            model.to(device)

        hvd.broadcast_parameters(model.state_dict(), root_rank=0)

        return self._module, model

    def auto_optim(self, optimizer: Optimizer) -> Optimizer:
        optimizer = hvd.DistributedOptimizer(optimizer)
        hvd.broadcast_optimizer_state(optimizer, root_rank=0)

        return optimizer

    def finalize(self) -> None:
        pass

    def barrier(self) -> None:
        pass
