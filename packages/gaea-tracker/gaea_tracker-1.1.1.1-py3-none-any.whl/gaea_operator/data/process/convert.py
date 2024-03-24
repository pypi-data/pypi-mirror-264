#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : convert.py    
@Author        : yanxiaodong
@Date          : 2023/2/8
@Description   :
"""
import copy

from gaea_operator.utils import setup_logger
from .anno_parse import ImagenetDataConvert, COCODataConvert, data2common, json_dump, MODE_KEYS

setup_logger = setup_logger(__name__)


def imagenet2wsmp(source_dataset_dir: str, train_dest_ann_path: str, test_dest_ann_path: str):
    """
    Data from imagenet to WSMP.
    """
    setup_logger.info('Source dataset name is {}. Train destination annotation name is {}. '
                      'Validation destination annotation name is {}'.format(source_dataset_dir,
                                                                            train_dest_ann_path, test_dest_ann_path))

    data = ImagenetDataConvert(source_dataset_dir=source_dataset_dir)

    # 训练集保存
    train_data = copy.deepcopy(data)
    dist_ann = data2common(common_data=train_data, mode=(MODE_KEYS[0], MODE_KEYS[1]))
    json_dump(dest_path=train_dest_ann_path, data=dist_ann)
    setup_logger.info('Complete annotation to {}!'.format(train_dest_ann_path))

    # 测试集保存
    test_data = copy.deepcopy(data)
    dist_ann = data2common(common_data=test_data, mode=(MODE_KEYS[2],))
    json_dump(dest_path=test_dest_ann_path, data=dist_ann)
    setup_logger.info('Complete annotation to {}!'.format(test_dest_ann_path))


def coco2wsmp(source_dataset_dir: str, train_dest_ann_path: str, test_dest_ann_path: str):
    """
    Data from coco to WSMP.
    """
    setup_logger.info('Source dataset name is {}. Train destination annotation name is {}. '
                      'Validation destination annotation name is {}'.format(source_dataset_dir,
                                                                            train_dest_ann_path, test_dest_ann_path))

    data = COCODataConvert(source_dataset_dir=source_dataset_dir)

    # 训练集保存
    train_data = copy.deepcopy(data)
    dist_ann = data2common(common_data=train_data, mode=(MODE_KEYS[0], MODE_KEYS[1]))
    json_dump(dest_path=train_dest_ann_path, data=dist_ann)
    setup_logger.info('Complete annotation to {}!'.format(train_dest_ann_path))

    # 测试集保存
    test_data = copy.deepcopy(data)
    dist_ann = data2common(common_data=test_data, mode=(MODE_KEYS[2],))
    json_dump(dest_path=test_dest_ann_path, data=dist_ann)
    setup_logger.info('Complete annotation to {}!'.format(test_dest_ann_path))

