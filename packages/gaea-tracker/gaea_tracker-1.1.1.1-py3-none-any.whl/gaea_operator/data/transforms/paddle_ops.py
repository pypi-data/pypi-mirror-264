#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : tensor_operators.py
@Author        : xuningyuan
@Date          : 2022/09/09
@Description   :
"""
import logging
import random
from numbers import Number
from typing import Union

from gaea_operator.plugin import paddle, Layer, F

from .paddle_fns import resize

try:
    from collections.abc import Sequence
except Exception:
    from collections import Sequence




pi = 3.141592653589793


class ToTensor(Layer):
    """
    转化为标准的NHWC布局的paddle张量
    """

    def __init__(self, precision=32):
        super(ToTensor, self).__init__()
        if precision == 16:
            self.dtype = paddle.float16
        else:
            self.dtype = paddle.float32

    def forward(self, array_dict: dict):
        tensor_dict = {}
        tensor_dict['img'] = paddle.to_tensor(array_dict['img'], self.dtype)
        tensor_dict['img'] = paddle.unsqueeze(tensor_dict['img'], 0)
        if 'label' in array_dict:
            tensor_dict['label'] = paddle.to_tensor(array_dict['label'], paddle.int64)
        if 'bbox' in array_dict:
            tensor_dict['bbox'] = paddle.to_tensor(array_dict['bbox'], paddle.int64)
        if 'mask' in array_dict:
            tensor_dict['mask'] = paddle.to_tensor(array_dict['mask'], self.dtype)
            tensor_dict['mask'] = paddle.unsqueeze(tensor_dict['mask'], 0)
        return tensor_dict


class ToGpu(Layer):
    """
    将张量都传输到gpu上
    """

    def __init__(self):
        super(ToGpu, self).__init__()

    def forward(self, tensor_dict):
        for key in tensor_dict:
            tensor_dict[key] = tensor_dict[key].cuda()
        return tensor_dict


class Resize(Layer):
    """
    将输入张量缩放到目标大小.
    """

    def __init__(self, target_size: Union[tuple, list, int], keep_ratio: bool, interp="bilinear"):
        """
        获取目标大小和 是否保持长宽比
        """
        super(Resize, self).__init__()
        self.target_size = target_size
        self.keep_ratio = keep_ratio
        self.interp = interp
        if self.keep_ratio:
            self._forward = self.forward_keep_ratio
        else:
            self._forward = self.forward_direct

    def forward_keep_ratio(self, tensor_dict: dict):
        """
        按比例缩放
        """
        n, c, h, w = tensor_dict['img'].shape
        factor = min(self.target_size[0] / h, self.target_size[1] / w)
        tensor_dict['img'] = F.interpolate(tensor_dict['img'], scale_factor=factor)
        return tensor_dict

    def forward_direct(self, tensor_dict: dict):
        """
        直接缩放到目标大小
        """
        tensor_dict['img'] = F.interpolate(tensor_dict['img'], self.target_size, mode=self.interp)
        return tensor_dict

    def forward(self, tensor_dict: dict):
        """
        将输入的张量中的图像缩放到目标大小
        """
        return self._forward(tensor_dict)


class NormalizeImage(Layer):
    """
    将图像进行归一化

    This object normalize the images

    :param mean: the mean of the image
    :param std: the standard deviation of the dataset
    :param is_scale: whether to scale the image to [0, 1], defaults to True (optional)
    """

    def __init__(self, mean=[0.485, 0.456, 0.406], std=[1, 1, 1], is_scale=True):

        super(NormalizeImage, self).__init__()
        if any(std) == 0:
            raise ValueError('{}: std is invalid!'.format(self))

        self.mean = paddle.to_tensor(mean)
        self.mean = paddle.reshape(self.mean, (1, -1, 1, 1))
        self.std = paddle.to_tensor(std)
        self.std = paddle.reshape(self.std, (1, -1, 1, 1))
        if is_scale:
            self.mean = 255 * self.mean
            self.std = 255 * self.std

    def forward(self, tensor_dict: dict):
        tensor_dict['img'] = tensor_dict['img'] - self.mean
        tensor_dict['img'] = tensor_dict['img'] / self.std
        return tensor_dict


class Permute(Layer):
    """
    HWC2CHW
    """

    def __init__(self):
        super(Permute, self).__init__()

    def forward(self, tensor_dict: dict):
        tensor_dict['img'] = paddle.transpose(tensor_dict['img'], (0, 3, 1, 2))
        if 'mask' in tensor_dict:
            tensor_dict['mask'] = paddle.transpose(tensor_dict['img'], (0, 3, 1, 2))
        return tensor_dict


class RandomResize(Layer):
    """
    随机裁剪

    This object takes in a list of target sizes, a boolean value for whether to keep the ratio, a string for the
    interpolation method, a boolean value for whether to use a random size, and a boolean value for whether to use a
    random interpolation method

    :param target_size: the size of the output image
    :type target_size: list
    :param keep_ratio: whether to keep the aspect ratio of the image, defaults to True (optional)
    :param interp: interpolation method, can be 'bilinear' or 'nearest', defaults to bilinear (optional)
    :param random_size: whether to randomly resize the image, defaults to True (optional)
    :param random_interp: whether to randomly choose an interpolation method from the following:, defaults to False
    (optional)
    """

    def __init__(self,
                 target_size: list,
                 keep_ratio=True,
                 interp='bilinear',
                 random_size=True,
                 random_interp=False):
        super(RandomResize, self).__init__()
        self.interps = ['linear', 'bilinear', 'trilinear', 'nearest', 'bicubic', 'area']
        assert interp in self.interps, "interp must be one of {}, however it is {}".format(self.interps, interp)
        self.interp = interp

        self.target_size = target_size
        self.keep_ratio = keep_ratio
        self.random_size = random_size
        self.random_interp = random_interp

    def forward(self, tensor_dict):
        if self.random_size:
            target_size = self.target_size[paddle.randint(high=len(self.target_size))]
        else:
            target_size = self.target_size[0]

        if self.random_interp:
            interp = self.interps[paddle.randint(high=len(self.target_size))]
        else:
            interp = self.interp

        return resize(tensor_dict, target_size, keep_ratio=self.keep_ratio, interp=interp)


class RandomFlip(Layer):
    """
    随机翻转

    :param prob: the probability of the image being flipped
    :param horizontal: whether to flip horizontally, defaults to True (optional)
    :param vertical: whether to do vertical flip, defaults to False (optional)
    :param depthwise: whether to use depthwise convolution, defaults to False (optional)
    :param ltrb: left-to-right, top-to-bottom, defaults to True (optional)
    :param layout: the layout of the input tensor. 'CHW' means the input tensor is in the format of (channel, height,
    width). 'HWC' means the input tensor is in the format of (height, width, channel), defaults to CHW (optional)
    """

    def __init__(self, prob=0.5, horizontal=True, vertical=False, depthwise=False, ltrb=True, layout='CHW'):
        super(RandomFlip, self).__init__()
        self.prob = prob
        self.horizontal = horizontal
        self.vertical = vertical
        self.depthwise = depthwise
        self.ltrb = ltrb
        self.layout = layout

    def apply_bbox(self, bboxes, hori, vert):
        """
        It takes a list of bounding boxes and returns a list of bounding boxes that have been flipped by the specified
        parameters

        :param bboxes: the bounding boxes to be applied
        :param hori: horizontal offset
        :param vert: vertical offset
        """
        if self.ltrb:
            if hori:
                for bbox in bboxes:
                    bbox[0] = 1 - bbox[0]
                    bbox[2] = 1 - bbox[2]
            if vert:
                for bbox in bboxes:
                    bbox[1] = 1 - bbox[1]
                    bbox[3] = 1 - bbox[3]
        else:
            if hori:
                for bbox in bboxes:
                    bbox[0] = 1 - bbox[0]
            if vert:
                for bbox in bboxes:
                    bbox[1] = 1 - bbox[1]
        return bboxes

    def apply_image(self, img, hori, vert, dept):
        """
        It flips an image

        :param img: the image to be applied
        :param hori: horizontal shift
        :param vert: vertical shift
        :param dept: depth of the image
        """
        if self.layout == 'CHW':
            if hori:
                img = img[:, :, ::-1]
            if vert:
                img = img[:, ::-1, :]
            if dept:
                img = img[::-1, :, :]
        return img

    def forward(self, tensor_dict) -> dict:
        if self.horizontal:
            hori = paddle.rand([1]) < self.prob
        else:
            hori = False
        if self.vertical:
            vert = paddle.rand([1]) < self.prob
        else:
            vert = False
        if self.depthwise:
            dept = paddle.rand([1]) < self.prob
        else:
            dept = False

        tensor_dict['img'] = self.apply_image(tensor_dict['img'], hori=hori, vert=vert, dept=dept)
        if 'bbox' in tensor_dict:
            tensor_dict['bbox'] = self.apply_bbox(tensor_dict['bbox'], hori=hori, vert=vert)
        if 'semantic' in tensor_dict:
            tensor_dict['semantic'] = self.apply_image(tensor_dict['semantic'], hori=hori, vert=vert, dept=False)
        return tensor_dict


class RandomDistort(Layer):
    """
    随机扭曲

    This object takes in a list of parameters and returns a list of augmented images

    :param hue: the range of hue values to randomly select from
    :param saturation: The saturation factor
    :param contrast: [0.5, 1.5, 0.5]
    :param brightness: [min, max, step]
    :param random_apply: Whether to apply the transform with a probability of 0.5, defaults to True (optional)
    :param count: number of augmentations to apply, defaults to 4 (optional)
    """

    def __init__(self,
                 hue=[-18, 18, 0.5],
                 saturation=[0.5, 1.5, 0.5],
                 contrast=[0.5, 1.5, 0.5],
                 brightness=[0.5, 1.5, 0.5],
                 random_apply=True,
                 count=4):
        super(RandomDistort, self).__init__()
        self.hue = hue
        self.saturation = saturation
        self.contrast = contrast
        self.brightness = brightness
        self.random_apply = random_apply
        self.count = count

    def apply_hue(self, img, low, high):
        """
        It takes an image, and a low and high saturation value, and returns a new image with the hue adjusted

        :param img: The image to be modified
        :param low: The lower bound of the hue range
        :param high: The maximum hue value to use
        """
        # it works, but result differ from HSV version
        delta = paddle.uniform(low, high)
        u = paddle.cos(delta * pi)
        w = paddle.sin(delta * pi)
        bt = paddle.to_tensor([[1.0, 0.0, 0.0], [0.0, u, -w], [0.0, w, u]])
        tyiq = paddle.to_tensor([[0.299, 0.587, 0.114], [0.596, -0.274, -0.321],
                                 [0.211, -0.523, 0.311]])
        ityiq = paddle.to_tensor([[1.0, 0.956, 0.621], [1.0, -0.272, -0.647],
                                  [1.0, -1.107, 1.705]])
        t = paddle.dot(paddle.dot(ityiq, bt), tyiq).T
        img = paddle.dot(img, t)
        return img

    def apply_saturation(self, img, low, high):
        """
        It takes an image, and a low and high saturation value, and returns a new image with the saturation adjusted

        :param img: The image to be modified
        :param low: The minimum value of the saturation range
        :param high: the maximum saturation value
        """
        delta = paddle.uniform(low, high)
        # it works, but result differ from HSV version
        gray = img * paddle.to_tensor([[[0.299, 0.587, 0.114]]], dtype=paddle.float32)
        gray = gray.sum(axis=2, keepdims=True)
        gray *= (1.0 - delta)
        img *= delta
        img += gray
        return img

    def apply_contrast(self, img, low, high):
        """
        It takes an image, and returns a new image with the contrast adjusted

        :param img: The image to be processed
        :param low: the minimum value of the contrast
        :param high: the maximum value of the output image
        """
        delta = paddle.uniform(low, high)
        img *= delta
        return img

    def apply_brightness(self, img, low, high):
        """
        It takes an image, and applies a random brightness to it

        :param img: The image to be modified
        :param low: the minimum brightness value
        :param high: The maximum brightness value to apply
        """
        delta = paddle.uniform(low, high)
        img += delta
        return img

    def forward(self, tensor_dict: dict):

        funcs = [self.apply_hue, self.apply_saturation,
                 self.apply_contrast, self.apply_brightness]
        params = [self.hue, self.saturation,
                  self.contrast, self.brightness]

        if self.random_apply:
            orders = paddle.randperm(4)
        else:
            orders = [0, 1, 2, 3]

        for order in orders:
            low, high, prob = params[order]
            if paddle.rand([1]) < prob:
                tensor_dict['img'] = funcs[order](tensor_dict['img'], low, high)
        return tensor_dict


class RandomExpand(Layer):
    """
    随机填充图像到一个更大到画布

    This object takes in a ratio, probability, and fill value and returns a random crop of the image

    :param ratio: the ratio of the image to be cropped
    :param prob: The probability of applying the transform
    :param fill_value: the value to fill the image with after the crop
    """

    def __init__(self, ratio=4., prob=0.5, fill_value=(127.5, 127.5, 127.5)):

        super(RandomExpand, self).__init__()
        assert ratio > 1.01, "expand ratio must be larger than 1.01"
        self.ratio = ratio
        self.prob = prob
        assert isinstance(fill_value, (Number, Sequence)), \
            "fill value must be either float or sequence"
        if isinstance(fill_value, Number):
            fill_value = (fill_value,) * 3
        if not isinstance(fill_value, tuple):
            fill_value = tuple(fill_value)
        self.fill_value = fill_value

    def forward(self, tensor_dict):
        if paddle.rand([1]) < self.prob:
            ratio = paddle.uniform([1], min=1, max=self.ratio)
            cur_h, cur_w, _ = tensor_dict['img'].shape
            h = (cur_h * ratio).astype(paddle.int64)
            w = (cur_w * ratio).astype(paddle.int64)
            if h > cur_h and w > cur_w:
                y = paddle.randint(0, h - cur_h)
                x = paddle.randint(0, w - cur_w)
                tensor_dict['img'] = F.pad(tensor_dict['img'], (x, w, y, h))

        return tensor_dict


class RandomCrop(Layer):
    """
    随机裁剪

    This object takes in a list of aspect ratios, a list of thresholds, a list of scaling factors, and a number of
    attempts, and returns a list of bounding boxes

    :param aspect_ratio: The list of aspect ratios for the crops
    :param thresholds: the IoU thresholds to use when computing the loss
    :param scaling: The scaling factor for the size of the smallest side of the image
    :param num_attempts: number of attempts at generating a cropped region of the image, defaults to 50 (optional)
    :param allow_no_crop: If True, then we allow the possibility that the crop completely misses the object, defaults to
    True (optional)
    :param cover_all_box: If True, the crop will cover the entire box, defaults to False (optional)
    :param is_mask_crop: if True, the crop will be done on the mask, not the image, defaults to False (optional)
    """

    def __init__(self,
                 aspect_ratio=[.5, 2.],
                 thresholds=[.0, .1, .3, .5, .7, .9],
                 scaling=[.3, 1.],
                 num_attempts=50,
                 allow_no_crop=True,
                 cover_all_box=False,
                 is_mask_crop=False):
        super(RandomCrop, self).__init__()
        self.aspect_ratio = aspect_ratio
        self.thresholds = thresholds
        self.scaling = scaling
        self.num_attempts = num_attempts
        self.allow_no_crop = allow_no_crop
        self.cover_all_box = cover_all_box
        self.is_mask_crop = is_mask_crop

    def crop_segms(self, segms, valid_ids, crop, height, width):
        """
        crop segms

        :param segms: a list of segmentation masks
        :param valid_ids: list of ints
        :param crop: [x1, y1, x2, y2]
        :param height: the height of the image
        :param width: the width of the image
        """

        def _crop_poly(segm, crop):
            """
            It crops a polygon

            :param segm: the segmentation mask
            :param crop: a tuple of 4 elements, (x1, y1, x2, y2)
            """
            xmin, ymin, xmax, ymax = crop
            crop_coord = [xmin, ymin, xmin, ymax, xmax, ymax, xmax, ymin]
            crop_p = paddle.to_tensor(crop_coord).reshape(4, 2)
            crop_p = Polygon(crop_p)

            crop_segm = list()
            for poly in segm:
                poly = paddle.to_tensor(poly).reshape(len(poly) // 2, 2)
                polygon = Polygon(poly)
                if not polygon.is_valid:
                    exterior = polygon.exterior
                    multi_lines = exterior.intersection(exterior)
                    polygons = shapely.ops.polygonize(multi_lines)
                    polygon = MultiPolygon(polygons)
                multi_polygon = list()
                if isinstance(polygon, MultiPolygon):
                    multi_polygon = copy.deepcopy(polygon)
                else:
                    multi_polygon.append(copy.deepcopy(polygon))
                for per_polygon in multi_polygon:
                    inter = per_polygon.intersection(crop_p)
                    if not inter:
                        continue
                    if isinstance(inter, (MultiPolygon, GeometryCollection)):
                        for part in inter:
                            if not isinstance(part, Polygon):
                                continue
                            part = paddle.squeeze(
                                paddle.to_tensor(part.exterior.coords[:-1]).reshape(1,
                                                                                    -1))
                            part[0::2] -= xmin
                            part[1::2] -= ymin
                            crop_segm.append(part.tolist())
                    elif isinstance(inter, Polygon):
                        crop_poly = paddle.squeeze(
                            paddle.to_tensor(inter.exterior.coords[:-1]).reshape(1, -1))
                        crop_poly[0::2] -= xmin
                        crop_poly[1::2] -= ymin
                        crop_segm.append(crop_poly.tolist())
                    else:
                        continue
            return crop_segm

        def _crop_rle(rle, crop, height, width):
            """
            It takes a run-length encoded mask, crops it, and returns the cropped mask

            :param rle: Run-length encoding of the mask
            :param crop: a tuple of (x, y, w, h)
            :param height: height of the image
            :param width: the width of the image
            """
            if 'counts' in rle and type(rle['counts']) == list:
                rle = mask_util.frPyObjects(rle, height, width)
            mask = mask_util.decode(rle)
            mask = mask[crop[1]:crop[3], crop[0]:crop[2]]
            rle = mask_util.encode(paddle.to_tensor(mask, order='F', dtype=paddle.uint8))
            return rle

        crop_segms = []
        for id in valid_ids:
            segm = segms[id]
            if isinstance(segm, list):
                import copy

                import shapely.ops
                from shapely.geometry import (GeometryCollection, MultiPolygon,
                                              Polygon)
                logging.getLogger("shapely").setLevel(logging.WARNING)
                # Polygon format
                crop_segms.append(_crop_poly(segm, crop))
            else:
                # RLE format
                import pycocotools.mask as mask_util
                crop_segms.append(_crop_rle(segm, crop, height, width))
        return crop_segms

    def forward(self, tensor_dict):
        if 'gt_bbox' in tensor_dict and len(tensor_dict['gt_bbox']) == 0:
            return tensor_dict

        h, w = tensor_dict['img'].shape[:2]
        gt_bbox = tensor_dict['gt_bbox']

        # NOTE Original method attempts to generate one candidate for each
        # threshold then randomly sample one from the resulting list.
        # Here a short circuit approach is taken, i.e., randomly choose a
        # threshold and attempt to find a valid crop, and simply return the
        # first one found.
        # The probability is not exactly the same, kinda resembling the
        # "Monty Hall" problem. Actually carrying out the attempts will affect
        # observability (just like opening doors in the "Monty Hall" game).
        thresholds = list(self.thresholds)
        if self.allow_no_crop:
            thresholds.append('no_crop')

        random.shuffle(thresholds)

        for thresh in thresholds:
            if thresh == 'no_crop':
                return tensor_dict

            found = False
            for i in range(self.num_attempts):
                min_scale, max_scale = self.scaling
                scale = paddle.uniform([1], min=min_scale, max=max_scale)
                if self.aspect_ratio is not None:
                    min_ar, max_ar = self.aspect_ratio
                    aspect_ratio = paddle.uniform([1], min=max(min_ar, scale ** 2), max=min(max_ar, scale ** -2))
                    h_scale = scale / paddle.sqrt(aspect_ratio)
                    w_scale = scale * paddle.sqrt(aspect_ratio)
                else:
                    h_scale = paddle.uniform(min=min_scale, max=max_scale)
                    w_scale = paddle.uniform(min=min_scale, max=max_scale)
                crop_h = h * h_scale
                crop_w = w * w_scale
                if self.aspect_ratio is None:
                    if crop_h / crop_w < 0.5 or crop_h / crop_w > 2.0:
                        continue

                crop_h = int(crop_h)
                crop_w = int(crop_w)
                crop_y = paddle.randint(0, h - crop_h)
                crop_x = paddle.randint(0, w - crop_w)
                crop_box = [crop_x, crop_y, crop_x + crop_w, crop_y + crop_h]
                iou = self._iou_matrix(
                    gt_bbox, paddle.to_tensor(
                        [crop_box], dtype=paddle.float32))
                if iou.max() < thresh:
                    continue

                if self.cover_all_box and iou.min() < thresh:
                    continue

                cropped_box, valid_ids = self._crop_box_with_center_constraint(
                    gt_bbox, paddle.to_tensor(
                        crop_box, dtype=paddle.float32))
                if valid_ids.size > 0:
                    found = True
                    break

            if found:
                if self.is_mask_crop and 'gt_poly' in tensor_dict and len(tensor_dict[
                                                                              'gt_poly']) > 0:
                    crop_polys = self.crop_segms(
                        tensor_dict['gt_poly'],
                        valid_ids,
                        paddle.to_tensor(
                            crop_box, dtype=paddle.int64),
                        h,
                        w)
                    if [] in crop_polys:
                        delete_id = list()
                        valid_polys = list()
                        for id, crop_poly in enumerate(crop_polys):
                            if crop_poly == []:
                                delete_id.append(id)
                            else:
                                valid_polys.append(crop_poly)
                        valid_ids.__delitem__(delete_id)
                        if len(valid_polys) == 0:
                            return tensor_dict
                        tensor_dict['gt_poly'] = valid_polys
                    else:
                        tensor_dict['gt_poly'] = crop_polys

                if 'gt_segm' in tensor_dict:
                    tensor_dict['gt_segm'] = self._crop_segm(tensor_dict['gt_segm'],
                                                             crop_box)
                    tensor_dict['gt_segm'] = tensor_dict['gt_segm'][valid_ids]

                tensor_dict['img'] = self._crop_image(tensor_dict['img'], crop_box)
                ### add template
                if 'template' in tensor_dict.keys():
                    tensor_dict['template'] = self._crop_image(tensor_dict['template'], crop_box)
                tensor_dict['gt_bbox'] = cropped_box[valid_ids]
                tensor_dict['gt_class'] = tensor_dict['gt_class'][valid_ids]
                if 'gt_score' in tensor_dict:
                    tensor_dict['gt_score'] = tensor_dict['gt_score'][valid_ids]

                if 'is_crowd' in tensor_dict:
                    tensor_dict['is_crowd'] = tensor_dict['is_crowd'][valid_ids]

                if 'difficult' in tensor_dict:
                    tensor_dict['difficult'] = tensor_dict['difficult'][valid_ids]

                return tensor_dict

        return tensor_dict

    def _iou_matrix(self, a, b):
        """
        It takes two lists of bounding boxes and returns a matrix of IoU values

        :param a: (N, 4) paddle tensor of float
        :param b: (N, 4) paddle tensor of float
        """
        tl_i = paddle.maximum(a[:, None, :2], b[:, :2])
        br_i = paddle.minimum(a[:, None, 2:], b[:, 2:])

        area_i = paddle.prod(br_i - tl_i, axis=2) * (tl_i < br_i).all(axis=2)
        area_a = paddle.prod(a[:, 2:] - a[:, :2], axis=1)
        area_b = paddle.prod(b[:, 2:] - b[:, :2], axis=1)
        area_o = (area_a[:, None] + area_b - area_i)
        return area_i / (area_o + 1e-10)

    def _crop_box_with_center_constraint(self, box, crop):
        """
        > Given a box and a crop, return the box that is the intersection of the two, but with the center of the box
        constrained to be within the crop

        :param box: the bounding box to be cropped
        :param crop: a tuple of (x, y, w, h)
        """
        cropped_box = box.copy()

        cropped_box[:, :2] = paddle.maximum(box[:, :2], crop[:2])
        cropped_box[:, 2:] = paddle.minimum(box[:, 2:], crop[2:])
        cropped_box[:, :2] -= crop[:2]
        cropped_box[:, 2:] -= crop[:2]

        centers = (box[:, :2] + box[:, 2:]) / 2
        valid = paddle.logical_and(crop[:2] <= centers,
                                   centers < crop[2:]).all(axis=1)
        valid = paddle.logical_and(
            valid, (cropped_box[:, :2] < cropped_box[:, 2:]).all(axis=1))
        return cropped_box, paddle.where(valid)[0].tolist()

    def _crop_image(self, img, crop):
        """
        It crops the image to the specified crop size

        :param img: the image to be cropped
        :param crop: a tuple of (x, y, w, h)
        """
        x1, y1, x2, y2 = crop
        return img[:, :, y1:y2, x1:x2]
