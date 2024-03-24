#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : image_classification_multiclass.py
@Author        : yanxiaodong
@Date          : 2023/5/24
@Description   :
"""
from typing import Any, Tuple, Union, Dict, List
import numpy as np
import copy
import os
import itertools

from gaea_operator.plugin import Tensor, PTensor, paddle, torch
import gaea_operator.distributed as idist
from .metric import BaseMetric
from .function import Accuracy, AveragePrecision, PrecisionRecallF1score, ConfusionMatrix, PrecisionRecallCurve


class ImageClassificationMultiClassMetric(BaseMetric):
    """
    Category: Image/ImageClassification/MultiClass metric.
    """

    def __init__(self, **kwargs):
        super(ImageClassificationMultiClassMetric, self).__init__(**kwargs)

        metrics = (Accuracy(num_classes=self.num_classes),
                   AveragePrecision(num_classes=self.num_classes, thresholds=100, average='none'),
                   PrecisionRecallF1score(num_classes=self.num_classes, average='macro'),
                   ConfusionMatrix(num_classes=self.num_classes),
                   PrecisionRecallCurve(num_classes=self.num_classes, thresholds=100))

        self.current_sum_image = {}
        for metric in metrics:
            self.metrics[metric.name] = metric
            self.current_sum_image[metric.name] = 0

        self.batch_size = 0

    def reset(self) -> None:
        """
        Reset attribution
        """
        super().reset()
        for name in self.current_sum_image:
            self.current_sum_image[name] = 0

    def update(self, output: Tuple[Union[np.ndarray, Tensor], Union[np.ndarray, Tensor]]) -> None:
        predictions, groundtruths = output[0], output[1]
        assert type(predictions) == type(groundtruths), 'prediction type and ground truth type should be same, got ' \
                                                        f'prediction {type(predictions)} and ' \
                                                        f'ground truth {type(groundtruths)} instead.'

        for name, m in self.metrics.items():
            if isinstance(list(m.get_state().values())[0], List):
                if idist.get_world_size() == 1:
                    last_sum_image = self.current_sum_image[name]
                    self.current_sum_image[name] += len(predictions)
                    if self.current_sum_image[name] > self.dataset_length:
                        cut_predictions = predictions[:self.dataset_length - last_sum_image, ...]
                        cut_groundtruths = groundtruths[:self.dataset_length - last_sum_image]
                        m.update(cut_predictions, cut_groundtruths)
                    else:
                        m.update(predictions, groundtruths)
                else:
                    m.update(predictions=predictions, references=groundtruths)
            else:
                last_sum_image = self.current_sum_image[name]
                batch_size = len(predictions)
                self.batch_size = batch_size
                self.current_sum_image[name] += batch_size

                if self.current_sum_image[name] * idist.get_world_size() > self.dataset_length:
                    if self.last_batch_padding_policy == self.all_last_batch_padding_policy[0]:
                        every_rank_images = self.dataset_length // idist.get_world_size()
                        if idist.get_rank() == idist.get_world_size() - 1:
                            residue = self.dataset_length % idist.get_world_size() + every_rank_images % batch_size
                            cut_predictions = predictions[:residue, ...]
                            cut_groundtruths = groundtruths[:residue]
                            if residue != 0:
                                m.update(predictions=cut_predictions, references=cut_groundtruths)
                        else:
                            residue = every_rank_images % batch_size
                            if residue != 0:
                                cut_predictions = predictions[:residue, ...]
                                cut_groundtruths = groundtruths[:residue]
                                m.update(predictions=cut_predictions, references=cut_groundtruths)
                    if self.last_batch_padding_policy == self.all_last_batch_padding_policy[1]:
                        no_append_image = self.dataset_length - last_sum_image * idist.get_world_size()
                        input_int = no_append_image // batch_size
                        if idist.get_rank() < input_int:
                            m.update(predictions=predictions, references=groundtruths)
                        if idist.get_rank() == input_int:
                            residue = no_append_image % batch_size
                            cut_predictions = predictions[:residue, ...]
                            cut_groundtruths = groundtruths[:residue]
                            m.update(predictions=cut_predictions, references=cut_groundtruths)
                else:
                    m.update(predictions=predictions, references=groundtruths)

    def _format_metric_results(self, results: Dict):
        result_metrics = dict()

        result_metrics['accuracy'] = results[Accuracy.global_name()]
        result_metrics['precision'] = results[PrecisionRecallF1score.global_name()][0]
        result_metrics['recall'] = results[PrecisionRecallF1score.global_name()][1]
        result_metrics['f1score'] = results[PrecisionRecallF1score.global_name()][2]

        try:
            from terminaltables import SingleTable
        except Exception as err:
            raise err

        table_data = [['accuracy', 'precision', 'recall', 'f1score']]
        table_data.append(list(result_metrics.values()))
        table_data = SingleTable(table_data)
        self._logger.info(table_data.table)

        result_metrics['confusionMatrix'] = {'annotationSpecs': [], 'rows': []}
        cid2cname = {cate['id']: cate['name'] for cate in self.categories}
        for i, res in enumerate(results[ConfusionMatrix.global_name()]):
            result_metrics['confusionMatrix']['annotationSpecs'].append({'id': i, 'categoryName': cid2cname[i]})
            result_metrics['confusionMatrix']['rows'].append({'row': res})

        result_metrics['categoryMetrics'] = []
        if self.num_classes == 2:
            metrics = {'categoryName': self.categories[1]['name'],
                       'auPrc': results[AveragePrecision.global_name()],
                       'confidenceMetrics': []}
            for precision, recall, threshold in zip(*results[PrecisionRecallCurve.global_name()]):
                metrics['confidenceMetrics'].append({'confidenceThreshold': threshold,
                                                     'precision': precision,
                                                     'recall': recall})
            result_metrics['categoryMetrics'].append(metrics)
        else:
            for i in range(len(self.categories)):
                metrics = {'categoryName': self.categories[i]['name'],
                           'auPrc': results[AveragePrecision.global_name()][i],
                           'confidenceMetrics': []}
                precisions = results[PrecisionRecallCurve.global_name()][0][i]
                recalls = results[PrecisionRecallCurve.global_name()][1][i]
                thresholds = results[PrecisionRecallCurve.global_name()][2]
                for precision, recall, threshold in zip(precisions, recalls, thresholds):
                    metrics['confidenceMetrics'].append({'confidenceThreshold': threshold,
                                                         'precision': precision,
                                                         'recall': recall})
                result_metrics['categoryMetrics'].append(metrics)

        return result_metrics

    def format_check_metric_results(self, results: Dict):
        result_metrics = self._format_metric_results(results=results)

        schema_file = self.prefix + os.path.splitext(os.path.split(os.path.abspath(__file__))[1])[0] + ".yaml"
        schema_file = os.path.join(os.path.dirname(__file__), schema_file)

        self._check_metric_results(results=result_metrics, schema_file=schema_file)

        return result_metrics

    def gather(self):
        for _, m in self.metrics.items():
            for s_name, s_value in m.get_state().items():
                collected_results = copy.deepcopy(s_value)

                if isinstance(s_value, List):
                    for res in getattr(m, s_name):
                        collected_results.extend(idist.all_gather_object(res))
                    if self.dataset_length is not None:
                        if isinstance(collected_results[0], np.ndarray):
                            collected_results = np.concatenate(collected_results, axis=0)
                        elif isinstance(collected_results[0], PTensor):
                            collected_results = paddle.concat(collected_results, axis=0)
                        else:
                            collected_results = torch.concat(collected_results, axis=0)

                        if self.last_batch_padding_policy == self.all_last_batch_padding_policy[0]:
                            every_rank_images = self.dataset_length // idist.get_world_size()
                            iter_num = every_rank_images // self.batch_size
                            residue = every_rank_images % self.batch_size
                            delete_ids = []
                            current_id = iter_num * self.batch_size * idist.get_world_size()
                            if residue > 0:
                                for i in range(1, idist.get_world_size()):
                                    delete_ids.extend(range(current_id + residue, current_id + self.batch_size))
                                    current_id += self.batch_size
                            delete_ids.extend(range(self.dataset_length + len(delete_ids), len(collected_results)))
                            res_ids = np.arange(len(collected_results))
                            retain_ids = np.delete(res_ids, delete_ids, axis=0).tolist()
                            collected_results = collected_results[retain_ids]
                        if self.last_batch_padding_policy == self.all_last_batch_padding_policy[1]:
                            collected_results = collected_results[:self.dataset_length]
                        collected_results = [collected_results]
                else:
                    collected_results = idist.all_reduce(getattr(m, s_name))

                setattr(m, s_name, collected_results)

    def compute(self) -> Any:
        results = {}
        for k, m in self.metrics.items():
            results[k] = m.compute()

        return self.format_check_metric_results(results=results)
