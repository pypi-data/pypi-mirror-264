#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : paddledet_2_4.py
@Author        : yanxiaodong
@Date          : 2023/2/6
@Description   :
"""
from typing import Dict, List, Sequence
import copy
import paddle
from paddle.nn import functional as F
from paddleseg.cvlibs import Config, SegBuilder, manager
from paddleseg.transforms import Compose


class DictConfig(Config, dict):
    pass


def load_paddleseg_cfg(model_config_file: str, num_classes: int = None):
    """
    create PaddleSeg 2.8 config.
    """

    if num_classes is not None:
        attr_config = DictConfig(model_config_file, opts=["model.num_classes={}".format(num_classes)])
    else:
        attr_config = DictConfig(model_config_file)
    
    if "pretrained" in attr_config.model_cfg:
        pretrain_weights = attr_config.dic["model"].pop("pretrained")
    elif "backbone" in attr_config.model_cfg and "pretrained" in attr_config.model_cfg["backbone"]:
        pretrain_weights = attr_config.model_cfg["backbone"].pop("pretrained")
    else:
        pretrain_weights = ""

    return pretrain_weights, attr_config, copy.deepcopy(attr_config.dic)


def create_paddleseg_model(cfg: DictConfig):
    """
    create PaddleSeg 2.8 model
    """
    builder = SegBuilder(cfg)
    model = builder.model
    lr = builder.lr_scheduler
    optimizer = builder.optimizer
    loss = builder.loss
    loss_fn = create_loss_fn(loss, model)

    _nranks = paddle.distributed.get_world_size()
    sync_bn = (getattr(cfg, 'norm_type', None) == 'sync_bn' and _nranks > 1)
    if sync_bn:
        model = paddle.nn.SyncBatchNorm.convert_sync_batchnorm(model)

    return model, lr, optimizer, loss_fn


def create_loss_fn(losses, model):
    def check_logits_losses(logits_list, losses):
        len_logits = len(logits_list)
        len_losses = len(losses['types'])
        if len_logits != len_losses:
            raise RuntimeError(
                'The length of logits_list should equal to the types of loss config: {} != {}.'
                .format(len_logits, len_losses))
            
    def loss_computation(logits_list, batch, losses=losses):
        check_logits_losses(logits_list, losses)
        loss_list = []
        for i in range(len(logits_list)):
            logits = logits_list[i]
            loss_i = losses['types'][i]
            coef_i = losses['coef'][i]
            if loss_i.__class__.__name__ in ('BCELoss', ) and loss_i.edge_label:
                # Use edges as labels According to loss type.
                loss_list.append(coef_i * loss_i(logits, batch["edges"]))
            elif loss_i.__class__.__name__ == 'MixedLoss':
                mixed_loss_list = loss_i(logits, batch["label"].astype(paddle.int64))
                for mixed_loss in mixed_loss_list:
                    loss_list.append(coef_i * mixed_loss)
            elif loss_i.__class__.__name__ in ("KLLoss", ):
                loss_list.append(coef_i *
                                loss_i(logits_list[0], logits_list[1].detach()))
            else:
                loss_list.append(coef_i * loss_i(logits, batch["label"].astype(paddle.int64)))
        return sum(loss_list)
    
    def model_loss_computation(logits_list, batch, model=model, losses=losses):
        loss_list = model.loss_computation(logits_list, losses, batch)
        return sum(loss_list)
    
    if hasattr(model, 'loss_computation'):
        return model_loss_computation
    else:
        return loss_computation


def create_paddleseg_transforms(cfg: Dict):
    """
    create PaddleSeg 2.8 transforms
    """
    builder = SegBuilder(cfg, comp_list=[manager.TRANSFORMS])
    transforms = []
    for item in cfg.get('transforms', []):
        transforms.append(builder.build_component(item))
    return Compose(transforms)


def paddleseg_miou_input_transform():
    """
    paddleseg 2.8 transfrom model output to metric input
    """

    def eval_result(output: Sequence):
        label: paddle.Tensor = output[1].astype(paddle.float32).squeeze()
        predict = F.interpolate(output[0], size=label.shape[-2:], mode='bilinear')
        predict: paddle.Tensor = paddle.argmax(predict, axis=1).squeeze()

        return predict, label
    
    return eval_result
    
    
def paddledseg_output_transform(categories: List):
    """
    PaddleDet 2.4 output to metric input or COCO Store input.
    """
    clsid2cateid = [cate['id'] for cate in categories]
    
    def infer_result(output: Sequence):
        predict = output[0]
        im_id = output[1]

        return predict, im_id

    return infer_result


def seg_score_function(engine):
    """
    score function
    """
    return engine.state.metrics['meanIou']
