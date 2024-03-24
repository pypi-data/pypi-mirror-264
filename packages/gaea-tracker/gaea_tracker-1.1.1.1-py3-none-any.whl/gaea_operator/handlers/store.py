#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : store.py
@Author        : yanxiaodong
@Date          : 2022/12/8
@Description   :
"""
import fcntl
import os
import copy
from abc import ABCMeta, abstractmethod
from pathlib import Path
import shutil
from typing import Any, Callable, List, Mapping, Optional, Union

import json

import gaea_operator.distributed as idist
from gaea_operator.engine import Engine, Events
from gaea_operator.data.source import BaseMultiDataset, DALIBaseMultiDataset
from gaea_operator.utils import MOUNT_PATH, MASTER_RANK

from .checkpoint import DiskSaver


class ResultDiskSaver(DiskSaver):
    """
    Handler that saves input checkpoint on a disk.

    :param results: The results of the experiment
    :type results: Mapping
    :param filename: The name of the file to write to
    :type filename: str
    :param metadata: A dictionary of metadata to be saved with the results
    :type metadata: Optional[Mapping]
    """
    def __init__(
            self,
            dirname: Union[str, Path],
            atomic: bool = True,
            create_dir: bool = True,
            require_empty: bool = True):
        super(ResultDiskSaver, self).__init__(dirname=dirname, atomic=atomic, create_dir=create_dir,
                                              require_empty=require_empty)
        if MOUNT_PATH is not None and len(MOUNT_PATH) > 0:
            self.tem_dirname = Path(os.path.relpath(self.dirname, MOUNT_PATH)).expanduser()
        else:
            self.tem_dirname = self.dirname

        if not self.tem_dirname.exists():
            self.tem_dirname.mkdir(parents=True)

    def __call__(self, results: Mapping, filename: str, metadata: Optional[Mapping] = None) -> None:
        if os.path.exists(filename):
            with open(filename, 'r+') as fw:
                fcntl.flock(fw, fcntl.LOCK_EX)
                reader = json.load(fw)
                for key in reader:
                    if key not in ["categories", "images"]:
                        reader[key].extend(results[key])
                fw.seek(0)
                fw.truncate()
                json.dump(reader, fw, indent=2)
                fcntl.flock(fw, fcntl.LOCK_UN)
        else:
            with open(filename, 'w') as fw:
                fcntl.flock(fw, fcntl.LOCK_EX)
                json.dump(results, fw, indent=2)
                fcntl.flock(fw, fcntl.LOCK_UN)
        # 保持所有进程同步
        idist.barrier()


class OutputStore(metaclass=ABCMeta):
    """
    OutputStore handler to save output prediction
    after every epoch, could be useful for e.g., visualization purposes.

    :param output_transform: A function that takes in the output of the dataset and transforms it
    :type output_transform: Callable
    """

    def __init__(self, output_transform: Callable = lambda x: x):
        self.data = []  # type: List[Any]
        self.output_transform = output_transform
        self.dist_tem_file = None

    @property
    def store_file(self):
        return self.dist_tem_file

    def reset(self) -> None:
        """
        Reset the attribute data to empty list.
        """
        self.data = []

    def update(self, engine: Engine) -> None:
        """
        Append the output of Engine to attribute data.
        """
        output = self.output_transform(engine.state.output)
        if isinstance(output, List):
            self.data.extend(output)
        else:
            self.data.append(output)

    @abstractmethod
    def store(self, engine: Engine) -> None:
        """
        Store results.
        """
        pass

    def attach_engine(self, engine: Engine) -> None:
        """
        Attaching `reset` method at EPOCH_STARTED and `update` method at ITERATION_COMPLETED.
        """
        engine.add_event_handler(Events.EPOCH_STARTED, self.reset)
        engine.add_event_handler(Events.ITERATION_COMPLETED, self.update)
        engine.add_event_handler(Events.EPOCH_COMPLETED, self.store)


class COCOOutputStore(OutputStore):
    """
    COCOOutputStore handler to save output prediction
    after every epoch, could be useful for e.g., visualization purposes.

    :param dirname: The directory where the results will be saved
    :type dirname: Union[str, Path]
    :param require_empty: If True, the directory must be empty. If False, the directory must exist, defaults to True
    :type require_empty: bool (optional)
    :param create_dir: If True, the directory will be created if it doesn't exist, defaults to True
    :type create_dir: bool (optional)
    :param threshold: The minimum score for a detection to be considered a positive prediction
    :type threshold: float
    """
    result_file = "result.json"

    def __init__(self,
                 dirname: Union[str, Path],
                 dataset: Union[BaseMultiDataset, DALIBaseMultiDataset],
                 require_empty: bool = False,
                 create_dir: bool = True,
                 threshold: float = 0.1,
                 **kwargs
                 ):
        super(COCOOutputStore, self).__init__(**kwargs)
        self.threshold = threshold
        self.disk_saver = ResultDiskSaver(dirname,
                                          atomic=False,
                                          create_dir=create_dir,
                                          require_empty=require_empty)
        self.dist_file = os.path.join(self.disk_saver.dirname, self.result_file)
        self.dist_tem_file = os.path.join(self.disk_saver.tem_dirname, self.result_file)
        self.data_raw = dataset.common_data_instance.meta_data
        self.images = copy.deepcopy(self.data_raw["images"])
        for img in self.images:
            if img["file_name"].startswith(MOUNT_PATH):
                img["file_name"] = os.path.relpath(img["file_name"], MOUNT_PATH)
        self.categories = self.data_raw["categories"]

    def reset(self) -> None:
        """
        Reset the attribute data to empty list.
        """
        super(COCOOutputStore, self).reset()
        if idist.get_rank() == MASTER_RANK:
            if os.path.exists(self.dist_file):
                os.remove(self.dist_file)

    def store(self, engine: Engine) -> None:
        """
        Store results.
        """
        outputs = {"annotations": [],
                   "images": self.images, 
                   "categories": self.categories}
        anno_id = 1
        for res in self.data:
            if res["score"] < self.threshold:
                continue
            outputs["annotations"].append(res)
            anno_id += 1

        self.disk_saver(outputs, self.dist_tem_file)
        if not os.path.samefile(os.path.split(self.dist_tem_file)[0], os.path.split(self.dist_file)[0]):
            if idist.get_rank() == MASTER_RANK:
                shutil.copyfile(self.dist_tem_file, self.dist_file)

