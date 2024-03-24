#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : tensor_operators.py
@Author        : xuningyuan
@Date          : 2022/11/08
@Description   :
"""

from typing import Union

from gaea_operator.plugin import F


def resize(tensor_dict: dict, target_size: Union[tuple, list, int], keep_ratio=True, interp='linear') -> dict:
    """
    Resize the input tensor to the target size

    :param tensor_dict: The input tensor dictionary
    :type tensor_dict: dict
    :param target_size: The target size of the image
    :type target_size: Union[tuple, list, int]
    :param keep_ratio: If True, the image will be resized to the target size while keeping the aspect ratio, defaults to
    False, defaults to False (optional)
    :return: The resized image
    """
    if keep_ratio:
        n, c, h, w = tensor_dict['img'].shape
        factor = min(target_size[0] / h, target_size[1] / w)
        tensor_dict['img'] = F.interpolate(tensor_dict['img'], scale_factor=factor, mode=interp)
    else:
        tensor_dict['img'] = F.interpolate(tensor_dict['img'], size=target_size, mode=interp)
    return tensor_dict
