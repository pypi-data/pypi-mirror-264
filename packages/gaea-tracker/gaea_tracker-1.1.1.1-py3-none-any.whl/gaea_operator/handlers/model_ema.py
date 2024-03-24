#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : model_ema.py    
@Author        : yanxiaodong
@Date          : 2023/1/6
@Description   :
"""
import math
import copy
import weakref
from abc import ABCMeta, abstractmethod
from typing import Optional, Sequence, Union

from gaea_operator.engine import (CallableEventWithFilter, Engine, Events,
                                  EventsList)
from gaea_operator.plugin import Layer, paddle


class ModelEMA(metaclass=ABCMeta):
    """
    Exponential moving average (EMA) can be used to compute a smoothed version of model.
    """
    name = 'ema_model'

    def attach_engine(self,
                      engine: Engine,
                      apply_event: Union[str, Events, CallableEventWithFilter, EventsList] = Events.EPOCH_COMPLETED,
                      reset_model_event: Union[str, Events, CallableEventWithFilter, EventsList] = Events.EPOCH_STARTED
                      ) -> None:
        """
        Attach the handler to engine.

        Args:
            engine: trainer to which the handler will be attached.
            apply_event: event when the EMA model are apply.
            reset_model_event: event when reset original weight.
        """
        engine.add_event_handler(Events.ITERATION_COMPLETED, self.update)
        engine.add_event_handler(apply_event, self.apply, self.name)
        engine.add_event_handler(reset_model_event, self.reset_model)

    def ema_weight(self, engine: Engine):
        """
        save model dict.
        """
        engine.add_once_state(self.name, self.weight)

    @abstractmethod
    def update(self, engine: Engine):
        """
        Update weights of ema model.
        """
        pass

    @abstractmethod
    def reset_model(self, engine: Engine):
        """
        Reset original weight.
        """
        pass

    @abstractmethod
    def apply(self, engine: Engine, name: str):
        """
        apply weights of ema model.
        """
        pass


class PaddleModelEMA(ModelEMA):
    """
    Exponential moving average (EMA) for paddle framework.
    https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.5/ppdet/optimizer/ema.py

    Args:
        model: Detector of model.
        decay: The decay used for updating ema parameter.
        ema_decay_type: type in ['threshold', 'normal', 'exponential'], 'threshold' as default.
        cycle_epoch: The epoch of interval to reset ema_param and step.
        ema_black_list: The custom EMA black_list.
    """
    ema_decay_type_keys = ('threshold', 'exponential')

    def __init__(self,
                 model: Layer,
                 decay: Optional[float] = 0.9998,
                 ema_decay_type: Optional[str] = 'threshold',
                 cycle_epoch: Optional[int] = -1,
                 ema_black_list: Optional[Sequence] = None):
        if not isinstance(model, Layer):
            raise TypeError(f'Argument `model` should be paddle.Layer, but given {type(model)}')
        assert ema_decay_type in self.ema_decay_type_keys or ema_decay_type is None, \
            f'ema_decay_type should be in `{self.ema_decay_type_keys}` or is `None`.'

        self.step = 0
        self.epoch = 0
        self.decay = decay
        self.ema_decay_type = ema_decay_type
        self.cycle_epoch = cycle_epoch

        self.ema_black_list = self._match_ema_black_list(model.state_dict().keys(), ema_black_list)

        self.state_dict = dict()
        for k, v in model.state_dict().items():
            if k in self.ema_black_list:
                self.state_dict[k] = v
            else:
                self.state_dict[k] = paddle.zeros_like(v)

        self._model_state = {
            k: weakref.ref(p)
            for k, p in model.state_dict().items()
        }

        self.model = model
        self.weight = None

    def update(self, engine: Engine, model=None):
        if self.ema_decay_type == self.ema_decay_type_keys[0]:
            decay = min(self.decay, (1 + self.step) / (10 + self.step))
        elif self.ema_decay_type == self.ema_decay_type_keys[1]:
            decay = self.decay * (1 - math.exp(-(self.step + 1) / 2000))
        else:
            decay = self.decay
        self._decay = decay

        if model is not None:
            model_dict = model.state_dict()
        else:
            model_dict = {k: p() for k, p in self._model_state.items()}
            assert all([v is not None for _, v in model_dict.items()]), 'python gc.'

        for k, v in self.state_dict.items():
            if k not in self.ema_black_list:
                v = decay * v + (1 - decay) * model_dict[k]
                v.stop_gradient = True
                self.state_dict[k] = v
        self.step += 1

    def reset(self):
        self.step = 0
        self.epoch = 0
        for k, v in self.state_dict.items():
            if k in self.ema_black_list:
                self.state_dict[k] = v
            else:
                self.state_dict[k] = paddle.zeros_like(v)

    def reset_model(self, engine: Engine):
        if self.weight is not None:
            self.model.set_dict(self.weight)

    def apply(self, engine: Engine, name: str):
        if self.step == 0:
            return self.state_dict
        state_dict = dict()
        # Andrew Ng在Course 2 Improving Deep Neural Networks中讲到，Bias correction
        for k, v in self.state_dict.items():
            if k in self.ema_black_list:
                v.stop_gradient = True
                state_dict[k] = v
            else:
                if self.ema_decay_type != self.ema_decay_type_keys[1]:
                    v = v / (1 - self._decay ** self.step)
                v.stop_gradient = True
                state_dict[k] = v
        self.epoch += 1

        if 0 < self.cycle_epoch == self.epoch:
            self.reset()

        # attribute name for store EMA model from ``Engine.state``.
        self.weight = copy.deepcopy(self.model.state_dict())
        self.model.set_dict(state_dict)

    def resume(self, state_dict, step=0):
        for k, v in state_dict.items():
            if k in self.state_dict:
                if self.state_dict[k].dtype == v.dtype:
                    self.state_dict[k] = v
                else:
                    self.state_dict[k] = v.astype(self.state_dict[k].dtype)
        self.step = step

    def _match_ema_black_list(self, weight_name, ema_black_list=None):
        out_list = set()
        if ema_black_list:
            for name in weight_name:
                for key in ema_black_list:
                    if key in name:
                        out_list.add(name)
        return out_list



