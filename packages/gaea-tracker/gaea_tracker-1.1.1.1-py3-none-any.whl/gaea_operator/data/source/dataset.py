#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : dataset.py
@Author        : yanxiaodong
@Date          : 2022/11/14
@Description   :
"""
import copy
import random
from abc import ABCMeta, abstractmethod
from typing import Dict, List
import os.path as osp
import numpy as np

from gaea_operator.utils import (
    MOUNT_PATH,
    CustomCOCO,
)

from .anno_parse import (
    DataConfig,
    COCODataConfig,
    CVATDataConfig,
    ImagenetDataConfig,
    WSMPDataConfig,
    CityscapesDataConfig,
    ChangeDetectionDataConfig,
    anno_common2cityscape,
    anno_common2coco,
    anno_common2imagenet,
    anno_common2imageonly,
    get_id2path,
    check_filepaths
)

from .base import Dataset, MultiDataset

try:
    from collections.abc import Sequence
except Exception:
    from collections import Sequence


class BaseDataset(Dataset, metaclass=ABCMeta):
    """
    An abstract class to encapsulate methods and behaviors of datasets.
    Args:
        kind: dataset source.
        mode: train or validation.
    """

    def __init__(
            self,
            dataset_uri: str,
            mode: str = "train",
            anno_path: str = "",
            image_dir: str = "",
            categories: list = [],
            **kwargs):
        super(BaseDataset, self).__init__(dataset_uri, mode=mode,
                                          anno_path=anno_path, image_dir=image_dir, categories=categories, **kwargs)

        self.transforms = []
        self.batch_transforms = []

    @abstractmethod
    def __getitem__(self, idx):
        """
        获取元素
        """
        pass

    def parse_dataset(self):
        """
        parse dataset
        """
        pass

    def set_transform(self, transforms: List[Dict], module):
        """
        set transform
        """
        for transform in transforms:
            for k, v in transform.items():
                op = getattr(module, k)(**v)
                self.transforms.append(op)

    def set_batch_transform(self, transforms: List[Dict], module):
        """
        set batch transform
        """
        for transform in transforms:
            for k, v in transform.items():
                op = getattr(module, k)(**v)
                self.batch_transforms.append(op)

    def _transform(self, data):
        for t in self.transforms:
            data = t(data)
        return data

    def set_kwargs(self, **kwargs):
        """
        set kwargs
        """
        pass


class BaseMultiDataset(BaseDataset, MultiDataset):
    """
    非DALI的多数据集基类
    """

    def __init__(
            self,
            dataset_uri: str,
            mode: str = "train",
            anno_path: str = "",
            image_dir: str = "",
            categories: list = [],
            kind: str = "",
            ratio: float = 0,
            common_data_instance: DataConfig = None
    ):
        super().__init__(dataset_uri, mode=mode, anno_path=anno_path,
                         image_dir=image_dir, categories=categories, kind=kind, ratio=ratio,
                         common_data_instance=common_data_instance)


class CityscapesDataset(BaseDataset):
    """
    非DALI的cityscapes格式的数据集迭代器
    """

    def __init__(self, dataset_uri: str = "", mode: str = "", anno_path: str = "", image_dir: str = "", categories: list = [], edge: str = False):
        super().__init__(osp.join(MOUNT_PATH, dataset_uri), mode=mode, anno_path=osp.join(MOUNT_PATH, anno_path),
                         image_dir=osp.join(MOUNT_PATH, image_dir), categories=categories)
        self.edge = edge
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

    def __getitem__(self, idx):
        data = {}
        data['trans_info'] = []
        image_path = self.image_paths[idx]
        label_path = self.label_path = self.label_paths[idx]
        data['img'] = image_path
        data['label'] = label_path
        # If key in gt_fields, the data[key] have transforms synchronous.
        data['gt_fields'] = []
        if self.mode == 'train':
            data['gt_fields'].append('label')
            data = self.transforms(data)
            if self.edge:
                import paddleseg.transforms.functional as F
                edge_mask = F.mask_to_binary_edge(
                    data['label'], radius=2, num_classes=self.num_classes)
                data['edge'] = edge_mask
        else:
            data = self.transforms(data)
            data['label'] = data['label'][np.newaxis, :, :]
        return data

    def __len__(self):
        return len(self.image_paths)

    def parse_dataset(self):
        pass


class ObjectDetectionDataset(BaseMultiDataset):
    """
    Image/ObjectDetection模型类别数据集迭代器，支持多数据集。

    :param anno_path: the path to the annotation file
    :type anno_path: str
    :param data_fields: the fields to be returned, including image, semantic, and label
    :type data_fields: list
    :param sample_num: the number of samples to be sampled from the dataset. If it is -1, all samples will be used
    :type sample_num: int
    :param use_default_label: If the label is not annotated, use the default label, defaults to False
    :type use_default_label: bool (optional)
    :param load_crowd: Whether to load the crowd annotation, defaults to False
    :type load_crowd: bool (optional)
    :param allow_empty: Whether to allow empty annotations, defaults to False
    :type allow_empty: bool (optional)
    :param empty_ratio: the ratio of empty images in the dataset
    :type empty_ratio: float
    :param repeat: the number of times to repeat the dataset, defaults to 1
    :type repeat: int (optional)
    :param kind: the type of annotation file, which can be "WSMP" or "default"("coco"), defaults to "default"
    :type kind: str (optional)
    :param mode: train or val, defaults to train
    :type mode: str (optional)
    :param image_dir: the path to the image directory
    :type image_dir: str
    """

    kind_keys = ["WSMP", "COCO", "CVAT"]

    def __init__(
            self,
            dataset_uri: str = "",
            mode: str = "train",
            anno_path: str = "",
            image_dir: str = "",
            categories: list = [],
            kind: str = "COCO",
            allow_empty: bool = False,
            data_fields: list = ["image"],
            sample_num: int = -1,
            use_default_label: bool = False,
            load_crowd: bool = False,
            empty_ratio: float = 1.0,
            repeat: int = 1,
            ratio: float = 0,
            common_data_instance: DataConfig = None
    ):
        super(ObjectDetectionDataset, self).__init__(
            dataset_uri=dataset_uri,
            mode=mode,
            anno_path=anno_path,
            image_dir=image_dir,
            categories=categories,
            kind=kind,
            ratio=ratio,
            common_data_instance=common_data_instance,
        )

        self.data_fields = data_fields
        self.sample_num = sample_num
        self.use_default_label = use_default_label
        self.repeat = repeat
        self.allow_empty = allow_empty
        self.load_crowd = load_crowd
        self.empty_ratio = empty_ratio
        self.skip_empty = not allow_empty

        self.data = anno_common2coco(self.common_data_instance)
        if mode == self.mode_keys[0]:
            self.load_image_only = False
        else:
            self.load_image_only = True
        self.load_semantic = False
        self._epoch = 0
        self._curr_iter = 0

        if self.skip_empty:
            anno_image_ids = [
                anno["image_id"]
                for anno in self.common_data_instance.meta_data["annotations"]
            ]
            anno_image_ids = set(anno_image_ids)
            images = []
            for img in self.data["images"]:
                if img["id"] in anno_image_ids:
                    images.append(img)
            self.data["images"] = images
            self.length = len(anno_image_ids)
        else:
            self.length = len(self.common_data_instance.meta_data["images"])

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

    def parse_dataset(self):
        """
        parse dataset
        """
        coco = CustomCOCO(self.data)

        img_ids = coco.getImgIds()
        img_ids.sort()
        records = []
        empty_records = []
        ct = 0

        if "annotations" not in coco.dataset:
            self.load_image_only = True
            self._logger.warning(
                "Annotation file: {} does not contains ground truth "
                "and load image information only.".format(self.anno_path)
            )

        for img_id in img_ids:
            coco_rec = self.parse_images(coco, img_id)
            if len(coco_rec) == 0:
                continue
            is_empty = False

            if not self.load_image_only:
                ins_anno_ids = coco.getAnnIds(
                    imgIds=[img_id], iscrowd=None if self.load_crowd else False
                )
                instances = coco.loadAnns(ins_anno_ids)

                bboxes = []
                is_rbox_anno = False
                for inst in instances:
                    # check gt bbox
                    if inst.get("ignore", False):
                        continue
                    if "bbox" not in inst.keys():
                        continue
                    else:
                        if not any(np.array(inst["bbox"])):
                            continue

                    # read rbox anno or not
                    is_rbox_anno = True if len(inst["bbox"]) == 5 else False
                    if is_rbox_anno:
                        xc, yc, box_w, box_h, angle = inst["bbox"]
                        x1 = xc - box_w / 2.0
                        y1 = yc - box_h / 2.0
                        x2 = x1 + box_w
                        y2 = y1 + box_h
                    else:
                        x1, y1, box_w, box_h = inst["bbox"]
                        x2 = x1 + box_w
                        y2 = y1 + box_h
                    eps = 1e-5
                    if inst["area"] > 0 and x2 - x1 > eps and y2 - y1 > eps:
                        inst["clean_bbox"] = [
                            round(float(x), 3) for x in [x1, y1, x2, y2]
                        ]
                        if is_rbox_anno:
                            inst["clean_rbox"] = [xc, yc, box_w, box_h, angle]
                        bboxes.append(inst)
                    else:
                        self._logger.warning(
                            "Found an invalid bbox in annotations: im_id: {}, "
                            "area: {} x1: {}, y1: {}, x2: {}, y2: {}.".format(
                                img_id, float(inst["area"]), x1, y1, x2, y2
                            )
                        )

                num_bbox = len(bboxes)
                if num_bbox <= 0 and not self.allow_empty:
                    continue
                elif num_bbox <= 0:
                    is_empty = True

                gt_bbox = np.zeros((num_bbox, 4), dtype=np.float32)
                if is_rbox_anno:
                    gt_rbox = np.zeros((num_bbox, 5), dtype=np.float32)
                gt_theta = np.zeros((num_bbox, 1), dtype=np.int32)
                gt_class = np.zeros((num_bbox, 1), dtype=np.int32)
                is_crowd = np.zeros((num_bbox, 1), dtype=np.int32)
                gt_poly = [None] * num_bbox

                has_segmentation = False
                for i, box in enumerate(bboxes):
                    catid = box["category_id"]
                    gt_class[i][0] = self.catid2clsid[catid]
                    gt_bbox[i, :] = box["clean_bbox"]
                    # xc, yc, w, h, theta
                    if is_rbox_anno:
                        gt_rbox[i, :] = box["clean_rbox"]
                    is_crowd[i][0] = box["iscrowd"]
                    # check RLE format
                    if "segmentation" in box and box["iscrowd"] == 1:
                        gt_poly[i] = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
                    elif "segmentation" in box and box["segmentation"]:
                        if (
                                not np.array(box["segmentation"]).size > 0
                                and not self.allow_empty
                        ):
                            bboxes.pop(i)
                            gt_poly.pop(i)
                            np.delete(is_crowd, i)
                            np.delete(gt_class, i)
                            np.delete(gt_bbox, i)
                        else:
                            gt_poly[i] = box["segmentation"]
                        has_segmentation = True

                if has_segmentation and not any(gt_poly) and not self.allow_empty:
                    continue

                if is_rbox_anno:
                    gt_rec = {
                        "is_crowd": is_crowd,
                        "gt_class": gt_class,
                        "gt_bbox": gt_bbox,
                        "gt_rbox": gt_rbox,
                        "gt_poly": gt_poly,
                    }
                else:
                    gt_rec = {
                        "is_crowd": is_crowd,
                        "gt_class": gt_class,
                        "gt_bbox": gt_bbox,
                        "gt_poly": gt_poly,
                    }

                for k, v in gt_rec.items():
                    if k in self.data_fields:
                        coco_rec[k] = v

            if is_empty:
                empty_records.append(coco_rec)
            else:
                records.append(coco_rec)
            ct += 1
            if self.sample_num > 0 and ct >= self.sample_num:
                break
        assert ct > 0, "not found any coco record in %s" % (self.anno_path)
        self._logger.debug("{} samples in file {}".format(ct, self.anno_path))
        if self.allow_empty and len(empty_records) > 0:
            empty_records = self._sample_empty(empty_records, len(records))
            records += empty_records
        self.roidbs = records

    def parse_images(self, coco, img_id):
        img_anno = coco.loadImgs([img_id])[0]
        im_path = img_anno["file_name"]
        # 平台传入的数据可能不包含width和height
        im_w, im_h = None, None
        if "width" in img_anno and "height" in img_anno:
            im_w = float(img_anno["width"])
            im_h = float(img_anno["height"])

        if im_w is not None and im_h is not None:
            if im_w < 0 or im_h < 0:
                self._logger.warning(
                    "Illegal width: {} or height: {} in annotation, "
                    "and im_id: {} will be ignored".format(im_w, im_h, img_id)
                )
                return im_path, {}

            coco_rec = (
                {
                    "im_file": im_path,
                    "im_id": np.array([img_id]),
                    "h": im_h,
                    "w": im_w,
                }
                if "image" in self.data_fields
                else {}
            )
        else:
            coco_rec = (
                {
                    "im_file": im_path,
                    "im_id": np.array([img_id]),
                }
                if "image" in self.data_fields
                else {}
            )
        self._logger.debug(
            "Load file: {}, im_id: {}, h: {}, w: {}.".format(
                im_path, img_id, im_h, im_w
            )
        )

        return coco_rec

    def __len__(self):
        return len(self.roidbs) * self.repeat

    def __call__(self, *args, **kwargs):
        return self

    def __getitem__(self, idx):
        n = len(self.roidbs)
        if self.repeat > 1:
            idx %= n
        # data batch
        roidb = copy.deepcopy(self.roidbs[idx])
        if self.mixup_epoch == 0 or self._epoch < self.mixup_epoch:
            idx = np.random.randint(n)
            roidb = [roidb, copy.deepcopy(self.roidbs[idx])]
        elif self.cutmix_epoch == 0 or self._epoch < self.cutmix_epoch:
            idx = np.random.randint(n)
            roidb = [roidb, copy.deepcopy(self.roidbs[idx])]
        elif self.mosaic_epoch == 0 or self._epoch < self.mosaic_epoch:
            roidb = [
                roidb,
            ] + [copy.deepcopy(self.roidbs[np.random.randint(n)]) for _ in range(4)]
        if isinstance(roidb, Sequence):
            for r in roidb:
                r["curr_iter"] = self._curr_iter
        else:
            roidb["curr_iter"] = self._curr_iter
        self._curr_iter += 1

        return self._transform(roidb)

    def set_kwargs(self, **kwargs):
        """
        set kwargs
        """
        self.mixup_epoch = kwargs.get("mixup_epoch", -1)
        self.cutmix_epoch = kwargs.get("cutmix_epoch", -1)
        self.mosaic_epoch = kwargs.get("mosaic_epoch", -1)

    def set_epoch(self, epoch_id):
        """
        set epoch
        """
        self._epoch = epoch_id

    def _sample_empty(self, records, num):
        # if empty_ratio is out of [0. ,1.), do not sample the records
        if self.empty_ratio < 0.0 or self.empty_ratio >= 1.0:
            return records

        sample_num = min(
            int(num * self.empty_ratio / (1 - self.empty_ratio)), len(records)
        )
        records = random.sample(records, sample_num)
        return records


class ClassficationDataset(BaseMultiDataset):
    """
    通用的imagenet格式的数据集迭代器（用于训练）

    Args:
        :param anno_path: the path to the annotation file
        :type anno_path: str
        :param kind: "default" or "coco", defaults to default
        :type kind: str (optional)
        :param mode: "train" or "val", defaults to train
        :type mode: str (optional)
        :param image_dir: the directory where the images are stored
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
            kind: str = "default",
    ):
        super(ClassficationDataset, self).__init__(
            dataset_uri=dataset_uri,
            mode=mode,
            anno_path=anno_path,
            image_dir=image_dir,
            categories=categories,
            kind=kind,
        )

        (
            self.imgs,
            self.labels,
            self.img_id_list,
        ) = anno_common2imagenet(self.common_data_instance)

        if mode == self.mode_keys[0]:
            self.load_image_only = False
        else:
            self.load_image_only = True

    def parse_data(self, kind_item, anno_path_item, image_dir_item):
        if kind_item == self.kind_keys[0]:
            common_data_instance = ImagenetDataConfig(
                anno_path_item, image_dir=image_dir_item, mode=self.mode)
        return common_data_instance

    def parse_dataset(self):
        """
        parse dataset
        """
        pass

    def set_kwargs(self, **kwargs):
        """
        set kwargs
        """
        pass

    def __getitem__(self, idx):
        try:
            with open(self.imgs[idx], "rb") as f:
                img = f.read()
            img = self._transform(img)

            img = img.transpose((2, 0, 1))
            if self.load_image_only:
                return {0: img, "im_id": self.img_id_list[idx]}
            else:
                return {0: img, 1: self.labels[idx], "im_id": self.img_id_list[idx]}
        except Exception as ex:
            self._logger.error(
                "Exception occured when parse line: {} with msg: {}".format(
                    self.imgs[idx], ex
                )
            )
            rnd_idx = np.random.randint(self.__len__())
            return self.__getitem__(rnd_idx)

    def __len__(self):
        return len(self.imgs)


class SemanticSegmentationDataset(BaseMultiDataset):
    """
    通用的cityscape格式的数据集迭代器（用于训练）待完善
    """

    kind_keys = ["Cityscapes"]

    def __init__(self,
                 dataset_uri: str = "",
                 mode: str = "",
                 anno_path: str = "",
                 image_dir: str = "",
                 categories: list = [],
                 kind="Cityscapes",
                 edge: str = False,
                 ratio: float = 0,
                 common_data_instance: DataConfig = None
                 ):
        super().__init__(dataset_uri, mode=mode, anno_path=anno_path, image_dir=image_dir, categories=categories,
                         kind=kind, ratio=ratio, common_data_instance=common_data_instance)

        self.edge = edge

        self.image_paths, self.label_paths = anno_common2cityscape(common_data=self.common_data_instance)

    def __getitem__(self, idx):
        try:
            data = {}
            data['trans_info'] = []
            image_path = self.image_paths[idx]
            label_path = self.label_path = self.label_paths[idx]
            data['img'] = image_path
            data['label'] = label_path
            # If key in gt_fields, the data[key] have transforms synchronous.
            data['gt_fields'] = []
            if self.mode == 'train':
                data['gt_fields'].append('label')
                data = self.transforms(data)
                if self.edge:
                    import paddleseg.transforms.functional as F
                    edge_mask = F.mask_to_binary_edge(
                        data['label'], radius=2, num_classes=self.num_classes)
                    data['edge'] = edge_mask
            else:
                data = self.transforms(data)
                data['label'] = data['label'][np.newaxis, :, :]
        except Exception as ex:
            self._logger.error(
                "Exception occured when parse line: {} with msg: {}".format(self.image_paths[idx], ex)
            )
            rnd_idx = np.random.randint(self.__len__())
            return self.__getitem__(rnd_idx)

        return data

    def __len__(self):
        return len(self.image_paths)

    def parse_data(self, kind_item, anno_path_item, image_dir_item):
        if kind_item == self.kind_keys[0]:
            common_data_instance = CityscapesDataConfig(
                anno_path=anno_path_item, image_dir=image_dir_item, mode=self.mode
            )

        return common_data_instance

    def parse_dataset(self):
        pass
            
            
class ValidateDataset(BaseMultiDataset):
    """ 
    deprecated
    通用的数据集迭代器（用于验证或评估），加载含有部分或者全部数据标注数据集.

    :param anno_path: the path to the annotation file
    :type anno_path: str
    :param kind: 'default' or 'coco', defaults to 'default'
    :type kind: str (optional)
    :param mode: 'single_val' or 'multi_val', defaults to single_val
    :type mode: str (optional)
    :param image_dir: the directory where the images are stored
    :type image_dir: str
    """

    kind_keys = ["WSMP", "default"]

    def __init__(
            self,
            anno_path: str,
            kind: str = "default",
            mode: str = "single_val",
            image_dir: str = "",
            allow_empty=True,
            categories: list = [],
    ):
        super(ValidateDataset, self).__init__(
            anno_path=anno_path,
            kind=kind,
            mode=mode,
            image_dir=image_dir,
            categories=categories,
        )

        self.images, self.catid2clsid, self.catid2cname = anno_common2imageonly(
            self.common_data_instance, allow_empty=allow_empty
        )
        self.clsid2catid = {v: k for k, v in self.catid2clsid.items()}

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

    def __getitem__(self, idx):
        img_meta = self.images[idx]

        with open(img_meta["file_name"], "rb") as f:
            img = f.read()
        img = self._transform(img)
        img = img.transpose((2, 0, 1))
        return {self.img_key: img, "im_id": img_meta["id"]}

    def __len__(self):
        return len(self.images)

    def parse_dataset(self):
        """
        parse dataset
        """
        pass

    def set_kwargs(self, **kwargs):
        """
        set kwargs
        """
        pass


class TestDataset(BaseMultiDataset):
    """
    支持只有图片路径传入的场景. 待完善
    """


class ChangeDetectionDataset(ObjectDetectionDataset):
    """
    变化检测的Dataset
    """

    kind_keys = ["WSMP", "COCO"]

    def __init__(
            self,
            dataset_uri: str = "",
            mode: str = "train",
            anno_path: str = "",
            image_dir: str = "",
            categories: list = [],
            kind: str = "COCO",
            allow_empty: bool = False,
            data_fields: list = ["image"],
            sample_num: int = -1,
            use_default_label: bool = False,
            load_crowd: bool = False,
            empty_ratio: float = 1.0,
            repeat: int = 1,
    ):
        super(ChangeDetectionDataset, self).__init__(
            dataset_uri=dataset_uri,
            mode=mode,
            anno_path=anno_path,
            image_dir=image_dir,
            categories=categories,
            kind=kind,
            allow_empty=allow_empty,
            data_fields=data_fields,
            sample_num=sample_num,
            use_default_label=use_default_label,
            load_crowd=load_crowd,
            empty_ratio=empty_ratio,
            repeat=repeat,
        )

        self.template_id2paths = get_id2path(
            self.common_data_instance.meta_data_template
        )

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
                self.categories = [{"name": cate['name'], "id": cate['id']} for cate in
                                   self.common_data_instance.meta_data["categories"]]
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

    def parse_images(self, coco, img_id):
        img_anno = coco.loadImgs([img_id])[0]
        im_path = img_anno["file_name"]
        template_path = self.template_id2paths[img_id]
        # 平台传入的数据可能不包含width和height
        im_w, im_h = None, None
        if "width" in img_anno and "height" in img_anno:
            im_w = float(img_anno["width"])
            im_h = float(img_anno["height"])

        if im_w is not None and im_h is not None:
            if im_w < 0 or im_h < 0:
                self._logger.warning(
                    "Illegal width: {} or height: {} in annotation, "
                    "and im_id: {} will be ignored".format(im_w, im_h, img_id)
                )
                return {}

            coco_rec = (
                {
                    "im_file": im_path,
                    "tmp_file": template_path,
                    "im_id": np.array([img_id]),
                    "h": im_h,
                    "w": im_w,
                }
                if "image" in self.data_fields
                else {}
            )
        else:
            coco_rec = (
                {
                    "im_file": im_path,
                    "tmp_file": template_path,
                    "im_id": np.array([img_id]),
                }
                if "image" in self.data_fields
                else {}
            )

        self._logger.debug(
            "Load file: {}, im_id: {}, h: {}, w: {}.".format(
                im_path, img_id, im_h, im_w
            )
        )

        return coco_rec
