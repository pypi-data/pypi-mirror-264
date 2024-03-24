#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : metric.py    
@Author        : yanxiaodong
@Date          : 2023/5/26
@Description   :
"""
from typing import List, Union, Optional, Any
from abc import ABCMeta, abstractmethod
import numpy as np
import copy

from .plugin import Tensor


class MetricArgumentParser(object):
    """
    Metric Argument Parser.
    """
    def __init__(self, num_classes: int = 2):
        pass


class Metric(metaclass=ABCMeta):
    """
    Base class for all metrics present in the Metrics API.
    """
    metric_name = 'none'

    def __init__(self, num_classes: int = 2):
        self._defaults = {}
        self.num_classes = num_classes
        self.decimals = 4

    @property
    def name(self):
        return self.metric_name

    @classmethod
    def global_name(cls):
        return cls.metric_name

    def add_state(self, name: str, default: Any):
        """
        Add metric state variable.
        """
        setattr(self, name, default)
        self._defaults[name] = copy.deepcopy(default)

    def get_state(self):
        """
        Get metric state variable.
        """
        return self._defaults

    def reset(self) -> None:
        """
        Reset metric state variables to their default value.
        """
        for attr, default in self._defaults.items():
            setattr(self, attr, copy.deepcopy(default))

    @abstractmethod
    def update(self, predictions: Union[List, Tensor], references: Union[List, Tensor]) -> None:
        """
        Override this method to update the state variables of your metric class.
        """
        pass

    @abstractmethod
    def compute(self) -> Any:
        """
        Override this method to compute the final metric value.
        """
        pass

    def __call__(self, predictions: Union[List, Tensor], references: Union[List, Tensor]):
        self.update(predictions=predictions, references=references)
        self.compute()
