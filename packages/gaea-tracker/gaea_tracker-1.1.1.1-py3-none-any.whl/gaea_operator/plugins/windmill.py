#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : __init__.py.py
@Author        : yanxiaodong
@Date          : 2022/11/3
@Description   :
"""
from artifactv1.client.artifact_client import ArtifactClient
from windmill_train.client.training_client import TrainingClient
from windmillcomputev1.client.compute_client import ComputeClient

from gaea_operator.user import UserSetting
from gaea_operator.utils import FILESYSTEM


user_setting = UserSetting()
artifact_client = None
training_client = None
compute_client = None
if len(user_setting.endpoint) > 0:
    artifact_client = ArtifactClient(ak=user_setting.ak, sk=user_setting.sk, endpoint=user_setting.endpoint)
    training_client = TrainingClient(ak=user_setting.ak, sk=user_setting.sk, endpoint=user_setting.endpoint)

if len(user_setting.endpoint) > 0 and len(FILESYSTEM):
    compute_client = ComputeClient(ak=user_setting.ak, sk=user_setting.sk, endpoint=user_setting.endpoint)
