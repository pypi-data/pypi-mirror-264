#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : parse.py    
@Author        : yanxiaodong
@Date          : 2023/5/23
@Description   :
"""
from typing import Optional
from argparse import ArgumentParser


def parse_args(prog: Optional[str], description: Optional[str]):
    """
    parse params
    """
    parser = ArgumentParser(prog=prog, description=description)
    parser.add_argument(
        '-c',
        '--config',
        type=str,
        default='./config.yaml',
        help='config file path')
    parser.add_argument(
        '-o',
        '--override',
        action='append',
        default=[],
        help='config options to be overridden')
    args = parser.parse_args()
    return args