#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : paddledet_2_4.py
@Author        : yanxiaodong
@Date          : 2023/2/6
@Description   :
"""
from typing import Callable, Dict, List, Sequence, Union
from collections import defaultdict
import paddle
import yaml
import os

import ppdet.utils.check as check
from ppdet.core.workspace import create
from ppdet.core.workspace import load_config
from ppdet.metrics.json_results import get_det_res, get_seg_res

from gaea_operator.utils import MOUNT_PATH
from gaea_operator.metric.coco_detection import ann_to_rle
from gaea_operator.data import ValidateDataset, DALIValidateDataset

__all__ = ['load_paddledet_cfg', 'create_paddledet_model', 'paddledet_output_transform', 'bbox_score_function']


def load_paddledet_cfg(model_config_file: str, num_classes: int = None):
    """
    create PaddleDet 2.4 config.
    """
    assert os.path.exists(model_config_file), 'Config file: {} do not exist.'.format(model_config_file)

    attr_config = load_config(model_config_file)
    with open(model_config_file) as f:
        config = yaml.load(f, Loader=yaml.Loader)

    pretrain_weights = attr_config['pretrain_weights']

    if num_classes is not None:
        attr_config['num_classes'] = num_classes

    return pretrain_weights, attr_config, config


def create_paddledet_model(cfg: Dict, loader: Callable):
    """
    create PaddleDet 2.4 model
    """
    if cfg.use_gpu:
        paddle.set_device('gpu')
    else:
        paddle.set_device('cpu')

    if 'norm_type' in cfg and cfg['norm_type'] == 'sync_bn' and not cfg.use_gpu:
        cfg['norm_type'] = 'bn'

    check.check_config(cfg)
    check.check_gpu(cfg.use_gpu)

    if 'model' not in cfg:
        model = create(cfg.architecture)
    else:
        model = cfg.model
    model.load_meanstd(cfg['TestReader']['sample_transforms'])

    steps_per_epoch = len(loader)
    lr = create('LearningRate')(steps_per_epoch)
    optimizer = create('OptimizerBuilder')(lr, model)

    _nranks = paddle.distributed.get_world_size()
    sync_bn = (getattr(cfg, 'norm_type', None) == 'sync_bn' and cfg.use_gpu and _nranks > 1)
    if sync_bn:
        model = paddle.nn.SyncBatchNorm.convert_sync_batchnorm(model)

    return model, lr, optimizer


def paddledet_coco_metric_input_transform(dataset: Union[ValidateDataset, DALIValidateDataset]):
    """
    paddledet 2.4 transfrom model output to metric input
    """
    data = dataset.common_data_instance.meta_data
    clsid2cateid = dataset.clsid2catid

    annos = prepare_anno(data)

    def eval_result(output: Sequence):
        predict = output[0]
        im_id = output[1].cpu()
        
        res = {}
        if 'bbox' in predict:
            bboxes = predict['bbox'].cpu()
            res['bbox'] = get_det_res(bboxes, predict['bbox_num'], im_id, clsid2cateid)
        
        if 'mask' in predict:
            res['mask'] = get_seg_res(predict['mask'].cpu(), bboxes, predict['bbox_num'], im_id, clsid2cateid)
        
        im_id_unique = set([int(x[0]) for x in im_id])
        gts = []
        for id in im_id_unique:
            if id in annos:
                gts.extend(annos[id])
        gts_dict = {'bbox': gts}
        if 'mask' in predict:
            gts_dict['mask'] = gts

        return res, gts_dict
    
    return eval_result


def prepare_anno(anno_data):
    """准备gt的annotation

    Args:
        anno_data (_type_): _description_

    Returns:
        _type_: _description_
    """
    annos = defaultdict(list)
    image_properties = {img['id']: img for img in anno_data['images']}
    for anno in anno_data['annotations']:
        im_id = anno['image_id']
        image_prop = image_properties[im_id]
        anno['height'] = image_prop['height']
        anno['width'] = image_prop['width']
        if "mask" in anno:
            anno["segmentation"] = anno.pop("mask")
        if "segmentation" in anno and len(anno["segmentation"]) > 0:
            anno["segmentation"] = ann_to_rle(anno)
            
        anno['ignore'] = anno['ignore'] if 'ignore' in anno else 0
        anno['ignore'] = "iscrowd" in anno and anno["iscrowd"]
        if 'num_keypoints' in anno:
            anno["ignore"] = (anno["num_keypoints"] == 0) or anno["ignore"]        
        annos[im_id].append(anno)
    
    return annos
    
    
def paddledet_output_transform(categories: List):
    """
    PaddleDet 2.4 output to metric input or COCO Store input.
    """
    clsid2cateid = [cate['id'] for cate in categories]
    
    def infer_result(output: Sequence):
        predict = output[0]
        im_id = output[1]
        
        res = {}
        if 'bbox' in predict:
            bboxes = predict['bbox'].cpu()
            res['bbox'] = get_det_res(bboxes, predict['bbox_num'], im_id, clsid2cateid)
        
        if 'mask' in predict:
            res['mask'] = get_seg_res(predict['mask'].cpu(), bboxes, predict['bbox_num'], im_id, clsid2cateid)

        return res['bbox']

    return infer_result


def bbox_score_function(engine):
    """
    score function
    """
    return engine.state.metrics['boundingBoxMeanAveragePrecision']
