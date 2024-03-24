#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : dali_dataloader.py
@Author        : xuningyuan
@Date          : 2022/11/14
@Description   :
"""
import math
from typing import List, Union, Iterator
from enum import Enum, unique

import numpy as np

from gaea_operator.data.source.dali_dataset import DALIBaseMultiDataset
from gaea_operator.engine import PADDLE_BACKEND, TORCH_BACKEND
from gaea_operator.plugin import _DaliBaseIterator, LastBatchPolicy
from gaea_operator.utils import setup_logger
from gaea_operator.utils.dali import feed_paddle_tensor, feed_torch_tensor
from gaea_operator.distributed import get_world_size, get_rank


class DaliIterator(_DaliBaseIterator):
    """
    General DALI iterator. It can return any number of
    outputs from the DALI pipeline in the form of Paddle's Tensors.
    """

    def __init__(
            self,
            pipelines,
            output_map,
            size=-1,
            reader_name=None,
            auto_reset=False,
            fill_last_batch=None,
            last_batch_padded=False,
            last_batch_policy="FILL",
            prepare_first_batch=True,
            backend="paddle",
    ):

        if last_batch_policy == "FILL":
            last_batch_policy = LastBatchPolicy.FILL
        # check the assert first as _DaliBaseIterator would run the prefetch
        output_map = [v for v in output_map]
        assert len(set(output_map)) == len(
            output_map
        ), "output_map names should be distinct"
        self.output_map = output_map

        super().__init__(
            pipelines,
            size,
            reader_name,
            auto_reset,
            fill_last_batch,
            last_batch_padded,
            last_batch_policy,
            prepare_first_batch
        )

        self._num_pipes = len(self._pipes)
        self._num_gpus = get_world_size()
        self.local_rank = get_rank()
        self._logger = setup_logger(__name__ + "." + self.__class__.__name__)

        if backend == TORCH_BACKEND:
            self.feed_tensor = feed_torch_tensor
        elif backend == PADDLE_BACKEND:
            self.feed_tensor = feed_paddle_tensor

        self._first_batch = None
        if self._prepare_first_batch:
            try:
                self._first_batch = self.__next__()
                # call to `next` sets _ever_consumed to True but if we are just calling it from
                # here we should set if to False again
                self._ever_consumed = False
            except StopIteration:
                assert False, (
                    "It seems that there is no data in the pipeline. This may happen "
                    "if `last_batch_policy` is set to PARTIAL and the requested batch size is "
                    "greater than the shard size."
                )

    def __next__(self):
        self._ever_consumed = True
        if self._first_batch is not None:
            batch = self._first_batch
            self._first_batch = None
            return batch

        # Gather outputs
        outputs = self._get_outputs()

        data_batches = [None for i in range(self._num_pipes)]

        for i in range(self._num_pipes):
            dev_id = self._pipes[i].device_id
            # Initialize dict for all output categories
            category_outputs = dict()
            # Segregate outputs into categories
            for j, out in enumerate(outputs[i]):
                try:
                    category_outputs[self.output_map[j]] = self.feed_tensor(out, dev_id)
                except RuntimeError as e:
                    self._logger.error(
                        "there is some problems when current output filed is {}".format(self.output_map[j]))
                    raise e
            data_batches[i] = category_outputs

        self._schedule_runs()

        self._advance_and_check_drop_last()

        if self._reader_name:
            if_drop, left = self._remove_padded()
            if np.any(if_drop):
                output = []
                for batch, to_copy in zip(data_batches, left):
                    batch = batch.copy()
                    for cat in self.output_map:
                        batch[cat] = batch[cat][:to_copy]
                    output.append(batch)
                return output

        else:
            if (
                    self._last_batch_policy == LastBatchPolicy.PARTIAL
                    and (self._counter > self._size)
                    and self._size > 0
            ):
                # First calculate how much data is required to
                # return exactly self._size entries.
                diff = self._num_gpus * self.batch_size - (self._counter - self._size)
                # Figure out how many GPUs to grab from.
                num_gpus_to_grab = int(math.ceil(diff / self.batch_size))
                # Figure out how many results to grab from the last GPU
                # (as a fractional GPU batch may be required to bring us
                # right up to self._size).
                mod_diff = diff % self.batch_size
                data_from_last_gpu = mod_diff if mod_diff else self.batch_size

                # Grab the relevant data.
                # 1) Grab everything from the relevant GPUs.
                # 2) Grab the right data from the last GPU.
                # 3) Append data together correctly and return.
                outputs = data_batches
                if self.world_size > 1 and self.local_rank == self.world_size - 1:
                    for output in outputs:
                        for cat in self.output_map:
                            lod_tensor = output[-1][cat]
                            outputs[cat] = lod_tensor[:data_from_last_gpu]
                return outputs

        if self._num_pipes == 1:
            return data_batches[0]
        else:
            return data_batches


def build_dali_loader(
        dataset: Union[DALIBaseMultiDataset, List[DALIBaseMultiDataset]],
        module: str,
        transforms: list = [],
        shuffle=False,
        batch_size=4,
        num_threads=4,
        drop_last=False
) -> Iterator:
    """
    It builds a DALI iterator that can be used as a PyTorch or PaddlePaddle dataloader

    :param dataset: The dataset to be used
    :type dataset: Union[DALIDataset, List[DALIDataset]]
    :param module: paddle or torch
    :type module: str
    :param transforms: a list of DALI transforms
    :type transforms: list
    :param shuffle: Whether to shuffle the data, defaults to False (optional)
    :param batch_size: batch size, defaults to 4 (optional)
    :param num_threads: The number of threads used to read data, defaults to 4 (optional)
    :param drop_last: If True, the last batch will be dropped if its size is less than batch_size, defaults to False
    (optional)
    :return: A DaliIterator object.
    """
    logger = setup_logger("build_dali_loader")
    if len(dataset) // get_world_size() < batch_size:
        logger.warning("The dataset is too small, reduce the batch size from {} to {}".format(
            batch_size, len(dataset) // get_world_size()
        ))
        batch_size = len(dataset) // get_world_size()

    if dataset.local_rank >= dataset.ranks:
        return None

    if isinstance(dataset, List):
        pipeline = [
            ds.build_pipeline(
                transforms,
                shuffle=shuffle,
                batch_size=batch_size,
                num_threads=num_threads,
            )
            for ds in dataset
        ]
        reader_name = None
    else:
        pipeline = dataset.build_pipeline(
            transforms, shuffle=shuffle, batch_size=batch_size, num_threads=num_threads, device_id=get_rank()
        )
        reader_name = "Reader"

    if drop_last:
        policy = LastBatchPolicy.DROP
    else:
        policy = LastBatchPolicy.FILL

    assert module in ("paddle", "torch")
    dataloader = iter(
        DaliIterator(
            pipeline,
            output_map=dataset.output_fields,
            reader_name=reader_name,
            backend=module,
            last_batch_policy=policy,
        )
    )
    # import paddle
    # print("current paddle fleet rank is {}, current local rank is {}, while previous loacl rank is {}, world size is {}".format(paddle.distributed.fleet.local_rank(), get_local_rank(), dataset.local_rank, get_world_size()))
    return dataloader
