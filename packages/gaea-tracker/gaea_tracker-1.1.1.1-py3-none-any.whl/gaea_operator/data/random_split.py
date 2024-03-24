#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : random_split.py
@Author        : yanxiaodong
@Date          : 2023/08/05
@Description   :
"""
import copy
import os
from typing import Optional, Dict

from gaea_operator.utils import setup_logger, FILESYSTEM


class RandomSample(object):
    def __init__(self,
                 dataset,
                 dataset_uri: str,
                 kind: Optional[str] = "COCO",
                 train_kwargs: Optional[Dict] = None,
                 validation_kwargs: Optional[Dict] = None):
        self._logger = setup_logger(__name__ + "." + self.__class__.__name__)

        self.dataset = dataset
        self.dataset_uri = dataset_uri
        self.kind = kind
        self.train_kwargs = train_kwargs
        self.validation_kwargs = validation_kwargs

        if self.train_kwargs is None:
            self.train_kwargs = {}
        if self.validation_kwargs is None:
            self.train_kwargs = {}

    def __call__(self, dataset_uri: Optional[str] = None, ratio: Optional[str] = None):
        validation_split = {}
        if ratio is not None:
            validation_split["ratio"] = ratio
        if dataset_uri is not None:
            validation_split["dataset_uri"] = dataset_uri

        if "dataset_uri" in validation_split:
            train_dataset = self.dataset(dataset_uri=self.dataset_uri, kind=self.kind, **self.train_kwargs)
            val_dataset = self.dataset(dataset_uri=dataset_uri, kind=self.kind, **self.validation_kwargs)

            return train_dataset, val_dataset

        if "ratio" in validation_split:
            ratio = float(validation_split["ratio"])

            train_dataset = self.dataset(dataset_uri=self.dataset_uri, kind=self.kind, **self.train_kwargs, ratio=ratio)
            common_data_instance = copy.deepcopy(train_dataset.common_data_instance)
            val_dataset = self.dataset(dataset_uri=self.dataset_uri, kind=self.kind, **self.validation_kwargs,
                                       common_data_instance=common_data_instance)

            return train_dataset, val_dataset
