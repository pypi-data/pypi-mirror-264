#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : dataloader.py    
@Author        : yanxiaodong
@Date          : 2022/10/26
@Description   :
"""
import os
import sys
import numpy as np
import traceback
import warnings
from typing import Callable, List, Optional, Iterator

import gaea_operator.distributed as idist
from gaea_operator.data.source.anno_parse import TRAIN
from gaea_operator.data.source.dataset import BaseMultiDataset
from gaea_operator.plugin import paddle
from gaea_operator.utils.setup_logger import setup_logger

SIZE_UNIT = ['K', 'M', 'G', 'T']
SHM_QUERY_CMD = 'df -h'
SHM_KEY = 'shm'
SHM_DEFAULT_MOUNT = '/dev/shm'


def get_shared_memory_size():
    """
    获得当前共享内存大小
    """

    def parse_size(size_str: str) -> float:
        """
        解析size_str得到具体的size

        Args:
            size_str (str): 描述大小的字符串

        Returns:
            float: 以MB为单位的大小
        """
        if size_str[-1] == 'B':
            num, unit = size_str[:-2], size_str[-2]
        else:
            num, unit = size_str[:-1], size_str[-1]
        assert unit in SIZE_UNIT, \
            "unknown shm size unit {}".format(unit)
        return float(num) * (1024 ** (SIZE_UNIT.index(unit) - 1))

    try:
        df_infos = os.popen(SHM_QUERY_CMD).readlines()
    except:
        return None
    else:
        shm_infos = []
        for df_info in df_infos:
            info = df_info.strip()
            if info.find(SHM_KEY) >= 0:
                shm_infos.append(info.split())

        if len(shm_infos) == 0:
            return None
        elif len(shm_infos) == 1:
            return parse_size(shm_infos[0][3])
        else:
            default_mount_infos = [
                si for si in shm_infos if si[-1] == SHM_DEFAULT_MOUNT
            ]
            if default_mount_infos:
                return parse_size(default_mount_infos[0][3])
            else:
                return max([parse_size(si[3]) for si in shm_infos])


class BatchCollateFunction(object):
    """
    Function to generate mini-batch data by merging the sample list.
    """
    def __init__(self, datatset, collate_batch: True):
        self.dataset = datatset
        self.collate_batch = collate_batch

    def __call__(self, batch):
        for f in self.dataset.batch_transforms:
            try:
                batch = f(batch)
            except Exception as e:
                stack_info = traceback.format_exc()
                warnings.warn("fail to map batch transform [{}] with error: {} and stack:\n{}".format(
                    f, e, str(stack_info)))
                raise e

        # remove keys which is not needed by model
        extra_key = ['h', 'w', 'flipped']
        for k in extra_key:
            for sample in batch:
                if k in sample:
                    sample.pop(k)

        from paddle.fluid.io import default_collate_fn

        if self.collate_batch:
            batch_data = default_collate_fn(batch)
        else:
            batch_data = {}
            for k in batch[0].keys():
                tmp_data = []
                for i in range(len(batch)):
                    tmp_data.append(batch[i][k])
                if not 'gt_' in k and not 'is_crowd' in k and not 'difficult' in k:
                    tmp_data = np.stack(tmp_data, axis=0)
                batch_data[k] = tmp_data

        return batch_data


def build_paddle_loader(dataset: BaseMultiDataset,
                        sample_transforms: Optional[List] = [],
                        batch_transforms: Optional[List] = [],
                        batch_size: Optional[int] = 1,
                        num_workers: Optional[int] = 4,
                        shuffle: Optional[bool] = False,
                        drop_last: Optional[bool] = False,
                        collate_batch: Optional[bool] = True,
                        use_shared_memory: Optional[bool] = False,
                        preprocessing_module: Optional[Callable] = None,
                        batch_sampler: Optional[Callable] = None,
                        return_list: Optional[bool] = False,
                        prefetch_factor: Optional[int] = 2,
                        **kwargs) -> Iterator:
    """
    > This function returns a PaddlePaddle data loader that can be used to iterate over a dataset

    :param dataset: The dataset to be used for the loader
    :type dataset: BaseDataset
    :param sample_transforms: A list of transforms to be applied to each sample
    :type sample_transforms: Optional[List]
    :param batch_transforms: Optional[List] = [],
    :type batch_transforms: Optional[List]
    :param batch_size: The number of samples in each batch, defaults to 1
    :type batch_size: Optional[int] (optional)
    :param num_workers: The number of workers to use for loading the data, defaults to 4
    :type num_workers: Optional[int] (optional)
    :param shuffle: Whether to shuffle the data, defaults to False
    :type shuffle: Optional[bool] (optional)
    :param drop_last: If True, the last batch will be dropped in the case that its size would be less than batch_size,
    defaults to False
    :type drop_last: Optional[bool] (optional)
    :param collate_batch: Whether to collate the batch. If False, the batch will be a list of tensors, defaults to True
    :type collate_batch: Optional[bool] (optional)
    :param use_shared_memory: Whether to use shared memory for data loading, defaults to False
    :type use_shared_memory: Optional[bool] (optional)
    :param preprocessing_module: Optional[Callable] = None,
    :type preprocessing_module: Optional[Callable]
    :param batch_preprocessing_fn: Optional[Callable] = None,
    :type batch_preprocessing_fn: Optional[Callable]
    :param batch_sampler: Optional[Callable] = None,
    :type batch_sampler: Optional[Callable]
    :param return_list: If True, the loader will return a list of samples instead of a dict, defaults to False
    :type return_list: Optional[bool] (optional)
    :prefetch_factor: Number of batch data the DataLoader would prefetch, if use_buffer_reader=True. Default 2.
    :type prefetch_factor: (int, optional)
    :return: A Iterator object.
    """
    logger = setup_logger("build_paddle_loader")
    dataset.parse_dataset()
    if len(dataset)//idist.get_world_size() < batch_size:
        logger.warning("The dataset is too small, reduce the batch size from {} to {}".format(
            batch_size, len(dataset)//idist.get_world_size()
        ))
        batch_size = len(dataset)//idist.get_world_size() if len(dataset)//idist.get_world_size() > 0 else 1
    # set sample transforms
    dataset.set_transform(sample_transforms, preprocessing_module)
    dataset.set_kwargs(**kwargs)
    # set batch transforms
    dataset.set_batch_transform(batch_transforms, preprocessing_module)

    batch_collate_fn = BatchCollateFunction(datatset=dataset, collate_batch=collate_batch)
    batch_preprocessing_fn = batch_collate_fn

    # batch sampler 默认初始化
    if batch_sampler is None:
        if dataset.mode == TRAIN:
            batch_sampler = paddle.io.DistributedBatchSampler(dataset,
                                                              batch_size=batch_size,
                                                              shuffle=shuffle,
                                                              drop_last=drop_last)
        else:
            if dataset.distribute_val:
                batch_sampler = paddle.io.DistributedBatchSampler(dataset,
                                                                  batch_size=batch_size,
                                                                  shuffle=shuffle,
                                                                  drop_last=drop_last)
            else:
                if idist.get_rank() == 0:
                    batch_sampler = paddle.io.BatchSampler(dataset,
                                                           batch_size=batch_size,
                                                           shuffle=shuffle,
                                                           drop_last=drop_last)

    # DataLoader do not start sub-process in Windows and Mac
    # system, do not need to use shared memory
    use_shared_memory = use_shared_memory and sys.platform not in ['win32', 'darwin']
    # check whether shared memory size is bigger than 1G(1024M)
    if use_shared_memory:
        shm_size = get_shared_memory_size()
        if shm_size is not None and shm_size < 1024.:
            warnings.warn("Shared memory size is less than 1G, disable shared_memory in DataLoader")
            use_shared_memory = False

    data_loader = None
    if batch_sampler is not None:
        data_loader = paddle.io.DataLoader(
            dataset=dataset,
            batch_sampler=batch_sampler,
            collate_fn=batch_preprocessing_fn,
            num_workers=num_workers,
            return_list=return_list,
            use_shared_memory=use_shared_memory,
            persistent_workers=True,
            prefetch_factor=prefetch_factor,
            timeout=10)

    return data_loader