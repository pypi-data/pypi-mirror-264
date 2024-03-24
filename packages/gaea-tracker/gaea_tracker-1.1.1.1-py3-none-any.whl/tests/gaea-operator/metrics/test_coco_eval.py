#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : test_dali_ops_basic.py
@Author        : xuningyuan
@Date          : 2023/03/01
@Description   :
"""
from gaea_operator.metric.coco_detection import DistCocoEval, COCOMetric
from copy import deepcopy
    

def sample_case1():
    """_summary_

    Returns:
        _type_: _description_
    """
    pred = {
        "bbox": [
            {
                "image_id": 0,
                "category_id": 0,
                "bbox": [1, 20, 300, 400],
                "score": 0.5,
            }
        ]
    }
    gt = {
        "bbox": [
            {
                "id": 1,
                "image_id": 0,
                "category_id": 0,
                "bbox": [1, 20, 300, 400],
                "iscrowd": 0,
                "ignore": 0,
            }
        ]
    }
    return pred, gt    
        

def sample_case2():
    """_summary_

    Returns:
        _type_: _description_
    """
    pred = {
        "bbox": [
            {
                "image_id": 0,
                "category_id": 0,
                "bbox": [1, 20, 300, 400],
                "score": 0.5,
            },
            {
                "image_id": 0,
                "category_id": 1,
                "bbox": [1, 20, 300, 400],
                "score": 0.5,
            }            
        ]
    }
    gt = {
        "bbox": [
            {
                "id": 1,
                "image_id": 0,
                "category_id": 0,
                "bbox": [1, 20, 300, 400],
                "iscrowd": 0,
                "ignore": 0,
            },
            {
                "id": 2,
                "image_id": 0,
                "category_id": 1,
                "bbox": [1, 20, 30, 40],
                "iscrowd": 0,
                "ignore": 0,
            }            
        ]
    }
    return pred, gt

  
def test_coco_metric_update():
    """测试accumulate方法"""
    coco_eval = COCOMetric(
        categories=[{"name": "cate_a", "id": 0}, {"name": "cate_b", "id": 1}]
    )

    # case1
    res = evaluate(coco_eval, *sample_case1())
    assert round(res['bbox iou 0.5-0.05-0.95'], 3) == 1.000
    # case2
    res = evaluate(coco_eval, *sample_case2())
    assert round(res['bbox iou 0.5-0.05-0.95'], 3) == 0.500
    

def evaluate(coco_eval: COCOMetric, pred, gt):
    """_summary_

    Args:
        coco_eval (_type_): _description_
        pred (_type_): _description_
        gt (_type_): _description_
    """
    coco_eval.update((pred, gt))
    coco_eval.before_gather()
    return coco_eval.compute()
    
    
if __name__ == "__main__":
    test_coco_metric_update()