#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : __init__.py.py    
@Author        : yanxiaodong
@Date          : 2022/11/29
@Description   :
"""
from typing import List, Tuple, Type, Union

from .base import _SerialModel
from .paddle_dist import _PaddleDistModel, has_paddle_native_dist_support
from .torch_dist import _TorchDistModel, has_torch_native_dist_support
from .horovod_dist import _HorovodDistModel, has_hvd_dist_support


def setup_available_computation_models() -> Tuple:
    models = [
        _SerialModel,
    ]  # type: List[Type[Union[_SerialModel, '_PaddleDistModel', '_TorchDistModel', '_HorovodDistModel']]]
    if has_paddle_native_dist_support:
        models.append(_PaddleDistModel)
    if has_torch_native_dist_support:
        models.append(_TorchDistModel)
    if has_hvd_dist_support:
        models.append(_HorovodDistModel)

    return tuple(models)


def list_all_backends() -> List[str]:
    """
    a list of all distributed backend names.
    Returns:
        List: A list of all distributed backend names.
    """
    _backends = _PaddleDistModel.available_backends + \
                _TorchDistModel.available_backends + \
                _HorovodDistModel.available_backends

    return _backends


registered_computation_models = setup_available_computation_models()

_all__ = ['registered_computation_models', '_SerialModel', 'list_all_backends']
