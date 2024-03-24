#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : metric_logger.py
@Author        : yanxiaodong
@Date          : 2022/10/31
@Description   :
"""
import numbers
import os
import warnings
import random
from abc import ABCMeta, abstractmethod
from collections import OrderedDict, defaultdict
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

from gaea_operator.plugin import mlflow, aim, DEFAULT_SYSTEM_TRACKING_INT

import gaea_operator.distributed as idist
from gaea_operator.engine import (CallableEventWithFilter, Engine, Events,
                                  EventsList, RemovableEventHandle, State)
from gaea_operator.plugin import TTensor, PTensor
from gaea_operator.utils import visualize_box_mask, get_color_map_list, MASTER_RANK, setup_logger, PRODUCT_PATH


class BaseHandler(metaclass=ABCMeta):
    """
    Base handler for defining various useful metric logger handlers."""

    @abstractmethod
    def __call__(self, engine: Engine, logger: Any, event_name: Union[str, Events]) -> None:
        pass


class ExperimentTrackerArgument(metaclass=ABCMeta):
    """
    Experiment Tracker Argument.
    """
    def __init__(self,
                 experiment_kind: Optional[str] = None,
                 tracking_uri: Optional[str] = None,
                 experiment_name: Optional[str] = 'default',
                 run_name: Optional[str] = None):
        pass


class BaseLogger(ExperimentTrackerArgument):
    """
    Base logger handler.

    :param experiment_kind: tracker kind.
    :type experiment_kind: Optional[str]
    :param tracking_uri: The URL of the experiment tracker server.
    :type tracking_uri: Optional[str]
    :param experiment_name: The name of the experiment to log to.
    :type experiment_name: Optional[str]
    :param run_name: The name of the run.
    :type run_name: Optional[str]
    """
    all_kind = ('Aim', 'MLFlow')

    def __init__(self,
                 experiment_kind: Optional[str] = None,
                 tracking_uri: Optional[str] = None,
                 experiment_name: Optional[str] = 'default',
                 run_name: Optional[str] = None,
                 **kwargs):
        self.experiment_kind = experiment_kind
        self.tracking_uri = tracking_uri
        self.experiment_name = experiment_name
        self.run_name = run_name

        assert self.experiment_kind in self.all_kind, f'Experiment kind should be in {self.all_kind}, ' \
                                                      f'but given {self.experiment_kind}'
        if tracking_uri is None:
            raise ValueError('tracking_uri cat not None, '
                             'you should set tracking_uri equal to experiment tracker endpoint.')

        self._logger = setup_logger(__name__ + "." + self.__class__.__name__)

    def attach(
            self,
            engine: Engine,
            log_handler: Callable,
            event_name: Union[str, Events, CallableEventWithFilter, EventsList],
            *args: Any,
            **kwargs: Any,
    ) -> RemovableEventHandle:
        """
        Attach the logger to the engine and execute `log_handler` function at `event_name` events.

        Args:
            engine: engine object.
            log_handler: a logging handler to execute
            event_name: event to attach the logging handler to.
            args: args forwarded to the `log_handler` method
            kwargs: kwargs forwarded to the  `log_handler` method
        """
        if isinstance(event_name, EventsList):
            for name in event_name:
                if name not in State.event_to_attr:
                    raise RuntimeError(f"Unknown event name '{name}'")
                engine.add_event_handler(name, log_handler, self, name)

            return RemovableEventHandle(event_name, log_handler, engine)

        else:

            if event_name not in State.event_to_attr:
                raise RuntimeError(f"Unknown event name '{event_name}'")

            return engine.add_event_handler(event_name, log_handler, self, event_name, *args, **kwargs)

    def __enter__(self) -> "BaseLogger":
        return self

    def __exit__(self, type: Any, value: Any, traceback: Any) -> None:
        self.close()

    def close(self) -> None:
        pass


class BaseOutputHandler(BaseHandler):
    """
    Helper handler to log engine's output and/or metrics
    """
    metric_key = "metric"
    output_key = "output"
    attribute_key = "attribute"

    def __init__(
            self,
            tag: str,
            metric_names: Optional[Union[str, List[str]]] = None,
            output_transform: Optional[Callable] = None,
            state_attributes: Optional[Union[Dict, List[Union[str, Dict]]]] = None,
            annotation_transform: Optional[Callable] = None,
            global_step_transform: Optional[Callable] = None,
    ):

        if metric_names is not None:
            if not (isinstance(metric_names, list) or (isinstance(metric_names, str) and metric_names == "all")):
                raise TypeError(
                    f"metric_names should be either a list or equal 'all', got {type(metric_names)} instead."
                )

        if output_transform is not None and not callable(output_transform):
            raise TypeError(
                f"output_transform should be a function, got {type(output_transform)} instead.")

        if metric_names is None and output_transform is None and metric_names is None and \
                state_attributes is None and annotation_transform is None:
            raise ValueError(
                "Either metric_names, output_transform state_attributes or annotation_transform should be defined")

        if annotation_transform is not None and not callable(annotation_transform):
            raise TypeError(f"annotation_transform should be a function, got {type(annotation_transform)} instead.")

        if global_step_transform is not None and not callable(global_step_transform):
            raise TypeError(
                f"global_step_transform should be a function, got {type(global_step_transform)} instead.")

        if global_step_transform is None:
            def global_step_transform(engine: Engine, event_name: Union[str, Events]) -> int:
                return engine.state.get_event_attrib_value(event_name)

        self.tag = tag
        self.metric_names = metric_names
        self.output_transform = output_transform
        self.global_step_transform = global_step_transform
        self.state_attributes = state_attributes
        self.annotation_transform = annotation_transform

    def _setup_output_metrics_state_attrs(
            self, engine: Engine, log_text: Optional[bool] = False, key_tuple: Optional[bool] = True
    ) -> Dict[Any, Any]:
        """
        Helper method to setup metrics and state attributes to log
        """
        all_state_attrs = {self.metric_key: OrderedDict(),
                           self.output_key: OrderedDict(),
                           self.attribute_key: OrderedDict()}

        if self.metric_names is not None:
            if isinstance(self.metric_names, str) and self.metric_names == "all":
                all_state_attrs[self.metric_key] = OrderedDict(
                    engine.state.metrics)
            else:
                for name in self.metric_names:
                    if name not in engine.state.metrics:
                        warnings.warn(
                            f"Provided metric name '{name}' is missing "
                            f"in engine's state metrics: {list(engine.state.metrics.keys())}"
                        )
                        continue
                    all_state_attrs[self.metric_key][name] = engine.state.metrics[name]

        if self.output_transform is not None:
            output_dict = self.output_transform(engine.state.output)

            if not isinstance(output_dict, dict):
                output_dict = {"output": output_dict}

            all_state_attrs[self.output_key].update(output_dict)

        if self.state_attributes is not None:
            if isinstance(self.state_attributes, List):
                for attr in self.state_attributes:
                    if isinstance(attr, str):
                        all_state_attrs[self.attribute_key].update({attr: getattr(engine.state, attr, None)})
                    if isinstance(attr, Dict):
                        all_state_attrs[self.attribute_key].update(attr)
            if isinstance(self.state_attributes, Dict):
                all_state_attrs[self.attribute_key].update(self.state_attributes)

        all_state_attrs_dict = {}  # type: Dict[Any, OrderedDict]

        def key_tuple_tf(tag: str, name: str, *args: str) -> Tuple[str, ...]:
            return (tag, name) + args

        def key_str_tf(tag: str, name: str, *args: str) -> str:
            return "/".join((tag, name) + args)

        for attr_name, attr_value in all_state_attrs.items():
            key_tf = key_tuple_tf if key_tuple else key_str_tf
            state_attrs_dict = OrderedDict()

            for name, value in attr_value.items():
                if isinstance(value, PTensor):
                    if value.ndimension() == 1 and value.size == 1:
                        state_attrs_dict[key_tf(self.tag, name)] = value.item()
                    if value.ndimension() == 1 and value.size > 1:
                        for i, v in enumerate(value):
                            state_attrs_dict[key_tf(
                                self.tag, name, str(i))] = v.item()

                if isinstance(value, TTensor):
                    if value.ndimension() == 0:
                        state_attrs_dict[key_tf(self.tag, name)] = value.item()
                    if value.ndimension() == 1:
                        for i, v in enumerate(value):
                            state_attrs_dict[key_tf(
                                self.tag, name, str(i))] = v.item()

                if isinstance(value, numbers.Number):
                    state_attrs_dict[key_tf(self.tag, name)] = value
                elif isinstance(value, Sequence):
                    if attr_name != self.metric_key:
                        for i, v in enumerate(value):
                            state_attrs_dict[key_tf(self.tag, name, str(i))] = v
                elif isinstance(value, Dict):
                    if attr_name == self.attribute_key:
                        state_attrs_dict[key_tf(self.tag, name)] = value
                else:
                    if isinstance(value, str) and log_text:
                        state_attrs_dict[key_tf(self.tag, name)] = value
                    else:
                        warnings.warn(
                            f"Logger output_handler can not log metrics value type {type(value)}")

            all_state_attrs_dict[attr_name] = state_attrs_dict

        if self.annotation_transform is not None:
            all_state_attrs_dict['annotations'] = self.annotation_transform()

        return all_state_attrs_dict


class MLflowLogger(BaseLogger):
    """
    MLflow tracking client handler to log parameters and metrics during the training and validation.
    """
    def __init__(self, **kwargs):
        super(MLflowLogger, self).__init__(**kwargs)

        if idist.get_rank() == MASTER_RANK:
            mlflow.set_tracking_uri(self.tracking_uri)
            experiment_name = mlflow.set_experiment(experiment_name=str(self.experiment_name))
            experiment_id = experiment_name.experiment_id
            run_id = mlflow.start_run(experiment_id=experiment_id, run_name=self.run_name).info.run_id
            os.environ["GAEA_EXPERIMENT__RUN_ID"] = str(run_id)

    def __getattr__(self, attr: Any) -> Any:
        return getattr(mlflow, attr)

    def close(self) -> None:
        mlflow.end_run()

    @staticmethod
    def log_params(params: Dict):
        """
        Log a batch of params for the current run.
        """
        if idist.get_rank() == MASTER_RANK:
            for key, value in params.items():
                try:
                    if isinstance(value, Dict):
                        for k, v in value.items():
                            mlflow.log_params(params={k: v})
                    else:
                        mlflow.log_params(params={key: value})
                except mlflow.exceptions.RestException as err:
                    pass

    @staticmethod
    def log_metrics(metrics: Dict, step: int):
        """
         Log multiple metrics for the current run.
        """
        if idist.get_rank() == MASTER_RANK:
            mlflow.log_metrics(metrics=metrics, step=step)

    def create_output_handler(self,
                              tag: str = '',
                              metric_names: Optional[Union[str,
                                                           List[str]]] = None,
                              output_transform: Optional[Callable] = None,
                              state_attributes: Optional[Union[Dict, List[Union[str, Dict]]]] = None,
                              annotation_transform: Optional[Callable] = None,
                              global_step_transform: Optional[Callable] = None
                              ):
        return MLflowOutputHandler(tag=tag, metric_names=metric_names, output_transform=output_transform,
                                   state_attributes=state_attributes, annotation_transform=annotation_transform,
                                   global_step_transform=global_step_transform)

    def attach_engine(self,
                      engine: Engine,
                      tag: str = '',
                      metric_names: Optional[Union[str, List[str]]] = None,
                      output_transform: Optional[Callable] = None,
                      state_attributes: Optional[Union[Dict, List[Union[str, Dict]]]] = None,
                      annotation_transform: Optional[Callable] = None,
                      global_step_transform: Optional[Callable] = None) -> RemovableEventHandle:
        """
        Shortcut method to attach `OutputHandler` to the logger.
        """
        log_handler = MLflowOutputHandler(tag=tag, metric_names=metric_names, output_transform=output_transform,
                                          state_attributes=state_attributes, annotation_transform=annotation_transform,
                                          global_step_transform=global_step_transform)
        return self.attach(engine=engine, log_handler=log_handler, event_name=Events.EPOCH_COMPLETED)


class MLflowOutputHandler(BaseOutputHandler):
    """
    MLflow helper handler to log engine's output and/or metrics.
    Args:
        tag: common title for all produced plots. For example, 'training'
        metric_names: list of metric names to plot or a string "all" to plot all available metrics.
        output_transform: output transform function to prepare `engine.state.output` as a number.
        state_attributes: list of attributes of the ``trainer.state`` to plot.
    """

    def __init__(self,
                 tag: str,
                 metric_names: Optional[Union[str, List[str]]] = None,
                 output_transform: Optional[Callable] = None,
                 state_attributes: Optional[Union[Dict, List[Union[str, Dict]]]] = None,
                 annotation_transform: Optional[Callable] = None,
                 global_step_transform: Optional[Callable] = None,
                 ) -> None:
        super(MLflowOutputHandler, self).__init__(tag, metric_names, output_transform,
                                               state_attributes, annotation_transform, global_step_transform)

    def __call__(self, engine: Engine, logger: MLflowLogger, event_name: Union[str, Events]) -> None:
        if not isinstance(logger, MLflowLogger):
            raise TypeError(
                "Handler `MLflowOutputHandler` works only with MLflowLogger")

        rendered = self._setup_output_metrics_state_attrs(engine)

        annotations = None
        if "annotations" in rendered:
            annotations = rendered.pop("annotations")

        global_step = self.global_step_transform(
            engine, event_name)  # type: ignore[misc]

        if not isinstance(global_step, int):
            raise TypeError(
                f"global_step must be int, got {type(global_step)}."
                " Please check the output of global_step_transform."
            )

        # Additionally recheck metric names as MLflow rejects non-valid names with MLflowException
        from mlflow.utils.validation import _VALID_PARAM_AND_METRIC_NAMES

        for attr_key, attr_value in rendered.items():
            metrics = {}
            for keys, value in attr_value.items():
                key = " ".join(keys).strip()
                metrics[key] = value

            for key in list(metrics.keys()):
                if not _VALID_PARAM_AND_METRIC_NAMES.match(key):
                    warnings.warn(
                        f"MLflowLogger output_handler encountered an invalid metric name '{key}' that "
                        "will be ignored and not logged to MLflow"
                    )
                    del metrics[key]
            if len(metrics) > 0:
                if attr_key == self.metric_key or attr_key == self.output_key:
                    logger.log_metrics(metrics, step=global_step)
                else:
                    logger.log_params(metrics)


class AimLogger(BaseLogger):
    """
    Aim tracking client handler to log parameters and metrics during the training and validation.

    :param log_system_params: Enable/Disable logging of system params such as installed packages, git info,
    environment variables, etc.
    :type log_system_params: Optional[bool] (optional)
    :param system_tracking_interval: Sets the tracking interval in seconds for system usage metrics (CPU, Memory, etc.).
     Set to `None` to disable system metrics tracking.
    :type system_tracking_interval: Optional[Union[int, float]]
    :param capture_terminal_logs: Enable process output capturing.
    :type capture_terminal_logs: Optional[bool] (optional)
    """
    def __init__(self,
                 log_system_params: Optional[bool] = True,
                 system_tracking_interval: Optional[Union[int,
                                                          float]] = DEFAULT_SYSTEM_TRACKING_INT,
                 capture_terminal_logs: Optional[bool] = True,
                 is_get_job: Optional[bool] = True,
                 **kwargs):
        super(AimLogger, self).__init__(**kwargs)
        if self.tracking_uri.startswith("http"):
            self.tracking_uri = self.tracking_uri.replace("http", "aim")
        elif self.tracking_uri.startswith("https"):
            self.tracking_uri = self.tracking_uri.replace("https", "aim")
        elif self.tracking_uri.startswith("aim"):
            self.tracking_uri = self.tracking_uri
        else:
            self.tracking_uri = "aim://" + self.tracking_uri

        self.config_param = {}
        if idist.get_rank() == MASTER_RANK:
            self.aim_run = aim.Run(repo=self.tracking_uri,
                                   experiment=self.experiment_name,
                                   log_system_params=log_system_params,
                                   system_tracking_interval=system_tracking_interval,
                                   capture_terminal_logs=capture_terminal_logs)
            run_id = self.aim_run.hash
            os.environ["GAEA_EXPERIMENT__RUN_ID"] = run_id
            if self.run_name is not None and len(self.run_name) > 0:
                self.aim_run.name = self.run_name
                if is_get_job:
                    self._get_windmill_job()
            self._write_run_id(run_id=run_id)

    def _write_run_id(self, run_id: str = ""):
        """
        Writes the run id to the environment variable GAEA_EXPERIMENT__RUN_ID
        """
        if run_id != "":
            file = os.path.join(PRODUCT_PATH, "run_id")
            with open(file, "w") as fd:
                fd.write(run_id)

    def _get_windmill_job(self):
        """
        Get windmill job.
        """
        from gaea_operator.plugins import training_client

        assert training_client is not None, "When get job, the training_client must be not None."

        name = os.environ["JOB_NAME"]

        name = name.split("/")
        response = training_client.get_job(workspace_id=name[1], project_name=name[3], local_name=name[5])

        value = {"org_id": response.org_id, "project_name": response.project_name}

        self.log_params(value=value, name="config")

        self.config_param = value

    def close(self) -> None:
        self.aim_run.close()

    def log_params(self, value: Any, name: str):
        """
        Log a batch of params for the current run.
        """
        if isinstance(value, Dict):
            value.update(self.config_param)
        self.aim_run[name] = value

    def log_metrics(self, value: Any, name: str, step: int, context: Dict):
        """
         Log multiple metrics for the current run.
        """
        self.aim_run.track(value=value, name=name, epoch=step, context=context)

    def log_annotations(self, file_name: int, anno: Optional[List] = None,
                        color_map_list: Optional[List] = None, catid2clsid: Optional[Dict] = None):
        """
        Log annotation on image for the current run.
        """
        im = visualize_box_mask(im=file_name, results=anno, catid2clsid=catid2clsid, color_list=color_map_list)

        caption = f"file_name: {file_name}\nwidth: {anno[0]['width']}  height:  {anno[0]['height']}"
        aim_figure = aim.Image(im, caption=caption)
        name = os.environ.get('GAEA_BASE_MODEL_URI', 'annotation')
        self.aim_run.track(aim_figure, name=name)

    def add_atg(self, value: str):
        try:
            self.aim_run.add_tag(value)
        except Exception as err:
            self._logger.error(err)

    def create_output_handler(self,
                              tag: str,
                              metric_names: Optional[Union[str,
                                                           List[str]]] = None,
                              output_transform: Optional[Callable] = None,
                              state_attributes: Optional[Union[Dict, List[Union[str, Dict]]]] = None,
                              annotation_transform: Optional[Callable] = None,
                              global_step_transform: Optional[Callable] = None
                              ):
        return AimOutputHandler(tag=tag, metric_names=metric_names, output_transform=output_transform,
                                state_attributes=state_attributes, annotation_transform=annotation_transform,
                                global_step_transform=global_step_transform)

    def attach_engine(self,
                      engine: Engine,
                      tag: str,
                      metric_names: Optional[Union[str, List[str]]] = None,
                      output_transform: Optional[Callable] = None,
                      state_attributes: Optional[Union[Dict, List[Union[str, Dict]]]] = None,
                      annotation_transform: Optional[Callable] = None,
                      global_step_transform: Optional[Callable] = None) -> RemovableEventHandle:
        """
        Shortcut method to attach `OutputHandler` to the logger.
        """
        log_handler = AimOutputHandler(tag=tag, metric_names=metric_names, output_transform=output_transform,
                                       state_attributes=state_attributes, annotation_transform=annotation_transform,
                                       global_step_transform=global_step_transform)

        if idist.get_rank() == MASTER_RANK:
            engine.add_event_handler(Events.TERMINATE, self.close)
            self.attach(engine=engine, log_handler=log_handler, event_name=Events.EPOCH_COMPLETED)


class AimOutputHandler(BaseOutputHandler):
    """
    Aim helper handler to log engine's output and/or metrics.
    Args:
        tag: common title for all produced plots. For example, 'training'
        metric_names: list of metric names to plot or a string "all" to plot all available metrics.
        output_transform: output transform function to prepare `engine.state.output` as a number.
        state_attributes: list of attributes of the ``trainer.state`` to plot.
    """

    def __init__(self,
                 tag: str,
                 metric_names: Optional[Union[str, List[str]]] = None,
                 output_transform: Optional[Callable] = None,
                 state_attributes: Optional[Union[Dict, List[Union[str, Dict]]]] = None,
                 annotation_transform: Optional[Callable] = None,
                 global_step_transform: Optional[Callable] = None,
                 ) -> None:
        self.origin_tag = tag
        super(AimOutputHandler, self).__init__("", metric_names, output_transform,
                                               state_attributes, annotation_transform, global_step_transform)

    def __call__(self, engine: Engine, logger: AimLogger, event_name: Union[str, Events]) -> None:
        if not isinstance(logger, AimLogger):
            raise TypeError(
                "Handler `AimOutputHandler` works only with AimLogger")

        rendered = self._setup_output_metrics_state_attrs(engine)

        annotations = None
        if "annotations" in rendered:
            annotations = rendered.pop("annotations")

        global_step = self.global_step_transform(
            engine, event_name)  # type: ignore[misc]

        if not isinstance(global_step, int):
            raise TypeError(
                f"global_step must be int, got {type(global_step)}."
                " Please check the output of global_step_transform."
            )

        logger.add_atg(value=self.origin_tag)

        for attr_key, attr_value in rendered.items():
            metrics = {}
            for keys, value in attr_value.items():
                key = " ".join(keys).strip()
                metrics[key] = value

            if len(metrics) > 0:
                if attr_key == self.metric_key or attr_key == self.output_key:
                    for name, value in metrics.items():
                        context = {'subset': self.origin_tag}
                        logger.log_metrics(value=value, name=name, step=global_step, context=context)
                else:
                    for name, value in metrics.items():
                        logger.log_params(name=name, value=value)

        if annotations is not None:
            is_log = True
            random_k = 1

            categories = set()
            image2annotation = defaultdict(list)
            for anno in annotations:
                if 'category_id' in anno:
                    categories.add(anno['category_id'])
                image2annotation[anno['file_name']].append(anno)
            color_map_list = get_color_map_list(len(categories))
            catid2clsid = {catid: i for i, catid in enumerate(categories)}

            is_log = bool(os.environ.get('GAEA_EXPERIMENT__IS_LOG', is_log))
            if is_log:
                random_k = float(os.environ.get('GAEA_EXPERIMENT__RANDOM_K', random_k))
                random_k = max(random_k, 0)
                random_k = random_k * len(image2annotation) if random_k <= 1 else random_k
                random_k = min(random_k, len(image2annotation))

                if random_k < len(image2annotation):
                    random_key = random.sample(image2annotation.keys(), random_k)
                    random_annotations = {}
                    for file_name in random_key:
                        random_annotations[file_name] = image2annotation[file_name]
                    image2annotation = random_annotations

                for file_name, anno in image2annotation.items():
                    logger.log_annotations(file_name=file_name, anno=anno,
                                           color_map_list=color_map_list, catid2clsid=catid2clsid)
