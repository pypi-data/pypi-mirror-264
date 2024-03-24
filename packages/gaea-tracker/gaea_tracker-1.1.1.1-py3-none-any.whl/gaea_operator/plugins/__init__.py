#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : __init__.py.py
@Author        : yanxiaodong
@Date          : 2022/11/3
@Description   :
"""
from .windmill import artifact_client, training_client, compute_client

__all__ = ['artifact_client', 'training_client', 'compute_client']