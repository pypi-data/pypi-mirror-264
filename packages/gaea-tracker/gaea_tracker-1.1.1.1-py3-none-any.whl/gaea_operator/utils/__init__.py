#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : __init__.py.py    
@Author        : yanxiaodong
@Date          : 2022/10/17
@Description   :
"""
from .__meta__ import MOUNT_PATH, IMAGE_CLASSIFICATION, IMAGE_OBJECT_DETECTION, ALL_MODEL_TYPE, SEMANTIC_SEGMENTATION, \
    MASTER_RANK, PRODUCT_PATH, FILESYSTEM
from .coco import CustomCOCO
from .misc import (is_list_of, is_tuple_of, training_stats, try_import,
                   try_import_class)
from .setup_logger import setup_logger
from .config import train_config, eval_config
from .parse import parse_args
from .visualize import visualize_box_mask, get_color_map_list

__all__ = ['MOUNT_PATH', 'CustomCOCO', 'try_import', 'setup_logger', 'is_list_of', 'training_stats', 'train_config',
           'eval_config', 'IMAGE_CLASSIFICATION', 'IMAGE_OBJECT_DETECTION', 'SEMANTIC_SEGMENTATION', 'parse_args',
           'ALL_MODEL_TYPE', 'visualize_box_mask', 'get_color_map_list', 'MASTER_RANK', 'PRODUCT_PATH', 'FILESYSTEM']
