#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : __meta__.py    
@Author        : yanxiaodong
@Date          : 2022/11/14
@Description   :
"""
import os


MOUNT_PATH = os.environ.get("PF_WORK_DIR", "")
FILESYSTEM = os.environ.get("FILESYSTEM", MOUNT_PATH.split("/")[-1].split("-")[-1])
LIBRARY_DIR = os.environ.get("LIBRARY_DIR", "gaea-training/requirements")
STEP = os.environ.get("PF_STEP_NAME", "")

JOB_NAME=os.environ.get("JOB_NAME", "jobs")

PRODUCT_PATH = os.path.join(MOUNT_PATH, JOB_NAME, STEP)
if not os.path.exists(PRODUCT_PATH):
    os.makedirs(PRODUCT_PATH, exist_ok=True)

IMAGE_CLASSIFICATION = "Image/ImageClassification/MultiClass"
IMAGE_OBJECT_DETECTION = "Image/ObjectDetection"
SEMANTIC_SEGMENTATION = "Image/SemanticSegmentation"

MASTER_RANK = 0

ALL_MODEL_TYPE = (IMAGE_CLASSIFICATION, IMAGE_OBJECT_DETECTION, SEMANTIC_SEGMENTATION)