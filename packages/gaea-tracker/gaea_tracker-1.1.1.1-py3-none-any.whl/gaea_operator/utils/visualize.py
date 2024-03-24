#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : visualize.py    
@Author        : yanxiaodong
@Date          : 2023/6/13
@Description   :
"""
from typing import Union, Dict, Optional, List
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def visualize_box_mask(im: Union[str, np.ndarray], results: Optional[Dict] = None,
                       catid2clsid: Optional[Dict] = None, color_list: Optional[List] = None):
    """
    Visualize box&&mask on image.
    """
    if isinstance(im, str):
        im = Image.open(im).convert('RGB')
    elif isinstance(im, np.ndarray):
        im = Image.fromarray(im)
    else:
        raise TypeError(f'Parameter im type should be one of str|np.ndarray, but got {type(im)}')

    if len(results) > 0:
        if 'bbox' in results[0]:
            boxes = []
            labels = []
            categories = []
            classes = []
            scores = []
            for res in results:
                boxes.append(res['bbox'])
                labels.append(res['category_name'])
                categories.append(res['category_id'])
                classes.append(catid2clsid[res['category_id']])
                scores.append(res['score'])
            im = draw_box(im, boxes=boxes, labels=labels, classes=classes, scores=scores, color_list=color_list)

    return im


def draw_box(im, boxes: List, labels: List, classes: List, scores: List, color_list: List):
    """
    Draw box.
    """
    draw_thickness = 2
    font_size = 18
    draw = ImageDraw.Draw(im)
    clsid2color = {}

    for i, bbox in enumerate(boxes):
        clsid = classes[i]
        label = labels[i]
        score = scores[i]
        if clsid not in clsid2color:
            clsid2color[clsid] = color_list[clsid]
        color = tuple(clsid2color[clsid])

        xmin, ymin = bbox[0], bbox[1]
        xmax, ymax = xmin + bbox[2], ymin + bbox[3]

        # draw bbox
        draw.line([(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin), (xmin, ymin)],
                  width=draw_thickness,
                  fill=color)

        # draw label
        font = ImageFont.truetype("SimSun.ttf", font_size, encoding="unic")
        text = "{} {:.4f}".format(label, score)
        text_xmin, text_ymin, text_xmax, text_ymax = draw.textbbox([xmin, ymin], text, font=font)
        tw, th = text_xmax - text_xmin, text_ymax - text_ymin
        draw.text((xmin + 1, ymin - 2 * th if ymin - 2 * th >= 0 else ymin), text, fill=color, font=font)
    return im


def get_color_map_list(num_classes):
    """
    Color map list.
    """
    color_map = (num_classes + 1) * [0, 0, 0]
    for i in range(0, num_classes + 1):
        j = 0
        lab = i
        while lab:
            color_map[i * 3] |= (((lab >> 0) & 1) << (7 - j))
            color_map[i * 3 + 1] |= (((lab >> 1) & 1) << (7 - j))
            color_map[i * 3 + 2] |= (((lab >> 2) & 1) << (7 - j))
            j += 1
            lab >>= 3
    color_map = [color_map[i:i + 3] for i in range(3, len(color_map), 3)]
    return color_map