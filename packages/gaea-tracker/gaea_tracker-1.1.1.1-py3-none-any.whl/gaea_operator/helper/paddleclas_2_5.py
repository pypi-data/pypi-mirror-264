#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : paddleclas_2_5.py
@Author        : yanxiaodong
@Date          : 2023/2/10
@Description   :
"""
import paddle
import yaml
import os
from typing import Dict, Callable, List, Sequence, Union

from ppcls.loss import build_loss
from ppcls.arch import build_model
from ppcls.optimizer import build_optimizer
from ppcls.utils.config import get_config

from gaea_operator.utils import setup_logger
from gaea_operator.data import ValidateDataset, DALIValidateDataset

__all__ = ['load_paddlecls_cfg', 'create_paddlecls_model', 'paddleclas_output_transform', 'top_score_function',
           'paddleclas_accuracy_input_transform']

logger = setup_logger(__name__)


def load_paddlecls_cfg(file_path: str, num_classes: int = None):
    """
    create Paddlecls 2.5 config.
    """
    assert os.path.exists(file_path), 'Config file: {} do not exist.'.format(file_path)

    attr_config = get_config(file_path)
    with open(file_path) as f:
        config = yaml.load(f, Loader=yaml.Loader)
        
    pretrained_weights = attr_config["Global"]["pretrained_model"]
    
    if num_classes is not None:
        attr_config["Arch"]["class_num"] = num_classes
    

    return pretrained_weights, attr_config, config


def create_paddlecls_model(cfg: Dict, loader: Callable):
    """
    create model
    """
    assert cfg["Global"]["device"] in ["cpu", "gpu", "xpu", "npu", "mlu"]
    paddle.set_device(cfg["Global"]["device"])

    if "class_num" in cfg["Global"]:
        global_class_num = cfg["Global"]["class_num"]
        if "class_num" not in cfg["Arch"]:
            cfg["Arch"]["class_num"] = global_class_num
            msg = f"The Global.class_num will be deprecated. Please use Arch.class_num instead. " \
                  f"Arch.class_num has been set to {global_class_num}."
        else:
            msg = "The Global.class_num will be deprecated. Please use Arch.class_num instead. " \
                  "The Global.class_num has been ignored."
        logger.info(msg)

    loss_info = cfg["Loss"]["Train"]
    loss = build_loss(loss_info)

    # build model
    model = build_model(cfg)

    # build optimizer
    optimizer, lr = build_optimizer(cfg["Optimizer"], cfg["Global"]["epochs"], len(loader), [model, loss])

    return model, lr, optimizer, loss


def paddleclas_accuracy_input_transform(dataset: Union[ValidateDataset, DALIValidateDataset]):
    """
    Accuracy metric input.
    """
    data = dataset.common_data_instance.meta_data

    ann_dict = {}
    for ann in data["annotations"]:
        ann_dict[ann["image_id"]] = ann["category_id"]

    def metric_input(output: Sequence):
        predict = output[0]
        im_id = output[1].squeeze()

        gt_list = []
        dt_list = []
        if predict.shape[1] == 2:
            predict = paddle.nn.functional.softmax(predict, axis=-1)
            pred_scores, _ = paddle.topk(predict, 1)
            predict = paddle.reshape(pred_scores, paddle.to_tensor(-1))

        for i in range(len(im_id)):
            if im_id[i].item() in ann_dict:
                gt_list.append(ann_dict[im_id[i].item()])
                if predict[i].ndim == 1 and predict[i].size == 1:
                    dt_list.append(predict[i].item())
                else:
                    dt_list.append(predict[i])

        return paddle.to_tensor(dt_list), paddle.to_tensor(gt_list, paddle.int32)

    return metric_input


def paddleclas_output_transform(categories: List):
    """
    PaddleClas 2.5 output to COCO Store input.
    """
    def infer_result(output: Sequence):
        """
        get infer results
        """
        predict = output[0]
        im_id = output[1]

        im_id = im_id.numpy()
        predict = paddle.nn.functional.softmax(predict, axis=-1).numpy()
        index = predict.argsort(axis=-1)
        res = []
        for i in range(len(im_id)):
            cur_image_id = int(im_id[i])
            score = float(predict[i][index[i][-1]])
            category_id = categories[int(index[i][-1])]['id']
            dt_res = {'image_id': cur_image_id, 'category_id': category_id, 'score': score}

            res.append(dt_res)

        return res
    return infer_result


def top_score_function(engine):
    """
    score function
    """
    return engine.state.metrics["accuracy"]
