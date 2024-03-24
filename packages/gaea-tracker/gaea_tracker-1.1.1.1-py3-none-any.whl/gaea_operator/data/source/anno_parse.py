#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : anno_parse.py
@Author        : yanxiaodong
@Date          : 2022/10/26
@Description   :
"""
import json
import os
from typing import Dict, List
import os.path as osp
from abc import abstractmethod
import copy
import random
import requests

from gaea_operator.utils import MOUNT_PATH, setup_logger, MASTER_RANK
import gaea_operator.distributed as idist

TRAIN = 'train'
VAL = 'validation'


class ExistSet():
    """
    判断文件是否存在
    """

    def __init__(self, dirs: list, prefix: str = ""):
        dirs = set([osp.join(prefix, dir) for dir in dirs])
        exist_file_names = []
        for dir in dirs:
            base_names = os.listdir(dir)
            full_names = [os.path.join(dir, name) for name in base_names]
            exist_file_names.extend(full_names)
        self.exist_file_names = set(exist_file_names)

    def exists(self, file):
        """
        判断文件是否在set里
        """
        return file in self.exist_file_names


class DataConfig(object):
    """
    将平台的数据格式转换为统一的数据格式

    Args:
        anno_path (str): 平台的数据文件
    """

    def __init__(self, anno_path, image_dir="", mode='train'):
        self.anno_path = anno_path
        self.image_dir = image_dir
        self.mode = mode
        self.samples = {}
        self.template_samples = {}

        self.meta_data = {"annotations": [], "images": [], "categories": []}
        self.val_meta_data = {"annotations": [], "images": [], "categories": []}

        self.meta_data_template = {
            "annotations": [], "images": [], "categories": []}
        self._logger = setup_logger(__name__ + "." + self.__class__.__name__)

        self.from_dict()

    def random_split(self, ratio: float = 0.2):
        """
        随机划分数据集
        """
        if ratio < 0 or ratio >= 1:
            raise ValueError("Validation ratio {} is not between 0 and 1".format(ratio))

        random.seed(0)

        image_list = []
        for img in self.meta_data["images"]:
            image_list.append(img["id"])

        train_meta_data = {"annotations": [], "images": [], "categories": []}
        val_meta_data = {"annotations": [], "images": [], "categories": []}
        subset_length = int(len(image_list) * ratio)

        val_list = random.sample(image_list, subset_length)
        val_set = set(val_list)

        for img in self.meta_data["images"]:
            if img["id"] in val_set:
                val_meta_data["images"].append(img)
            else:
                train_meta_data["images"].append(img)

        for ann in self.meta_data["annotations"]:
            if ann["image_id"] in val_set:
                val_meta_data["annotations"].append(ann)
            else:
                train_meta_data["annotations"].append(ann)

        train_meta_data["categories"] = self.meta_data["categories"]
        val_meta_data["categories"] = self.meta_data["categories"]

        self.meta_data = train_meta_data
        self.val_meta_data = val_meta_data

    @abstractmethod
    def from_dict(self):
        """
        解析平台数据
        """
        pass


def file_download(url: str, save_dir: str, exist_set: ExistSet, retry=6) -> str:
    """下载文件到指定目录

    Args:
        url (str): 文件的url地址
        save_dir (str): 保存目录
        retry (int, optional): 下载失败的重试次数. Defaults to 6.

    Returns:
        str: 本地的保存路径
    """
    save_path = osp.join(save_dir, osp.basename(url))
    for i in range(retry):
        if exist_set.exists(save_path):
            return save_path
        else:
            req = requests.get(url, stream=True)
            if req.ok:
                with open(save_path, "wb") as f:
                    f.write(req.content)
    return ""


def check_filepaths(filepaths: list, image_dir: str = "") -> list:
    """
    检查文件路径是否存在, 返回确实存在的文件路径
    """
    logger = setup_logger(__name__ + "." + "check_filepaths")
    prefix = osp.join(MOUNT_PATH, image_dir)
    dirs = [osp.dirname(filepath) for filepath in filepaths]
    exist_set = ExistSet(dirs, prefix)
    new_filepaths = []
    for file in filepaths:
        new_file = osp.join(prefix, file)
        if not exist_set.exists(new_file):
            logger.debug("file not exist: {}".format(file))
        else:
            new_filepaths.append(new_file)
    logger.info('there are {} images, and there are {} images not exsit'.format(
        len(filepaths), len(filepaths) - len(new_filepaths)))
    return new_filepaths


def get_id2path(data: Dict[str, List], image_dir: str = ""):
    """获得image的id到image文件路径的映射, 并对data的images字段规范化

    Args:
        data (_type_): _description_
        image_dir:
::
    Returns:
        _type_: _description_
    """
    logger = setup_logger(__name__ + "." + "get_id2path")
    img_id2path = {}
    images = []
    dirs = [osp.dirname(img['file_name']) for img in data["images"]]
    filename_set = ExistSet(dirs, prefix=image_dir)
    if len(data["images"]) > 0 and 'label_file' in data["images"][0]:
        label_dirs = [osp.dirname(img['label_file']) for img in data["images"]]
        label_filename_set = ExistSet(label_dirs, prefix=image_dir)
    for img in data["images"]:
        img["file_name"] = osp.join(image_dir, img["file_name"])
        if img["file_name"] != "" and filename_set.exists(img["file_name"]):
            if 'label_file' in img:
                img['label_file'] = osp.join(image_dir, img["label_file"])
                if img["label_file"] != "" and label_filename_set.exists(img["label_file"]):
                    images.append(img)
                    img_id2path[img["id"]] = img["file_name"]
            else:
                images.append(img)
                img_id2path[img["id"]] = img["file_name"]
        else:
            logger.debug(f'image: {img["file_name"]} is not exist!')
    logger.info('there are {} images, and there are {} images not exsit'.format(
        len(data["images"]), len(data["images"]) - len(img_id2path)))
    data["images"] = images
    return img_id2path


def get_catid2clsid(data: dict, preserve_background=False):
    """
    根据type获得对应的数据, 并且计算catid2clsid

    Args:
        data (_type_): _description_
    """

    catid2clsid = {}
    for clsid, cate in enumerate(data["categories"]):
        if preserve_background:
            catid2clsid[cate["id"]] = clsid + 1
        else:
            catid2clsid[cate["id"]] = clsid
    return catid2clsid


def anno_common2coco(common_data: DataConfig, std_anno_path: str = "", image_dir: str = ""):
    """
    把统一格式转换为coco格式

    Args:
        common_data (DataConfig): 统一的数据对象
        std_anno_path (str, optional): 保存的路径，如果指定，即会在该路径保存转化后的文件. Defaults to "".
        type (str, optional): ['train', 'val']. Defaults to "train".
        image_dir: 文件路径

    Returns:
        _type_: _description_
    """
    data = common_data.meta_data
    catid2clsid = get_catid2clsid(data)

    img_id2path = get_id2path(data, image_dir=image_dir)

    annotations = []
    filtered_nums = 0
    _logger = setup_logger(__name__+"."+"anno_common2coco")
    for anno in data["annotations"]:
        if anno["image_id"] in img_id2path and anno["category_id"] in catid2clsid:
            annotations.append(anno)
        else:
            filtered_nums += 1
    _logger.info("filtered invalid {} annotations".format(filtered_nums))
    data["annotations"] = annotations

    if std_anno_path != "":
        data = copy.deepcopy(data)
        for anno in data['annotations']:
            anno['category_id'] = catid2clsid[anno['category_id']]
        if idist.get_world_size() > 1:
            idist.barrier()
        if idist.get_rank() == MASTER_RANK:
            with open(std_anno_path, "w") as f:
                json.dump(data, f)
        if idist.get_world_size() > 1:
            idist.barrier()

    return data


def anno_common2imagenet(common_data: DataConfig, image_dir: str = ""):
    """
    将平台格式转换为分类的数据集的标准格式

    Args:
        common_data: 统一的数据对象
        image_dir: image dir, when mode is default, need image dir.
    """
    data = common_data.meta_data
    catid2clsid = get_catid2clsid(data)

    img_id2path = get_id2path(data, image_dir=image_dir)

    img_list = []
    label_list = []
    img_id_list = []
    for anno in data["annotations"]:
        if anno["image_id"] in img_id2path and anno["category_id"] in catid2clsid:
            img_id_list.append(anno["image_id"])
            img_list.append(img_id2path[anno["image_id"]])
            label_list.append(catid2clsid[anno["category_id"]])

    return img_list, label_list, img_id_list


def anno_common2imageonly(common_data: DataConfig, image_dir: str = "", allow_empty=True):
    """将统一格式转化为仅有图像格式

    Args:
        common_data (DataConfig): _description_
    """
    data = common_data.meta_data
    catid2clsid = get_catid2clsid(data)
    catid2cname = {cate['id']: cate['name'] for cate in data["categories"]}

    image_ids_valid = set()
    for anno in data["annotations"]:
        if anno['image_id'] not in image_ids_valid:
            image_ids_valid.add(anno['image_id'])
    get_id2path(data, image_dir=image_dir)

    if not allow_empty:
        images = []
        for img in data["images"]:
            if img['id'] in image_ids_valid:
                images.append(img)
        data['images'] = images

    return data['images'], catid2clsid, catid2cname


def anno_common2cityscape(common_data: DataConfig):
    """将平台格式转换为语义分割数据集的标准格式

    Args:
        common_data (DataConfig): 统一的数据对象
        type (str, optional): _description_. Defaults to 'train'.

    Returns:
        _type_: _description_
    """
    data = common_data.meta_data

    img_id2path = get_id2path(data)

    img_list = []
    label_list = []
    for anno in data["annotations"]:
        if anno["image_id"] in img_id2path:
            img_list.append(img_id2path[anno["image_id"]])
            label_list.append(anno["segmentation"])

    return img_list, label_list


class WSMPDataConfig(DataConfig):
    """
    Load wsmp dataset to common dataset.
    Args:
        anno_path (str): annotation file path.
    """
    keys = {"train": 'train', "validation": 'validation', "test": "validation"}

    def __init__(self, anno_path: str, image_dir="", mode='train'):
        super().__init__(anno_path, image_dir=image_dir, mode=mode)

    def from_dict(self):
        """
        参数解析，转换为对象变量
        """
        if osp.isdir(self.anno_path):
            self.anno_path = osp.join(self.anno_path, "annotation.json")
        assert os.path.exists(self.anno_path), (
            "invalid coco annotation file: " + self.anno_path
        )
        assert self.anno_path.endswith(".json"), (
            "invalid coco annotation file: " + self.anno_path
        )

        meta_data = json.load(open(self.anno_path, "r"))
        _anno_content = meta_data.get("annotations", [])
        if not _anno_content:
            _anno_content = {}
        _sample_list = meta_data.get("images", [])
        _categories = meta_data.get("categories", [])
        _templates = meta_data.get("templates", [])
        if _templates is None:
            _templates = []
        if _categories is None:
            _categories = []
        for c in _categories:
            if "id" in c:
                c["id"] = int(c["id"])
                self.meta_data["categories"].append(c)
        for s in _sample_list:
            _type = s.pop("type", self.keys["train"])
            _type = self.keys[_type]
            if "id" in s:
                s["id"] = int(s["id"])
            _id = s.get("id", 0)
            s["file_name"] = osp.join(self.image_dir, s["file_name"])
            if _type == self.keys[self.mode]:
                self.samples[_id] = 1
                self.meta_data["images"].append(s)

        for _tem in _templates:
            if "id" in _tem:
                _tem["id"] = int(_tem["id"])
            _tem["file_name"] = osp.join(self.image_dir, _tem["file_name"])

            _id = _tem.get("id", 0)
            if not (_id in self.samples):
                self._logger.warning(
                    "template id {} not in train or validation ids".format(
                        _tem["id"])
                )
                continue
            self.template_samples[_id] = 1
            self.meta_data_template["images"].append(_tem)

        for ann in _anno_content:
            if "category_id" in ann:
                ann["category_id"] = int(ann["category_id"])
            if "image_id" in ann:
                ann["image_id"] = int(ann["image_id"])
            if "iscrowd" not in ann:
                ann["iscrowd"] = 0
            if ann["image_id"] in self.samples:
                self.meta_data["annotations"].append(ann)


class COCODataConfig(DataConfig):
    """Load standard COCO dataset

    Args:
        DataConfig (_type_): _description_
    """

    def __init__(self, anno_path: str, image_dir="", mode='train'):
        super().__init__(anno_path, image_dir=image_dir, mode=mode)

    def from_dict(self):
        """
        参数解析，转换为对象变量
        """
        files = ["annotation.json", "annotations"]
        anno_path = self.anno_path

        if osp.isdir(self.anno_path):
            for file in os.listdir(self.anno_path):
                if file == files[0]:
                    anno_path = osp.join(self.anno_path, file)
                    if osp.exists(osp.join(self.anno_path, "images")):
                        self.image_dir = osp.join(self.image_dir, "images")
                    else:
                        self.image_dir = ""
                    break
                elif file == files[1]:
                    anno_path = osp.join(self.anno_path, "annotations", self.mode + ".json")
                    self.image_dir = osp.join(self.image_dir, "images", self.mode)
                    break
                else:
                    pass

        self.anno_path = anno_path
        assert os.path.exists(self.anno_path), (
            "invalid coco annotation file: " + self.anno_path
        )
        assert self.anno_path.endswith(".json"), (
            "invalid coco annotation file: " + self.anno_path
        )
        with open(self.anno_path) as f:
            data = json.load(f)

        fs_endpoint = os.environ.get("FS_ENDPOINT", None)
        # 拼接路径
        for img in data["images"]:
            if fs_endpoint is not None and img["file_name"].startswith(fs_endpoint):
                img["file_name"] = img["file_name"].replace(fs_endpoint, "")
                img["file_name"] = os.path.join(MOUNT_PATH, img["file_name"])
            else:
                img["file_name"] = osp.join(self.image_dir, img["file_name"])

        self.meta_data = data


class CVATDataConfig(DataConfig):
    """Load standard COCO dataset

    Args:
        DataConfig (_type_): _description_
    """

    def __init__(self, anno_path: str, image_dir="", mode='train'):
        super().__init__(anno_path, image_dir=image_dir, mode=mode)

    def from_dict(self):
        """
        参数解析，转换为对象变量
        """
        if osp.isdir(self.anno_path):
            self.anno_path = osp.join(
                self.anno_path, self.mode + ".json")

        assert os.path.exists(self.anno_path), (
            "invalid coco annotation file: " + self.anno_path
        )
        assert self.anno_path.endswith(".json"), (
            "invalid coco annotation file: " + self.anno_path
        )
        with open(self.anno_path) as f:
            data = json.load(f)

        # 拼接路径
        for img in data["images"]:
            img["file_name"] = osp.join(self.image_dir, img["file_name"])

        self.meta_data = data
        
        
class ImagenetDataConfig(DataConfig):
    """
    Load Standart Imagenet dataset

    Args:
        DataConfig (_type_): _description_
    """

    def __init__(self, anno_path, image_dir="", mode='train'):
        super().__init__(anno_path, image_dir=image_dir, mode=mode)

    def from_dict(self):
        """
        参数解析，转换为对象变量
        """
        files = ["annotation.txt", self.mode + ".txt"]
        if osp.isdir(self.anno_path):
            for file in os.listdir(self.anno_path):
                if file in files:
                    self.anno_path = osp.join(self.anno_path, file)
                    break
        assert os.path.exists(self.anno_path), ("invalid coco annotation file: " + self.anno_path)

        assert self.anno_path.endswith(".txt"), (
            "invalid ImageNet annotation file: " + self.anno_path
        )
        with open(self.anno_path) as f:
            data = f.readlines()

        image_paths = [s.split("\n")[0].rsplit(" ", 1)[0] for s in data]
        label_names = [s.split("\n")[0].rsplit(" ", 1)[1] for s in data]

        cate_names = sorted(set(label_names))
        catname2catid = {}
        for idx, cate_name in enumerate(cate_names):
            self.meta_data['categories'].append({'id': idx, 'name': cate_name})
            catname2catid[cate_name] = idx

        fs_endpoint = os.environ.get("FS_ENDPOINT", None)
        for idx, (img_path, label_name) in enumerate(zip(image_paths, label_names)):
            if fs_endpoint is not None and img_path.startswith(fs_endpoint):
                self.image_dir = ""
                img_path = img_path.replace(fs_endpoint, "")
                img_path = os.path.join(MOUNT_PATH, img_path)
            self.meta_data['images'].append(
                {'id': idx, 'file_name': osp.join(self.image_dir, img_path)})
            self.meta_data['annotations'].append(
                {'id': idx, 'image_id': idx, 'category_id': catname2catid[label_name]})


class ChangeDetectionDataConfig(COCODataConfig):
    """
    Load standard change detection dataset
    """

    def __init__(self, anno_path, image_dir="", mode='train'):
        super().__init__(anno_path, image_dir=image_dir, mode=mode)

    def from_dict(self):
        """
        参数解析，转换为对象变量
        """
        super(ChangeDetectionDataConfig, self).from_dict()
        template_images = []
        for img in self.meta_data['images']:
            temp_img = copy.deepcopy(img)
            temp_img['file_name'] = osp.join(
                self.image_dir, temp_img.pop("template_name"))
            template_images.append(temp_img)
        self.meta_data_template = {"annotations": self.meta_data["annotations"],
                                   "images": template_images,
                                   "categories": self.meta_data["categories"]}


class CityscapesDataConfig(DataConfig):
    """
    Load standard change detection dataset
    """

    def __init__(self, anno_path, image_dir="", mode='train'):
        super().__init__(anno_path, image_dir=image_dir, mode=mode)

    def from_dict(self):
        """
        参数解析，转换为对象变量
        """
        with open(osp.join(self.anno_path, "labels.txt")) as f:
            catenames = f.read()
        catenames = catenames.strip("\n").split("\n")
        categories = [{"name": name, "id": id} for id, name in enumerate(catenames)]
        self.meta_data['categories'] = categories

        files = ["annotation.txt", self.mode + ".txt"]
        if osp.isdir(self.anno_path):
            for file in os.listdir(self.anno_path):
                if file in files:
                    self.anno_path = osp.join(self.anno_path, file)
                    break
        assert os.path.exists(self.anno_path), ("invalid cityscape annotation file: " + self.anno_path)

        assert self.anno_path.endswith(".txt"), (
                "invalid ImageNet annotation file: " + self.anno_path
        )

        with open(self.anno_path) as f:
            data = f.readlines()

        image_paths = [s.split("\n")[0].rsplit(" ", 1)[0] for s in data]
        label_names = [s.split("\n")[0].rsplit(" ", 1)[1] for s in data]

        fs_endpoint = os.environ.get("FS_ENDPOINT", None)

        for idx, (img_path, label_name) in enumerate(zip(image_paths, label_names)):
            if fs_endpoint is not None and img_path.startswith(fs_endpoint):
                self.image_dir = ""
                img_path = img_path.replace(fs_endpoint, "")
                img_path = os.path.join(MOUNT_PATH, img_path)
                label_name = label_name.replace(fs_endpoint, "")
                label_name = os.path.join(MOUNT_PATH, label_name)
            self.meta_data['images'].append(
                {'id': idx,
                 'file_name': osp.join(self.image_dir, img_path),
                 'label_file': osp.join(self.image_dir, label_name)})
            self.meta_data['annotations'].append(
                {'id': idx, 'image_id': idx, 'segmentation': osp.join(self.image_dir, label_name), 'category_id': 0})

