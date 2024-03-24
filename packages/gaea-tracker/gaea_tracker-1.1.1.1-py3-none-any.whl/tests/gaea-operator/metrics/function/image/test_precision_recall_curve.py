#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : test_precision_recall_curve.py    
@Author        : yanxiaodong
@Date          : 2023/6/22
@Description   :
"""
import numpy as np
import paddle
from gaea_operator.metric.function.image import PrecisionRecallCurve


def test_precision_recall_curve():
    num_classes = 2
    thresholds = None
    precision_recall_curve = PrecisionRecallCurve(num_classes=num_classes, thresholds=thresholds)

    precision_recall_curve.reset()
    references = np.array([0, 1, 1, 0])
    predictions = np.array([0, 0.5, 0.7, 0.8])
    precision_recall_curve.update(predictions=predictions, references=references)
    res = precision_recall_curve.compute()
    assert (np.array(res[0]) == np.array([0.6667, 0.5, 0, 1])).all(), \
        'Binary input np.ndarray score error for precision.'
    assert (np.array(res[1]) == np.array([1, 0.5, 0, 0])).all(), \
        'Binary input np.ndarray score error for recall.'
    assert (np.array(res[2]) == np.array([0.5, 0.7, 0.8])).all(), \
        'Binary input np.ndarray score error for thresholds.'

    precision_recall_curve.reset()
    references = paddle.to_tensor([0, 1, 1, 0])
    predictions = paddle.to_tensor([0, 0.5, 0.7, 0.8])
    precision_recall_curve.update(predictions=predictions, references=references)
    res = precision_recall_curve.compute()
    assert (paddle.to_tensor(res[0]) == paddle.to_tensor([0.6667, 0.5, 0, 1])).all(), \
        'Binary input paddle.tensor score error for precision.'
    assert (paddle.to_tensor(res[1]) == paddle.to_tensor([1, 0.5, 0, 0])).all(), \
        'Binary input paddle.tensor score error for recall.'
    assert (paddle.to_tensor(res[2]) == paddle.to_tensor([0.5, 0.7, 0.8])).all(), \
        'Binary input paddle.tensor score error for thresholds.'

    num_classes = 2
    thresholds = 5
    precision_recall_curve = PrecisionRecallCurve(num_classes=num_classes, thresholds=thresholds)

    precision_recall_curve.reset()
    references = np.array([0, 1, 1, 0])
    predictions = np.array([0, 0.5, 0.7, 0.8])
    precision_recall_curve.update(predictions=predictions, references=references)
    res = precision_recall_curve.compute()
    assert (np.array(res[0]) == np.array([0.5, 0.6667, 0.6667, 0.0, 0.0, 1.0])).all(), \
        'Binary input np.ndarray score error for precision.'
    assert (np.array(res[1]) == np.array([1.0, 1.0, 1.0, 0.0, 0.0, 0.0])).all(), \
        'Binary input np.ndarray score error for recall.'
    assert (np.array(res[2]) == np.array([0.0, 0.25, 0.5, 0.75, 1.0])).all(), \
        'Binary input np.ndarray score error for thresholds.'

    precision_recall_curve.reset()
    references = paddle.to_tensor([0, 1, 1, 0])
    predictions = paddle.to_tensor([0, 0.5, 0.7, 0.8])
    precision_recall_curve.update(predictions=predictions, references=references)
    res = precision_recall_curve.compute()
    assert (paddle.to_tensor(res[0]) == paddle.to_tensor([0.5, 0.6667, 0.6667, 0.0, 0.0, 1.0])).all(), \
        'Binary input np.ndarray score error for precision.'
    assert (paddle.to_tensor(res[1]) == paddle.to_tensor([1.0, 1.0, 1.0, 0.0, 0.0, 0.0])).all(), \
        'Binary input np.ndarray score error for recall.'
    assert (paddle.to_tensor(res[2]) == paddle.to_tensor([0.0, 0.25, 0.5, 0.75, 1.0])).all(), \
        'Binary input np.ndarray score error for thresholds.'

    num_classes = 5
    thresholds = None
    precision_recall_curve = PrecisionRecallCurve(num_classes=num_classes, thresholds=thresholds)

    precision_recall_curve.reset()
    references = np.array([0, 1, 3, 2])
    predictions = np.array([
        [0.75, 0.05, 0.05, 0.05, 0.05],
        [0.05, 0.75, 0.05, 0.05, 0.05],
        [0.05, 0.05, 0.75, 0.05, 0.05],
        [0.05, 0.05, 0.05, 0.75, 0.05]
    ])
    precision_recall_curve.update(predictions=predictions, references=references)
    res = precision_recall_curve.compute()
    assert (np.array(res[0]) == np.array([[1.0, 1.0],
                                          [1.0, 1.0],
                                          [0.25, 0.0, 1.0],
                                          [0.25, 0.0, 1.0],
                                          [0.0, 1.0]])).all(), \
        'Multiclass input np.ndarray score error for precision.'
    assert (np.array(res[1]) == np.array([[1.0, 0.0],
                                          [1.0, 0.0],
                                          [1.0, 0.0, 0.0],
                                          [1.0, 0.0, 0.0],
                                          [np.nan, 0.0]])).all(), \
        'Multiclass input np.ndarray score error for recall.'
    assert (np.array(res[2]) == np.array([[0.75], [0.75], [0.05, 0.75], [0.05, 0.75], [0.05]])).all(), \
        'Multiclass input np.ndarray score error for thresholds.'

    precision_recall_curve.reset()
    references = paddle.to_tensor([0, 1, 3, 2])
    predictions = paddle.to_tensor([
        [0.75, 0.05, 0.05, 0.05, 0.05],
        [0.05, 0.75, 0.05, 0.05, 0.05],
        [0.05, 0.05, 0.75, 0.05, 0.05],
        [0.05, 0.05, 0.05, 0.75, 0.05]
    ])
    precision_recall_curve.update(predictions=predictions, references=references)
    res = precision_recall_curve.compute()
    assert res[0] == [[1.0, 1.0],
                      [1.0, 1.0],
                      [0.25, 0.0, 1.0],
                      [0.25, 0.0, 1.0],
                      [0.0, 1.0]], \
        'Multiclass input paddle.tensor score error for precision.'

    num_classes = 5
    thresholds = 5
    precision_recall_curve = PrecisionRecallCurve(num_classes=num_classes, thresholds=thresholds)

    precision_recall_curve.reset()
    references = np.array([0, 1, 3, 2])
    predictions = np.array([
        [0.75, 0.05, 0.05, 0.05, 0.05],
        [0.05, 0.75, 0.05, 0.05, 0.05],
        [0.05, 0.05, 0.75, 0.05, 0.05],
        [0.05, 0.05, 0.05, 0.75, 0.05]
    ])
    precision_recall_curve.update(predictions=predictions, references=references)
    res = precision_recall_curve.compute()
    assert (np.array(res[0]) == np.array(
        [[0.2500, 1.0000, 1.0000, 1.0000, 0.0000, 1.0000],
         [0.2500, 1.0000, 1.0000, 1.0000, 0.0000, 1.0000],
         [0.2500, 0.0000, 0.0000, 0.0000, 0.0000, 1.0000],
         [0.2500, 0.0000, 0.0000, 0.0000, 0.0000, 1.0000],
         [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 1.0000]])).all(), \
        'Multiclass input np.ndarray score error for precision.'
    assert (np.array(res[1]) == np.array(
        [[1., 1., 1., 1., 0., 0.],
         [1., 1., 1., 1., 0., 0.],
         [1., 0., 0., 0., 0., 0.],
         [1., 0., 0., 0., 0., 0.],
         [0., 0., 0., 0., 0., 0.]])).all(), \
        'Multiclass input np.ndarray score error for recall.'
    assert (np.array(res[2]) == np.array([0.0000, 0.2500, 0.5000, 0.7500, 1.0000])).all(), \
        'Multiclass input np.ndarray score error for thresholds.'

    precision_recall_curve.reset()
    references = paddle.to_tensor([0, 1, 3, 2])
    predictions = paddle.to_tensor([
        [0.75, 0.05, 0.05, 0.05, 0.05],
        [0.05, 0.75, 0.05, 0.05, 0.05],
        [0.05, 0.05, 0.75, 0.05, 0.05],
        [0.05, 0.05, 0.05, 0.75, 0.05]
    ])
    precision_recall_curve.update(predictions=predictions, references=references)
    res = precision_recall_curve.compute()
    assert (paddle.to_tensor(res[0]) == paddle.to_tensor(
        [[0.2500, 1.0000, 1.0000, 1.0000, 0.0000, 1.0000],
         [0.2500, 1.0000, 1.0000, 1.0000, 0.0000, 1.0000],
         [0.2500, 0.0000, 0.0000, 0.0000, 0.0000, 1.0000],
         [0.2500, 0.0000, 0.0000, 0.0000, 0.0000, 1.0000],
         [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 1.0000]])).all(), \
        'Multiclass input paddle.tensor score error for precision.'
    assert (paddle.to_tensor(res[1]) == paddle.to_tensor(
        [[1., 1., 1., 1., 0., 0.],
         [1., 1., 1., 1., 0., 0.],
         [1., 0., 0., 0., 0., 0.],
         [1., 0., 0., 0., 0., 0.],
         [0., 0., 0., 0., 0., 0.]])).all(), \
        'Multiclass input paddle.tensor score error for recall.'
    assert (paddle.to_tensor(res[2]) == paddle.to_tensor([0.0000, 0.2500, 0.5000, 0.7500, 1.0000])).all(), \
        'Multiclass input paddle.tensor score error for thresholds.'
