#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : test_accuracy.py    
@Author        : yanxiaodong
@Date          : 2023/6/22
@Description   :
"""
import numpy as np
import paddle
from gaea_operator.metric.function.image import Accuracy


def test_accuracy():
    num_classes = 2
    topk = 1
    accuracy = Accuracy(num_classes=num_classes, topk=topk)

    accuracy.reset()
    references = np.array([0, 1, 0, 1, 0, 1])
    predictions = np.array([0, 0, 1, 1, 0, 1])
    accuracy.update(predictions=predictions, references=references)
    res = accuracy.compute()
    assert res == 0.6667, 'Binary input np.ndarray category error for accuracy.'

    accuracy.reset()
    references = np.array([0, 1, 0, 1, 0, 1])
    predictions = np.array([0.11, 0.22, 0.84, 0.73, 0.33, 0.92])
    accuracy.update(predictions=predictions, references=references)
    res = accuracy.compute()
    assert res == 0.6667, 'Binary input np.ndarray score error for accuracy.'

    accuracy.reset()
    references = paddle.to_tensor([0, 1, 0, 1, 0, 1])
    predictions = paddle.to_tensor([0, 0, 1, 1, 0, 1])
    accuracy.update(predictions=predictions, references=references)
    res = accuracy.compute()
    assert res == 0.6667, 'Binary input paddle.tensor category error for accuracy.'

    accuracy.reset()
    references = paddle.to_tensor([0, 1, 0, 1, 0, 1])
    predictions = paddle.to_tensor([0.11, 0.22, 0.84, 0.73, 0.33, 0.92])
    accuracy.update(predictions=predictions, references=references)
    res = accuracy.compute()
    assert res == 0.6667, 'Binary input paddle.tensor score error for accuracy.'

    num_classes = 3
    topk = 1
    accuracy = Accuracy(num_classes=num_classes, topk=topk)

    accuracy.reset()
    references = np.array([2, 1, 0, 0])
    predictions = np.array([2, 1, 0, 1])
    accuracy.update(predictions=predictions, references=references)
    res = accuracy.compute()
    assert res == 0.75, 'Multiclass input np.ndarray category error for accuracy.'

    accuracy.reset()
    references = np.array([2, 1, 0, 0])
    predictions = np.array([
        [0.16, 0.26, 0.58],
        [0.22, 0.61, 0.17],
        [0.71, 0.09, 0.20],
        [0.05, 0.82, 0.13],
    ])
    accuracy.update(predictions=predictions, references=references)
    res = accuracy.compute()
    assert res == 0.75, 'Multiclass input np.ndarray score error for accuracy.'

    accuracy.reset()
    references = paddle.to_tensor([2, 1, 0, 0])
    predictions = paddle.to_tensor([2, 1, 0, 1])
    accuracy.update(predictions=predictions, references=references)
    res = accuracy.compute()
    assert res == 0.75, 'Multiclass input paddle.tensor category error for accuracy.'

    accuracy.reset()
    references = paddle.to_tensor([2, 1, 0, 0])
    predictions = paddle.to_tensor([
        [0.16, 0.26, 0.58],
        [0.22, 0.61, 0.17],
        [0.71, 0.09, 0.20],
        [0.05, 0.82, 0.13],
    ])
    accuracy.update(predictions=predictions, references=references)
    res = accuracy.compute()
    assert res == 0.75, 'Multiclass input paddle.tensor score error for accuracy.'

    num_classes = 3
    topk = (1, 2)
    accuracy = Accuracy(num_classes=num_classes, topk=topk)

    accuracy.reset()
    references = np.array([2, 1, 0, 0])
    predictions = np.array([
        [0.16, 0.26, 0.58],
        [0.22, 0.61, 0.17],
        [0.71, 0.09, 0.20],
        [0.13, 0.82, 0.05],
    ])
    accuracy.update(predictions=predictions, references=references)
    res = accuracy.compute()
    assert res[0] == 0.75, 'Multiclass top 1 input np.ndarray score error for accuracy.'
    assert res[1] == 1, 'Multiclass top 2 input np.ndarray score error for accuracy.'

    accuracy.reset()
    references = paddle.to_tensor([2, 1, 0, 0])
    predictions = paddle.to_tensor([
        [0.16, 0.26, 0.58],
        [0.22, 0.61, 0.17],
        [0.71, 0.09, 0.20],
        [0.05, 0.82, 0.13],
    ])
    accuracy.update(predictions=predictions, references=references)
    res = accuracy.compute()
    assert res[0] == 0.75, 'Multiclass top 1 input paddle.tensor score error for accuracy.'
    assert res[1] == 0.75, 'Multiclass top 2 input paddle.tensor score error for accuracy.'
