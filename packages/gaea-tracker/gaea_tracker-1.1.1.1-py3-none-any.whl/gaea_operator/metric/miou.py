#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : base_metric.py    
@Author        : xuningyuan
@Date          : 2023/05/29
@Description   :
"""
from typing import Union, Tuple
import numpy as np
from numpy import ndarray
import os.path as osp
import json

from gaea_operator.plugin import Tensor, PTensor, TTensor
from .base_metric import BaseMetric
import gaea_operator.distributed as idist


def calculate_area(pred: Union[Tensor, ndarray], label: Union[Tensor, ndarray], num_classes: int, ignore_index: int = 255, reduce_labels: bool = False) -> dict:
    """Calculate the area of intersection, pred and label.
    Args:
        pred (`Tensor or ndarray`):
            Prediction segmentation map of shape (channels, height, width) or (batch, channels, height, width).
        label (`Tensor or ndarray`):
            Ground truth segmentation map of shape (channels, height, width) or (batch, channels, height, width, channels).
        num_classes (`int`):
            Number of categories.
        ignore_index (`int`):
            Index that will be ignored during evaluation.
        reduce_labels (`bool`, *optional*, defaults to `False`):
            Whether or not to reduce all label values of segmentation maps by 1. Usually used for datasets where 0 is used for background,
            and background itself is not included in all classes of a dataset (e.g. ADE20k). The background label will be replaced by 255.
     Returns:
         area_intersect (`Tensor or ndarray`):
            The intersection of prediction and ground truth histogram on all classes.
         area_union (`Tensor or ndarray`):
            The union of prediction and ground truth histogram on all classes.
         area_pred_label (`Tensor or ndarray`):
            The prediction histogram on all classes.
         area_label (`Tensor or ndarray`):
            The ground truth histogram on all classes.
    """

    def calculate_area_paddle(pred: PTensor, label: PTensor, num_classes: int, ignore_index: int = 255) -> PTensor:
        import paddle
        pred_area = []
        label_area = []
        intersect_area = []
        mask = label != ignore_index

        for i in range(num_classes):
            pred_i = paddle.logical_and(pred == i, mask)
            label_i = label == i
            intersect_i = paddle.logical_and(pred_i, label_i)
            pred_area.append(paddle.sum(pred_i.astype(paddle.int32)))
            label_area.append(paddle.sum(label_i.astype(paddle.int32)))
            intersect_area.append(paddle.sum(intersect_i.astype(paddle.int32)))

        pred_area = paddle.concat(pred_area)
        label_area = paddle.concat(label_area)
        intersect_area = paddle.concat(intersect_area)
        
        return pred_area, label_area, intersect_area   

    def calculate_area_torch(pred: TTensor, label: TTensor, num_classes: int, ignore_index: int = 255) -> TTensor:
        import torch
        pred_area = []
        label_area = []
        intersect_area = []
        mask = label != ignore_index

        for i in range(num_classes):
            pred_i = torch.logical_and(pred == i, mask)
            label_i = label == i
            intersect_i = torch.logical_and(pred_i, label_i)
            pred_area.append(torch.sum(pred_i.type(torch.int32)))
            label_area.append(torch.sum(label_i.type(torch.int32)))
            intersect_area.append(torch.sum(intersect_i).type(torch.int32))

        pred_area = torch.concat(pred_area)
        label_area = torch.concat(label_area)
        intersect_area = torch.concat(intersect_area)
        
        return pred_area, label_area, intersect_area   
        
    def calcuate_area_numpy(pred: PTensor, label: PTensor, num_classes: int, ignore_index: int = 255) -> ndarray:
        mask = label != ignore_index
        mask = np.not_equal(label, ignore_index)
        pred = pred[mask]
        label = np.array(label)[mask]

        intersect = pred[pred == label]

        pred_area = np.histogram(pred, bins=num_classes, range=(0, num_classes - 1))[0]
        label_area = np.histogram(label, bins=num_classes, range=(0, num_classes - 1))[0]
        intersect_area = np.histogram(intersect, bins=num_classes, range=(0, num_classes - 1))[0]

        return pred_area, label_area,  intersect_area
    
        
    # chech the shape of pred and label
    if len(pred.shape) == 4:
        pred = pred.squeeze(axis=1)
    if len(label.shape) == 4:
        label = label.squeeze(axis=1)
    if not pred.shape == label.shape:
        raise ValueError('Shape of `pred` and `label should be equal, '
                         'but there are {} and {}.'.format(pred.shape, label.shape))
        
    # if reduce_labels, change the backgrond label to 255                                              
    if reduce_labels:
        label[label == 0] = 255
        label = label - 1
        label[label == 254] = 255
        
    # calculate the area
    if isinstance(pred, PTensor):
        return calculate_area_paddle(pred, label, num_classes, ignore_index)
    elif isinstance(pred, TTensor):
        return calculate_area_torch(pred, label, num_classes, ignore_index)
    elif isinstance(pred, ndarray):
        return calcuate_area_numpy(pred, label, num_classes, ignore_index)
    else:
        raise TypeError("Unsupported type {} for calculating area ".format(type(pred)))


class MeanIou(BaseMetric):
    def __init__(self, categories: list = [], ignore_index: int = 255, reduce_labels: bool = False, **kwargs):
        super().__init__(backend="paddle", **kwargs)

        self.num_classes = len(categories) + 1
        self.categories = categories
        self.ignore_index = ignore_index
        self.reduce_labels = reduce_labels
        self.reset()

    def reset(self):
        self.total_pred_area = 0.
        self.total_label_area = 0.
        self.total_intersect_area = 0.
        self._results = {}

    def update(self, output: Tuple[Tensor]) -> ndarray:
        pred_tensor, label_tensor = output
        pred_area, label_area, intersect_area = calculate_area(
            pred_tensor, label_tensor, self.num_classes, ignore_index=self.ignore_index)
        self.total_pred_area += pred_area
        self.total_label_area += label_area
        self.total_intersect_area += intersect_area
        
    def gather(self):
        world_size = idist.get_world_size()
        self.total_pred_area = idist.all_reduce(self.total_pred_area) / world_size
        self.total_label_area = idist.all_reduce(self.total_label_area) / world_size
        self.total_intersect_area = idist.all_reduce(self.total_intersect_area) / world_size
        if idist.get_rank() != 0:
            self.reset()

    def compute(self) -> ndarray:
        metrics = {}

        iou = self.total_intersect_area / (self.total_pred_area + self.total_label_area - self.total_intersect_area + 1e-8)
        acc = self.total_intersect_area / (self.total_label_area + 1e-8)
        
        metrics["meanIou"] = round(iou.mean().item(), 4)
        metrics["meanPixelAccuracy"] = round(acc.mean().item(), 4)
        metrics["categoryMetrics"] = []
        for idx, cat in enumerate(self.categories):
            metrics["categoryMetrics"].append({"categoryName": cat["name"],
                                               "iou": round(iou[idx + 1].item(), 4),
                                               "pixelAccuracy": round(acc[idx + 1].item(), 4)})
        for key in metrics:
            self._logger.info(f"{key}: {metrics[key]}")
        self.reset()

        self.metrics = metrics

        return metrics
    
    def save(self, dirname: str) -> None:
        """
        save to metric.json
        """
        if idist.get_rank() == 0:
            self._logger.info("writing metric in : {}".format(osp.join(dirname, "metric.json")))
            with open(osp.join(dirname, "metric.json"), "w") as f:
                json.dump(self.metrics, f, indent=4)
        
        
