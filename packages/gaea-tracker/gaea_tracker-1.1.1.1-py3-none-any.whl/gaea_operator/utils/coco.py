#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : coco_detection.py
@Author        : yanxiaodong
@Date          : 2022/10/26
@Description   :
"""
import copy
import json
from collections import defaultdict

from pycocotools.coco import COCO


class CustomCOCO(COCO):
    """
    COCO类继承
    """
    def __init__(self, annotation_file=None):
        # load dataset
        self.dataset, self.anns, self.cats, self.imgs = dict(), dict(), dict(), dict()
        self.imgToAnns, self.catToImgs = defaultdict(list), defaultdict(list)
        if annotation_file:
            if isinstance(annotation_file, str):
                dataset = json.load(open(annotation_file, 'r'))
            else:
                dataset = copy.deepcopy(annotation_file)
            assert type(dataset) == dict, 'annotation file format {} not supported'.format(type(dataset))
            self.dataset = dataset
            self.createIndex()
