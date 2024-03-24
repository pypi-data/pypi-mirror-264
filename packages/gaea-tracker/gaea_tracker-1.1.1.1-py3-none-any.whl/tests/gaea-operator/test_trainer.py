#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : test_trainer.py
@Author        : yanxiaodong
@Date          : 2022/12/1
@Description   :
"""
import paddle
import torch
from paddle import nn as paddle_nn
from torch import nn as torch_nn

from gaea_operator import Trainer
from gaea_operator.utils import CLASSIFICATION


class PaddleDummyModel(paddle_nn.Layer):
    def __init__(self):
        super(PaddleDummyModel, self).__init__()
        self.net = paddle_nn.Linear(1, 1)

    def forward(self, x):
        return self.net(x)


class TorchDummyModel(torch_nn.Module):
    def __init__(self):
        super(TorchDummyModel, self).__init__()
        self.net = torch_nn.Linear(1, 1)

    def forward(self, x):
        return self.net(x)


paddle_model = PaddleDummyModel()
paddle_scheduler = paddle.optimizer.lr.StepDecay(learning_rate=0.5, step_size=5, gamma=0.8, verbose=True)
paddle_optimizer = paddle.optimizer.SGD(learning_rate=paddle_scheduler, parameters=paddle_model.parameters())
paddle_loss = paddle_nn.BCEWithLogitsLoss()

torch_model = TorchDummyModel()
torch_optimizer = torch.optim.SGD(torch_model.parameters(), lr=0.5, momentum=0.9, weight_decay=1e-4)
torch_scheduler = torch.optim.lr_scheduler.StepLR(optimizer=torch_optimizer, step_size=1)
torch_loss = torch_nn.BCEWithLogitsLoss()


def test_create_paddle_trainer():
    trainer = Trainer(model_type=CLASSIFICATION)

    x = paddle.to_tensor([[0.01], [0.02], [0.03], [0.04], [0.05]])
    y = paddle.to_tensor([[1.0], [0.0], [1.0], [0.0], [1.0]])
    im_id = paddle.to_tensor([[10], [11], [12], [13], [14]])
    train_data = [(_x, _y) for _x, _y in zip(x, y)]
    validate_data = [{0: _x, 'im_id': _id} for _x, _id in zip(x, im_id)]

    trainer.train_build(model=paddle_model, optimizer=paddle_optimizer, train_loader=train_data,
                        lr_scheduler=paddle_scheduler, loss_fn=paddle_loss)
    trainer.validate_build(validation_loader=validate_data)
    trainer.run()


def test_create_torch_trainer():
    trainer = Trainer(model_type=CLASSIFICATION)

    x = torch.tensor([[0.01], [0.02], [0.03], [0.04], [0.05]])
    y = torch.tensor([[1.0], [0.0], [1.0], [0.0], [1.0]])
    im_id = torch.tensor([[10], [11], [12], [13], [14]])
    train_data = [(_x, _y) for _x, _y in zip(x, y)]
    validate_data = [{0: _x, 'im_id': _id} for _x, _id in zip(x, im_id)]

    trainer.train_build(model=torch_model, optimizer=torch_optimizer, train_loader=train_data,
                        lr_scheduler=torch_scheduler, loss_fn=torch_loss)
    trainer.validate_build(validation_loader=validate_data)
    trainer.run()
