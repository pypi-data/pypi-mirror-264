#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : module.py
@Author        : yanxiaodong
@Date          : 2023/6/18
@Description   :
"""
from typing import List
from abc import ABCMeta, abstractmethod
from pathlib import Path
from datetime import datetime
import json

from .registry import METRIC


def list_metric_name():
    """
    List all metric name.
    """
    return list(METRIC.module_dict.keys())


def load(name: str, **init_kwargs):
    """
    Load a metric name to instance.
    """
    assert name in METRIC.module_dict, f'Metric name {name} is not in the {METRIC.module_dict.keys()}, ' \
                                       f'please use list_metric_name get right metric name.'
    module_class = METRIC.get(name)

    metric_instance = module_class(**init_kwargs)

    return metric_instance


def save(path, **data):
    """
    Saves results to a JSON file.
    """
    folder = Path(path)
    folder.mkdir(parents=True, exist_ok=True)
    file_name = 'metric.json'

    file_path = folder / file_name

    current_time = datetime.now()
    data["_timestamp"] = current_time.isoformat()

    with open(file_path, "w") as f:
        json.dump(data, f)


class DataModule(metaclass=ABCMeta):
    """
    A DataModule standardizes the ground true and prediction for metric calculation.
    """

    def __init__(self, ground_true_path: str = "", prediction_path: str = "", **kwargs):
        self.ground_true_path = ground_true_path
        self.prediction_path = prediction_path

    @abstractmethod
    def prepare_references(self):
        pass

    @abstractmethod
    def prepare_predictions(self):
        pass
