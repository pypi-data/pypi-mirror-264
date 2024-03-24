#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : trainer.py
@Author        : yanxiaodong
@Date          : 2022/10/26
@Description   :
"""
from typing import Any, Dict, Iterable, Optional, Union

import gaea_operator.distributed as idist
from gaea_operator.distributed import Accelerator
from gaea_operator.engine import Engine, Events, PADDLE_BACKEND, TORCH_BACKEND
from gaea_operator.metric.metric import BaseMetric
from gaea_operator.plugin import Model, Optimizer, Layer, Module
from gaea_operator.utils import setup_logger, training_stats, ALL_MODEL_TYPE, IMAGE_OBJECT_DETECTION
from gaea_operator.handlers import ModelCheckpoint


class StrategyArgument(object):
    """
    Traininge strategies to accelerating.
    """
    def __init__(self,
                 amp: bool = False,
                 resume: str = None,
                 nproc_per_node: int = None):
        pass


class TrainerArgument(object):
    """
    Trainer arguments.
    """

    def __init__(self,
                 backend: Optional[str] = None,
                 amp_param: Optional[Dict] = {},
                 ema_param: Optional[Dict] = {},
                 gradient_accumulation_steps: int = 1,
                 model_type: Optional[str] = IMAGE_OBJECT_DETECTION,
                 multiple_train_loader_mode: str = 'max_size_cycle',
                 auto_scale_batch_size: Union[str, bool] = False):
        pass


class Trainer(TrainerArgument):
    """
     Customize every aspect of training.

     Args:
        backend：Support different backend types ('paddle', 'torch', 'horovod')
        amp_param: The mixed precision mode param.
        ema_param: Exponential moving average (EMA) param.
        gradient_accumulation_steps: Number of steps the gradients should be accumulated across.
        model_type: Train model type, which can be set to `Image/ObjectDetection`, etc .
        multiple_train_loader_mode: How to loop over the datasets when there are multiple train loaders.
        auto_scale_batch_size: If set to True, will `initially` run a batch size
            finder trying to find the largest batch size that fits into memory.
        kwargs: kwargs forwarded to the distribute strategy
    """

    def __init__(self,
                 backend: Optional[str] = None,
                 amp_param: Optional[Dict] = {},
                 ema_param: Optional[Dict] = {},
                 gradient_accumulation_steps: int = 1,
                 model_type: Optional[str] = IMAGE_OBJECT_DETECTION,
                 multiple_train_loader_mode: str = 'max_size_cycle',
                 auto_scale_batch_size: Union[str, bool] = False,
                 **kwargs: Any,
                 ):

        super(Trainer, self).__init__(backend=backend, model_type=model_type)
        self.amp_param = amp_param
        self.ema_param = ema_param
        self.gradient_accumulation_steps = gradient_accumulation_steps
        if self.gradient_accumulation_steps <= 0:
            raise ValueError('Gradient_accumulation_steps must be strictly positive.'
                             'No gradient accumulation if the value set to one (default).')

        assert model_type in ALL_MODEL_TYPE, 'Train model type {} must be in {}'.format(model_type, ALL_MODEL_TYPE)

        self._model = None
        self._optimizer = None
        self._module = None
        self._train_loader = None
        self._validation_loader = None
        self._check_val_every_n_epoch = None
        self._check_val_every_n_iter = None
        self._max_epoch = 1

        self._trainer = None
        self._validator = None
        self.ema = None

        self.start_epoch = 0

        self._accelerator = Accelerator(model_type=model_type, backend=backend, **kwargs)

        self._logger = setup_logger(__name__ + "." + self.__class__.__name__)

    def _auto_distribute(self, model: Optional[Model] = None, optimizer: Optional[Optimizer] = None):
        """
        Helper method to adapt for non-distributed and distributed configurations

        Args:
            model: the model to train.
            optimizer: the optimizer to use.
        """
        module, model, optimizer = self._accelerator.auto_adapt(model=model, optimizer=optimizer)
        self._model = model
        self._optimizer = optimizer
        self._module = module

    def _get_module(self, model: Model):
        if isinstance(model, Layer):
            self._module = PADDLE_BACKEND
        elif isinstance(model, Module):
            self._module = TORCH_BACKEND
        else:
            raise TypeError(f"Argument model should be class: `Layer` or `Module`, but given {type(model)}")

    def train_build(self,
                    model: Model,
                    optimizer: Optimizer,
                    train_loader: Iterable,
                    pretrain_weight: Optional[str] = None,
                    resume_weight: Optional[str] = None,
                    max_epoch: Optional[int] = 1,
                    lr_scheduler: Optional[Any] = None,
                    loss_fn: Optional[Any] = None,
                    check_val_every_n_epoch: Optional[int] = None,
                    check_val_every_n_iter: Optional[int] = None,
                    log_interval: Optional[int] = 20):
        """
        Build the train routine.

        Args:
            model: the model to train.
            optimizer: the optimizer to use.
            lr_scheduler: the learning rate to use.
            max_epoch: Max epochs to run.
            loss_fn: the loss function to use.
            train_loader: Collection of batches allowing repeated iteration (e.g., list or `DataLoader`).
            pretrain_weight:  pretrain model path(dir or file).
            resume_weight: resume model path(dir or file).
            check_val_every_n_epoch: Perform a validation loop every after every `N` training epochs.
            check_val_every_n_iter: Perform a validation loop every after every `N` training iterations.
                if ``check_val_every_n_epoch`` not None, it is possible to validate using `N` epochs.
                if ``check_val_every_n_epoch`` None,  `N` iterations can be used.
            log_interval: log execute at the end of every log_interval-th iteration.
        """
        self._get_module(model=model)

        self._model = model
        if self._module == PADDLE_BACKEND:
            from gaea_operator.handlers import PaddleModelEMA

            if len(self.ema_param) > 0:
                self.ema = PaddleModelEMA(model=self._model, **self.ema_param)
        else:
            pass

        self.start_epoch = ModelCheckpoint.load_checkpoint(model=self._model,
                                                           resume_weight=resume_weight,
                                                           pretrain_weight=pretrain_weight,
                                                           optimizer=optimizer,
                                                           ema=self.ema,
                                                           module=self._module)
        self._logger.info('Finish resume model weights: {} or load model weights: {} of epoch {}'.format(
            resume_weight, pretrain_weight, self.start_epoch))

        self._auto_distribute(model=self._model, optimizer=optimizer)

        if len(self.amp_param) > 0:
            _update = self._accelerator.amp_training_step(model=self._model,
                                                          optimizer=self._optimizer,
                                                          lr_scheduler=lr_scheduler,
                                                          loss_fn=loss_fn,
                                                          gradient_accumulation_steps=self.gradient_accumulation_steps,
                                                          amp_param=self.amp_param)
        else:
            _update = self._accelerator.training_step(model=self._model,
                                                      optimizer=self._optimizer,
                                                      lr_scheduler=lr_scheduler,
                                                      loss_fn=loss_fn,
                                                      gradient_accumulation_steps=self.gradient_accumulation_steps)
        trainer = Engine(_update)
        trainer.logger = setup_logger('trainer')
        if self.ema is not None:
            self.ema.attach_engine(trainer)

        if check_val_every_n_epoch is None and check_val_every_n_iter is None:
            check_val_every_n_epoch = 1
        if check_val_every_n_epoch is not None:
            check_val_every_n_iter = None

        if idist.get_rank() == 0:
            @trainer.on(Events.ITERATION_COMPLETED(every=log_interval))
            def log_training_loss(engine):
                epoch = engine.state.epoch
                iteration = engine.state.iteration
                loss = engine.state.output
                steps_per_epoch = engine.state.epoch_length
                learning_rate = engine.state.learning_rate
                data_time = engine.state.times[Events.ITERATION_STARTED.name]
                batch_time = engine.state.times[Events.ITERATION_COMPLETED.name]

                fmt = training_stats(epoch, iteration, loss, learning_rate, steps_per_epoch, data_time, batch_time)
                trainer.logger.info(fmt)

        self._check_val_every_n_epoch = check_val_every_n_epoch
        self._check_val_every_n_iter = check_val_every_n_iter
        self._train_loader = train_loader
        self._max_epoch = max_epoch
        self._trainer = trainer

        return trainer

    def validate_build(self,
                       validation_loader: Union[None, Iterable],
                       model: Optional[Model] = None,
                       weights: Optional[str] = None,
                       metric: Optional[BaseMetric] = None):
        """
        Build the validate routine.

        Args:
            model: the model to train.
            weights: validate model path(dir or file).
            validation_loader: Collection of batches allowing repeated iteration (e.g., list or `DataLoader`).
            metric: metric class instance.
        """
        if self._model is None:
            assert model is not None, 'The model must be instance in when only validation is available'

            self._get_module(model=model)
            ModelCheckpoint.load_checkpoint(model=model, pretrain_weight=weights, module=self._module)
            self._logger.info('Finish load model weights: {}'.format(weights))
            self._auto_distribute(model=model)

        if len(self.amp_param) > 0:
            _update = self._accelerator.amp_validating_step(model=self._model, amp_param=self.amp_param)
        else:
            _update = self._accelerator.validating_step(model=self._model)
        validator = Engine(_update)
        validator.logger = setup_logger('validator')

        if validation_loader is not None and metric is not None:
            metric.attach_engine(validator)

        self._validation_loader = validation_loader
        self._validator = validator

        if self._model is not None:
            validator.add_once_state("model", self._model)
        if self._optimizer is not None:
            validator.add_once_state("optimizer", self._optimizer)
        if self.ema is not None:
            validator.add_event_handler(Events.STARTED, self.ema.ema_weight)

        return validator

    def run(self):
        """
        Start to train or validate.
        """
        # only train not validate
        if self._trainer is not None and self._validator is None:
            self._trainer.run(data=self._train_loader, max_epochs=self._max_epoch)

        # train and validate
        if self._trainer is not None and self._validator is not None:
            if self._validation_loader is not None:
                if self._check_val_every_n_epoch is not None:
                    @self._trainer.on(Events.EPOCH_COMPLETED(every=self._check_val_every_n_epoch))
                    def validation_results(engine):
                        self._validator.run(data=self._validation_loader, max_epochs=1)
                if self._check_val_every_n_iter is not None:
                    @self._trainer.on(Events.ITERATION_COMPLETED(every=self._check_val_every_n_iter))
                    def validation_results(engine):
                        self._validator.run(data=self._validation_loader, max_epochs=1)
            self._trainer.run(data=self._train_loader, max_epochs=self._max_epoch)

        # not train only validate
        if self._trainer is None and self._validator is not None:
            self._validator.run(data=self._validation_loader, max_epochs=1)
