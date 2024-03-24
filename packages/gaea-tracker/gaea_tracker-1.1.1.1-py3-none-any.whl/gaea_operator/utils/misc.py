#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : misc.py    
@Author        : yanxiaodong
@Date          : 2022/11/14
@Description   :
"""
import importlib
import warnings
from collections import OrderedDict, abc
from types import ModuleType
from typing import Any, Dict, Optional, Type, Union, Callable, Sequence


def try_import(name: str) -> Optional[ModuleType]:
    """Try to import a module.
    Args:
        name: Specifies what module to import in absolute or relative
            terms (e.g. either pkg.mod or ..mod).
    Returns:
        ModuleType or None: If importing successfully, returns the imported
        module, otherwise returns None.
    """
    try:
        return importlib.import_module(name)
    except ImportError:
        warnings.warn("'{}' library import error, please check install correctly".format(name))
        return None


def try_import_class(module: ModuleType, target: str):
    """
    Try to import a class.

    Args:
        module: Specifies what module to import in absolute or relative
            terms (e.g. either pkg.mod or ..mod).
        target: class name.
    """
    if module is None:
        return CustomObject

    strs = target.rsplit('.', maxsplit=1)
    if len(strs) == 2:
        module = module.__name__ + '.' + strs[0]
        module = importlib.import_module(module)
        target = strs[-1]
    return getattr(module, target)


class CustomObject(Dict):
    """
    Inheritance object.
    """
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        pass


def is_seq_of(seq: Any,
              expected_type: Union[Type, tuple],
              seq_type: Type = None) -> bool:
    """
    Check whether it is a sequence of some type.

    Args:
        seq: The sequence to be checked.
        expected_type: Expected type of sequence items.
        seq_type: Expected sequence type. Defaults to None.
    """
    if seq_type is None:
        exp_seq_type = abc.Sequence
    else:
        assert isinstance(seq_type, type)
        exp_seq_type = seq_type
    if not isinstance(seq, exp_seq_type):
        return False
    for item in seq:
        if not isinstance(item, expected_type):
            return False
    return True


def is_list_of(seq, expected_type):
    """
    Check whether it is a list of some type.
    """
    return is_seq_of(seq, expected_type, seq_type=list)


def is_tuple_of(seq, expected_type):
    """
    Check whether it is a tuple of some type.
    """
    return is_seq_of(seq, expected_type, seq_type=tuple)


def training_stats(epoch: int, iteration: int, loss: Any, learning_rate: float, steps_per_epoch: int,
                   data_time: float, batch_time: float):
    """
    print training stats
    """
    stats = OrderedDict()
    if isinstance(loss, Dict):
        for k, v in loss.items():
            stats[k] = format(v.median, '.6f')
    else:
        stats['loss'] = format(loss, '.6f')

    strs = []
    for k, v in stats.items():
        strs.append("{}: {}".format(k, str(v)))

    space_fmt = ':' + str(len(str(steps_per_epoch))) + 'd'

    fmt = ' '.join([
        'Epoch: [{}]',
        '[{' + space_fmt + '}/{}]',
        'learning_rate: {lr:.6f}',
        '{meters}',
        'batch_cost: {btime}',
        'data_cost: {dtime}',
    ])
    step_id = iteration % steps_per_epoch if iteration % steps_per_epoch != 0 else steps_per_epoch
    fmt = fmt.format(epoch, step_id, steps_per_epoch, lr=learning_rate, meters=strs,
                     btime=str(format(batch_time, '.4f')), dtime=str(format(data_time, '.4f')))
    return fmt


def is_url(path: str):
    """
    Whether path is URL.

    Args:
        path (string): URL string or not.
    """
    return path.startswith('http://') or path.startswith('https://')
