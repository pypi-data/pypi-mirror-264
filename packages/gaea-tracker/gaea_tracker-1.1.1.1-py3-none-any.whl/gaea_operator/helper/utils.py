#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : utils.py    
@Author        : yanxiaodong
@Date          : 2023/4/13
@Description   :
"""
import yaml
import json
import os

from gaea_operator.utils import MOUNT_PATH
from gaea_operator.handlers.store import OutputStore

__all__ = ['get_categories']


def get_categories(file_path: str):
    """
    Read meta get categories.
    """
    file_path = os.path.join(MOUNT_PATH, file_path)

    with open(file_path) as fp:
        categories = yaml.load(fp, Loader=yaml.Loader)['categories']

    return categories


def coco_store_to_tracker_annotations(store: OutputStore):
    """
    Read meta get categories.
    """
    file_path = store.store_file
    if os.path.isdir(file_path):
        file_path = os.path.join(file_path, 'result.json')

    def convert():
        with open(file_path) as fp:
            data = json.load(fp)

        image_dict = {}
        category_dict = {}
        annotations = set()

        for img in data['images']:
            image_dict[img['id']] = img

        for cat in data['categories']:
            category_dict[cat['id']] = cat

        for anno in data['annotations']:
            anno['file_name'] = os.path.join(MOUNT_PATH, image_dict[anno['image_id']]['file_name'])
            anno['width'] = image_dict[anno['image_id']]['width']
            anno['height'] = image_dict[anno['image_id']]['height']
            anno['category_name'] = category_dict[anno['category_id']]['name']

            annotations.add(anno['image_id'])

        for img in data['images']:
            if img['id'] not in annotations:
                anno = {}
                anno['file_name'] = os.path.join(MOUNT_PATH, img['file_name'])
                anno['width'] = img['width']
                anno['height'] = img['height']
                data['annotations'].append(anno)

        return data['annotations']

    return convert
