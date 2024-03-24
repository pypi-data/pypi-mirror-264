#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : __init__.py.py
@Author        : yanxiaodong
@Date          : 2022/11/3
@Description   :
"""
from typing import Optional
import os


class UserSetting(object):
    def __init__(self,
                 ak: Optional[str] = "",
                 sk: Optional[str] = "",
                 endpoint: Optional[str] = ""):
        if len(ak) == 0:
            ak = os.environ.get("GAEA_USER__AK", "")

        if len(sk) == 0:
            sk = os.environ.get("GAEA_USER__SK", "")

        if len(endpoint) == 0:
            endpoint = os.environ.get("GAEA_USER__ENDPOINT", "")

        self._ak = ak
        self._sk = sk
        self._endpoint = endpoint

    @property
    def ak(self):
        return self._ak

    @property
    def sk(self):
        return self._sk

    @property
    def endpoint(self):
        return self._endpoint
