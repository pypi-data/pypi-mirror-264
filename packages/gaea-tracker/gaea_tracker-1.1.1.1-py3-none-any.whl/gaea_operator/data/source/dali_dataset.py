#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : dali_dataset.py
@Author        : xuningyuan
@Date          : 2022/11/09
@Description   :
"""
import copy
import os
import os.path as osp
from abc import abstractmethod, ABCMeta
from typing import Dict, List
import random

import gaea_operator.data.transforms.dali_ops as ops
from gaea_operator.distributed import get_rank, get_world_size
from gaea_operator.plugin import fn, pipeline_def
from gaea_operator.utils import MOUNT_PATH

from .anno_parse import (
    DataConfig,
    ChangeDetectionDataConfig,
    COCODataConfig,
    CVATDataConfig,
    ImagenetDataConfig,
    WSMPDataConfig,
    anno_common2cityscape,
    anno_common2coco,
    anno_common2imagenet,
    check_filepaths,
    get_id2path,
)

from .base import Dataset, MultiDataset


class DALIBaseDataset(Dataset, metaclass=ABCMeta):
    """
    基于DALI预处理加速的数据集迭代器基类

    """

    def __init__(
            self, dataset_uri, mode: str = "train", anno_path: str = "", image_dir: str = "", categories=[], **kwargs
    ):
        super(DALIBaseDataset, self).__init__(
            dataset_uri, mode=mode, anno_path=anno_path, image_dir=image_dir, categories=categories, **kwargs
        )

        self.local_rank = get_rank()
        self.ranks = get_world_size()

        if mode == self.mode_keys[1]:
            self.distribute_val = False
            self.ranks = 1
        else:
            self.distribute_val = True

    def _build_transforms(
            self, output_map: tuple, tensor_tuple: tuple, transforms: List[Dict]
    ):
        """
        It takes a list of transforms and applies them to the tensor_tuple

        :param output_map: A dictionary mapping the names of the outputs to their corresponding tensors
        :param tensor_tuple: A tuple of tensors that are the inputs to the model
        :param transforms: a list of transforms to apply to the tensor_tuple
        """
        tensor_dict = {k: v for k, v in zip(output_map, tensor_tuple)}
        for transform in transforms:
            for k, v in transform.items():
                tensor_dict = getattr(ops, k)(tensor_dict, **v)
        return tuple(tensor_dict.values())

    @abstractmethod
    def build_pipeline(self, transforms: List[Dict], shuffle=True):
        """
        构建数据变换pipeline
        """
        pass

    @abstractmethod
    def set_output_fields(self):
        """
        设置预处理变换时的字段和最后输出时的字段
        """
        pass


class DALIBaseMultiDataset(DALIBaseDataset, MultiDataset, metaclass=ABCMeta):
    """
    基于DALI预处理加速的多数据集迭代器基类

    """

    def __init__(
            self, dataset_uri="", mode="train", anno_path: str = "", image_dir: str = "", categories=[], kind: str = "",
            ratio: float = 0, common_data_instance: DataConfig = None
    ):
        super().__init__(dataset_uri,
                         mode=mode,
                         anno_path=anno_path,
                         image_dir=image_dir,
                         categories=categories,
                         kind=kind,
                         ratio=ratio,
                         common_data_instance=common_data_instance)


class DALICityscapesDataset(DALIBaseDataset):
    """
    基于DALI的cityscapes格式的数据集迭代器
    """

    def __init__(self, dataset_uri="", mode="train", anno_path: str = "", image_dir: str = "", categories=[]):
        super().__init__(dataset_uri, mode=mode, anno_path=anno_path,
                         image_dir=image_dir, categories=categories)
        if osp.isdir(self.anno_path):
            if len(self.categories) == 0:
                with open(osp.join(MOUNT_PATH, self.anno_path, "labels.txt")) as f:
                    catenames = f.readlines()
                self.categories = [{"name": name, "id": id}
                                   for id, name in enumerate(catenames)]

            if self.mode == self.mode_keys[0]:
                self.anno_path = osp.join(self.anno_path, "train.txt")
            else:
                self.anno_path = osp.join(self.anno_path, "val.txt")

        with open(osp.join(MOUNT_PATH, self.anno_path)) as f:
            data = f.readlines()

        self.image_paths = [s.split("\n")[0].rsplit(" ", 1)[0] for s in data]
        self.label_paths = [s.split("\n")[0].rsplit(" ", 1)[1] for s in data]

        self.image_paths = check_filepaths(
            self.image_paths, image_dir=self.image_dir)
        self.label_paths = check_filepaths(
            self.label_paths, image_dir=self.image_dir)

        self.set_output_fields()

    def __len__(self):
        return len(self.image_paths)

    @pipeline_def
    def build_pipeline(self, transforms: List[Dict], shuffle=True):
        reader_seed = random.randint(0, 2 ** 32 - 1)
        images, _ = fn.readers.file(
            files=self.image_paths,
            shard_id=self.local_rank,
            num_shards=self.ranks,
            random_shuffle=shuffle,
            name="Reader",
            seed=reader_seed,
        )
        labels, _ = fn.readers.file(
            files=self.label_paths,
            shard_id=self.local_rank,
            num_shards=self.ranks,
            random_shuffle=shuffle,
            name="ReaderLabel",
            seed=reader_seed,
            pad_last_batch=True,
        )
        return self._build_transforms(self.output_map, (images, labels), transforms)

    def set_output_fields(self):
        if self.mode == "train":
            self.output_map = ["images", "segm"]
        else:
            self.output_map = ["images", "segm_ori"]
        self.output_fields = ["img", "label", "im_shape", "scale_factor"]


class DALIClassficationDataset(DALIBaseMultiDataset):
    """
    基于DALI预处理加速的imagenet格式的数据集迭代器（用于训练）

    :param anno_path: the path to the annotation file
    :type anno_path: str
    :param mode: 'train' or 'validation', defaults to train
    :type mode: str (optional)
    :param kind: 'WSMP' or 'default'('ImageNet'), defaults to 'default'
    :type kind: str (optional)
    :param image_dir: the directory where the images are stored, defaults to ""
    :type image_dir: str
    """

    kind_keys = ["ImageNet"]

    def __init__(
            self,
            dataset_uri: str = "",
            mode: str = "train",
            anno_path: str = "",
            image_dir: str = "",
            categories: list = [],
            kind: str = "ImageNet",
            ratio: float = 0,
            common_data_instance: DataConfig = None
    ):
        super().__init__(
            dataset_uri, mode=mode, anno_path=anno_path, image_dir=image_dir, categories=categories, kind=kind,
            ratio=ratio, common_data_instance=common_data_instance
        )

        (
            self.imgs,
            self.labels,
            self.img_id_list,
        ) = anno_common2imagenet(self.common_data_instance)

        self.set_output_fields()

    def set_output_fields(self):
        if self.mode == self.mode_keys[0]:
            self.output_map = ["images", "labels"]
            self.output_fields = [0, 1, "im_shape", "scale_factor"]
        else:
            self.output_map = ["images", "ids"]
            self.output_fields = [0, "im_id", "im_shape", "scale_factor"]

    def __len__(self):
        return len(self.imgs)

    def parse_data(self, kind_item, anno_path_item, image_dir_item):
        if kind_item == self.kind_keys[0]:
            common_data_instance = ImagenetDataConfig(
                anno_path_item, image_dir=image_dir_item, mode=self.mode)
        return common_data_instance

    @pipeline_def
    def build_pipeline(self, transforms: dict, shuffle: bool = True):
        """
        > This function takes a dictionary of transforms and returns a pipeline of transforms

        :param transforms: a dictionary of transforms to apply to the data
        :type transforms: dict
        :param shuffle: Whether to shuffle the data, defaults to True
        :type shuffle: bool (optional)
        """
        if self.mode == self.mode_keys[0]:
            labels = self.labels
        else:
            labels = self.img_id_list

        tensor_tuple = fn.readers.file(
            files=self.imgs,
            labels=labels,
            shard_id=self.local_rank,
            num_shards=self.ranks,
            random_shuffle=shuffle,
            name="Reader",
            pad_last_batch=True,
        )
        return self._build_transforms(self.output_map, tensor_tuple, transforms)


class DALIObjectDetectionDataset(DALIBaseMultiDataset):
    """
    基于DALI预处理加速的COCO格式的数据集迭代器（用于训练）

    :param anno_path: path to the annotation file
    :type anno_path: str
    :param mode: 'train' or 'val', defaults to train
    :type mode: str (optional)
    :param kind: 'default'('coco') or 'WSMP', defaults to 'default'
    :type kind: str (optional)
    :param image_dir: The directory where the images are stored
    :type image_dir: str
    :param image_ids: If True, the dataset will return the image ids, defaults to False
    :type image_ids: bool (optional)
    :param polygons: If True, the polygons will be returned for instance segmentation task, defaults to False
    :type polygons: bool (optional)
    :param pixel_masks: If True, the dataset will return a pixel mask for instance segmentation, defaults to False
    :type pixel_masks: bool (optional)
    """

    kind_keys = ["WSMP", "COCO", "CVAT"]

    def __init__(
            self,
            dataset_uri: str = "",
            mode: str = "train",
            anno_path: str = "",
            image_dir: str = "",
            image_ids: bool = False,
            categories: list = [],
            kind: str = "COCO",
            allow_empty: bool = False,
            polygons: bool = False,
            pixel_masks: bool = False,
            ratio: float = 0,
            common_data_instance: DataConfig = None
    ):
        super().__init__(
            dataset_uri, mode=mode, anno_path=anno_path, image_dir=image_dir, categories=categories, kind=kind,
            ratio=ratio, common_data_instance=common_data_instance
        )
        self.anno_orig = anno_path
        self.mode = mode
        self.kind = kind
        self.image_dir = image_dir
        self.image_ids = image_ids
        self.polygon_masks = polygons
        self.pixelwise_masks = pixel_masks
        self.skip_empty = not allow_empty

        os.makedirs("tmp", exist_ok=True)
        self.anno_path = "tmp/{}.json".format(self.mode)
        self.data = anno_common2coco(
            self.common_data_instance, std_anno_path=self.anno_path
        )

        self.set_output_fields()

        if self.skip_empty:
            anno_image_ids = [
                anno["image_id"]
                for anno in self.common_data_instance.meta_data["annotations"]
            ]
            self.length = len(set(anno_image_ids))
        else:
            self.length = len(self.common_data_instance.meta_data["images"])

    def set_output_fields(self):
        if self.mode == self.mode_keys[0]:
            self.output_map = ["images", "bboxes", "labels"]
            self.output_fields = ["image", "gt_bbox", "gt_class"]
            if self.polygon_masks:
                self.output_map.extend(["polygons", "vertices"])
                self.output_fields.extend(["gt_poly", "gt_vertices"])
            if self.image_ids:
                self.output_map.extend(["image_ids"])
                self.output_fields.extend(["im_id"])
            self.output_fields.extend(
                ["im_shape", "scale_factor", "pad_gt_mask"])
        else:
            self.image_ids = True
            self.output_map = ["images", "ids"]
            self.output_fields = [
                "image",
                "im_id",
                "im_shape",
                "scale_factor",
            ]

    def parse_data(self, kind_item, anno_path_item, image_dir_item):
        if kind_item == self.kind_keys[0]:
            common_data_instance = WSMPDataConfig(
                anno_path=anno_path_item, image_dir=image_dir_item, mode=self.mode
            )
        elif kind_item == self.kind_keys[1]:
            common_data_instance = COCODataConfig(
                anno_path=anno_path_item, image_dir=image_dir_item, mode=self.mode
            )
        elif kind_item == self.kind_keys[2]:
            common_data_instance = CVATDataConfig(
                anno_path=anno_path_item, image_dir=image_dir_item, mode=self.mode
            )

        return common_data_instance

    def __len__(self):
        return self.length

    @pipeline_def(enable_conditionals=True)
    def build_pipeline(self, transforms: dict, shuffle=True):
        """
        > This function takes a dictionary of transforms and returns a pipeline of transforms

        :param transforms: a dictionary of transforms to apply to the data
        :type transforms: dict
        :param shuffle: Whether to shuffle the data, defaults to True (optional)
        """
        tensor_tuple = fn.readers.coco(
            file_root="",
            avoid_class_remapping=True,
            annotations_file=self.anno_path,
            image_ids=self.image_ids,
            pixelwise_masks=self.pixelwise_masks,
            polygon_masks=self.polygon_masks,
            skip_empty=self.skip_empty,
            shard_id=self.local_rank,
            num_shards=self.ranks,
            ratio=True,
            ltrb=True,
            random_shuffle=shuffle,
            name="Reader",
            pad_last_batch=True,
        )
        if self.mode != self.mode_keys[0]:
            tensor_tuple = (tensor_tuple[0], tensor_tuple[-1])
        return self._build_transforms(self.output_map, tensor_tuple, transforms)


class DALISemanticSegmentationDataset(DALIBaseMultiDataset):
    """
    基于DALI预处理加速的imagenet格式的数据集迭代器（用于训练）待完善

    Args:
        object (_type_): _description_
    """

    kind_keys = ["WSMP", "default"]

    def __init__(
            self, anno_path, mode="train", kind="default", image_dir="", categories=[]
    ) -> None:
        super().__init__(
            anno_path, mode=mode, kind=kind, image_dir=image_dir, categories=categories
        )
        self.output_map = ["images", "labels"]

        self.file_list, self.segm_list = anno_common2cityscape(
            self.common_data_instance)

    def parse_data(self, kind_item: str, anno_path_item: str):
        if kind_item == "WSMP":
            data = WSMPDataConfig(anno_path=anno_path_item)
        return data

    def __len__(self):
        return len(self.file_list)

    @pipeline_def
    def build_pipeline(self, transforms: dict, shuffle=True):
        images, _ = fn.readers.file(
            files=self.file_list,
            shard_id=self.local_rank,
            num_shards=self.ranks,
            random_shuffle=shuffle,
            name="Reader",
            seed=1,
        )
        labels, _ = fn.readers.file(
            files=self.segm_list,
            shard_id=self.local_rank,
            num_shards=self.ranks,
            random_shuffle=shuffle,
            name="ReaderLabel",
            seed=1,
        )
        return self._build_transforms(self.output_map, (images, labels), transforms)


class DALIValidateDataset(DALIBaseMultiDataset):
    """
    基于DALI预处理加速的数据集迭代器（用于验证或评估）

    :param anno_path: the path to the annotation file
    :type anno_path: str
    :param mode: 'single_val' or 'multi_val', defaults to single_val
    :type mode: str (optional)
    :param kind: 'default'('coco'), 'WSMP' or 'ImageNet', defaults to 'default'
    :type kind: str (optional)
    :param image_dir: the directory where the images are stored
    :type image_dir: str
    """

    kind_keys = ["WSMP", "default"]

    def __init__(
            self,
            anno_path: str,
            mode: str = "single_val",
            kind: str = "default",
            image_dir: str = "",
            allow_empty: bool = True,
            categories: list = [],
    ) -> None:
        super().__init__(
            anno_path, mode=mode, kind=kind, image_dir=image_dir, categories=categories
        )
        self.image_dir = image_dir
        self.anno_orig = anno_path
        self.mode = mode
        self.skip_empty = not allow_empty

        os.makedirs("tmp", exist_ok=True)
        self.anno_path = "tmp/validation.json"
        anno_common2coco(self.common_data_instance,
                         std_anno_path=self.anno_path)

        self.output_map = ["images", "ids"]
        self.output_fields = ["image", "im_id", "im_shape", "scale_factor"]
        if self.skip_empty:
            anno_image_ids = [
                anno["image_id"]
                for anno in self.common_data_instance.meta_data["annotations"]
            ]
            self.length = len(set(anno_image_ids))
        else:
            self.length = len(self.common_data_instance.meta_data["images"])

    def parse_data(self, anno_path_item, kind_item):
        if kind_item == self.kind_keys[0]:
            common_data_instance = WSMPDataConfig(
                anno_path_item, mode=self.mode)
        else:
            self.img_key = 0
            common_data_instance = ImagenetDataConfig(
                anno_path_item, mode=self.mode
            )
        return common_data_instance

    def __len__(self):
        return self.length

    @pipeline_def
    def build_pipeline(self, transforms: dict, shuffle=True):
        """
        > This function takes a dictionary of transforms and returns a pipeline of transforms

        :param transforms: a dictionary of transforms to apply to the data
        :type transforms: dict
        :param shuffle: Whether to shuffle the data, defaults to True (optional)
        """
        images, bboxes, labels, image_ids = fn.readers.coco(
            file_root="",
            avoid_class_remapping=True,
            annotations_file=self.anno_path,
            image_ids=True,
            pixelwise_masks=False,
            polygon_masks=False,
            skip_empty=self.skip_empty,
            shard_id=self.local_rank,
            num_shards=self.ranks,
            ratio=True,
            ltrb=True,
            random_shuffle=shuffle,
            name="Reader",
            pad_last_batch=True,
        )
        return self._build_transforms(self.output_map, (images, image_ids), transforms)


class DALIChangeDetectionDataset(DALIObjectDetectionDataset):
    """
    基于DALI预处理加速的COCO格式的数据集迭代器（用于训练）

    :param anno_path: path to the annotation file
    :type anno_path: str
    :param mode: 'train' or 'val', defaults to train
    :type mode: str (optional)
    :param kind: 'default'('coco') or 'WSMP', defaults to 'default'
    :type kind: str (optional)
    :param image_dir: The directory where the images are stored
    :type image_dir: str
    :param image_ids: If True, the dataset will return the image ids, defaults to False
    :type image_ids: bool (optional)
    :param polygons: If True, the polygons will be returned for instance segmentation task, defaults to False
    :type polygons: bool (optional)
    :param pixel_masks: If True, the dataset will return a pixel mask for instance segmentation, defaults to False
    :type pixel_masks: bool (optional)
    """

    kind_keys = ["WSMP", "COCO"]

    def __init__(
            self,
            dataset_uri: str = "",
            mode: str = "train",
            anno_path: str = "",
            image_dir: str = "",
            image_ids: bool = False,
            categories: list = [],
            kind: str = "COCO",
            allow_empty: bool = False,
            polygons: bool = False,
            pixel_masks: bool = False,
    ):
        super().__init__(
            dataset_uri,
            mode=mode,
            anno_path=anno_path,
            image_dir=image_dir,
            image_ids=image_ids,
            categories=categories,
            kind=kind,
            allow_empty=allow_empty,
            polygons=polygons,
            pixel_masks=pixel_masks,
            pad_last_batch=True,
        )

        self.template_anno_path = "tmp/anno_template_{}.json".format(self.mode)
        template_data = copy.deepcopy(self.common_data_instance)
        template_data.meta_data = self.common_data_instance.meta_data_template
        self.template_data = anno_common2coco(
            template_data, std_anno_path=self.template_anno_path
        )

    def set_output_fields(self):
        if self.mode == self.mode_keys[0]:
            self.output_map = ["images", "bboxes", "labels", "templates"]
            self.output_fields = ["image", "gt_bbox", "gt_class", "tmp_image"]
            if self.polygon_masks:
                self.output_map.extend(["polygons", "vertices"])
                self.output_fields.extend(["gt_poly", "gt_vertices"])
            if self.image_ids:
                self.output_map.extend(["image_ids"])
                self.output_fields.extend(["im_id"])
            self.output_fields.extend(
                ["im_shape", "scale_factor", "pad_gt_mask"])
        else:
            self.output_map = ["images", "ids", "templates"]
            self.output_fields = [
                "image",
                "im_id",
                "tmp_image",
                "im_shape",
                "scale_factor",
            ]

    def parse_data(self, kind_item, anno_path_item, image_dir_item):
        if kind_item == self.kind_keys[0]:
            common_data_instance = WSMPDataConfig(
                anno_path=anno_path_item, mode=self.mode
            )
        elif kind_item == self.kind_keys[1]:
            common_data_instance = ChangeDetectionDataConfig(
                anno_path=anno_path_item, image_dir=image_dir_item, mode=self.mode
            )

        return common_data_instance

    def rebuild_data(self, anno_path_item, common_data_instance):
        # 整合数据
        if type(self.common_data_instance) == DataConfig:
            self.common_data_instance = common_data_instance
            if len(self.categories) == 0:
                self.categories = [{"name": cate['name'], "id": cate['id']}
                                   for cate in self.common_data_instance.meta_data["categories"]]
                self.cname2clsid = {cate["name"]: cate["id"]
                                    for cate in self.categories}
        else:
            base_data = self.common_data_instance.meta_data
            cur_data = common_data_instance.meta_data

            newcatid2basecatid = self.get_catid_tranform(
                anno_path_item, cur_data)
            self.common_data_instance.meta_data = self.merge_history_data(
                base_data, cur_data, newcatid2basecatid
            )
            self.common_data_instance.meta_data_template = self.merge_history_data(
                self.common_data_instance.meta_data_template,
                common_data_instance.meta_data_template,
                newcatid2basecatid,
            )

    def __len__(self):
        return self.length

    @pipeline_def
    def build_pipeline(self, transforms: dict, shuffle=True):
        """
        > This function takes a dictionary of transforms and returns a pipeline of transforms

        :param transforms: a dictionary of transforms to apply to the data
        :type transforms: dict
        :param shuffle: Whether to shuffle the data, defaults to True (optional)
        """
        reader_seed = random.randint(0, 2 ** 32 - 1)
        images, bboxes, labels, image_ids = fn.readers.coco(
            file_root="",
            avoid_class_remapping=True,
            annotations_file=self.anno_path,
            image_ids=True,
            pixelwise_masks=self.pixelwise_masks,
            polygon_masks=self.polygon_masks,
            skip_empty=self.skip_empty,
            shard_id=self.local_rank,
            num_shards=self.ranks,
            ratio=True,
            ltrb=True,
            random_shuffle=shuffle,
            name="Reader",
            seed=reader_seed,
        )
        templates, _, _, temp_ids = fn.readers.coco(
            file_root="",
            avoid_class_remapping=True,
            annotations_file=self.template_anno_path,
            image_ids=True,
            pixelwise_masks=self.pixelwise_masks,
            polygon_masks=self.polygon_masks,
            skip_empty=self.skip_empty,
            shard_id=self.local_rank,
            num_shards=self.ranks,
            ratio=True,
            ltrb=True,
            random_shuffle=shuffle,
            name="Reader_template",
            seed=reader_seed,
        )
        if self.mode == self.mode_keys[0]:
            tensor_tuple = (images, bboxes, labels, templates)
        else:
            tensor_tuple = (images, image_ids, templates)
        return self._build_transforms(self.output_map, tensor_tuple, transforms)


class DALIAttrDataset(DALIBaseDataset):
    def __init__(self, dataset_uri="", mode="train", anno_path: str = "", image_dir: str = "",
                 categories=[], annotations=[], img_id2path={}):
        super().__init__(dataset_uri=dataset_uri, mode=mode,
                         anno_path=anno_path, image_dir=image_dir, categories=categories)
        self.get_meta_data(annotations, img_id2path)

    def get_meta_data(self, annotations, img_id2path):
        self.img_list = []
        self.label_list = []
        self.img_id_list = []
        for anno in annotations:
            if anno["image_id"] in img_id2path and anno["category_id"] in self.catid2clsid:
                self.img_list.append(img_id2path[anno["image_id"]])
                self.label_list.append(self.catid2clsid[anno["category_id"]])
                self.img_id_list.append(anno["image_id"])
        self._logger.info("AttrDataset len: {} cat: {}".format(len(self.img_list),
                                                               self.categories))

    def __len__(self):
        return len(self.images)

    def set_output_fields(self):
        if self.mode == self.mode_keys[0]:
            self.output_map = ["images", "labels"]
            self.output_fields = [0, 1, "im_shape", "scale_factor"]
        else:
            self.output_map = ["images", "ids"]
            self.output_fields = [0, "im_id", "im_shape", "scale_factor"]

    @pipeline_def(enable_conditionals=True)
    def build_pipeline(self, transforms: List[Dict], shuffle=True):
        if self.mode == self.mode_keys[0]:
            labels = self.label_list
        else:
            labels = self.img_id_list

        tensor_tuple = fn.readers.file(
            files=self.imgs,
            labels=labels,
            shard_id=self.local_rank,
            num_shards=self.ranks,
            random_shuffle=shuffle,
            name="Reader",
            pad_last_batch=True,
        )
        return self._build_transforms(self.output_map, tensor_tuple, transforms)


class DALIMultiAttrDataset(MultiDataset):
    kind = ["WSMP"]

    def __init__(self, dataset_uri="", mode="train", anno_path: str = "", image_dir: str = "", categories=[],
                 kind="WSMP", multi_heads=[]):
        super().__init__(dataset_uri=dataset_uri, mode=mode, anno_path=anno_path,
                         image_dir=image_dir, categories=categories, kind=kind)
        self.attr_datasets = []
        annotations_total = self.common_data_instance.meta_data["annotations"]
        img_id2path = get_id2path(self.common_data_instance.meta_data)
        for head in multi_heads:
            head_name = list(head.keys())[0]
            head_attrs = list(head.values())[0]
            head_attrs = set(attr.replace("|", "_") for attr in head_attrs)
            head_category = [
                cate for cate in self.categories if cate["name"] in head_attrs]

            self._logger.info(
                "Initialize AttrDataset for head: {}".format(head_name))
            self.attr_datasets.append(DALIAttrDataset(dataset_uri=self.dataset_uri,
                                                      mode="train",
                                                      anno_path=self.anno_path,
                                                      image_dir=image_dir,
                                                      categories=head_category,
                                                      annotations=annotations_total,
                                                      img_id2path=img_id2path))

    def __len__(self):
        return self.length

    def parse_data(self, kind_item: str, anno_path_item: str, image_dir_item):
        if kind_item == self.kind_keys[0]:
            common_data_instance = WSMPDataConfig(
                anno_path_item, image_dir=image_dir_item, mode=self.mode)
        return common_data_instance
