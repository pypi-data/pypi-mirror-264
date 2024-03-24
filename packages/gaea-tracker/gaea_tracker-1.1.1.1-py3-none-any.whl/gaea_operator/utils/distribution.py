#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : distribution.py    
@Author        : yanxiaodong
@Date          : 2023/1/4
@Description   :
"""
from gaea_operator.plugin import horovod, paddle, torch


class ReduceOP(object):
    """
    define reduce key.
    """
    @staticmethod
    def paddle_reduce_op_map():
        """
        paddle reduce op map
        """
        _reduce_op_map = {
            "SUM": paddle.distributed.ReduceOp.SUM,
            "PROD": paddle.distributed.ReduceOp.PROD,
            "MIN": paddle.distributed.ReduceOp.MIN,
            "MAX": paddle.distributed.ReduceOp.MAX,
        }
        return _reduce_op_map

    @staticmethod
    def torch_reduce_op_map():
        """
        torch reduce op map
        """
        _reduce_op_map = {
            "SUM": torch.distributed.ReduceOp.SUM,
            "OR": torch.distributed.ReduceOp.BOR,
            "MIN": torch.distributed.ReduceOp.MIN,
            "MAX": torch.distributed.ReduceOp.MAX,
            "PRODUCT": torch.distributed.ReduceOp.PRODUCT,
            "AND": torch.distributed.ReduceOp.BAND,
        }
        return _reduce_op_map

    @staticmethod
    def horovod_manual_reduce_op_map():
        """
        horovod manual reduce op map
        """
        _manual_reduce_op_map = {
            "MIN": torch.min,
            "MAX": torch.max,
            "PRODUCT": torch.prod}
        return _manual_reduce_op_map

    @staticmethod
    def horovod_reduce_op_map():
        """
        horovod reduce op map
        """
        _reduce_op_map = {
            "SUM": horovod.torch.mpi_ops.Sum,
            "AVERAGE": horovod.torch.mpi_ops.Average,
            "ADASUM": horovod.torch.mpi_ops.Adasum,
        }
        return _reduce_op_map
