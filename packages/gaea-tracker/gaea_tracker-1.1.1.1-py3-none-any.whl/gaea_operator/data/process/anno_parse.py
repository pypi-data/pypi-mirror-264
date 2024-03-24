#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : anno_parse.py    
@Author        : yanxiaodong
@Date          : 2023/2/8
@Description   :
"""
from typing import Dict, List, Optional
import os
import json
import copy
from abc import ABCMeta, abstractmethod
from collections import defaultdict
import shutil
from pycocotools.coco import COCO

from gaea_operator.utils import MOUNT_PATH, setup_logger

ANN_FILE = 'annotation.json'
MODE_KEYS = ('train', 'validation', 'test')


class DataConvert(metaclass=ABCMeta):
    """
    将开源不同的数据格式转换为统一的数据格式.

    Args:
       source_dataset_dir: Open source data format.
    """
    mode_keys = ['train', 'validation', 'test']

    def __init__(self, source_dataset_dir: str):
        self._logger = setup_logger(__name__ + "." + self.__class__.__name__)

        assert os.path.isdir(source_dataset_dir), 'Invalid imagenet dataset dir: {}'.format(source_dataset_dir)

        self.meta_data = {"annotations": [], "images": [], "categories": []}

        self.from_source(source_dataset_dir=source_dataset_dir)

    @abstractmethod
    def from_source(self, source_dataset_dir: str) -> None:
        """
        Parse open source data.
        """
        raise NotImplementedError


class COCODataConvert(DataConvert):
    """
    COCO数据源格式转换为统一的数据格式.
    """

    def _ann_parse(self, ann_file: str):
        assert os.path.isfile(ann_file), 'train annotation file: {} is invalid.'.format(ann_file)
        coco = COCO(annotation_file=ann_file)

        self._logger.info('Complete parse annotation file {}.'.format(ann_file))
        return coco.imgs, coco.anns, coco.cats

    def from_source(self, source_dataset_dir: str) -> None:
        """
        Parse coco data.
        """
        train_file = os.path.join(source_dataset_dir, 'annotations', 'train.json')
        train_imgs, train_anns, train_cats = self._ann_parse(ann_file=train_file)

        val_file = os.path.join(source_dataset_dir, 'annotations', 'validation.json')
        val_imgs, val_anns, val_cats = dict(), dict(), dict()
        if os.path.isfile(val_file):
            val_imgs, val_anns, val_cats = self._ann_parse(ann_file=val_file)

        test_imgs, test_anns, test_cats = copy.deepcopy(val_imgs), copy.deepcopy(val_anns), copy.deepcopy(val_cats)

        max_im_id = 0
        max_ann_id = 0
        all_imgs = {}
        all_anns = {}

        max_ann_id, max_im_id = self._ann_generate(source_dataset_dir=source_dataset_dir, imgs=train_imgs,
                                                   anns=train_anns, cats=train_cats, max_ann_id=max_ann_id,
                                                   max_im_id=max_im_id, mode=self.mode_keys[0],
                                                   all_imgs=all_imgs, all_anns=all_anns)

        max_ann_id, max_im_id = self._ann_generate(source_dataset_dir=source_dataset_dir, imgs=val_imgs,
                                                   anns=val_anns, cats=val_cats, max_ann_id=max_ann_id,
                                                   max_im_id=max_im_id, mode=self.mode_keys[1],
                                                   all_imgs=all_imgs, all_anns=all_anns)

        _, _ = self._ann_generate(source_dataset_dir=source_dataset_dir, imgs=test_imgs,
                                  anns=test_anns, cats=test_cats, max_ann_id=max_ann_id,
                                  max_im_id=max_im_id, mode=self.mode_keys[2], all_imgs=all_imgs, all_anns=all_anns)

    def _ann_generate(self, source_dataset_dir: str, imgs: Dict, anns: dict, cats: dict, max_im_id: int,
                      max_ann_id: int, mode: str, all_imgs: {}, all_anns: {}):
        old2new_im_id = {}

        for im_id, img in imgs.items():
            if im_id > max_im_id:
                max_im_id = im_id
            if im_id in all_imgs:
                max_im_id += 1
                img['id'] = max_im_id
                old2new_im_id[im_id] = max_im_id
            img['type'] = mode
            img_file = os.path.join(source_dataset_dir, 'images',
                                    mode if mode == self.mode_keys[0] else self.mode_keys[1], img['file_name'])
            if len(MOUNT_PATH) > 0:
                img_file = os.path.relpath(img_file, MOUNT_PATH)
            img['file_name'] = img_file

            self.meta_data['images'].append(img)

        for ann_id, ann in anns.items():
            if ann_id > max_ann_id:
                max_ann_id = ann_id
            if ann_id in all_anns:
                max_ann_id += 1
                ann['id'] = max_ann_id
            if ann['image_id'] in old2new_im_id:
                ann['image_id'] = old2new_im_id[ann['image_id']]
            if ann['category_id'] not in cats:
                continue
            self.meta_data['annotations'].append(ann)

        if mode == self.mode_keys[0]:
            for _, cat in cats.items():
                self.meta_data['categories'].append(cat)

        all_imgs.update(imgs)
        all_anns.update(anns)

        return max_ann_id, max_im_id


class ImagenetDataConvert(DataConvert):
    """
    Imagenet数据源格式转换为统一的数据格式.
    """

    def from_source(self, source_dataset_dir: str) -> None:
        """
        Parse imagenet data.
        """
        attr_dir_list = []
        for attr in os.listdir(source_dataset_dir):
            attr_dir = os.path.join(source_dataset_dir, attr)
            # 属性命名不能以. _开头的隐藏文件，防止误判断为属性
            if os.path.isdir(attr_dir) and not attr.startswith(('.', '_')):
                attr_dir_list.append(attr_dir)
            else:
                self._logger.warning('Please check attribution: {}, it is not folder'.format(attr))

        _sample_list = []
        _ann_list = []
        _cat_list = []
        category_id = 1
        image_id = 1
        ann_id = 1
        for attr_dir in attr_dir_list:
            category_dict = {}
            attr = os.path.split(attr_dir)[1]
            labels, train_ann, validation_ann = self._attr_parse(attr_dir=attr_dir, attr=attr)
            for name in labels:
                _cat_list.append(dict(id=category_id, name=name, super=attr))
                category_dict[name] = category_id
                category_id += 1
            test_ann = copy.deepcopy(validation_ann)

            image_id, ann_id = self._ann_parse(attr_dir=attr_dir, attr=attr, ann=train_ann, sample_list=_sample_list,
                                               ann_list=_ann_list, category_dict=category_dict, labels=labels,
                                               mode=self.mode_keys[0], image_id=image_id, ann_id=ann_id)

            image_id, ann_id = self._ann_parse(attr_dir=attr_dir, attr=attr, ann=validation_ann,
                                               sample_list=_sample_list, ann_list=_ann_list,
                                               category_dict=category_dict, labels=labels, mode=self.mode_keys[1],
                                               image_id=image_id, ann_id=ann_id)

            image_id, ann_id = self._ann_parse(attr_dir=attr_dir, attr=attr, ann=test_ann,
                                               sample_list=_sample_list, ann_list=_ann_list,
                                               category_dict=category_dict, labels=labels, mode=self.mode_keys[2],
                                               image_id=image_id, ann_id=ann_id)

        self.meta_data['images'] = _sample_list
        self.meta_data['annotations'] = _ann_list
        self.meta_data['categories'] = _cat_list

    def _ann_parse(self, attr_dir: str, attr: str, ann: List, sample_list: List, ann_list: List, category_dict: Dict,
                   labels: List, mode: str, image_id: int, ann_id: int):
        label_dict = defaultdict(int)
        img_dict = {}
        for image in ann:
            # txt标注每一行格式，文件名不能出现空格。 ***.jpg 0
            img, catid = image.rsplit(" ", 1)[0], int(image.rsplit(" ", 1)[1])
            if len(img_dict) == 0:
                img_list = os.listdir(os.path.dirname(os.path.join(attr_dir, img)))
                for i in range(len(img_list)):
                    img_dict[img_list[i]] = 1
            if catid < len(labels):
                img_file = os.path.join(attr_dir, img)
                if os.path.split(img_file)[1] in img_dict:
                    if len(MOUNT_PATH) > 0:
                        img_file = os.path.relpath(img_file, MOUNT_PATH)
                    sample_list.append(dict(id=image_id, file_name=img_file, type=mode))
                    ann_list.append(dict(id=ann_id, image_id=image_id, area=1, iscrowd=0,
                                         category_id=category_dict[labels[catid]]))
                    image_id += 1
                    ann_id += 1
                label_dict[labels[catid]] += 1
        self._logger.info('[{}] Attribution: {} annotation count {}.'.format(mode, attr, dict(label_dict)))

        return image_id, ann_id

    def _attr_parse(self, attr_dir: str, attr: str):
        label_file = os.path.join(attr_dir, 'labels.txt')
        assert os.path.isfile(label_file), 'Attribution: {} label file: {} is invalid.'.format(attr, label_file)

        with open(label_file) as f:
            labels = f.read()
        labels = labels.rstrip("\n").split("\n")
        self._logger.info('Attribution: {} label file: {} parse completed.'.format(attr, label_file))

        train_file = os.path.join(attr_dir, 'train.txt')
        assert os.path.isfile(train_file), 'Attribution: {} train annotation file: ' \
                                           '{} is invalid.'.format(attr, train_file)

        with open(train_file) as f:
            images = f.read()
        train_ann = images.rstrip("\n").split("\n")
        self._logger.info('Attribution: {} train annotation file: {} parse completed.'.format(attr, train_file))

        validation_ann = []
        validation_file = os.path.join(attr_dir, 'validation.txt')
        if os.path.isfile(validation_file):
            with open(validation_file) as f:
                images = f.read()
            validation_ann = images.rstrip("\n").split("\n")
            self._logger.info('Attribution: {} validation annotation file: {} parse completed.'.format(attr,
                                                                                                       validation_file))

        return labels, train_ann, validation_ann


def data2common(common_data: DataConvert, mode: Optional[tuple]) -> Dict:
    """
    Imagenet data convert common annotation in order to unify to different users.
    """
    data = common_data.meta_data

    imgs = {}
    for img in data['images']:
        if img['type'] in mode:
            imgs[img['id']] = img

    img_list, ann_list = [], []
    for key in imgs:
        img_list.append(imgs[key])
    for ann in data['annotations']:
        if ann['image_id'] in imgs:
            ann_list.append(ann)

    data['images'] = img_list
    data['annotations'] = ann_list

    return data


def json_dump(dest_path: str, data: Dict) -> None:
    """
    json文件保存，先保存在临时文件
    """
    dest_path = os.path.join(MOUNT_PATH, dest_path)
    if not os.path.exists(dest_path):
        os.makedirs(dest_path, exist_ok=True)

    dest_file = os.path.join(dest_path, ANN_FILE)
    root, ext = os.path.splitext(dest_file)[0], os.path.splitext(dest_file)[1]
    tmp_file = root + '_tmp' + ext

    with open(tmp_file, "w") as fb:
        json.dump(data, fb, indent=4)

    shutil.move(tmp_file, dest_file)
