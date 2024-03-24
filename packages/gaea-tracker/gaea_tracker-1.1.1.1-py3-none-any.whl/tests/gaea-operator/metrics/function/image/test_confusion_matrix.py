#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : test_confusion_matrix.py    
@Author        : yanxiaodong
@Date          : 2023/6/22
@Description   :
"""
import numpy as np
import paddle
from gaea_operator.metric.function.image import ConfusionMatrix


def test_confusion_matrix():
    num_classes = 2
    confusion_matrix = ConfusionMatrix(num_classes=num_classes)

    confusion_matrix.reset()
    references = np.array([1, 1, 0, 0])
    predictions = np.array([0, 1, 0, 0])
    confusion_matrix.update(predictions=predictions, references=references)
    res = confusion_matrix.compute()
    assert (np.array(res) == np.array([[2, 0], [1, 1]])).all(), \
        'Binary input np.ndarray category error for confusion_matrix.'

    confusion_matrix.reset()
    references = np.array([1, 1, 0, 0])
    predictions = np.array([0.35, 0.85, 0.48, 0.01])
    confusion_matrix.update(predictions=predictions, references=references)
    res = confusion_matrix.compute()
    assert (np.array(res) == np.array([[2, 0], [1, 1]])).all(), \
        'Binary input np.ndarray score error for confusion_matrix.'

    confusion_matrix.reset()
    references = paddle.to_tensor([1, 1, 0, 0])
    predictions = paddle.to_tensor([0.35, 0.85, 0.48, 0.01])
    confusion_matrix.update(predictions=predictions, references=references)
    res = confusion_matrix.compute()
    assert (paddle.to_tensor(res) == paddle.to_tensor([[2, 0], [1, 1]])).all(), \
        'Binary input paddle.tensor category error for confusion_matrix.'

    confusion_matrix.reset()
    references = paddle.to_tensor([1, 1, 0, 0])
    predictions = paddle.to_tensor([0.35, 0.85, 0.48, 0.01])
    confusion_matrix.update(predictions=predictions, references=references)
    res = confusion_matrix.compute()
    assert (paddle.to_tensor(res) == paddle.to_tensor([[2, 0], [1, 1]])).all(), \
        'Binary input paddle.tensor score error for confusion_matrix.'

    num_classes = 3
    confusion_matrix = ConfusionMatrix(num_classes=num_classes)

    confusion_matrix.reset()
    references = np.array([2, 1, 0, 0])
    predictions = np.array([2, 1, 0, 1])
    confusion_matrix.update(predictions=predictions, references=references)
    res = confusion_matrix.compute()
    assert (np.array(res) == np.array([[1, 1, 0], [0, 1, 0], [0, 0, 1]])).all(), \
    'Multiclass input np.ndarray category error for confusion_matrix.'

    confusion_matrix.reset()
    references = np.array([2, 1, 0, 0])
    predictions = np.array([
        [0.16, 0.26, 0.58],
        [0.22, 0.61, 0.17],
        [0.71, 0.09, 0.20],
        [0.05, 0.82, 0.13],
    ])
    confusion_matrix.update(predictions=predictions, references=references)
    res = confusion_matrix.compute()
    assert (np.array(res) == np.array([[1, 1, 0], [0, 1, 0], [0, 0, 1]])).all(), \
        'Multiclass input np.ndarray score error for confusion_matrix.'

    confusion_matrix.reset()
    references = paddle.to_tensor([2, 1, 0, 0])
    predictions = paddle.to_tensor([2, 1, 0, 1])
    confusion_matrix.update(predictions=predictions, references=references)
    res = confusion_matrix.compute()
    assert (paddle.to_tensor(res) == paddle.to_tensor([[1, 1, 0], [0, 1, 0], [0, 0, 1]])).all(), \
        'Multiclass input paddle.tensor category error for confusion_matrix.'

    confusion_matrix.reset()
    references = paddle.to_tensor([2, 1, 0, 0])
    predictions = paddle.to_tensor([
        [0.16, 0.26, 0.58],
        [0.22, 0.61, 0.17],
        [0.71, 0.09, 0.20],
        [0.05, 0.82, 0.13],
    ])
    confusion_matrix.update(predictions=predictions, references=references)
    res = confusion_matrix.compute()
    assert (paddle.to_tensor(res) == paddle.to_tensor([[1, 1, 0], [0, 1, 0], [0, 0, 1]])).all(), \
        'Multiclass input paddle.tensor score error for confusion_matrix.'

