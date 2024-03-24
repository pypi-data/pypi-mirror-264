#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : accuracy.py
@Author        : yanxiaodong
@Date          : 2022/12/20
@Description   :
"""
from numbers import Number
from typing import Optional, Sequence, Tuple, Union

import numpy as np

from gaea_operator.plugin import PTensor, Tensor, TTensor, paddle, torch

from .base_metric import BaseMetric


def _numpy_topk(inputs: np.ndarray, k: int, axis: Optional[int] = None) -> Tuple:
    """
    A implementation of numpy top-k.
    This implementation returns the values and indices of the k largest
    elements along a given axis.
    Args:
        inputs: The input numpy array.
        k: The k in `top-k`.
        axis: The axis to sort along.
    """
    indices = np.argsort(inputs * -1.0, axis=axis)
    indices = np.take(indices, np.arange(k), axis=axis)
    values = np.take_along_axis(inputs, indices, axis=axis)
    return values, indices


class Accuracy(BaseMetric):
    """
    Top-k accuracy evaluation metric.
    Args:
        topk: If the predictions in ``topk`` matches the target, the predictions will be regarded as
            correct ones. Defaults to 1.
        thrs: Predictions with scores under the thresholds are considered negative. None means no
            thresholds. Defaults to 0.
        **kwargs: Keyword parameters passed to :class:`BaseMetric`.
    """
    name = 'top{}'

    def __init__(self,
                 topk: Union[int, Sequence[int]] = (1,),
                 thrs: Union[float, Sequence[Union[float, None]], None] = 0.,
                 **kwargs) -> None:
        super(Accuracy, self).__init__(**kwargs)

        if isinstance(topk, int):
            self.topk = (topk,)
        else:
            self.topk = tuple(topk)
        self.maxk = max(self.topk)

        if isinstance(thrs, float) or thrs is None:
            self.thrs = (thrs,)
        else:
            self.thrs = tuple(thrs)

    def update(self, output: Tuple[Union[np.ndarray, Tensor], Union[np.ndarray, Tensor]]) -> None:
        predictions, groundtruths = output[0], output[1]
        assert type(predictions) == type(groundtruths), 'prediction type and ground truth type should be same, got ' \
                                                        f'prediction {type(predictions)} and ' \
                                                        f'ground truth {type(groundtruths)} instead.'

        if isinstance(predictions, PTensor):
            corrects = self._compute_corrects_paddle(predictions, groundtruths)
        elif isinstance(predictions, np.ndarray):
            corrects = self._compute_corrects_numpy(predictions, groundtruths)
        elif isinstance(predictions, TTensor):
            corrects = self._compute_corrects_torch(predictions, groundtruths)
        else:
            raise TypeError('prediction support (`np.ndarray` or `paddle.Tensor` or `torch.Tensor`), '
                            f'got prediction {type(predictions)} instead.')

        if isinstance(corrects, Number):
            self._results.append(corrects)
        else:
            for correct in corrects:
                self._results.append(correct)

    def _compute_corrects_paddle(self, predictions: PTensor, labels: PTensor) -> PTensor:
        """
        Compute the correct number of per topk and threshold with Paddle.
        """
        if predictions.ndim == 1:
            corrects = (predictions.cast(labels.dtype) == labels)
            return corrects.cast('int32')

        predictions = paddle.nn.functional.softmax(predictions, axis=-1)
        pred_scores, pred_label = paddle.topk(predictions, self.maxk)
        pred_label = pred_label.t()

        corrects = (pred_label == labels.reshape((1, -1)).expand_as(pred_label))

        corrects_per_sample = paddle.zeros((len(predictions), len(self.topk), len(self.thrs)), 'int32')
        for i, k in enumerate(self.topk):
            for j, thr in enumerate(self.thrs):
                # Only prediction socres larger than thr are counted as correct
                if thr is not None:
                    thr_corrects = corrects & (pred_scores.t() > thr)
                else:
                    thr_corrects = corrects
                corrects_per_sample[:, i, j] = thr_corrects[:k].sum(0, keepdim=False).cast('int32')
        return corrects_per_sample

    def _compute_corrects_torch(self, predictions: PTensor, labels: TTensor) -> TTensor:
        """
        Compute the correct number of per topk and threshold with Torch.
        """
        if predictions.ndim == 1 or predictions.ndim == 0:
            corrects = (predictions.int() == labels)
            return corrects.int()

        predictions = torch.nn.functional.softmax(predictions, dim=-1)
        pred_scores, pred_label = predictions.topk(self.maxk)
        pred_label = pred_label.t()

        corrects = (pred_label == labels.view((1, -1)).expand_as(pred_label))

        corrects_per_sample = torch.zeros((len(predictions), len(self.topk), len(self.thrs)))
        for i, k in enumerate(self.topk):
            for j, thr in enumerate(self.thrs):
                # Only prediction socres larger than thr are counted as correct
                if thr is not None:
                    thr_corrects = corrects & (pred_scores.t() > thr)
                else:
                    thr_corrects = corrects
                corrects_per_sample[:, i, j] = thr_corrects[:k].sum(0, keepdim=False).int()
        return corrects_per_sample

    def _compute_corrects_numpy(self, predictions: np.ndarray, labels: np.ndarray) -> np.ndarray:
        """
        Compute the correct number of per topk and threshold with NumPy.
        """
        if predictions.ndim == 1 or predictions.ndim == 0:
            corrects = (predictions == labels)
            return corrects.astype(np.int32)

        pred_scores, pred_label = _numpy_topk(predictions, self.maxk, axis=1)
        pred_label = pred_label.T

        labels = np.broadcast_to(labels.reshape(1, -1), pred_label.shape)
        corrects = (pred_label == labels)

        corrects_per_sample = np.zeros((len(predictions), len(self.topk), len(self.thrs)))
        for i, k in enumerate(self.topk):
            for j, thr in enumerate(self.thrs):
                # Only prediction socres larger than thr are counted as correct
                if thr is not None:
                    thr_corrects = corrects & (pred_scores.T > thr)
                else:
                    thr_corrects = corrects
                corrects_per_sample[:, i, j] = thr_corrects[:k].sum(0, keepdims=True).astype(np.int32)

        return corrects_per_sample

    def compute(self):
        if isinstance(self._results[0], np.number) or self._results[0].ndim == 0 or self._results[0].ndim == 1:
            if isinstance(self._results[0], PTensor) and self._results[0].size == 1:
                return {'top1': float(sum(self._results) / len(self._results))}
            if not isinstance(self._results[0], PTensor):
                return {'top1': float(sum(self._results) / len(self._results))}

        metric_results = {}
        for i, k in enumerate(self.topk):
            for j, thr in enumerate(self.thrs):
                corrects = [result[i][j] for result in self._results]  # type: ignore
                acc = float(sum(corrects) / len(corrects))
                name = self.name.format(k)
                if len(self.thrs) > 1:
                    name += '_no-thr' if thr is None else f'_thr-{thr:.2f}'
                metric_results[name] = acc

        metric_msg = ", ".join(["{}: {:.5f}".format(key, metric_results[key]) for key in metric_results])
        self._logger.info(metric_msg)

        return metric_results
    
    def save(self, dirname: str) -> None:
        """
        Saves results to a JSON file.
        """
        pass
