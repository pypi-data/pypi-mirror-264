#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : __init__.py.py    
@Author        : yanxiaodong
@Date          : 2022/11/29
@Description   :
"""
from .accelerator import Accelerator
from .launcher import Parallel
from .comp_models import list_all_backends
from .utils import get_local_rank, get_module, get_rank, get_world_size, all_gather_object, broadcast_object, \
    get_backend, get_device, all_reduce, get_model_type, barrier, setup_spawn_params, set_module, set_model_type

__all__ = ['get_rank', 'get_module', 'Accelerator', 'get_local_rank', 'get_world_size',
           'all_gather_object', 'broadcast_object', 'get_backend', 'get_device', 'all_reduce', 'get_model_type',
           'barrier', 'Parallel', 'list_all_backends', 'setup_spawn_params', 'set_module', 'set_model_type']
