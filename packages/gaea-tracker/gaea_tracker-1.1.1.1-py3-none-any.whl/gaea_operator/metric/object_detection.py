#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2023/9/2
# @Author  : yanxiaodong
# @File    : object_detection.py
"""
from typing import Union, Sequence, Optional, Tuple, Dict, List, Any
import copy
import os

import gaea_operator.distributed as idist
from .metric import BaseMetric
from .function import MeanAveragePrecision


class ObjectDetectionMetric(BaseMetric):
    """
    Compute the `Mean-Average-Precision (mAP)
    """

    def __init__(self,
                 iou_thrs: Union[float, Sequence[float], None] = None,
                 area_rng: Union[float, Sequence[float], None] = None,
                 max_dets: Union[float, Sequence[float], None] = None,
                 classwise: Optional[bool] = False,
                 proposal_nums: Sequence[int] = (100, 300, 1000),
                 **kwargs):
        super(ObjectDetectionMetric, self).__init__(**kwargs)

        metrics = (MeanAveragePrecision(iou_thrs=iou_thrs,
                                        area_rng=area_rng,
                                        max_dets=max_dets,
                                        classwise=classwise,
                                        proposal_nums=proposal_nums,
                                        categories=self.categories,
                                        num_classes=self.num_classes),
                   )

        self._results = {}
        for metric in metrics:
            self.metrics[metric.name] = metric

    def update(self, output: Tuple[Dict[str, List], Dict[str, List]]) -> None:
        predictions, references = output[0], output[1]

        for name, m in self.metrics.items():
            m.update(predictions=predictions, references=references)

    def _format_metric_results(self, results: Dict):
        result_metrics = dict()

        if len(results[MeanAveragePrecision.global_name()]['bbox']) > 0:
            stats = results[MeanAveragePrecision.global_name()]['bbox']
            result_metrics['boundingBoxMeanAveragePrecision'] = stats[0]
            result_metrics['boundingBoxCategoryMetrics'] = \
                results[MeanAveragePrecision.global_name()]['bbox_results_per_category']
            result_metrics['boundingBoxIouMetrics'] = [
                {
                    'iouThreshold': 0.5,
                    'meanAveragePrecision': stats[1],
                },
                {
                    'iouThreshold': 0.75,
                    'meanAveragePrecision': stats[2],
                }
            ]

        if len(results[MeanAveragePrecision.global_name()]['segm']) > 0:
            stats = results[MeanAveragePrecision.global_name()]['segm']
            result_metrics['segmentationMeanAveragePrecision'] = stats[0]
            result_metrics['segmentationCategoryMetrics'] = \
                results[MeanAveragePrecision.global_name()]['segm_results_per_category']
            result_metrics['segmentationIouMetrics'] = [
                {
                    'iouThreshold': 0.5,
                    'meanAveragePrecision': stats[1],
                },
                {
                    'iouThreshold': 0.75,
                    'meanAveragePrecision': stats[2],
                }
            ]

        return result_metrics

    def format_check_metric_results(self, results: Dict):
        result_metrics = self._format_metric_results(results=results)

        schema_file = self.prefix + os.path.splitext(os.path.split(os.path.abspath(__file__))[1])[0] + ".yaml"
        schema_file = os.path.join(os.path.dirname(__file__), schema_file)

        self._check_metric_results(results=result_metrics, schema_file=schema_file)

        return result_metrics

    def gather(self):
        """
        在对不同进程的数据进行聚合
        """
        for _, m in self.metrics.items():
            for s_name, s_value in m.get_state().items():
                instance = copy.deepcopy(s_value)
                if getattr(instance, 'iouType') == 'bbox':
                    self._results['bbox'] = getattr(instance, 'eval_imgs_all')
                if getattr(instance, 'iouType') == 'segm':
                    self._results['segm'] = getattr(instance, 'eval_imgs_all')

        for key in self._results:
            res_list = self._results[key]
            K = len(res_list)
            A = len(res_list[0]) if len(res_list) > 0 else 0
            for k in range(K):
                for a in range(A):
                    res = res_list[k][a]
                    gather_res = idist.all_gather_object(res)
                    gather_res_list = []
                    for rank_res in gather_res:
                        gather_res_list.extend(rank_res)
                    if self.dataset_length is not None:
                        gather_res_list = gather_res_list[:self.dataset_length]
                    res_list[k][a] = gather_res_list

    def compute(self) -> Any:
        results = {}
        for k, m in self.metrics.items():
            results[k] = m.compute()

        return self.format_check_metric_results(results=results)