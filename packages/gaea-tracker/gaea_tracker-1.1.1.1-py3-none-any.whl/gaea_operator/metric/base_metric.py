#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : base_metric.py    
@Author        : yanxiaodong
@Date          : 2022/11/14
@Description   :
"""
from abc import ABCMeta, abstractmethod
from typing import (Any, Callable, Dict, List, Mapping, Optional, Sequence,
                    Tuple, Union)

import numpy as np

import gaea_operator.distributed as idist
from gaea_operator.data.source import BaseMultiDataset, DALIBaseMultiDataset
from gaea_operator.engine import CallableEventWithFilter, Engine, Events
from gaea_operator.plugin import Tensor, paddle, torch, TTensor, PTensor
from gaea_operator.utils import setup_logger


class MetricUsage(object):
    """
    Base class for all usages of metrics.

    A usage of metric defines the events when a metric starts to compute, updates and completes.
    Valid events are from :class:`~Events`.

    Args:
        started: event when the metric starts to compute.
        completed: event when the metric completes.
        iteration_completed: event when the metric updates.
    """

    def __init__(self, started: Events, completed: Events, iteration_completed: CallableEventWithFilter) -> None:
        self.__started = started
        self.__completed = completed
        self.__iteration_completed = iteration_completed
        

    @property
    def STARTED(self) -> Events:
        return self.__started

    @property
    def COMPLETED(self) -> Events:
        return self.__completed

    @property
    def ITERATION_COMPLETED(self) -> CallableEventWithFilter:
        return self.__iteration_completed


class EpochWise(MetricUsage):
    """
    Epoch-wise usage of Metrics. It's the default and most common usage of metrics.

    Attributes:
        usage_name: usage name string
    """

    usage_name: str = "epoch_wise"

    def __init__(self) -> None:
        super(EpochWise, self).__init__(
            started=Events.EPOCH_STARTED,
            completed=Events.EPOCH_COMPLETED,
            iteration_completed=Events.ITERATION_COMPLETED,
        )


class BatchWise(MetricUsage):
    """
    Batch-wise usage of Metrics.

    Attributes:
        usage_name: usage name string
    """

    usage_name: str = "batch_wise"

    def __init__(self) -> None:
        super(BatchWise, self).__init__(
            started=Events.ITERATION_STARTED,
            completed=Events.ITERATION_COMPLETED,
            iteration_completed=Events.ITERATION_COMPLETED,
        )


class BatchFiltered(MetricUsage):
    """
    Batch filtered usage of Metrics. This usage is similar to epoch-wise but update event is filtered.

    Args:
        args: Positional arguments to setup.
        kwargs: Keyword arguments to setup.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(BatchFiltered, self).__init__(
            started=Events.EPOCH_STARTED,
            completed=Events.EPOCH_COMPLETED,
            iteration_completed=Events.ITERATION_COMPLETED(*args, **kwargs),
        )


class BaseMetric(metaclass=ABCMeta):
    """
    Base class for metric.

    Args:
        dataset: validation dataset in order to get validation mode `single_val` or `parallel_val`.
        output_transform: a callable that is used to transform the Engine`'s ``process_function``'s output into the
            form expected by the metric.
        dataset_meta: Meta information of the dataset, this is required for some metrics that require
            dataset information.
        size: The length of the entire dataset, it is only used when distributed evaluation.
        backend: Support different backend types ('paddle_dist', 'torch_dist', 'None')
    """
    # public class attribute
    required_output_keys: Optional[Tuple] = ("y_pred", "y")

    def __init__(self,
                 dataset: Optional[Any] = None,
                 backend: Optional[str] = None,
                 size: Optional[int] = None,
                 output_transform: Callable = lambda x: (x[0], x[1]),
                 dataset_meta: Optional[Dict] = None,
                 **kwargs):
        self._output_transform = output_transform
        self._dataset_meta = dataset_meta
        self._results: List[Any] = []
        if isinstance(dataset, (BaseMultiDataset, DALIBaseMultiDataset)):
            self.distribute_val = dataset.distribute_val
            self.dataset_length = len(dataset)
        else:
            idist.Accelerator(backend=backend, **kwargs)
            self.distribute_val = True
            self.dataset_length = size
        self.dataset = dataset
        self.model_type = idist.get_model_type()
        self._logger = setup_logger(__name__ + "." + self.__class__.__name__)

    @property
    def dataset_meta(self) -> Optional[Dict]:
        """
        Meta information of the dataset.
        """
        if self._dataset_meta is None:
            return self._dataset_meta
        else:
            return self._dataset_meta.copy()

    @dataset_meta.setter
    def dataset_meta(self, dataset_meta: Optional[Dict]) -> None:
        """
        Set the dataset meta information to the metric.
        """
        if dataset_meta is None:
            self._dataset_meta = dataset_meta
        else:
            self._dataset_meta = dataset_meta.copy()

    def reset(self) -> None:
        """
        Resets the metric to it's initial state.
        """
        self._results.clear()

    @abstractmethod
    def update(self, output: Any) -> None:
        """
        Override this method to update the intermediate results to ``self._results``
        """
        pass

    @abstractmethod
    def compute(self) -> Any:
        """
        Computes the metric based on it's accumulated state.
        By default, this is called at the end of each epoch.

        Raises:
            NotComputableError: raised when the metric cannot be computed.
        """
        pass

    @abstractmethod
    def save(self, dirname: str) -> None:
        """
        Saves results to a JSON file.
        """
        pass

    def started(self, engine: Engine) -> None:
        """
        Helper method to start data gathering for metric's computation.

        Args:
            engine: the engine to which the metric must be attached
        """
        self.reset()

    def iteration_completed(self, engine: Engine) -> None:
        """
        Helper method to update metric's computation.

        Args:
            engine: the engine to which the metric must be attached

        Note:
            ``engine.state.output`` is used to compute metric values.
        """
        output = self._output_transform(engine.state.output)
        if isinstance(output, Mapping):
            if self.required_output_keys is None:
                raise TypeError(
                    f"Transformed engine output for {self.__class__.__name__} metric should be a tuple/list, "
                    f"but given {type(output)}"
                )
            if not all([k in output for k in self.required_output_keys]):
                raise ValueError(
                    "When transformed engine's output is a mapping, "
                    f"it should contain {self.required_output_keys} keys, but given {list(output.keys())}"
                )
            output = tuple(output[k] for k in self.required_output_keys)
        # # (y_pred, im_id) format
        # elif isinstance(output, Tuple):
        #     if not (len(output) == 2 and len(output[0]) == len(output[1])):
        #         raise ValueError(
        #             f"Output should have 2 items of the same length, "
        #             f"got {len(output)} and {len(output[0])}, {len(output[1])}"
        #         )
        # y_pred format
        else:
            if isinstance(output, List):
                output = (output, [None] * len(output))

        self.update(output)

    def gather(self):
        """
        汇聚多个进程的结果
        """
        pass

    def completed(self, engine: Engine = None, name: str = "metric") -> None:
        """
        Helper method to compute metric's value and put into the engine.

        Args:
            engine: the engine to which the metric must be attached
            name: the name of the metric used as key in dict `engine.state.metrics`
        """

        if idist.get_world_size() == 1 or not self.distribute_val:
            result = self.compute()

        else:
            if idist.get_backend() == idist.list_all_backends()[0]:
                to_tensor = paddle.to_tensor
            if idist.get_backend() == idist.list_all_backends()[1] or idist.get_backend() == idist.list_all_backends()[2]:
                to_tensor = torch.tensor

            if isinstance(self._results, list):
                collected_results = []
                for res in self._results:
                    if isinstance(res, np.ndarray):
                        res = to_tensor(res)
                    collected_results.extend(idist.all_gather_object(res))

                if self.dataset_length is not None:
                    collected_results = collected_results[:self.dataset_length]
                self._results = collected_results

            self._logger.info("start gathering -------------")
            if isinstance(self._results, dict):
                self.gather()

            self._logger.info("finished gathering to {}".format(idist.get_rank()))
            if idist.get_rank() == 0:
                result = self.compute()
            else:
                result = {}

        if isinstance(result, Mapping):
            if name in result.keys():
                raise ValueError(f"Argument name '{name}' is conflicting with mapping keys: {list(result.keys())}")

            for key, value in result.items():
                if engine is not None:
                    engine.state.metrics[key] = value
                else:
                    self._logger.info("[metric message] key: {} value: {}".format(key, value))
        if engine is not None:
            engine.state.metrics[name] = result
        else:
            self._logger.info("[metric message] key: {} value: {}".format(name, result))

    def _check_usage(self, usage: Union[str, MetricUsage]) -> MetricUsage:
        if isinstance(usage, str):
            if usage == EpochWise.usage_name:
                usage = EpochWise()
            elif usage == BatchWise.usage_name:
                usage = BatchWise()
            else:
                raise ValueError(f"usage should be 'EpochWise.usage_name' or 'BatchWise.usage_name', get {usage}")
        if not isinstance(usage, MetricUsage):
            raise TypeError(f"Unhandled usage type {type(usage)}")
        return usage

    def attach_engine(self, engine: Engine, name: str = "map", usage: Union[str, MetricUsage] = EpochWise()) -> None:
        """
        Attaches current metric to provided engine. On the end of engine's run, `metrics` dictionary will
        contain computed metric's value under provided name.

        Args:
            engine: the engine to which the metric must be attached
            name: the name of the metric to attach
            usage: the usage of the metric. Valid string values should be
                :attr:`EpochWise.usage_name` (default) or
                :attr:`BatchWise.usage_name`.
        """
        usage = self._check_usage(usage)
        if not engine.has_event_handler(self.started, usage.STARTED):
            engine.add_event_handler(usage.STARTED, self.started)
        if not engine.has_event_handler(self.iteration_completed, usage.ITERATION_COMPLETED):
            engine.add_event_handler(usage.ITERATION_COMPLETED, self.iteration_completed)
        engine.add_event_handler(usage.COMPLETED, self.completed, name)

    def detach(self, engine: Engine, usage: Union[str, MetricUsage] = EpochWise()) -> None:
        """
        Detaches current metric from the engine and no metric's computation is done during the run.
        """
        usage = self._check_usage(usage)
        if engine.has_event_handler(self.completed, usage.COMPLETED):
            engine.remove_event_handler(self.completed, usage.COMPLETED)
        if engine.has_event_handler(self.started, usage.STARTED):
            engine.remove_event_handler(self.started, usage.STARTED)
        if engine.has_event_handler(self.iteration_completed, usage.ITERATION_COMPLETED):
            engine.remove_event_handler(self.iteration_completed, usage.ITERATION_COMPLETED)

    def is_attached(self, engine: Engine, usage: Union[str, MetricUsage] = EpochWise()) -> bool:
        """
        Checks if current metric is attached to provided engine.

        Args:
            engine: the engine checked from which the metric should be attached
            usage: the usage of the metric. Valid string values should be
                'epoch_wise' (default) or 'batch_wise'.
        """
        usage = self._check_usage(usage)
        return engine.has_event_handler(self.completed, usage.COMPLETED)
