#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : test_average_precision.py    
@Author        : yanxiaodong
@Date          : 2023/6/22
@Description   :
"""
import numpy as np
import paddle
from gaea_operator.metric.function.image import AveragePrecision


def test_average_precision():
    num_classes = 2
    thresholds = None
    average = 'macro'
    average_precision = AveragePrecision(num_classes=num_classes, thresholds=thresholds, average=average)

    average_precision.reset()
    references = np.array([0, 1, 1, 0])
    predictions = np.array([0, 0.5, 0.7, 0.8])
    average_precision.update(predictions=predictions, references=references)
    res = average_precision.compute()
    assert res == 0.5834, 'Binary input np.ndarray score error for average precision.'

    average_precision.reset()
    references = paddle.to_tensor([0, 1, 1, 0])
    predictions = paddle.to_tensor([0, 0.5, 0.7, 0.8])
    average_precision.update(predictions=predictions, references=references)
    res = average_precision.compute()
    assert (paddle.to_tensor(res) == paddle.to_tensor(0.5834)).all(), \
        'Binary input paddle.tensor score error for average precision.'

    num_classes = 2
    thresholds = 5
    average = 'macro'
    average_precision = AveragePrecision(num_classes=num_classes, thresholds=thresholds, average=average)

    average_precision.reset()
    references = np.array([0, 1, 1, 0])
    predictions = np.array([0, 0.5, 0.7, 0.8])
    average_precision.update(predictions=predictions, references=references)
    res = average_precision.compute()
    assert res == 0.6667, 'Binary input np.ndarray score error for average precision.'

    average_precision.reset()
    references = paddle.to_tensor([0, 1, 1, 0])
    predictions = paddle.to_tensor([0, 0.5, 0.7, 0.8])
    average_precision.update(predictions=predictions, references=references)
    res = average_precision.compute()
    assert (paddle.to_tensor(res) == paddle.to_tensor(0.6667)).all(), \
        'Binary input np.ndarray score error for average precision.'

    num_classes = 5
    thresholds = None
    average = 'macro'
    average_precision = AveragePrecision(num_classes=num_classes, thresholds=thresholds, average=average)

    average_precision.reset()
    references = np.array([0, 1, 3, 2])
    predictions = np.array([
        [0.75, 0.05, 0.05, 0.05, 0.05],
        [0.05, 0.75, 0.05, 0.05, 0.05],
        [0.05, 0.05, 0.75, 0.05, 0.05],
        [0.05, 0.05, 0.05, 0.75, 0.05]
    ])
    average_precision.update(predictions=predictions, references=references)
    res = average_precision.compute()
    assert res == 0.6250, 'Multiclass input np.ndarray score error for average precision.'

    average_precision.reset()
    references = paddle.to_tensor([0, 1, 3, 2])
    predictions = paddle.to_tensor([
        [0.75, 0.05, 0.05, 0.05, 0.05],
        [0.05, 0.75, 0.05, 0.05, 0.05],
        [0.05, 0.05, 0.75, 0.05, 0.05],
        [0.05, 0.05, 0.05, 0.75, 0.05]
    ])
    average_precision.update(predictions=predictions, references=references)
    res = average_precision.compute()
    assert res == 0.6250, 'Multiclass input paddle.tensor score error for average precision.'

    num_classes = 5
    thresholds = None
    average = 'none'
    average_precision = AveragePrecision(num_classes=num_classes, thresholds=thresholds, average=average)

    average_precision.reset()
    references = np.array([0, 1, 3, 2])
    predictions = np.array([
        [0.75, 0.05, 0.05, 0.05, 0.05],
        [0.05, 0.75, 0.05, 0.05, 0.05],
        [0.05, 0.05, 0.75, 0.05, 0.05],
        [0.05, 0.05, 0.05, 0.75, 0.05]
    ])
    average_precision.update(predictions=predictions, references=references)
    res = average_precision.compute()
    assert (np.array(res[:-1]) == np.array([1, 1, 0.25, 0.25])).all(), \
        'Multiclass input np.ndarray score error for average precision on average = none.'
    assert np.isnan(res[-1]), 'Multiclass input np.ndarray score error for average precision on average = none.'

    average_precision.reset()
    references = paddle.to_tensor([0, 1, 3, 2])
    predictions = paddle.to_tensor([
        [0.75, 0.05, 0.05, 0.05, 0.05],
        [0.05, 0.75, 0.05, 0.05, 0.05],
        [0.05, 0.05, 0.75, 0.05, 0.05],
        [0.05, 0.05, 0.05, 0.75, 0.05]
    ])
    average_precision.update(predictions=predictions, references=references)
    res = average_precision.compute()
    assert (paddle.to_tensor(res[:-1]) == paddle.to_tensor([1, 1, 0.25, 0.25])).all(), \
        'Multiclass input paddle.tensor score error for average precision on average = none.'
    assert paddle.isnan(paddle.to_tensor(res[-1])), 'Multiclass input paddle.tensor score error for average precision on average = none.'

    num_classes = 5
    thresholds = 5
    average = 'macro'
    average_precision = AveragePrecision(num_classes=num_classes, thresholds=thresholds, average=average)

    average_precision.reset()
    references = np.array([0, 1, 3, 2])
    predictions = np.array([
        [0.75, 0.05, 0.05, 0.05, 0.05],
        [0.05, 0.75, 0.05, 0.05, 0.05],
        [0.05, 0.05, 0.75, 0.05, 0.05],
        [0.05, 0.05, 0.05, 0.75, 0.05]
    ])
    average_precision.update(predictions=predictions, references=references)
    res = average_precision.compute()
    assert res == 0.5, 'Multiclass input np.ndarray score error for precision.'

    average_precision.reset()
    references = paddle.to_tensor([0, 1, 3, 2])
    predictions = paddle.to_tensor([
        [0.75, 0.05, 0.05, 0.05, 0.05],
        [0.05, 0.75, 0.05, 0.05, 0.05],
        [0.05, 0.05, 0.75, 0.05, 0.05],
        [0.05, 0.05, 0.05, 0.75, 0.05]
    ])
    average_precision.update(predictions=predictions, references=references)
    res = average_precision.compute()
    assert res == 0.5, 'Multiclass input paddle.tensor score error for precision.'

    num_classes = 5
    thresholds = 5
    average = 'none'
    average_precision = AveragePrecision(num_classes=num_classes, thresholds=thresholds, average=average)

    average_precision.reset()
    references = np.array([0, 1, 3, 2])
    predictions = np.array([
        [0.75, 0.05, 0.05, 0.05, 0.05],
        [0.05, 0.75, 0.05, 0.05, 0.05],
        [0.05, 0.05, 0.75, 0.05, 0.05],
        [0.05, 0.05, 0.05, 0.75, 0.05]
    ])
    average_precision.update(predictions=predictions, references=references)
    res = average_precision.compute()
    assert (np.array(res) == np.array([1, 1, 0.25, 0.25, 0])).all(), \
        'Multiclass input np.ndarray score error for precision.'

    average_precision.reset()
    references = paddle.to_tensor([0, 1, 3, 2])
    predictions = paddle.to_tensor([
        [0.75, 0.05, 0.05, 0.05, 0.05],
        [0.05, 0.75, 0.05, 0.05, 0.05],
        [0.05, 0.05, 0.75, 0.05, 0.05],
        [0.05, 0.05, 0.05, 0.75, 0.05]
    ])
    average_precision.update(predictions=predictions, references=references)
    res = average_precision.compute()
    assert (paddle.to_tensor(res) == paddle.to_tensor([1, 1, 0.25, 0.25, 0])).all(), \
        'Multiclass input paddle.tensor score error for precision.'
