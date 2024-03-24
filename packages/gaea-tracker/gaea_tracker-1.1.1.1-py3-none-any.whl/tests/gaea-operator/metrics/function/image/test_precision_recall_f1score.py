#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : test_precision_recall_f1score.py
@Author        : yanxiaodong
@Date          : 2023/6/26
@Description   :
"""
import numpy as np
import paddle
from gaea_operator.metric.function.image import PrecisionRecallF1score, Precision, Recall, F1score


def test_precision_recsll_f1_score():
    num_classes = 2
    average = 'macro'
    precision_recsll_f1 = PrecisionRecallF1score(average=average, num_classes=num_classes)

    precision_recsll_f1.reset()
    references = np.array([0, 1, 0, 1, 0, 1])
    predictions = np.array([0, 0, 1, 1, 0, 1])
    precision_recsll_f1.update(predictions=predictions, references=references)
    res = precision_recsll_f1.compute()
    assert res[0] == 0.6667, 'Binary input np.ndarray category error for precision on macro.'
    assert res[1] == 0.6667, 'Binary input np.ndarray category error for recall on macro.'
    assert res[2] == 0.6667, 'Binary input np.ndarray category error for f1 on macro.'

    precision_recsll_f1.reset()
    references = np.array([0, 1, 0, 1, 0, 1])
    predictions = np.array([0.11, 0.22, 0.84, 0.73, 0.33, 0.92])
    precision_recsll_f1.update(predictions=predictions, references=references)
    res = precision_recsll_f1.compute()
    assert res[0] == 0.6667, 'Binary input np.ndarray score error for precision on macro.'
    assert res[1] == 0.6667, 'Binary input np.ndarray score error for recall on macro.'
    assert res[2] == 0.6667, 'Binary input np.ndarray score error for f1 on macro.'

    precision_recsll_f1.reset()
    references = paddle.to_tensor([0, 1, 0, 1, 0, 1])
    predictions = paddle.to_tensor([0, 0, 1, 1, 0, 1])
    precision_recsll_f1.update(predictions=predictions, references=references)
    res = precision_recsll_f1.compute()
    assert res[0] == 0.6667, 'Binary input paddle.tensor category error for precision on macro.'
    assert res[1] == 0.6667, 'Binary input paddle.tensor category error for precision on macro.'
    assert res[2] == 0.6667, 'Binary input paddle.tensor category error for precision on macro.'

    precision_recsll_f1.reset()
    references = paddle.to_tensor([0, 1, 0, 1, 0, 1])
    predictions = paddle.to_tensor([0.11, 0.22, 0.84, 0.73, 0.33, 0.92])
    precision_recsll_f1.update(predictions=predictions, references=references)
    res = precision_recsll_f1.compute()
    assert res[0] == 0.6667, 'Binary input paddle.tensor score error for precision on macro.'
    assert res[1] == 0.6667, 'Binary input paddle.tensor score error for recsll on macro.'
    assert res[2] == 0.6667, 'Binary input paddle.tensor score error for f1 on macro.'

    num_classes = 2
    average = 'micro'
    precision_recsll_f1 = PrecisionRecallF1score(average=average, num_classes=num_classes)

    precision_recsll_f1.reset()
    references = np.array([0, 1, 0, 1, 0, 1])
    predictions = np.array([0, 0, 1, 1, 0, 1])
    precision_recsll_f1.update(predictions=predictions, references=references)
    res = precision_recsll_f1.compute()
    assert res[0] == 0.6667, 'Binary input np.ndarray category error for precision on micro.'
    assert res[1] == 0.6667, 'Binary input np.ndarray category error for recall on micro.'
    assert res[2] == 0.6667, 'Binary input np.ndarray category error for f1 on micro.'

    precision_recsll_f1.reset()
    references = np.array([0, 1, 0, 1, 0, 1])
    predictions = np.array([0.11, 0.22, 0.84, 0.73, 0.33, 0.92])
    precision_recsll_f1.update(predictions=predictions, references=references)
    res = precision_recsll_f1.compute()
    assert res[0] == 0.6667, 'Binary input np.ndarray score error for precision on micro.'
    assert res[1] == 0.6667, 'Binary input np.ndarray score error for recall on micro.'
    assert res[2] == 0.6667, 'Binary input np.ndarray score error for f1 on micro.'

    precision_recsll_f1.reset()
    references = paddle.to_tensor([0, 1, 0, 1, 0, 1])
    predictions = paddle.to_tensor([0, 0, 1, 1, 0, 1])
    precision_recsll_f1.update(predictions=predictions, references=references)
    res = precision_recsll_f1.compute()
    assert res[0] == 0.6667, 'Binary input paddle.tensor category error for precision on micro.'
    assert res[1] == 0.6667, 'Binary input paddle.tensor category error for precision on micro.'
    assert res[2] == 0.6667, 'Binary input paddle.tensor category error for precision on micro.'

    precision_recsll_f1.reset()
    references = paddle.to_tensor([0, 1, 0, 1, 0, 1])
    predictions = paddle.to_tensor([0.11, 0.22, 0.84, 0.73, 0.33, 0.92])
    precision_recsll_f1.update(predictions=predictions, references=references)
    res = precision_recsll_f1.compute()
    assert res[0] == 0.6667, 'Binary input paddle.tensor score error for precision on micro.'
    assert res[1] == 0.6667, 'Binary input paddle.tensor score error for recsll on micro.'
    assert res[2] == 0.6667, 'Binary input paddle.tensor score error for f1 on micro.'

    num_classes = 3
    average = 'macro'
    precision_recsll_f1 = PrecisionRecallF1score(average=average, num_classes=num_classes)

    precision_recsll_f1.reset()
    references = np.array([2, 1, 0, 0])
    predictions = np.array([2, 1, 0, 1])
    precision_recsll_f1.update(predictions=predictions, references=references)
    res = precision_recsll_f1.compute()
    assert res[0] == 0.8333, 'Multiclass input np.ndarray category error for precision on macro.'
    assert res[1] == 0.8333, 'Multiclass input np.ndarray category error for recall on macro.'
    assert res[2] == 0.7778, 'Multiclass input np.ndarray category error for f1 on macro.'

    precision_recsll_f1.reset()
    references = np.array([2, 1, 0, 0])
    predictions = np.array([
        [0.16, 0.26, 0.58],
        [0.22, 0.61, 0.17],
        [0.71, 0.09, 0.20],
        [0.05, 0.82, 0.13],
    ])
    precision_recsll_f1.update(predictions=predictions, references=references)
    res = precision_recsll_f1.compute()
    assert res[0] == 0.8333, 'Multiclass input np.ndarray score error for precision on macro.'
    assert res[1] == 0.8333, 'Multiclass input np.ndarray score error for recall on macro.'
    assert res[2] == 0.7778, 'Multiclass input np.ndarray score error for f1 on macro.'

    precision_recsll_f1.reset()
    references = paddle.to_tensor([2, 1, 0, 0])
    predictions = paddle.to_tensor([2, 1, 0, 1])
    precision_recsll_f1.update(predictions=predictions, references=references)
    res = precision_recsll_f1.compute()
    assert res[0] == 0.8333, 'Multiclass input paddle.tensor category error for precision on macro.'
    assert res[1] == 0.8333, 'Multiclass input paddle.tensor category error for recall on macro.'
    assert res[2] == 0.7778, 'Multiclass input paddle.tensor category error for f1 on macro.'

    precision_recsll_f1.reset()
    references = paddle.to_tensor([2, 1, 0, 0])
    predictions = paddle.to_tensor([
        [0.16, 0.26, 0.58],
        [0.22, 0.61, 0.17],
        [0.71, 0.09, 0.20],
        [0.05, 0.82, 0.13],
    ])
    precision_recsll_f1.update(predictions=predictions, references=references)
    res = precision_recsll_f1.compute()
    assert res[0] == 0.8333, 'Multiclass input paddle.tensor score error for precision on macro.'
    assert res[1] == 0.8333, 'Multiclass input paddle.tensor score error for recall on macro.'
    assert res[2] == 0.7778, 'Multiclass input paddle.tensor score error for f1 on macro.'

    num_classes = 3
    average = 'micro'
    precision_recsll_f1 = PrecisionRecallF1score(average=average, num_classes=num_classes)

    precision_recsll_f1.reset()
    references = np.array([2, 1, 0, 0])
    predictions = np.array([2, 1, 0, 1])
    precision_recsll_f1.update(predictions=predictions, references=references)
    res = precision_recsll_f1.compute()
    assert res[0] == 0.75, 'Multiclass input np.ndarray category error for precision on micro.'
    assert res[1] == 0.75, 'Multiclass input np.ndarray category error for recall on micro.'
    assert res[2] == 0.75, 'Multiclass input np.ndarray category error for f1 on micro.'

    precision_recsll_f1.reset()
    references = np.array([2, 1, 0, 0])
    predictions = np.array([
        [0.16, 0.26, 0.58],
        [0.22, 0.61, 0.17],
        [0.71, 0.09, 0.20],
        [0.05, 0.82, 0.13],
    ])
    precision_recsll_f1.update(predictions=predictions, references=references)
    res = precision_recsll_f1.compute()
    assert res[0] == 0.75, 'Multiclass input np.ndarray score error for precision on micro.'
    assert res[1] == 0.75, 'Multiclass input np.ndarray score error for recall on micro.'
    assert res[2] == 0.75, 'Multiclass input np.ndarray score error for f1 on micro.'

    precision_recsll_f1.reset()
    references = paddle.to_tensor([2, 1, 0, 0])
    predictions = paddle.to_tensor([2, 1, 0, 1])
    precision_recsll_f1.update(predictions=predictions, references=references)
    res = precision_recsll_f1.compute()
    assert res[0] == 0.75, 'Multiclass input paddle.tensor category error for precision on micro.'
    assert res[1] == 0.75, 'Multiclass input paddle.tensor category error for recall on micro.'
    assert res[2] == 0.75, 'Multiclass input paddle.tensor category error for f1 on micro.'

    precision_recsll_f1.reset()
    references = paddle.to_tensor([2, 1, 0, 0])
    predictions = paddle.to_tensor([
        [0.16, 0.26, 0.58],
        [0.22, 0.61, 0.17],
        [0.71, 0.09, 0.20],
        [0.05, 0.82, 0.13],
    ])
    precision_recsll_f1.update(predictions=predictions, references=references)
    res = precision_recsll_f1.compute()
    assert res[0] == 0.75, 'Multiclass input paddle.tensor score error for precision on micro.'
    assert res[1] == 0.75, 'Multiclass input paddle.tensor score error for recall on micro.'
    assert res[2] == 0.75, 'Multiclass input paddle.tensor score error for f1 on micro.'

    num_classes = 3
    average = 'none'
    precision_recsll_f1 = PrecisionRecallF1score(average=average, num_classes=num_classes)

    precision_recsll_f1.reset()
    references = np.array([2, 1, 0, 0])
    predictions = np.array([2, 1, 0, 1])
    precision_recsll_f1.update(predictions=predictions, references=references)
    res = precision_recsll_f1.compute()
    assert (np.array(res[0]) == np.array([1, 0.5, 1])).all(), \
        'Multiclass input np.ndarray category error for precision on none.'
    assert (np.array(res[1]) == np.array([0.5, 1, 1])).all(), \
        'Multiclass input np.ndarray category error for recall on none.'
    assert (np.array(res[2]) == np.array([0.6667, 0.6667, 1])).all(), \
        'Multiclass input np.ndarray category error for f1 on none.'

    precision_recsll_f1.reset()
    references = np.array([2, 1, 0, 0])
    predictions = np.array([
        [0.16, 0.26, 0.58],
        [0.22, 0.61, 0.17],
        [0.71, 0.09, 0.20],
        [0.05, 0.82, 0.13],
    ])
    precision_recsll_f1.update(predictions=predictions, references=references)
    res = precision_recsll_f1.compute()
    assert (np.array(res[0]) == np.array([1, 0.5, 1])).all(), \
        'Multiclass input np.ndarray score error for precision on none.'
    assert (np.array(res[1]) == np.array([0.5, 1, 1])).all(), \
        'Multiclass input np.ndarray score error for recall on none.'
    assert (np.array(res[2]) == np.array([0.6667, 0.6667, 1])).all(), \
        'Multiclass input np.ndarray score error for f1 on none.'

    precision_recsll_f1.reset()
    references = paddle.to_tensor([2, 1, 0, 0])
    predictions = paddle.to_tensor([2, 1, 0, 1])
    precision_recsll_f1.update(predictions=predictions, references=references)
    res = precision_recsll_f1.compute()
    assert (paddle.to_tensor(res[0]) == paddle.to_tensor([1, 0.5, 1])).all(), \
        'Multiclass input paddle.tensor category error for precision on none.'
    assert (paddle.to_tensor(res[1]) == paddle.to_tensor([0.5, 1, 1])).all(), \
        'Multiclass input paddle.tensor category error for recall on none.'

    precision_recsll_f1.reset()
    references = paddle.to_tensor([2, 1, 0, 0])
    predictions = paddle.to_tensor([
        [0.16, 0.26, 0.58],
        [0.22, 0.61, 0.17],
        [0.71, 0.09, 0.20],
        [0.05, 0.82, 0.13],
    ])
    precision_recsll_f1.update(predictions=predictions, references=references)
    res = precision_recsll_f1.compute()
    assert (paddle.to_tensor(res[0]) == paddle.to_tensor([1, 0.5, 1])).all(), \
        'Multiclass input paddle.tensor score error for precision on none.'
    assert (paddle.to_tensor(res[1]) == paddle.to_tensor([0.5, 1, 1])).all(), \
        'Multiclass input paddle.tensor score error for recall on none.'

    num_classes = 2
    average = 'macro'
    precision = Precision(average=average, num_classes=num_classes)

    precision.reset()
    references = np.array([0, 1, 0, 1, 0, 1])
    predictions = np.array([0, 0, 1, 1, 0, 1])
    precision.update(predictions=predictions, references=references)
    res = precision.compute()
    assert round(res, 4) == 0.6667, 'Binary input np.ndarray category error for precision on macro.'

    num_classes = 2
    average = 'macro'
    recall = Recall(average=average, num_classes=num_classes)

    recall.reset()
    references = np.array([0, 1, 0, 1, 0, 1])
    predictions = np.array([0, 0, 1, 1, 0, 1])
    recall.update(predictions=predictions, references=references)
    res = recall.compute()
    assert round(res, 4) == 0.6667, 'Binary input np.ndarray category error for recall on macro.'

    num_classes = 2
    average = 'macro'
    f1score = F1score(average=average, num_classes=num_classes)

    f1score.reset()
    references = np.array([0, 1, 0, 1, 0, 1])
    predictions = np.array([0, 0, 1, 1, 0, 1])
    f1score.update(predictions=predictions, references=references)
    res = f1score.compute()
    assert round(res, 4) == 0.6667, 'Binary input np.ndarray category error for f1 on macro.'