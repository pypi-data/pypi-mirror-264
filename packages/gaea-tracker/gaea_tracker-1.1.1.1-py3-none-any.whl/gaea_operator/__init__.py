#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : __init__.py.py
@Author        : yanxiaodong
@Date          : 2022/11/3
@Description   :
"""
from gaea_operator.data import (
    ChangeDetectionDataset,
    ObjectDetectionDataset,
    CityscapesDataset,
    SemanticSegmentationDataset,
    DALICityscapesDataset,
    DALIObjectDetectionDataset,
    DALIChangeDetectionDataset,
    DALIClassficationDataset,
    DALIMultiAttrDataset,
    DALIValidateDataset,
    ClassficationDataset,
    TestDataset,
    ValidateDataset,
    build_dali_loader,
    build_paddle_loader,
    coco2wsmp,
    imagenet2wsmp,
    RandomSample,
)
from gaea_operator.handlers import (
    COCOOutputStore,
    MLflowLogger,
    AimLogger,
    ModelCheckpoint,
    PaddleModelEMA,
    PaddleProfiler,
    TorchProfiler,
    global_step_from_engine,
)
from gaea_operator.cli import entry, GaeaArgumentParser
from gaea_operator.metric import (
    Accuracy,
    COCOMetric,
    MeanIou,
    ImageClassificationMultiClassMetric,
    ObjectDetectionMetric,
    InstanceSegmentationMetric)
from gaea_operator.trainer import Trainer
from gaea_operator.utils import train_config, eval_config
from gaea_operator.engine import Engine

__all__ = [
    "Engine",
    "entry",
    "GaeaArgumentParser",
    "CityscapesDataset",
    "DALICityscapesDataset",
    "SemanticSegmentationDataset",
    "ChangeDetectionDataset",
    "ObjectDetectionDataset",
    "DALIObjectDetectionDataset",
    "DALIChangeDetectionDataset",
    "DALIClassficationDataset",
    "DALIMultiAttrDataset",
    "build_dali_loader",
    "build_paddle_loader",
    "MLflowLogger",
    "AimLogger",
    "ModelCheckpoint",
    "global_step_from_engine",
    "COCOMetric",
    "Trainer",
    "train_config",
    "eval_config",
    "TestDataset",
    "Accuracy",
    "PaddleProfiler",
    "TorchProfiler",
    "PaddleModelEMA",
    "imagenet2wsmp",
    "ValidateDataset",
    "coco2wsmp",
    "COCOOutputStore",
    "MeanIou",
    "DALIClassficationDataset",
    "ImageClassificationMultiClassMetric",
    "ObjectDetectionMetric",
    "InstanceSegmentationMetric",
    "RandomSample",
]
