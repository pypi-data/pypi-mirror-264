#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : accelerator.py    
@Author        : yanxiaodong
@Date          : 2022/11/29
@Description   :
"""
from typing import Callable, Optional

from gaea_operator.plugin import Model, Optimizer
from gaea_operator.utils import setup_logger

from .utils import (auto_adapt, available_backends, validating_step, amp_training_step, amp_validating_step,
                    get_local_rank, get_world_size, initialize, training_step, _assert_backend, is_initialized)


class Accelerator(object):
    """
    The Accelerator parses several Trainer arguments
    manager to simplify distributed configuration setup for multiple backends.

    Args:
        model_type: Train model type.
        backend: backend to use.

    """

    def __init__(self, backend: Optional[str], model_type: str = None, **kwargs) -> None:
        _assert_backend(backend=backend)

        self.backend = backend
        self.model_type = model_type
        self.kwargs = kwargs

        self._initialize()

    def _initialize(self):
        self._logger = setup_logger(__name__ + "." + self.__class__.__name__)

        self._logger.info(f"Run world size is {get_world_size()}")
        self._logger.info(f"Run local size is {get_local_rank()}")
        self._logger.info(f"Initialized distributed Accelerator with backend: '{self.backend}'")

    def auto_adapt(self, model: Model, optimizer: Optimizer):
        """
        Helper method to adapt for non-distributed and distributed configurations

        Args:
            model: the model to train.
            optimizer: the optimizer to use.
        """
        self._logger.info("Starting to adapt model and optimizer for non-distributed and distributed configurations")
        return auto_adapt(model=model, optimizer=optimizer)

    def training_step(self,
                      model: Model,
                      optimizer: Optimizer,
                      loss_fn: Callable,
                      lr_scheduler: Callable,
                      gradient_accumulation_steps: int):
        """
        Factory function for training.

        Args:
            model: the model to train.
            optimizer: the optimizer to use.
            lr_scheduler: the learning rate to use.
            loss_fn: the loss function to use.
            gradient_accumulation_steps: Number of steps the gradients should be accumulated across.
        """
        self._logger.info(f"[train] model: {model.__class__}, optimizer: {optimizer}, loss_fn: {loss_fn}, "
                          f"lr_scheduler: {lr_scheduler}")
        return training_step(model=model,
                             optimizer=optimizer,
                             loss_fn=loss_fn,
                             lr_scheduler=lr_scheduler,
                             gradient_accumulation_steps=gradient_accumulation_steps)

    def amp_training_step(self,
                          model: Model,
                          optimizer: Optimizer,
                          loss_fn: Callable,
                          lr_scheduler: Callable,
                          gradient_accumulation_steps: int,
                          amp_param: dict = {}):
        """
        Factory function for training.

        Args:
            model: the model to train.
            optimizer: the optimizer to use.
            lr_scheduler: the learning rate to use.
            loss_fn: the loss function to use.
            gradient_accumulation_steps: Number of steps the gradients should be accumulated across.
            amp_param: The mixed precision mode param.
        """
        self._logger.info(f"[amp train] model: {model.__class__}, optimizer: {optimizer}, loss_fn: {loss_fn}, "
                          f"lr_scheduler: {lr_scheduler}")
        return amp_training_step(model=model,
                                 optimizer=optimizer,
                                 loss_fn=loss_fn,
                                 lr_scheduler=lr_scheduler,
                                 gradient_accumulation_steps=gradient_accumulation_steps,
                                 amp_param=amp_param)

    def validating_step(self, model: Model):
        """
        Factory function for validating.

        Args:
            model: the model to evaluation.
        """
        self._logger.info(f"[validate] model: {model.__class__}")
        return validating_step(model=model)

    def amp_validating_step(self, model: Model, amp_param: dict = {}):
        """
        Factory function for validating.

        Args:
            model: the model to evaluation.
            amp_param: The mixed precision mode param.
        """
        self._logger.info(f"[amp validate] model: {model.__class__}")
        return amp_validating_step(model=model, amp_param=amp_param)
