#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : profiler.py    
@Author        : yanxiaodong
@Date          : 2023/1/3
@Description   :
"""
import os
from abc import ABCMeta
from pathlib import Path
from typing import Any, Callable, Iterable, Optional, Union

from gaea_operator.engine import Engine, Events
from gaea_operator.plugin import (ProfilerAction, ProfilerActivity,
                                   ProfilerState, ProfilerTarget, paddle, torch)
from gaea_operator.utils import setup_logger


class BaseProfiler(metaclass=ABCMeta):
    """
    BasicProfiler can be used to profile the train.
    """
    def __init__(self, dirname: Union[str, Path],):
        self.profiler_file = os.path.join(dirname, 'profiler')
        self._logger = setup_logger(__name__ + "." + self.__class__.__name__)
        self.profiler = None  # type: Callable

    def start(self):
        """
        Method to start the profiler.
        """
        self._logger.info('Start the performance analyzer.')
        self.profiler.start()

    def stop(self):
        """
        Method to stop the profiler
        """
        self._logger.info('Stop the performance analyzer.')
        self.profiler.stop()

    def status(self, engine: Engine):
        """
        Method to fetch the profiler results when the engine is run.
        """
        self.profiler.step()

    def attach_engine(self, engine: Engine) -> None:
        """
        Attaching `stats` method at EPOCH_STARTED and `update` method at ITERATION_COMPLETED.
        """
        if not isinstance(engine, Engine):
            raise TypeError(f"Argument engine should be class: `Engine`, but given {type(engine)}")
        engine.add_event_handler(Events.STARTED, self.start)
        engine.add_event_handler(Events.ITERATION_COMPLETED, self.status)
        engine.add_event_handler(Events.COMPLETED, self.stop)


class PaddleProfiler(BaseProfiler):
    """
    Paddle profiler to manage profiling process to start, stop, export profiling data.

    Args:
        targets: specify target devices to profile, and all existing and supported devices will be chosen by default.
        scheduler: If it is a callable object, it takes a step number as parameter.
            If not provided (None), the default scheduler will keep tracing until the profiler exits.
            If it is a tuple, it has two values start_batch and end_batch,
                which means profiling range [start_batch, end_batch).
        on_trace_ready: Callable object, serves as callback function, and takes the Profiler object as parameter.
        timer_only: If it is True, the cost of Dataloader and every step of the model will be count without profiling.
            Otherwise, the model will be timed and profiled. Default: False.
    """
    def __init__(self,
                 dirname: Optional[str] = None,
                 targets: Optional[Iterable[ProfilerTarget]] = None,
                 scheduler: Union[Callable[[int], ProfilerState], tuple, None] = None,
                 on_trace_ready: Optional[Callable[..., Any]] = None,
                 timer_only: Optional[bool] = False,
                 **kwargs):
        super(PaddleProfiler, self).__init__(dirname=dirname)

        if on_trace_ready is not None and not callable(on_trace_ready):
            raise TypeError(f'on_trace_ready should be a function, got {type(on_trace_ready)} instead.')
        if on_trace_ready is None:
            on_trace_ready = self._on_trace_ready

        self.profiler = paddle.profiler.Profiler(targets=targets,
                                                 scheduler=scheduler,
                                                 on_trace_ready=on_trace_ready,
                                                 timer_only=timer_only,
                                                 **kwargs)

    def _on_trace_ready(self, prof):
        callback = paddle.profiler.export_chrome_tracing(self.profiler_file)
        callback(prof)
        prof.summary(sorted_by=paddle.profiler.SortedKeys.GPUTotal)


class TorchProfiler(BaseProfiler):
    """
    Torch profiler to manage profiling process to start, stop, export profiling data.

    Args:
        activities: list of activity groups (CPU, CUDA) to use in profiling.
        schedule: callable that takes step (int) as a single parameter and returns
            ``ProfilerAction`` value that specifies the profiler action to perform at each step.
        on_trace_ready: callable that is called at each step when ``schedule``
            returns ``ProfilerAction.RECORD_AND_SAVE`` during the profiling.
        record_shapes: save information about operator's input shapes.
        profile_memory: track tensor memory allocation/deallocation.
        with_stack: record source information (file and line number) for the ops.
        with_flops: use formula to estimate the FLOPs (floating point operations) of specific operators
            (matrix multiplication and 2D convolution).
        with_modules: record module hierarchy (including function names).
    """
    def __init__(self,
                 activities: Optional[Iterable[ProfilerActivity]] = None,
                 schedule: Optional[Callable[[int], ProfilerAction]] = None,
                 on_trace_ready: Optional[Callable[..., Any]] = None,
                 record_shapes: bool = False,
                 profile_memory: bool = False,
                 with_stack: bool = False,
                 with_flops: bool = False,
                 with_modules: bool = False,
                 **kwargs):
        super(TorchProfiler, self).__init__(**kwargs)

        if on_trace_ready is not None and not callable(on_trace_ready):
            raise TypeError(f'on_trace_ready should be a function, got {type(on_trace_ready)} instead.')
        if on_trace_ready is None:
            on_trace_ready = self._on_trace_ready()

        self.profiler = torch.profiler.profile(activities=activities,
                                               schedule=schedule,
                                               on_trace_ready=on_trace_ready,
                                               record_shapes=record_shapes,
                                               profile_memory=profile_memory,
                                               with_stack=with_stack,
                                               with_flops=with_flops,
                                               with_modules=with_modules)

    def _on_trace_ready(self):
        return torch.profiler.tensorboard_trace_handler(self.profiler_file)
