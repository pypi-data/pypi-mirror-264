#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import os
import numbers
import numpy as np
from gaea_operator.utils import setup_logger
from gaea_operator.engine import Engine, Events


class EarlyStopping():
    """
    提前终止策略
    """
    def __init__(self,
                 monitor='loss',
                 mode='auto',
                 patience=0,
                 verbose=1,
                 min_delta=0,
                 baseline=None):
        super(EarlyStopping, self).__init__()
        self.monitor = monitor
        self.patience = patience
        self.verbose = verbose
        self.baseline = baseline
        self.min_delta = abs(min_delta)
        self.wait_epoch = 0
        self.best_weights = None
        self.stopped_epoch = 0
        # The value of `save_dir` is set in function `config_callbacks`
        self._logger = setup_logger(__name__ + "." + self.__class__.__name__)
        self.save_dir = None
        if mode not in ['auto', 'min', 'max']:
            self._logger.warn('EarlyStopping mode %s is unknown, '
                          'fallback to auto mode.' % mode)
            mode = 'auto'
        if mode == 'min':
            self.monitor_op = np.less
        elif mode == 'max':
            self.monitor_op = np.greater
        # When mode == 'auto', the mode should be inferred by `self.monitor`
        else:
            if 'acc' in self.monitor or "map" in self.monitor:
                self.monitor_op = np.greater
            else:
                self.monitor_op = np.less

        if self.monitor_op == np.greater:
            self.min_delta *= 1
        else:
            self.min_delta *= -1
            
        self.before_train_begin()

    def before_train_begin(self):
        """
        训练开始之前，相关属性的初始化
        """
        self.wait_epoch = 0
        if self.baseline is not None:
            self.best_value = self.baseline
        else:
            self.best_value = np.inf if self.monitor_op == np.less else -np.inf
            self.best_weights = None

    def on_eval_end(self, logs: dict=None):
        """在评估结束时，计算最优结果和当前相较于最优结果时多训的轮数
        """
        if logs is None or self.monitor not in logs:
            self._logger.warn(
                'Monitor of EarlyStopping should be loss or metric name.')
            return
        current = logs[self.monitor]
        if isinstance(current, (list, tuple)):
            current = current[0]
        elif isinstance(current, numbers.Number):
            current = current
        else:
            return

        if self.monitor_op(current - self.min_delta, self.best_value):
            self.best_value = current
            self.wait_epoch = 0
        else:
            self.wait_epoch += 1

        self.stopped_epoch += 1
        
    def on_train_begin(self, engine: Engine):
        """在训练开始时如果参数满足条件（比如epoch数达到一定阈值）则退出训练。Args:
            engine (Engine): 训练引擎
        """
        if self.wait_epoch >= self.patience:
            engine.terminate()
            if self.verbose > 0:
                self._logger.info('Epoch %d: Early stopping.' % (self.stopped_epoch + 1))
                if self.save_best_model and self.save_dir is not None:
                    self._logger.info('Best checkpoint has been saved at %s' %
                        (os.path.abspath(
                            os.path.join(self.save_dir, 'best_model'))))        
        
    def attach_engine(self, train_engine: Engine, val_engine: Engine) -> None:
        """在训练引擎和验证引擎之间关联上相应的回调函数。Args:
            train_engine: 训练引擎
            val_engine: 验证引擎
        """
        if not isinstance(train_engine, Engine):
            raise TypeError(f"Argument engine should be class: `Engine`, but given {type(train_engine)}")
        train_engine.add_event_handler(Events.EPOCH_STARTED, self.on_train_begin)
                
        if not isinstance(val_engine, Engine):
            raise TypeError(f"Argument engine should be class: `Engine`, but given {type(val_engine)}")
        val_engine.add_event_handler(Events.EPOCH_COMPLETED, self.on_eval_end, logs=val_engine.state.metrics)