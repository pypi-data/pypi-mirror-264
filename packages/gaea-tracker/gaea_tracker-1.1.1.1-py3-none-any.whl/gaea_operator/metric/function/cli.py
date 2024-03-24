#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : cli.py    
@Author        : yanxiaodong
@Date          : 2023/6/19
@Description   :
"""
from typing import Optional, List, Union, Any
import logging
import os
from jsonargparse import ArgumentParser, ActionConfigFile

from .module import DataModule, load, save
from .metric import Metric, MetricArgumentParser
from .registry import METRIC

MOUNT_PATH = os.environ.get("PF_WORK_DIR", "")


class GaeaMetricArgumentParser(ArgumentParser):
    """
    Extension of jsonargparse's ArgumentParser for Gaea Metric.
    """
    def __init__(
            self,
            *args: Any,
            description: str = "gaea metric command line tool",
            env_prefix: str = "GAEA_METRIC",
            default_env: bool = True,
            **kwargs: Any) -> None:
        super(GaeaMetricArgumentParser, self).__init__(*args,
                                                       description=description,
                                                       env_prefix=env_prefix,
                                                       default_env=default_env,
                                                       **kwargs)

    def add_metric_args(self, metric_class: Optional[Metric] = None, nested_key: str = 'metric'):
        self.add_class_arguments(metric_class, nested_key=nested_key)

    def add_data_module_args(self, data_module_class: Optional[DataModule] = None, nested_key: str = 'data'):
        self.add_class_arguments(data_module_class, nested_key=nested_key)


class GaeaMetricCLI(object):
    """
    Implementation of a configurable command line tool for Gaea Metric.
    """
    def __init__(self,
                 data_module_class: DataModule,
                 metric_module_class: Optional[Union[Metric, List[Metric]]] = None,
                 parser: GaeaMetricArgumentParser = None,
                 auto_instance: Optional[bool] = True):
        self.data_module_class = data_module_class
        self.metric_module_class = metric_module_class
        self.parser = parser

        assert issubclass(self.data_module_class, DataModule), \
            f'Input data_module_class {self.data_module_class} must inherite superclass `DataModule`.'

        self.data_nested_key = 'data'
        self.metric_nested_key = 'metric'

        self.parser = self.init_parser()

        self._add_arguments(parser=self.parser)

        self.config = self.parser.parse_args()
        self._join_mount_path()

        self.instantiate_dataset_classes()
        if auto_instance:
            self.instantiate_metric_classes()

    def _join_mount_path(self):
        self.config.output_uri = os.path.join(MOUNT_PATH, self.config.output_uri)
        self.config.data.prediction_path = os.path.join(MOUNT_PATH, self.config.data.prediction_path)
        self.config.data.ground_true_path = os.path.join(MOUNT_PATH, self.config.data.ground_true_path)

    def init_parser(self) -> GaeaMetricArgumentParser:
        if self.parser is None:
            parser = GaeaMetricArgumentParser()
        else:
            parser = self.parser

        parser.add_argument(
            "-c",
            "--config",
            action=ActionConfigFile,
            help="Path to a configuration file in json or yaml format"
        )
        parser.add_argument(
            "--name",
            type=str,
            nargs='+',
            help="Metric name"
        )
        parser.add_argument(
            "--output_uri",
            type=str,
            help="Output uri"
        )

        return parser

    def _add_arguments(self, parser: GaeaMetricArgumentParser) -> None:
        parser.add_data_module_args(self.data_module_class, nested_key=self.data_nested_key)
        parser.add_metric_args(MetricArgumentParser, nested_key=self.metric_nested_key)

    def instantiate_dataset_classes(self) -> None:
        self.config_init = self.parser.instantiate_classes(self.config)
        self.data_module = self.config_init.get(self.data_nested_key)

    def instantiate_metric_classes(self) -> None:
        self.loaded_modules = []
        if self.metric_module_class:
            logging.info(f'Paramter metric_module_class is {self.metric_module_class}')
            if not isinstance(self.metric_module_class, List):
                self.metric_module_class = [self.metric_module_class]
            self.loaded_modules = self.metric_module_class
        else:
            logging.info(f'Argument metric name is {self.config.name}')
            for name in self.config.name:
                self.loaded_modules.append(load(name=name, **self.config.metric.as_dict()))

    def __call__(self):
        predictions = self.data_module.prepare_predictions()
        references = self.data_module.prepare_references()

        for module in self.loaded_modules:
            module.update(predictions=predictions, references=references)

        results = {}
        for module in self.loaded_modules:
            results[module.name] = module.compute()

        save(self.config.output_uri, **results)

        return results









