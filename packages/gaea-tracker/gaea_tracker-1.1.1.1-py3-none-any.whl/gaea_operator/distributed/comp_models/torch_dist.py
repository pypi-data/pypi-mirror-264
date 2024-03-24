#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : torch_dist.py    
@Author        : yanxiaodong
@Date          : 2022/12/27
@Description   :
"""
import os
import warnings
from numbers import Number
from typing import Any, Dict, List, Optional, Tuple, Union, cast, Callable
from argparse import Namespace

from packaging.version import Version

from gaea_operator.engine import TORCH_BACKEND
from gaea_operator.plugin import (Device, Model, Module, Optimizer, TTensor,
                                  torch)
from gaea_operator.utils.distribution import ReduceOP

from .base import ComputationModel

if torch is None:
    has_torch_native_dist_support = False
    NCCL = None
    GLOO = None
    MPI = None
else:
    has_torch_native_dist_support = True
    NCCL = torch.distributed.Backend.NCCL
    GLOO = torch.distributed.Backend.GLOO
    MPI = torch.distributed.Backend.MPI


class _TorchDistModel(ComputationModel):
    """
    Private class for PyTorch native distributed computation model.
    """
    available_backends = ('torch',)

    if torch is not None:
        _reduce_op_map = {
            "SUM": torch.distributed.ReduceOp.SUM,
            "OR": torch.distributed.ReduceOp.BOR,
            "MIN": torch.distributed.ReduceOp.MIN,
            "MAX": torch.distributed.ReduceOp.MAX,
            "PRODUCT": torch.distributed.ReduceOp.PRODUCT,
            "AND": torch.distributed.ReduceOp.BAND,
        }

    @staticmethod
    def create_from_backend(model_type: str,
                            backend: str,
                            communicate_backend: Optional[str] = None,
                            init_method: Optional[str] = None,
                            world_size: Optional[int] = None,
                            rank: Optional[int] = None) -> "_TorchDistModel":
        if backend not in _TorchDistModel.available_backends:
            raise ValueError(f"Backend should be one of '{_TorchDistModel.available_backends}'")

        if communicate_backend not in (NCCL, GLOO, MPI):
            raise ValueError(f"Communicate backend should be one of '({NCCL}, {GLOO}, {MPI})'")

        if torch.distributed.is_available() and torch.distributed.is_initialized():
            raise RuntimeError("Can not create new distributed process group if default one is already initialized")

        if init_method is None:
            if world_size is not None or rank is not None:
                raise ValueError("Arguments rank and world_size should be None if no init_method is provided")
        else:
            has_rank = rank is not None
            has_ws = world_size is not None
            if (has_rank or has_ws) and (not has_rank or not has_ws):
                raise ValueError(f"Both rank and world_size should be provided, but given {rank} and {world_size}")

        return _TorchDistModel(model_type=model_type, backend=backend, communicate_backend=communicate_backend,
                               init_method=init_method, world_size=world_size, rank=rank)

    def __init__(self,
                 communicate_backend: Optional[str] = 'NCCL',
                 timeout: Optional[int] = None,
                 init_method: Optional[str] = None,
                 world_size: Optional[int] = None,
                 rank: Optional[int] = None,
                 **kwargs) -> None:
        super(_TorchDistModel, self).__init__(**kwargs)
        self._local_rank = None  # type: Optional[int]

        self._env_backup = None  # type: Optional[Dict[str, str]]
        self._master_port = None  # type: Optional[int]
        self._master_addr = None  # type: Optional[int]
        self._init_method = None  # type: Optional[int]

        if communicate_backend == 'NCCL' or communicate_backend == "nccl":
            communicate_backend = NCCL
        if communicate_backend == "GLOO" or communicate_backend == "goll":
            communicate_backend = GLOO
        if communicate_backend == "MPI" or communicate_backend == "mpi":
            communicate_backend = MPI

        if self._backend is not None:
            self._create_from_backend(self._backend, communicate_backend=communicate_backend, timeout=timeout,
                                      init_method=init_method, world_size=world_size, rank=rank)

    def _create_from_backend(self,
                             backend: str,
                             communicate_backend: Optional[str] = None,
                             timeout: Optional[int] = None,
                             init_method: Optional[str] = None,
                             world_size: Optional[int] = None,
                             rank: Optional[int] = None) -> None:
        self._backend = backend

        if communicate_backend == NCCL and not torch.cuda.is_available():
            raise RuntimeError("Nccl backend is required but no cuda capable devices")

        self._setup_env_vars(rank=rank, world_size=world_size)

        init_pg_kwargs: Dict[str, Any] = {}
        if timeout is not None:
            init_pg_kwargs["timeout"] = timeout

        if init_method is None:
            init_method = "env://"

        if "env" not in init_method:
            init_pg_kwargs["world_size"] = int(os.environ["WORLD_SIZE"])
            init_pg_kwargs["rank"] = int(os.environ["RANK"])
        self._init_method = init_method

        torch.distributed.init_process_group(communicate_backend, init_method=init_method, **init_pg_kwargs)

        if torch.cuda.is_available():
            torch.cuda.set_device(self._local_rank)

        if backend == NCCL and Version(torch.__version__) >= Version("1.8.0"):
            device_ids = [torch.cuda.current_device()]
            torch.distributed.barrier(device_ids=device_ids)
        else:
            # For older versions there is no device_ids arg
            torch.distributed.barrier()

        self._setup_attrs()

    def _setup_env_vars(self, rank: Optional[int] = None, world_size: Optional[int] = None) -> None:
        self._env_backup = os.environ.copy()

        env_vars = ["RANK", "LOCAL_RANK", "WORLD_SIZE"]
        all_env_vars_defined = [k in os.environ for k in env_vars]
        # check if all necessary env vars are set
        # if partially defined raise an error
        if any(all_env_vars_defined) and not all(all_env_vars_defined):
            raise RuntimeError(f"PyTorch distributed configuration should define env variables '{env_vars}'")

        os.environ["RANK"] = os.environ.get("RANK", f"{rank if rank is not None else 0}")
        os.environ["WORLD_SIZE"] = os.environ.get("WORLD_SIZE", f"{world_size if world_size is not None else 1}")
        os.environ["LOCAL_RANK"] = os.environ.get("LOCAL_RANK", "0")
        os.environ["MASTER_PORT"] = os.environ.get("MASTER_PORT", "15000")
        os.environ["MASTER_ADDR"] = os.environ.get("MASTER_ADDR", "127.0.0.1")

        self._local_rank = int(os.environ["LOCAL_RANK"])
        self._master_addr = os.environ["MASTER_ADDR"]
        self._master_port = int(os.environ["MASTER_PORT"])

    def _compute_nproc_per_node(self) -> int:
        local_rank = self.get_local_rank()
        # Create new cpu group to get nproc_per_node such we avoid using badly configured NCCL
        gloo_group = torch.distributed.new_group(backend="gloo")
        tensor = torch.tensor([local_rank + 1]).to("cpu")
        torch.distributed.all_reduce(tensor, op=torch.distributed.ReduceOp.MAX, group=gloo_group)
        return int(tensor.item())

    @staticmethod
    def setup_spawn_params(**spawn_kwargs: Any) -> Dict:
        nproc_per_node = spawn_kwargs.get("nproc_per_node")
        if nproc_per_node is None:
            nproc_per_node = torch.cuda.device_count()
        if nproc_per_node < 1:
            raise ValueError(f"Argument nproc_per_node should positive, but given {nproc_per_node}")

        nnodes = spawn_kwargs.get("nnodes", 1)
        if nnodes < 1:
            raise ValueError(f"Argument nnodes should positive, but given {nnodes}")

        node_rank = spawn_kwargs.get("node_rank", None)
        if node_rank is None:
            if nnodes > 1:
                raise ValueError("If number of nodes larger than one, arguments node_rank should be given")
            node_rank = 0
        if node_rank >= nnodes or node_rank < 0:
            raise ValueError(f"Argument node_rank should be between 0 and {nnodes - 1}, but given {node_rank}")

        master_addr = spawn_kwargs.get("master_addr", None)
        master_port = spawn_kwargs.get("master_port", None)
        init_method = spawn_kwargs.get("init_method", None)
        if nnodes > 1 and (master_addr is None or master_port is None) and init_method is None:
            raise ValueError(
                "If number of nodes larger than one, arguments master_addr and master_port or init_method "
                f"should be specified, but given master_addr={master_addr}, master_port={master_port} and "
                f"init_method={init_method}."
            )

        join = spawn_kwargs.get("join", True)
        daemon = spawn_kwargs.get("daemon", False)
        communicate_backend = spawn_kwargs.get("communicate_backend", "NCCL")

        params = {
            "communicate_backend": communicate_backend,
            "nproc_per_node": nproc_per_node,
            "nnodes": nnodes,
            "node_rank": node_rank,
            "master_addr": master_addr,
            "master_port": master_port,
            "init_method": init_method,
            "join": join,
            "daemon": daemon,
        }

        return {k: v for k, v in params.items() if v is not None}

    @staticmethod
    def _dist_worker_task_fn(
            local_rank: int,
            backend: str,
            communicate_backend: str,
            model_type: str,
            fn: Callable,
            args: Namespace,
            world_size: int,
            nprocs_per_node: int,
            node_rank: int,
            master_addr: Optional[str],
            master_port: Optional[str],
            init_method: str,
    ) -> None:
        from gaea_operator.distributed.utils import _set_model
        copy_env_vars = os.environ.copy()

        rank = node_rank * nprocs_per_node + local_rank
        os.environ["LOCAL_RANK"] = str(local_rank)
        os.environ["RANK"] = str(rank)
        os.environ["WORLD_SIZE"] = str(world_size)

        arg_world_size: Optional[int] = world_size
        arg_rank: Optional[int] = rank
        if init_method == "env://":
            os.environ["MASTER_ADDR"] = str(master_addr)
            os.environ["MASTER_PORT"] = str(master_port)
            arg_world_size = None
            arg_rank = None

        model = _TorchDistModel.create_from_backend(model_type,
                                                    backend,
                                                    communicate_backend=communicate_backend,
                                                    init_method=init_method,
                                                    world_size=arg_world_size,
                                                    rank=arg_rank)
        _set_model(model)
        fn(args)

        os.environ.clear()
        os.environ.update(copy_env_vars)

    @staticmethod
    def spawn(
            backend: str,
            model_type: str,
            fn: Callable,
            args: Namespace,
            nproc_per_node: int = 1,
            nnodes: int = 1,
            node_rank: int = 0,
            master_addr: Optional[str] = None,
            master_port: Optional[int] = None,
            communicate_backend: Optional[str] = "NCCL",
            init_method: Optional[str] = None,
            **kwargs: Any,
    ) -> None:
        world_size = nnodes * nproc_per_node

        spawn_kwargs = {
            "join": kwargs.get("join", True),
            "daemon": kwargs.get("daemon", False),
        }

        start_processes = torch.multiprocessing.spawn
        # start_method and start_processes in pytorch >= 1.5
        if Version(torch.__version__) >= Version("1.5.0"):
            import builtins

            if "__IPYTHON__" in builtins.__dict__:
                # use fork in jupyter
                default_start_method = "fork"
            else:
                default_start_method = "spawn"
            spawn_kwargs["start_method"] = kwargs.get("start_method", default_start_method)
            start_processes = torch.multiprocessing.start_processes
        # TODO: `spawn` wrongfully does not adopt address and port from environment if `init_method` is "env://"
        if init_method in [None, "env://"]:
            init_method = "env://"
            if master_port is None:
                master_port = 2222
            if master_addr is None:
                master_addr = "127.0.0.1"
        elif master_addr is not None:
            raise ValueError("master_addr should be None if init_method is provided other then 'env://'")
        elif master_port is not None:
            raise ValueError("master_port should be None if init_method is provided other then 'env://'")

        start_processes(
            _TorchDistModel._dist_worker_task_fn,
            nprocs=nproc_per_node,
            args=(
                backend,
                communicate_backend,
                model_type,
                fn,
                args,
                world_size,
                nproc_per_node,
                node_rank,
                master_addr,
                master_port,
                init_method,
            ),
            **spawn_kwargs,
        )

    def is_initialized(self) -> bool:
        return torch.distributed.is_initialized()

    def get_local_rank(self) -> int:
        return cast(int, self._local_rank)

    def get_world_size(self) -> int:
        return torch.distributed.get_world_size()

    def get_rank(self) -> int:
        return torch.distributed.get_rank()

    def get_nproc_per_node(self) -> int:
        return cast(int, self._nproc_per_node)

    def get_nnodes(self) -> int:
        return cast(int, self._nnodes)

    def get_node_rank(self) -> int:
        return cast(int, self._node)

    def device(self) -> Device:
        if torch.cuda.is_available():
            index = torch.cuda.current_device()
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
        if self.get_world_size() < 2:
            return tensor
        if op not in ReduceOP.torch_reduce_op_map():
            raise ValueError(f"Unsupported reduction operation: '{op}'")
        reduce_op = ReduceOP.torch_reduce_op_map()[op]
        torch.distributed.all_reduce(tensor, reduce_op)
        return tensor

    def _do_all_gather(self, tensor: TTensor) -> List:
        if self.get_world_size() < 2:
            return [tensor]
        tensor_list = [torch.zeros_like(tensor) for _ in range(self.get_world_size())]  # type: List[TTensor]
        torch.distributed.all_gather(tensor_list, tensor)
        return tensor_list

    def _do_broadcast(self, tensor: TTensor, src: int) -> TTensor:
        if self.get_world_size() < 2:
            return tensor
        torch.distributed.broadcast(tensor, src=src)
        return tensor

    def auto_model(self, model: Model) -> Tuple[str, Model]:
        assert isinstance(model, Module), f'model should torch.nn.Module, but give {type(model)}'

        self._module = TORCH_BACKEND

        # Put model's parameters to device if its parameters are not on the device
        device = self.device()
        if not all([p.device == device for p in model.parameters()]):
            model.to(device)

        kwargs = {}
        if torch.cuda.is_available():
            lrank = self.get_local_rank()
            kwargs["device_ids"] = [lrank]

        model = torch.nn.parallel.DistributedDataParallel(model, **kwargs)

        return self._module, model

    def auto_optim(self, optimizer: Optimizer) -> Optimizer:
        return optimizer

    def finalize(self) -> None:
        pass

    def barrier(self) -> None:
        torch.distributed.barrier()
