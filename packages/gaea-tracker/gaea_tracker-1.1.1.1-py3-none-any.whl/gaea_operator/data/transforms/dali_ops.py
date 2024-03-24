#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : dali_ops.py
@Author        : xuningyuan
@Date          : 2022/11/04
@Description   :
"""
from typing import Union

import numpy as np

from gaea_operator.plugin import dali, fn, types


def prob_uniform(range: list, prob=0.5, default=1.) -> dict:
    """
    It returns a random number from a uniform distribution with a range specified with a probability of (prob), 
    and returns default with a probability of (1-prob)
    otherwise

    :param range: the range of the uniform distribution
    :param prob: the probability of the random number being drawn
    :param default: the default value to use if the coin flip is False
    :return: A random number.
    """
    defa = types.Constant(default)
    idx = fn.random.coin_flip(probability=prob)
    random_num = fn.random.uniform(range=range)
    return fn.stack(defa, random_num)[idx]


def decode(tensor_dict: dict, device='mixed') -> dict:
    """
    `decode` decodes image from the tensor dictionary

    :param tensor_dict: The tensor dictionary
    :type tensor_dict: dict
    :param device: The device to decode the images on. This can be 'cpu', or 'mixed'. If 'mixed', the images will be
    decoded on the CPU and then moved to the GPU, defaults to mixed (optional)
    :return: The tensor dictionary with the images and segmentation images decoded.
    """

    tensor_dict['im_shape'] = fn.peek_image_shape(tensor_dict['images'])[:2]
    tensor_dict['images'] = fn.decoders.image(
        tensor_dict['images'], device=device)
    tensor_dict['scale_factor'] = types.Constant([1., 1.])
    if 'segm' in tensor_dict:
        tensor_dict['segm'] = fn.decoders.image(
            tensor_dict['segm'], device=device)[:, :, :1]
    if 'segm_ori' in tensor_dict:
        tensor_dict['segm_ori'] = fn.decoders.image(
            tensor_dict['segm_ori'], device=device)[:, :, :1]
    if 'templates' in tensor_dict:
        tensor_dict['templates'] = fn.decoders.image(
            tensor_dict['templates'], device=device)
    if "bboxes" in tensor_dict:
        tensor_dict['bboxes'] = dali.math.clamp(tensor_dict['bboxes'], 0, 1)
    return tensor_dict


def resize(tensor_dict_in: dict,  target_size: Union[tuple, list, int], mode: str = 'default', interp: str = 'linear') -> dict:
    """
    resize the image and segmantic map if exist

    :param tensor_dict: the tensor dictionary
    :type tensor_dict: dict
    :param target_size: The target size of the image. If it is a tuple, it will be the target width and height of the image. If it is an
    integer, the target width and height will be (target_size, target_size)
    :type target_size: Union[tuple, list, int]
    :param mode: one of ['not_larger', 'default', 'not_smaller'], decide whether to keep the aspect ratio of the image.
    :type mode: str (optional)
    :param interp: interpolation method, can be 'nn', 'linear', 'cubic', 'lanczos', 'gaussian', defaults to
    linear
    :type interp: str (optional)
    :return: A dictionary with the key 'images' and the value of the resized image.
    """

    if isinstance(target_size, int):
        target_size = [target_size, target_size]
    elif isinstance(target_size, (list, tuple)):
        target_size = [target_size[1], target_size[0]]

    interp_map = {'nn': types.DALIInterpType.INTERP_NN,
                  'linear': types.DALIInterpType.INTERP_LINEAR,
                  'cubic': types.DALIInterpType.INTERP_CUBIC,
                  'lanczos': types.DALIInterpType.INTERP_LANCZOS3,
                  'gaussian': types.DALIInterpType.INTERP_GAUSSIAN}
    if isinstance(interp, str):
        assert interp in interp_map, "interp must be one of {}, however it is {}".format(
            interp_map, interp)
        interp = interp_map[interp]

    tensor_dict = {k: v for k, v in tensor_dict_in.items()}

    tensor_dict['images'] = fn.resize(
        tensor_dict['images'], size=target_size, mode=mode, interp_type=interp)

    tensor_dict['scale_factor'] = tensor_dict['scale_factor'] * \
        fn.shapes(tensor_dict['images'])[:2] / tensor_dict['im_shape']
    tensor_dict['im_shape'] = fn.shapes(tensor_dict['images'])[:2]

    if "segm" in tensor_dict:
        tensor_dict['segm'] = fn.resize(
            tensor_dict['segm'], size=target_size, mode=mode, interp_type=types.DALIInterpType.INTERP_NN)
    if "templates" in tensor_dict:
        tensor_dict['templates'] = fn.resize(
            tensor_dict['templates'], size=target_size, mode=mode, interp_type=interp)

    return tensor_dict


def random_resize(tensor_dict: dict, target_size: list, mode: str = 'default', interp: str = 'linear',
                  random_size: bool = True, random_interp: bool = False) -> dict:
    """
    _randomly resize the tensor_dict image to a target size_

    :param tensor_dict: The tensor_dict image
    :type tensor_dict: dict
    :param target_size: The target size of the image
    :type target_size: list
    :param mode: one of ['not_larger', 'default', 'not_smaller'], whether to keep the aspect ratio of the image, defaults to True
    :type mode: str (optional)
    :param interp: interpolation method, can be 'nearest', 'bilinear', 'bicubic', 'area', 'lanczos', 'linear', defaults to
    linear
    :type interp: str (optional)
    :param random_size: If True, the target size will be randomly selected from the target_size list, defaults to True
    :type random_size: bool (optional)
    :param random_interp: If True, the interpolation method will be randomly selected from the following:, defaults to False
    :type random_interp: bool (optional)
    :return: A dictionary with the key 'images' and the value of the resized image.
    """

    if random_size:
        range_list = [i for i in range(len(target_size))]
        idx = fn.random.uniform(dtype=types.INT32, values=range_list)
    else:
        idx = 0

    target_size = np.array(target_size, np.float32)
    target_size = types.Constant(target_size)

    if random_interp:
        interps = [1, 2, 3, 5]
        interp_idx = fn.random.uniform(dtype=types.INT32, values=[0, 1, 2, 3])
        interp_results = [resize(tensor_dict, target_size=target_size[idx],
                                 mode=mode, interp=interp) for interp in interps]
        for key in tensor_dict:
            tensors = fn.stack(*[interp_res[key]
                               for interp_res in interp_results])
            tensor_dict[key] = tensors[interp_idx]
        return tensor_dict
    else:
        return resize(tensor_dict, target_size=target_size[idx], mode=mode, interp=interp)


def batch_random_resize(tensor_dict: dict, target_size: list, mode: str = 'default', interp: str = 'linear',
                        random_size: bool = True, random_interp: bool = False, batch_size=8) -> dict:
    """
    "Resize the tensor_dict image to the target size, with the option to keep the aspect ratio, and with the option to randomly
    resize the image."

    The function takes in a dictionary of images, and returns a dictionary of resized images

    :param tensor_dict: the tensor dictionary containing the image and the label
    :type tensor_dict: dict
    :param target_size: the size of the output image
    :type target_size: list
    :param mode: one of ['not_larger', 'default', 'not_smaller'], whether to keep the aspect ratio of the image, defaults to True
    :type mode: str (optional)
    :param interp: interpolation method, can be 'linear', 'nearest', 'bilinear', 'bicubic', 'trilinear', 'area', 'lanczos4',
    defaults to linear
    :type interp: str (optional)
    :param random_size: if True, the image will be resized to a random size between (0.5, 2) times the target size, defaults
    to True
    :type random_size: bool (optional)
    :param random_interp: If True, the interpolation method will be randomly chosen from the list of available interpolation
    methods, defaults to False
    :type random_interp: bool (optional)
    :param batch_size: the number of images to be resized in a batch, defaults to 8 (optional)
    :return: A dictionary with the key 'images' and the value of the resized image.
    """

    if random_size:
        range_list = [i for i in range(len(target_size))]
        idx = fn.random.uniform(dtype=types.INT32, values=range_list, seed=1)
        idx = fn.permute_batch(idx, indices=batch_size*[0])
    else:
        idx = 0

    target_size = np.array(target_size, np.float32)
    target_size = types.Constant(target_size)

    if random_interp:
        interps = [1, 2, 3, 5]
        interp_idx = fn.random.uniform(dtype=types.INT32, values=[0, 1, 2, 3])
        interp_idx = fn.permute_batch(interp_idx, indices=batch_size*[0])
        interp_results = [resize(tensor_dict, target_size=target_size[idx],
                                 mode=mode, interp=interp) for interp in interps]

        for key in tensor_dict:
            tensors = fn.stack(*[interp_res[key]
                               for interp_res in interp_results])
            tensor_dict[key] = tensors[interp_idx]
        return tensor_dict
    else:
        return resize(tensor_dict, target_size=target_size[idx], mode=mode, interp=interp)


def random_step_scaling(tensor_dict: dict, min_scale_factor: float = 0.75, max_scale_factor: float = 1.25, scale_step_size=0.25, interp='linear'):
    """
    This function randomly scales an image tensor within a given range and returns the resized tensor.

    :param tensor_dict: A dictionary containing the input image tensor and any associated labels or metadata
    :type tensor_dict: dict
    :param min_scale_factor: The minimum scaling factor that can be applied to the image
    :type min_scale_factor: float
    :param max_scale_factor: The maximum scaling factor that can be applied to the input image
    :type max_scale_factor: float
    :param scale_step_size: The step size used to generate a list of scale factors between min_scale_factor and
    max_scale_factor. If scale_step_size is 0, a single random scale factor will be generated between min_scale_factor and
    max_scale_factor
    :param interp: interp refers to the interpolation method used during image resizing. It can take values such as
    'nearest', 'bilinear', 'bicubic', etc. which determine how the pixel values are interpolated when the image is resized,
    defaults to linear (optional)
    :return: the output of the `resize` function applied to the input `tensor_dict` with a target size scaled randomly
    between `min_scale_factor` and `max_scale_factor`, using a step size of `scale_step_size` if it is not zero, and using
    the interpolation method specified by `interp`.
    """
    if scale_step_size == 0:
        scale_factor = fn.random.uniform(dtype=types.FLOAT32, range=[
                                         min_scale_factor, max_scale_factor], seed=1)
    else:
        scale_factor_list = np.linspace(
            min_scale_factor, max_scale_factor, num=int((max_scale_factor - min_scale_factor)//scale_step_size + 1), endpoint=True).tolist()
        scale_factor = fn.random.uniform(
            dtype=types.FLOAT, values=scale_factor_list, seed=1)
    shape = tensor_dict["im_shape"]
    size = fn.stack(shape[1], shape[0])
    size = size*scale_factor
    return resize(tensor_dict, target_size=size, interp=interp)


def random_distort(tensor_dict: dict, hue: list = [-18, 18, 0.5], saturation: list = [0.5, 1.5, 0.5], contrast: list = [0.5, 1.5, 0.5],
                   brightness: list = [0.5, 1.5, 0.5], random_apply: bool = True, count: int = 4, random_channel: bool = False) -> dict:
    """
    Randomly distort the hue, saturation, contrast, and brightness of the tensor_dict images

    :param tensor_dict: The tensor dictionary
    :type tensor_dict: dict
    :param hue: [-18, 18, 0.5]
    :type hue: list
    :param saturation: [0.5, 1.5, 0.5]
    :type saturation: list
    :param contrast: [0.5, 1.5, 0.5]
    :type contrast: list
    :param brightness: [0.5, 1.5, 0.5]
    :type brightness: list
    :param random_apply: If True, the random distortion will be applied to the image, defaults to True
    :type random_apply: bool (optional)
    :param count: The number of times to apply the random distortion, defaults to 4
    :type count: int (optional)
    :param random_channel: If True, the random distortion will be applied to each channel of the image separately, defaults
    to False
    :type random_channel: bool (optional)
    :return: The tensor dictionary with the images key updated to the new image.
    """
    h = prob_uniform(range=hue[:2], prob=hue[2], default=0.)
    s = prob_uniform(range=saturation[:2], prob=saturation[2], default=1.)
    b = prob_uniform(range=brightness[:2], prob=brightness[2], default=1.)
    c = prob_uniform(range=contrast[:2], prob=contrast[2], default=1.)
    tensor_dict['images'] = fn.hsv(
        tensor_dict['images'], dtype=types.FLOAT, hue=h, saturation=s)
    tensor_dict['images'] = fn.brightness_contrast(tensor_dict['images'],
                                                   contrast_center=128,
                                                   dtype=types.UINT8,
                                                   brightness=b,
                                                   contrast=c)

    if "templates" in tensor_dict:
        tensor_dict['templates'] = fn.hsv(
            tensor_dict['templates'], dtype=types.FLOAT, hue=h, saturation=s)
        tensor_dict['templates'] = fn.brightness_contrast(tensor_dict['templates'],
                                                          contrast_center=128,
                                                          dtype=types.UINT8,
                                                          brightness=b,
                                                          contrast=c)
    return tensor_dict


def random_gaussian_blur(tensor_dict: dict, sigma: Union[float, tuple] = 1., p: float = 0.5) -> dict:
    """
    对输入的tensor_dict中的图像随机使用高斯核进行模糊，高斯核的标准差由sigma指定.
    Args:
        tensor_dict (dict): 包含待模糊图像的tensor以及其标签的字典.
        sigma (float): 高斯核的标准差.默认为 1
        p(float): 模糊的概率，即有多少比例的图像会被模糊。默认为0.5.
    Returns:
        dict: 包含模糊后的图像tensor及其标签的字典.
    """
    if isinstance(sigma, (float, int)):
        sigma = (sigma, sigma)
    random_sigma = prob_uniform(range=sigma, prob=p, default=0)
    tensor_dict["images"] = fn.gaussian_blur(
        tensor_dict["images"], sigma=random_sigma)
    return tensor_dict


def random_equalize(tensor_dict: dict, p: float = 0.5) -> dict:
    do_equalize = fn.random.coin_flip(probability=p, dtype=types.DALIDataType.BOOL)
    if do_equalize:
        tensor_dict["images"] = fn.equalize(tensor_dict["images"])
    else:
        tensor_dict["images"] = tensor_dict["images"]
    return tensor_dict


def random_grayscale(tensor_dict: dict, p: float = 0.5) -> dict:
    """
    随机将输入的图像转换为灰度图像
    
    Args:
        tensor_dict (dict): 包含输入图像的字典，字典必须包含 "images" 键，对应输入的图像张量。
        p (float, optional): 转换为灰度图像的概率，默认为 0.5。
    
    Returns:
        dict: 包含输入图像张量的字典，如果随机概率小于等于给定概率 p，则将输入图像转换为灰度图像。
    
    """
    do_grayscale = fn.random.coin_flip(
        probability=p, dtype=types.DALIDataType.BOOL)
    if do_grayscale:
        tensor_dict["images"] = fn.color_space_conversion(tensor_dict["images"],
                                                          image_type=types.DALIImageType.RGB,
                                                          output_type=types.DALIImageType.GRAY)
    else:
        tensor_dict["images"] = tensor_dict["images"]
    return tensor_dict


def random_expand(tensor_dict: dict, ratio=4., prob=0.5, fill_value=(127, 127, 127)) -> dict:
    """
    It randomly expands the image and bounding boxes by a random ratio

    :param tensor_dict: The tensor dictionary
    :type tensor_dict: dict
    :param ratio: The maximum ratio of the image to be expanded
    :param prob: the probability of applying the transform
    :param fill_value: The value to fill the expanded area with
    :return: The tensor dictionary with the images and bboxes pasted.
    """

    random_ratio = prob_uniform(range=[1., ratio], prob=prob)
    tensor_dict['images'] = fn.paste(
        tensor_dict['images'], fill_value=fill_value, ratio=random_ratio)
    if 'bboxes' in tensor_dict:
        tensor_dict['bboxes'] = fn.bbox_paste(
            tensor_dict['bboxes'], ratio=random_ratio, ltrb=True)
    if 'vertices' in tensor_dict:
        mt = fn.transforms.scale(scale=fn.stack(
            1/random_ratio, 1/random_ratio), center=[0.5, 0.5])
        tensor_dict['vertices'] = fn.coord_transform(
            tensor_dict['vertices'], MT=mt)
    if "segm" in tensor_dict:
        tensor_dict['segm'] = fn.paste(
            tensor_dict['segm'], fill_value=0, ratio=random_ratio)
    if "templates" in tensor_dict:
        tensor_dict['templates'] = fn.paste(
            tensor_dict['templates'], fill_value=fill_value, ratio=random_ratio)
    return tensor_dict


def crop_image(tensor_dict: dict, size: Union[list, tuple, int], crop_center: Union[list, tuple, int] = [0.5, 0.5]):
    """
    It crops the image tensor to the specified size, with the specified center

    :param tensor_dict: a dictionary containing the tensors to be cropped
    :type tensor_dict: dict
    :param size: The size of the crop. If a single number is provided, the crop will be square
    :type size: Union[list, tuple, int]
    :param crop_center: The center of the crop. If you want to crop the center of the image, you can use [0.5, 0.5]
    :type crop_center: Union(list, tuple, int)
    :return: The cropped image.
    """

    if isinstance(size, int):
        size = [size, size]
    if isinstance(crop_center, int):
        crop_center = [crop_center, crop_center]
    tensor_dict['images'] = fn.crop(
        tensor_dict['images'], crop=size, crop_pos_x=crop_center[0], crop_pos_y=crop_center[1])
    if "segm" in tensor_dict:
        tensor_dict['segm'] = fn.crop(
            tensor_dict['segm'], crop=size, crop_pos_x=crop_center[0], crop_pos_y=crop_center[1])
    if "templates" in tensor_dict:
        tensor_dict['templates'] = fn.crop(
            tensor_dict['templates'], crop=size, crop_pos_x=crop_center[0], crop_pos_y=crop_center[1])
    return tensor_dict


def random_padding_crop(tensor_dict: dict, crop_size=(512, 512), im_padding_value=127.5, label_padding_value=255):
    """
    The function randomly crops and pads images, segmentation masks, and templates in a given dictionary.

    :param tensor_dict: A dictionary containing the input tensors, including 'images', 'segm', and 'templates'
    :type tensor_dict: dict
    :param crop_size: The size of the cropped image, specified as a tuple of (height, width) in pixels. In this case, it is
    set to (512, 512)
    :param im_padding_value: The value used to fill the padded pixels in the image tensor. In this case, it is set to 127.5
    :param label_padding_value: The value used for padding the label or segmentation map when cropping the image, defaults
    to 255 (optional)
    :return: the updated `tensor_dict` after applying random padding and cropping to the images, segmentation masks, and
    templates (if present).
    """

    pos_x = fn.random.uniform(types=types.FLOAT32, range=[0, 1])
    pos_y = fn.random.uniform(types=types.FLOAT32, range=[0, 1])
    tensor_dict['images'] = fn.crop(tensor_dict['images'], crop=crop_size, crop_pos_x=pos_x, crop_pos_y=pos_y,
                                    out_of_bounds_policy="pad", fill_values=im_padding_value)
    if "segm" in tensor_dict:
        tensor_dict['segm'] = fn.crop(tensor_dict['segm'], crop=crop_size, crop_pos_x=pos_x, crop_pos_y=pos_y,
                                      out_of_bounds_policy="pad", fill_values=label_padding_value)
    if "templates" in tensor_dict:
        tensor_dict['templates'] = fn.crop(tensor_dict['templates'], crop=crop_size, crop_pos_x=pos_x, crop_pos_y=pos_y,
                                           out_of_bounds_policy="pad", fill_values=im_padding_value)
    return tensor_dict


def random_crop_image(tensor_dict: dict, size: Union[list, tuple, int], ratio=[3 / 4, 4 / 3], scale=[0.08, 1.0]):
    """
    It takes an image, crops it to a random size between 0.08 and 1.0 of the original size, and then resizes it to the
    specified size

    :param tensor_dict: the dictionary of tensors that we want to apply the random crop to
    :type tensor_dict: dict
    :param size: The size of the output image
    :type size: Union[list, tuple, int]
    :param ratio: The aspect ratio of the crop
    :param scale: The area of the image to be cropped. The value is a list of two numbers, the first number is the minimum
    area, and the second number is the maximum area
    :return: A dictionary with the image and the label.
    """

    if isinstance(size, int):
        size = [size, size]
    tensor_dict['images'] = fn.random_resized_crop(tensor_dict['images'], size=size, random_area=scale,
                                                   random_aspect_ratio=ratio)
    return tensor_dict


def random_crop(tensor_dict: dict, aspect_ratio=[0.5, 2.0], threshold=[0.0, 0.1, 0.3, 0.5, 0.7, 0.9],
                scaling=[0.3, 1.0], num_attempts=50, allow_no_crop=True) -> dict:
    """
    "Randomly crop the tensor_dict image with the given aspect ratio and scaling."

    The first argument is the tensor_dict image. The second argument is the aspect ratio, which is the ratio of width to height.
    The third argument is the threshold, which is the minimum overlap between the tensor_dict image and the cropped image. The
    fourth argument is the scaling, which is the ratio of the cropped image to the tensor_dict image. The fifth argument is the
    number of attempts to crop the image. The sixth argument is whether to allow no crop

    :param tensor_dict: The tensor dictionary containing the image and bounding boxes
    :type tensor_dict: dict
    :param aspect_ratio: The list of aspect ratios for the crops
    :param threshold: The minimum overlap required between the cropped image and the original image
    :param scaling: The lower and upper bounds for the crop size as a fraction of the image size
    :param num_attempts: number of attempts at generating a cropped region of the image of the specified constraints. After
    `num_attempts` failures, return the entire image, defaults to 50 (optional)
    :param allow_no_crop: If True, allow the result to be the entire image, defaults to True (optional)
    """

    if 'bboxes' in tensor_dict and 'labels' in tensor_dict:
        crop_begin, crop_size, tensor_dict['bboxes'], tensor_dict['labels'], mask_ids = fn.random_bbox_crop(tensor_dict['bboxes'], tensor_dict['labels'],
                                                                                                            device='cpu',
                                                                                                            aspect_ratio=aspect_ratio,
                                                                                                            thresholds=threshold,
                                                                                                            scaling=scaling,
                                                                                                            bbox_layout='xyXY',
                                                                                                            allow_no_crop=allow_no_crop,
                                                                                                            num_attempts=num_attempts,
                                                                                                            output_bbox_indices=True)

        if 'polygons' in tensor_dict and 'vertices' in tensor_dict:
            tensor_dict['polygons'], tensor_dict['vertices'] = fn.segmentation.select_masks(mask_ids,
                                                                                            tensor_dict['polygons'],
                                                                                            tensor_dict['vertices'],
                                                                                            reindex_masks=True)
            mt = fn.transforms.crop(
                to_start=crop_begin, to_end=crop_begin+crop_size)
            tensor_dict['vertices'] = fn.coord_transform(
                tensor_dict['vertices'], MT=mt)
    else:
        bboxes = types.Constant(np.array([[0., 0., 1., 1.]]))
        labels = types.Constant([1])
        crop_begin, crop_size, _, _ = fn.random_bbox_crop(bboxes, labels,
                                                          device='cpu',
                                                          aspect_ratio=aspect_ratio,
                                                          thresholds=[0.],
                                                          scaling=scaling,
                                                          bbox_layout='xyXY',
                                                          allow_no_crop=allow_no_crop,
                                                          num_attempts=num_attempts)

    tensor_dict['images'] = fn.slice(
        tensor_dict['images'], crop_begin, crop_size)
    if "segm" in tensor_dict:
        tensor_dict['segm'] = fn.slice(
            tensor_dict['segm'], crop_begin, crop_size)
    if "templates" in tensor_dict:
        tensor_dict["templates"] = fn.slice(
            tensor_dict["templates"], crop_begin, crop_size)

    return tensor_dict


def random_crop_decode(tensor_dict: dict, aspect_ratio=[0.5, 2.0], threshold=[0.0, 0.1, 0.3, 0.5, 0.7, 0.9],
                       scaling=[0.3, 1.0], num_attempts=50, allow_no_crop=True, device='mixed') -> dict:
    """
    It crops the image randomly before decodes, and if bounding boxes are present, it crops the bounding boxes as well

    :param tensor_dict: The tensor dictionary
    :type tensor_dict: dict
    :param aspect_ratio: The aspect ratio of the crop
    :param threshold: The minimum IoU overlap with ground-truth bboxes to keep a bbox
    :param scaling: The area of the crop, as a fraction of the area of the original image
    :param num_attempts: The number of times to try to find a valid crop, defaults to 50 (optional)
    :param allow_no_crop: If True, the function will return the original image if no crop is found, defaults to True
    (optional)
    :param device: The device to run the operation on, defaults to mixed (optional)
    :return: The tensor dictionary with the images, bboxes, and labels.
    """

    if 'bboxes' in tensor_dict and 'labels' in tensor_dict:
        crop_begin, crop_size, tensor_dict['bboxes'], tensor_dict['labels'], mask_ids = fn.random_bbox_crop(tensor_dict['bboxes'], tensor_dict['labels'],
                                                                                                            device='cpu',
                                                                                                            aspect_ratio=aspect_ratio,
                                                                                                            thresholds=threshold,
                                                                                                            scaling=scaling,
                                                                                                            bbox_layout='xyXY',
                                                                                                            allow_no_crop=allow_no_crop,
                                                                                                            num_attempts=num_attempts,
                                                                                                            output_bbox_indices=True)

        if 'polygons' in tensor_dict and 'vertices' in tensor_dict:
            tensor_dict['polygons'], tensor_dict['vertices'] = fn.segmentation.select_masks(mask_ids,
                                                                                            tensor_dict['polygons'],
                                                                                            tensor_dict['vertices'],
                                                                                            reindex_masks=True)
            mt = fn.transforms.crop(
                to_start=crop_begin, to_end=crop_begin+crop_size)
            tensor_dict['vertices'] = fn.coord_transform(
                tensor_dict['vertices'], MT=mt)

        tensor_dict['images'] = fn.decoders.image_slice(
            tensor_dict['images'], crop_begin, crop_size, device=device)
        if "templates" in tensor_dict:
            tensor_dict['templates'] = fn.decoders.image_slice(
                tensor_dict['templates'], crop_begin, crop_size, device=device)
    else:
        tensor_dict['images'] = fn.decoders.image_random_crop(tensor_dict['images'],
                                                              device=device,
                                                              random_aspect_ratio=aspect_ratio,
                                                              random_area=scaling,
                                                              num_attempts=num_attempts,
                                                              seed=1)
        if "segm" in tensor_dict:
            tensor_dict['segm'] = fn.decoders.image_random_crop(tensor_dict['segm'],
                                                                device=device,
                                                                random_aspect_ratio=aspect_ratio,
                                                                random_area=scaling,
                                                                num_attempts=num_attempts,
                                                                seed=1)
        if "templates" in tensor_dict:
            tensor_dict["templates"] = fn.decoders.image_random_crop(tensor_dict["templates"],
                                                                     device=device,
                                                                     random_aspect_ratio=aspect_ratio,
                                                                     random_area=scaling,
                                                                     num_attempts=num_attempts,
                                                                     seed=1)

    return tensor_dict


def random_flip(tensor_dict: dict, prob=0.5, horizontal=True, vertical=False, depthwise=False) -> dict:
    """
    It flips the image and bounding boxes horizontally and/or vertically with a given probability

    :param tensor_dict: the tensor dictionary
    :type tensor_dict: dict
    :param prob: The probability of flipping the image
    :param horizontal: Flip the image horizontally, defaults to True (optional)
    :param vertical: flip the image vertically, defaults to False (optional)
    :param depthwise: If True, the image will be flipped along the depth axis, defaults to False (optional)
    :return: The tensor dictionary with the images, bboxes, and segm flipped.
    """

    if horizontal:
        hori = fn.random.coin_flip(probability=prob)
    else:
        hori = 0
    if vertical:
        vert = fn.random.coin_flip(probability=prob)
    else:
        vert = 0
    if depthwise:
        dept = fn.random.coin_flip(probability=prob)
    else:
        dept = 0

    if 'bboxes' in tensor_dict:
        tensor_dict['bboxes'] = fn.bb_flip(
            tensor_dict['bboxes'], ltrb=True, horizontal=hori, vertical=vert)
    if 'vertices' in tensor_dict:
        tensor_dict['vertices'] = fn.coord_flip(
            tensor_dict['vertices'], flip_x=hori, flip_y=vert)

    tensor_dict['images'] = fn.flip(
        tensor_dict['images'], depthwise=dept, horizontal=hori, vertical=vert)
    if 'segm' in tensor_dict:
        tensor_dict['segm'] = fn.flip(
            tensor_dict['segm'], depthwise=0, horizontal=hori, vertical=vert)
    if "templates" in tensor_dict:
        tensor_dict['templates'] = fn.flip(
            tensor_dict['templates'], depthwise=dept, horizontal=hori, vertical=vert)

    return tensor_dict


def normalize_image(tensor_dict: dict, mean=[0.485, 0.456, 0.406], std=[1., 1., 1.], is_scale=True) -> dict:
    """
    _normalize_image_ normalizes the tensor_dict image

    :param tensor_dict: the tensor dictionary
    :type tensor_dict: dict
    :param mean: The mean pixel value per channel
    :param std: The standard deviation of the normalization
    :param is_scale: If True, the mean and std are scaled by 255, defaults to True (optional)
    :return: A dictionary with the key 'images' and the value of the normalized image.
    """

    if is_scale:
        mean = [v*255 for v in mean]
        std = [v*255 for v in std]
    mean = fn.reshape(types.Constant(mean), shape=[1, 1, 3])
    std = fn.reshape(types.Constant(std), shape=[1, 1, 3])
    tensor_dict['images'] = fn.normalize(
        tensor_dict['images'], mean=mean, stddev=std)
    if "templates" in tensor_dict:
        tensor_dict['templates'] = fn.normalize(
            tensor_dict['templates'], mean=mean, stddev=std)
    return tensor_dict


def pad_batch(tensor_dict: dict, pad_to_stride=0) -> dict:
    """
    `pad_batch` pads the tensor_dict batch to the specified stride

    :param tensor_dict: the tensor dictionary
    :type tensor_dict: dict
    :param pad_to_stride: This is the stride of the network. For example, if the stride is 32, then the network will only
    accept images that are divisible by 32. If the image is not divisible by 32, then the image will be padded with zeros to
    make it divisible by 32, defaults to 0 (optional)
    :return: The padded images and segmentation masks.
    """

    tensor_dict['images'] = fn.pad(tensor_dict['images'], fill_value=0, axes=[
        0, 1], align=pad_to_stride)
    if 'segm' in tensor_dict:
        tensor_dict['segm'] = fn.pad(tensor_dict['segm'], fill_value=0, axes=[
            0, 1], align=pad_to_stride)
    if "templates" in tensor_dict:
        tensor_dict['templates'] = fn.pad(tensor_dict['templates'], fill_value=0,
                                          axes=[0, 1], align=pad_to_stride)
    return tensor_dict


def pad_gt(tensor_dict: dict) -> dict:
    """
    It pads the tensor dictionary with zeros

    :param tensor_dict: the tensor dictionary
    :type tensor_dict: dict
    :return: A dictionary with the keys 'bboxes', 'labels', and 'scores'
    """

    tensor_dict['bboxes'] = fn.pad(tensor_dict['bboxes'], fill_value=0, axes=0)
    tensor_dict['labels'] = fn.stack(tensor_dict['labels'], axis=1)
    gt_mask = tensor_dict['labels'] > -1
    tensor_dict['pad_gt_mask'] = fn.pad(gt_mask, fill_value=0, axes=0)
    tensor_dict['labels'] = fn.pad(tensor_dict['labels'], fill_value=0, axes=0)

    if 'polygons' in tensor_dict and 'vertices' in tensor_dict:
        tensor_dict['polygons'] = fn.pad(
            tensor_dict['polygons'], fill_value=0, axes=0)
        tensor_dict['vertices'] = fn.pad(
            tensor_dict['vertices'], fill_value=0, axes=0)

    if 'scores' in tensor_dict:
        tensor_dict['scores'] = fn.pad(
            tensor_dict['scores'], fill_value=0, axes=0)

    return tensor_dict


def to_gpu(tensor_dict: dict) -> dict:
    """
    It transfer the tensors to gpu

    Args:
        tensor_dict (dict): _description_

    Returns:
        dict: _description_
    """
    for key in tensor_dict:
        tensor_dict[key] = tensor_dict[key].gpu()
    return tensor_dict


def rel2abs(tensor_dict: dict) -> dict:
    """
    It transfer relative postion to absolute position

    Args:
        tensor_dict (dict): _description_

    Returns:
        dict: _description_
    """
    hw = fn.shapes(tensor_dict['images'])[:2]

    do_multiply = fn.shapes(tensor_dict["bboxes"])[0] > 0
    bboxes_true_branch, bboxes_false_branch = fn._conditional.split(
        tensor_dict["bboxes"], predicate=do_multiply)
    hw_true_branch, hw_false_branch = fn._conditional.split(
        hw, predicate=do_multiply)
    hw = hw_true_branch
    whwh = fn.stack(hw[1], hw[0], hw[1], hw[0])
    wh = fn.stack(hw[1], hw[0])

    result_true = bboxes_true_branch.gpu() * whwh
    result_false = bboxes_false_branch.gpu()
    tensor_dict['bboxes'] = fn._conditional.merge(
        result_true, result_false, predicate=do_multiply)

    if 'vertices' in tensor_dict:
        vertices_true_branch, vertices_false_branch = fn._conditional.split(
            tensor_dict["vertices"], predicate=do_multiply)
        vertices_true_res = vertices_true_branch.gpu() * wh
        vertices_false_res = vertices_false_branch.gpu()
        tensor_dict['vertices'] = fn._conditional.merge(
            vertices_true_res, vertices_false_res, predicate=do_multiply)

    return tensor_dict


def permute(tensor_dict: dict):
    """
    hwc2chw

    Args:
        tensor_dict (dict): _description_

    Returns:
        dict: _description_
    """
    tensor_dict['images'] = fn.transpose(tensor_dict['images'], perm=[2, 0, 1])

    if "templates" in tensor_dict:
        tensor_dict['templates'] = fn.transpose(
            tensor_dict['templates'], perm=[2, 0, 1])
    return tensor_dict
