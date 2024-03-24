#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : base_metric.py    
@Author        : yanxiaodong
@Date          : 2022/11/14
@Description   :
"""
from abc import ABCMeta, abstractmethod
import json
import os
import yaml
from jsonschema import validate
from typing import Any, Callable, List, Mapping, Optional, Tuple, Union, Dict

from .function.metric import Metric
import gaea_operator.distributed as idist
from gaea_operator.engine import CallableEventWithFilter, Engine, Events
from gaea_operator.utils import setup_logger, MASTER_RANK


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
    """
    # public class attribute
    required_output_keys: Optional[Tuple] = ("y_pred", "y")
    metric_file_name = "metric.json"
    all_last_batch_padding_policy = ("equalization", "sequence")

    def __init__(self,
                 dataset_length: Optional[int],
                 categories: Optional[List],
                 output_transform: Callable = lambda x: (x[0], x[1]),
                 is_saved: Optional[bool] = False,
                 dirname: Optional[str] = None,
                 last_batch_padding_policy: Optional[str] = "equalization",
                 **kwargs):
        self._output_transform = output_transform
        self.dataset_length = dataset_length
        self.categories = categories
        self.is_saved = is_saved
        self.dirname = dirname

        assert last_batch_padding_policy in self.all_last_batch_padding_policy, \
            "Last batch padding policy must be in {}, but given {}".format(self.all_last_batch_padding_policy,
                                                                           last_batch_padding_policy)
        self.last_batch_padding_policy = last_batch_padding_policy

        self.metrics: Dict[str, Metric] = {}
        self.metric_results = {}
        self.num_classes = len(self.categories)
        self.prefix = "schema/schema_modelevaluation_"

        self._logger = setup_logger(__name__ + "." + self.__class__.__name__)

        if self.is_saved:
            assert self.dirname is not None and len(self.dirname) > 0, \
                "If you want to save metric: {}, must set dirname, can not be None".format(self.is_saved)

    def reset(self) -> None:
        """
        Resets the metric to it's initial state.
        """
        for _, metric in self.metrics.items():
            metric.reset()

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

    def save(self, dirname: str) -> None:
        """
        Saves results to a JSON file.
        """
        if idist.get_rank() == MASTER_RANK or idist.get_world_size() == 1:
            if not os.path.exists(dirname):
                os.makedirs(dirname, exist_ok=True)

            metric_file = os.path.join(dirname, self.metric_file_name)
            with open(metric_file, "w") as fp:
                json.dump(self.metric_results, fp)

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
        else:
            if isinstance(output, List):
                output = (output, [None] * len(output))

        self.update(output)

    @abstractmethod
    def gather(self):
        """
        Gather all metric status from all rank.
        """
        pass

    def _check_metric_results(self, results: Dict, schema_file: str):
        with open(schema_file) as fp:
            schema_data = yaml.load(fp, Loader=yaml.Loader)

        validate(instance=results, schema=schema_data)

        self.metric_results = results

    def completed(self, engine: Engine = None) -> None:
        """
        Helper method to compute metric's value and put into the engine.

        Args:
            engine: the engine to which the metric must be attached.
        """

        if idist.get_world_size() == 1:
            self.metric_results = self.compute()

            for key, value in self.metric_results.items():
                engine.state.metrics[key] = value
        else:
            self._logger.info("-------------start gathering-------------")
            self.gather()
            self._logger.info("finished gathering to {}".format(idist.get_rank()))

            # 分布式情形下，只有master节点保存结果
            if idist.get_rank() == MASTER_RANK:
                self.metric_results = self.compute()

                for key, value in self.metric_results.items():
                    engine.state.metrics[key] = value

        if self.is_saved:
            self.save(dirname=self.dirname)

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

    def attach_engine(self, engine: Engine, usage: Union[str, MetricUsage] = EpochWise()) -> None:
        """
        Attaches current metric to provided engine. On the end of engine's run, `metrics` dictionary will
        contain computed metric value.

        Args:
            engine: the engine to which the metric must be attached.
            usage: the usage of the metric. Valid string values should be
                :attr:`EpochWise.usage_name` (default) or
                :attr:`BatchWise.usage_name`.
        """
        usage = self._check_usage(usage)
        if not engine.has_event_handler(self.started, usage.STARTED):
            engine.add_event_handler(usage.STARTED, self.started)
        if not engine.has_event_handler(self.iteration_completed, usage.ITERATION_COMPLETED):
            engine.add_event_handler(usage.ITERATION_COMPLETED, self.iteration_completed)
        engine.add_event_handler(usage.COMPLETED, self.completed)

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
