#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : dali_dataset.py
@Author        : xuningyuan
@Date          : 2022/11/09
@Description   :
"""
import os
import os.path as osp
from abc import ABCMeta, abstractmethod
from typing import List, Dict
from gaea_operator.utils import setup_logger, MOUNT_PATH
from .anno_parse import TRAIN, VAL, DataConfig


class DatasetArgument(metaclass=ABCMeta):
    """
    Dataset argument.
    """

    def __init__(self, dataset_uri: str = '', dataset_names: str = ''):
        pass


class Dataset(DatasetArgument):
    """
    An abstract class to encapsulate methods and behaviors of datasets.
    Args:
        kind: dataset source.
        mode: train or validation.
    """

    mode_keys = ["train", "single_val", "parallel_val"]

    def __init__(self,
                 dataset_uri: str,
                 mode: str = "train",
                 anno_path: str = "",
                 image_dir: str = "",
                 categories: list = []):
        self._logger = setup_logger(__name__ + "." + self.__class__.__name__)
        if MOUNT_PATH == "":
            self._logger.warning(
                "annotation path: {} must be the absolute file or "
                "the relative path for work directory.".format(anno_path)
            )

        self._logger.info("The dataset_uri is {}.".format(dataset_uri))

        if dataset_uri != "":
            self.dataset_uri = dataset_uri
            anno_path = dataset_uri
            image_dir = dataset_uri

        self.anno_path = anno_path
        self.mode = mode
        self.image_dir = image_dir
        self.categories = categories

        self.check_anno_path(anno_path)
        self.check_image_dir(image_dir)
        self.check_mode(mode)

        self.common_data_instance = DataConfig("")

        self.cname2clsid = {cate["name"]: cate["id"] for cate in self.categories}

    def check_mode(self, mode: str):
        assert (
                mode in self.mode_keys
        ), "please ensure mode, mode must be in {}, however it's {}.".format(
            self.mode_keys, mode
        )
        if mode == self.mode_keys[0]:
            self.mode = TRAIN
        else:
            self.mode = VAL
            if mode == self.mode_keys[1]:
                self.distribute_val = False
            else:
                self.distribute_val = True

    def check_anno_path(self, anno_path: str):
        if not isinstance(anno_path, str):
            raise TypeError(
                "please check the type of anno_path, which should be str not {}".format(
                    type(anno_path)
                )
            )

        if not osp.exists(anno_path):
            raise ValueError(
                "please check your anno_path, can't find the file {}".format(
                    anno_path
                )
            )

    def check_image_dir(self, image_dir: str):
        if not isinstance(image_dir, str):
            raise TypeError(
                "please check the type of image_dir, which should be str not {}".format(
                    type(image_dir)
                )
            )

        if not osp.exists(image_dir):
            raise ValueError(
                "please check your image_dir, can't find the directory {}".format(
                    image_dir
                )
            )

    @property
    def num_classes(self):
        return len(self.categories)

    @property
    def clsid2catid(self):
        return {clsid: cate['id'] for clsid, cate in enumerate(self.categories)}

    @property
    def catid2clsid(self):
        return {cate['id']: clsid for clsid, cate in enumerate(self.categories)}

    @abstractmethod
    def __len__(self):
        """
        获取数据集的长度
        """
        pass


class MultiDataset(Dataset, metaclass=ABCMeta):
    """
    多数据集解析与整合
    """

    def __init__(self,
                 dataset_uri: str,
                 mode: str,
                 anno_path: str = "",
                 image_dir: str = "",
                 categories: list = [],
                 kind: str = "",
                 ratio: float = 0,
                 common_data_instance: DataConfig = None):
        super(MultiDataset, self).__init__(dataset_uri, mode=mode, anno_path=anno_path, image_dir=image_dir,
                                           categories=categories)
        self.check_kind(kind)

        if common_data_instance is None:
            for kind_item, anno_path_item, image_dir_item in zip(self.kind_list, self.anno_path_list, self.image_dir_list):
                # 数据格式解析
                common_data_instance = self.parse_data(kind_item, anno_path_item, image_dir_item)
                # 整合数据
                self.rebuild_data(anno_path_item, common_data_instance)
            self.common_data_instance.random_split(ratio=ratio)
        else:
            self.common_data_instance = common_data_instance
            self.categories = [{"name": cate['name'], "id": cate['id']} for cate in
                               self.common_data_instance.meta_data["categories"]]
            self.cname2clsid = {cate["name"]: cate["id"] for cate in self.categories}
            self.common_data_instance.meta_data = self.common_data_instance.val_meta_data

    @abstractmethod
    def parse_data(self, kind_item: str, anno_path_item: str, image_dir_item):
        """
        parse data of according to the kind
        """
        pass

    def check_anno_path(self, anno_path: str):
        if not isinstance(anno_path, str):
            raise TypeError(
                "please check the type of anno_path, which should be str not {}".format(
                    type(anno_path)
                )
            )

        self.anno_path_list = anno_path.split(",")
        self.anno_path_list = [osp.join(MOUNT_PATH, anno_path) for anno_path in self.anno_path_list]

        for anno_path_item in self.anno_path_list:
            super().check_anno_path(anno_path_item)

    def check_image_dir(self, image_dir: str):
        if not isinstance(image_dir, str):
            raise TypeError(
                "please check the type of image_dir, which should be str not {}".format(
                    type(image_dir)
                )
            )

        self.image_dir_list = image_dir.split(",")
        self.image_dir_list = [osp.join(MOUNT_PATH, image_dir) for image_dir in self.image_dir_list]

        if len(self.image_dir_list) == 1:
            self.image_dir_list = self.image_dir_list * len(self.anno_path_list)
        assert len(self.image_dir_list) == len(
            self.anno_path_list
        ), "please check the numbert of image_dir and the number of anno_path, {} is different with {}".format(
            len(self.image_dir_list), len(self.anno_path_list)
        )
        for image_dir_item in self.image_dir_list:
            super().check_image_dir(image_dir_item)

    def check_kind(self, kind: str):
        if not isinstance(kind, str):
            raise TypeError(
                "please check the type of kind, which should be str not {}".format(
                    type(kind)
                )
            )
        self.kind_list = kind.split(",")
        if len(self.kind_list) == 1:
            self.kind_list = self.kind_list * len(self.anno_path_list)
        assert len(self.kind_list) == len(self.anno_path_list), \
            "please check the numbert of kind and the number of anno_path, {} is different with {}".format(
                len(self.kind_list), len(self.anno_path_list)
            )

        for kind_item in self.kind_list:
            assert kind_item in self.kind_keys, "please ensure kind, kind must be in {}, however it is {}.".format(
                self.kind_keys, kind_item
            )

    def rebuild_data(self, anno_path_item: str, common_data_instance: DataConfig):
        """
        重新构建self.common_data_instance
        """
        # 整合数据        
        if type(self.common_data_instance) == DataConfig:
            self.common_data_instance = common_data_instance
            if len(self.categories) == 0:
                self.categories = [{"name": cate['name'], "id": cate['id']} for cate in
                                   self.common_data_instance.meta_data["categories"]]
                self.cname2clsid = {cate["name"]: cate["id"] for cate in self.categories}
            else:
                base_data = {"annotations": [], "images": [], "categories": self.categories}
                cur_data = common_data_instance.meta_data

                newcatid2basecatid = self.get_catid_tranform(anno_path_item, cur_data)
                self.common_data_instance.meta_data = self.merge_history_data(base_data, cur_data, newcatid2basecatid)
        else:
            base_data = self.common_data_instance.meta_data
            cur_data = common_data_instance.meta_data

            newcatid2basecatid = self.get_catid_tranform(anno_path_item, cur_data)
            self.common_data_instance.meta_data = self.merge_history_data(base_data, cur_data, newcatid2basecatid)

    def get_catid_tranform(self, anno_path_item: str, cur_data: Dict[str, List]):
        newcatid2basecatid = {}
        for cate in cur_data["categories"]:
            if cate["name"] not in self.cname2clsid:
                raise ValueError("the categories of current annotation file {} has category name {}, "
                                 "which is not in the base annotation file {}".format(anno_path_item, cate['name'],
                                                                                      self.anno_path_list[0]))
            else:
                newcatid2basecatid[cate['id']] = self.cname2clsid[cate["name"]]
        return newcatid2basecatid

    def merge_history_data(self, base_data: Dict[str, List], cur_data: Dict[str, List],
                           newcatid2basecatid: Dict[int, int]):
        img_start_id = max([img['id'] for img in base_data["images"]]) if len(base_data["images"]) > 0 else 0
        anno_start_id = max([anno['id'] for anno in base_data["annotations"]]) \
            if len(base_data["annotations"]) > 0 else 0

        for img in cur_data["images"]:
            img['id'] = img_start_id + img['id']
        base_data["images"].extend(cur_data["images"])

        for anno in cur_data['annotations']:
            anno["image_id"] = img_start_id + anno["image_id"]
            anno["id"] = anno_start_id + anno["id"]
            anno['category_id'] = newcatid2basecatid[anno['category_id']]
        base_data["annotations"].extend(cur_data['annotations'])

        return base_data
