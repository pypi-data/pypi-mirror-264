#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : plugin.py
@Author        : yanxiaodong
@Date          : 2022/11/30
@Description   :
"""
from typing import TYPE_CHECKING, TypeVar

from gaea_operator.utils import try_import, try_import_class

if TYPE_CHECKING:
    import paddle
    from paddle.io import DataLoader as PDataLoader
    from paddle.nn import Layer
    from paddle.nn import functional as F
    from paddle.optimizer import Optimizer as POptimizer
    from paddle import Tensor as PTensor
    from paddle import CPUPlace, CUDAPlace
    from paddle.profiler import ProfilerTarget, ProfilerState
    from paddle.distributed.fleet.utils.hybrid_parallel_util import fused_allreduce_gradients
else:
    paddle = try_import('paddle')
    F = try_import('paddle.nn.functional')

    PDataLoader = try_import_class(paddle, 'io.DataLoader')
    PTensor = try_import_class(paddle, 'Tensor')
    Layer = try_import_class(paddle, 'nn.Layer')
    POptimizer = try_import_class(paddle, 'optimizer.Optimizer')
    CPUPlace = try_import_class(paddle, 'CPUPlace')
    CUDAPlace = try_import_class(paddle, 'CUDAPlace')
    ProfilerTarget = try_import_class(paddle, 'profiler.ProfilerTarget')
    ProfilerState = try_import_class(paddle, 'profiler.ProfilerState')
    fused_allreduce_gradients = try_import_class(
        paddle, 'distributed.fleet.utils.hybrid_parallel_util.fused_allreduce_gradients')

if TYPE_CHECKING:
    import torch
    from torch import Tensor as TTensor
    from torch.nn import Module
    from torch.optim import Optimizer as TOptimizer
    from torch.utils.data import DataLoader as TDataLoader
    from torch import device
    from torch.profiler import ProfilerActivity, ProfilerAction
else:
    torch = try_import('torch')

    TDataLoader = try_import_class(torch, 'utils.data.DataLoader')
    TTensor = try_import_class(torch, 'Tensor')
    Module = try_import_class(torch, 'nn.Module')
    TOptimizer = try_import_class(torch, 'optim.Optimizer')
    device = try_import_class(torch, 'device')
    ProfilerActivity = try_import_class(torch, 'profiler.ProfilerActivity')
    ProfilerAction = try_import_class(torch, 'profiler.ProfilerAction')

if TYPE_CHECKING:
    import nvidia.dali as dali
    import nvidia.dali.fn as fn
    import nvidia.dali.types as types
    from nvidia.dali import Pipeline
    from nvidia.dali.pipeline.experimental import pipeline_def
    from nvidia.dali.tensors import (TensorCPU, TensorGPU, TensorListCPU,
                                     TensorListGPU)
    from nvidia.dali.plugin.base_iterator import _DaliBaseIterator, LastBatchPolicy
else:
    dali = try_import('nvidia.dali')
    fn = try_import('nvidia.dali.fn')
    types = try_import('nvidia.dali.types')

    pipeline_def = try_import_class(dali, 'pipeline.experimental.pipeline_def')
    Pipeline = try_import_class(dali, 'Pipeline')
    TensorGPU = try_import_class(dali, 'tensors.TensorGPU')
    TensorListGPU = try_import_class(dali, 'tensors.TensorListGPU')
    TensorCPU = try_import_class(dali, 'tensors.TensorCPU')
    TensorListCPU = try_import_class(dali, 'tensors.TensorListCPU')
    _DaliBaseIterator = try_import_class(dali, 'plugin.base_iterator._DaliBaseIterator')
    LastBatchPolicy = try_import_class(dali, 'plugin.base_iterator.LastBatchPolicy')

if TYPE_CHECKING:
    import mlflow
else:
    mlflow = try_import('mlflow')

if TYPE_CHECKING:
    import aim
    from aim.ext.resource.configs import DEFAULT_SYSTEM_TRACKING_INT
else:
    aim = try_import('aim')
    DEFAULT_SYSTEM_TRACKING_INT = try_import_class(aim, 'ext.resource.configs.DEFAULT_SYSTEM_TRACKING_INT')

if TYPE_CHECKING:
    import horovod
else:
    horovod = try_import('horovod')

DataLoader = TypeVar('DataLoader', PDataLoader, TDataLoader)
Tensor = TypeVar('Tensor', PTensor, TTensor)
Model = TypeVar('Model', Layer, Module)
Optimizer = TypeVar('Optimizer', POptimizer, TOptimizer)
Device = TypeVar('Device', CPUPlace, CUDAPlace, device)
