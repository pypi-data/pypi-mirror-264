#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : utils.py    
@Author        : yanxiaodong
@Date          : 2022/11/29
@Description   :
"""
from typing import Any, Callable, Tuple, Union, List
from argparse import Namespace

from gaea_operator.plugin import Model, Optimizer, Tensor, Device

from .comp_models import (_SerialModel, registered_computation_models)

_model = _SerialModel(model_type=None)


def get_world_size() -> int:
    """
    Return world size of current distributed configuration. Returns 1 if no distributed configuration.
    """
    return _model.get_world_size()


def is_initialized() -> bool:
    """
    Return True if the distributed environment has been initialized.
    """
    return _model.is_initialized()


def get_local_rank() -> int:
    """
    Return local process rank within current distributed configuration.
    """
    return _model.get_local_rank()


def get_model_type() -> str:
    """
    Return train model type.
    """
    return _model.get_model_type()


def set_model_type(value) -> None:
    """
    Set train model type.
    """
    _model.set_model_type(value=value)


def get_rank() -> int:
    """
    Return process rank within current distributed configuration.
    """
    return _model.get_rank()


def get_device() -> Device:
    """
    Return current device.
    """
    return _model.device()


def get_backend() -> str:
    """
    Return current backend.
    """
    return _model.backend


def all_gather_object(tensor: Union[Tensor, float, str]) -> Union[Tensor, float, List[float], List[str]]:
    """
    All gather the given object from the current process group.
    """
    return _model.all_gather(tensor)


def broadcast_object(tensor: Union[Tensor, float, str, None], src: int = 0) -> Union[Tensor, float, str]:
    """
    Broadcast the given object from source process to the current process group.
    """
    return _model.broadcast(tensor=tensor, src=src)


def get_module() -> str:
    """
    Returns use framework torch or paddle
    """
    return _model.module


def set_module(value) -> None:
    """
    Set use framework torch or paddle
    """
    _model.module = value


def available_backends() -> Tuple[str, ...]:
    """
    Returns available backends.
    """
    out = ()  # type: Tuple[str, ...]
    for m in registered_computation_models:
        out += m.available_backends
    return out


def _assert_backend(backend: str) -> None:
    backends = available_backends()
    if backend not in backends:
        raise ValueError(f"Unknown backend '{backend}'. Available backends: {backends}")


def setup_spawn_params(backend: str, **kwargs: Any) -> None:
    _assert_backend(backend)

    for comp_model_cls in registered_computation_models:
        if backend not in comp_model_cls.available_backends:
            continue
        return comp_model_cls.setup_spawn_params(**kwargs)


def _set_model(model: Any) -> None:
    global _model
    _model = model


def spawn(
    backend: str,
    model_type: str,
    fn: Callable,
    args: Namespace,
    **kwargs: Any,
) -> None:
    """
    Spawns processes that run ``fn`` with ``args``/``kwargs_dict`` and initialize
    distributed configuration defined by ``backend``.
    """
    _assert_backend(backend)
    print("current model type is {}".format(model_type))

    for comp_model_cls in registered_computation_models:
        if backend not in comp_model_cls.available_backends:
            continue
        comp_model_cls.spawn(backend, model_type, fn, args=args, **kwargs)


def initialize(model_type: str, backend: str, **kwargs: Any) -> None:
    """
    Initializes distributed configuration according to provided ``backend``.
    """
    global _model

    _assert_backend(backend=backend)
    print("initializing computation models")

    for comp_model_cls in registered_computation_models:
        if backend not in comp_model_cls.available_backends:
            continue
        try:
            _model = comp_model_cls(model_type=model_type, backend=backend, **kwargs)
        except Exception:
            _model = _SerialModel(model_type=model_type)


def auto_adapt(model: Model, optimizer: Optimizer):
    """
    Helper method to adapt for non-distributed and distributed configurations.
    """
    module, model = _model.auto_model(model=model)
    if optimizer is not None:
        optimizer = _model.auto_optim(optimizer=optimizer)

    return module, model, optimizer


def training_step(model: Model,
                  optimizer: Optimizer,
                  loss_fn: Callable,
                  lr_scheduler: Callable,
                  gradient_accumulation_steps: int):
    """
    Factory function for training.
    """
    device = get_device()
    return _model.training_step(model=model,
                                optimizer=optimizer,
                                loss_fn=loss_fn,
                                lr_scheduler=lr_scheduler,
                                device=device,
                                gradient_accumulation_steps=gradient_accumulation_steps)


def amp_training_step(model: Model,
                      optimizer: Optimizer,
                      loss_fn: Callable,
                      lr_scheduler: Callable,
                      gradient_accumulation_steps: int,
                      amp_param: dict):
    """
    Factory function for amp training.
    """
    device = get_device()
    return _model.amp_training_step(model=model,
                                    optimizer=optimizer,
                                    loss_fn=loss_fn,
                                    lr_scheduler=lr_scheduler,
                                    device=device,
                                    gradient_accumulation_steps=gradient_accumulation_steps,
                                    amp_param=amp_param)


def validating_step(model: Model):
    """
    Factory function for validating.
    """
    device = get_device()
    return _model.validating_step(model=model, device=device)


def amp_validating_step(model: Model, amp_param: dict):
    """
    Factory function for amp_validating.
    """
    device = get_device()
    return _model.amp_validating_step(model=model, device=device, amp_param=amp_param)


def all_reduce(tensor: Union[Tensor, float], op: str = "SUM") -> Union[Tensor, float]:
    return _model.all_reduce(tensor, op)


def barrier() -> None:
    return _model.barrier()