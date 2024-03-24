#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : dali.py    
@Author        : xuningyuan
@Date          : 2022/11/25
@Description   :
"""
import ctypes

import numpy as np

from gaea_operator.plugin import (Pipeline, PTensor, TensorCPU, TensorListCPU,
                                   TensorListGPU, TTensor, fn, paddle, torch,
                                   types)


class TypeConv(object):
    """进行数据类型转换

    Returns:
        _type_: _description_
    """
    if types is not None:
        if paddle is not None:
            to_paddle_type = {
                types.DALIDataType.BOOL:    paddle.bool,
                types.DALIDataType.FLOAT:   paddle.float32,
                types.DALIDataType.FLOAT64: paddle.float64,
                types.DALIDataType.FLOAT16: paddle.float16,
                types.DALIDataType.UINT8:   paddle.uint8,
                types.DALIDataType.INT8:    paddle.int8,
                types.DALIDataType.INT16:   paddle.int16,
                types.DALIDataType.INT32:   paddle.int32,
                types.DALIDataType.INT64:   paddle.int64
            }
        if torch is not None:
            to_torch_type = {
                types.DALIDataType.FLOAT:   torch.float32,
                types.DALIDataType.FLOAT64: torch.float64,
                types.DALIDataType.FLOAT16: torch.float16,
                types.DALIDataType.UINT8:   torch.uint8,
                types.DALIDataType.INT8:    torch.int8,
                types.DALIDataType.INT16:   torch.int16,
                types.DALIDataType.INT32:   torch.int32,
                types.DALIDataType.INT64:   torch.int64
            }


def feed_paddle_tensor(dali_tensor, device=None) -> PTensor:
    """
    Copy contents of DALI tensor to Paddle's Tensor.

    Parameters
    ----------
    `dali_tensor` : nvidia.dali.backend.TensorCPU or nvidia.dali.backend.TensorGPU
                    Tensor from which to copy
    `device` : device id If device is None, the device is the current device. Default: None.
    """
    if isinstance(dali_tensor, (TensorListGPU, TensorListCPU)):
        dali_tensor = dali_tensor.as_tensor()
        
    if isinstance(dali_tensor, TensorCPU):
        return paddle.to_tensor(np.asarray(dali_tensor))
    
    paddle_type = TypeConv.to_paddle_type[dali_tensor.dtype]
    arr = paddle.empty(dali_tensor.shape(), paddle_type)

    cuda_stream = paddle.device.cuda.current_stream(device=device)
    cuda_stream = types._raw_cuda_stream(cuda_stream)

    # turn raw int to a c void pointer
    c_type_pointer = ctypes.c_void_p(arr.value().get_tensor()._ptr())
    stream = None if cuda_stream is None else ctypes.c_void_p(cuda_stream)
    dali_tensor.copy_to_external(c_type_pointer, stream, non_blocking=True)
    return arr


def feed_torch_tensor(dali_tensor, device=None) -> TTensor:
    """
    Copy contents of DALI tensor to Paddle's Tensor.

    Parameters
    ----------
    `dali_tensor` : nvidia.dali.backend.TensorCPU or nvidia.dali.backend.TensorGPU
                    Tensor from which to copy
    `device` : device id If device is None, the device is the current device. Default: None.
    """
    if isinstance(dali_tensor, (TensorListGPU, TensorListCPU)):
        dali_tensor = dali_tensor.as_tensor()
        
    if isinstance(dali_tensor, TensorCPU):
        return torch.as_tensor(np.asarray(dali_tensor))
    
    torch_type = TypeConv.to_torch_type[dali_tensor.dtype]
    arr = torch.empty(dali_tensor.shape(), torch_type)

    cuda_stream = torch.cuda.current_stream(device=device)
    cuda_stream = types._raw_cuda_stream(cuda_stream)

    # turn raw int to a c void pointer
    c_type_pointer = ctypes.c_void_p(arr.data_ptr())
    stream = None if cuda_stream is None else ctypes.c_void_p(cuda_stream)
    dali_tensor.copy_to_external(c_type_pointer, stream, non_blocking=True)
    return arr


def build_det_pipeline(transforms: list, params: list, batch_size=32, num_threads=4, device_id=0, seed=-1,
                       anno_path="example/annotation.json", file_root="example/images", polygon_masks=True):
    """创建检测pipeline

    Args:
        transforms (list): _description_
        params (list): _description_
        batch_size (int, optional): _description_. Defaults to 32.
        num_threads (int, optional): _description_. Defaults to 4.
        device_id (int, optional): _description_. Defaults to 0.
        seed (int, optional): _description_. Defaults to -1.

    Returns:
        _type_: _description_
    """
    pipeline = Pipeline(batch_size=batch_size, num_threads=num_threads, device_id=device_id, seed=seed)
    with pipeline:
        images, bboxes, labels, polygons, vertices = fn.readers.coco(
            file_root=file_root,
            annotations_file=anno_path,
            skip_empty=False,
            shard_id=0,
            num_shards=1,
            ratio=True,
            ltrb=True,
            random_shuffle=False,
            name="Reader",
            polygon_masks=polygon_masks
        )
        if polygon_masks:
            tensor_dict = {"images": images, "bboxes": bboxes, "labels": labels, "polygons": polygons, "vertices": vertices}
        for transform, kwargs in zip(transforms, params):
            tensor_dict = transform(tensor_dict, **kwargs)
        pipeline.set_outputs(*tuple(tensor_dict.values()))
    pipeline.build()
    return pipeline


def build_image_only_pipeline(transforms: list, params: list, batch_size=32, num_threads=4, device_id=0, seed=-1):
    """创建image pipeline

    Args:
        transforms (list): _description_
        params (list): _description_
        batch_size (int, optional): _description_. Defaults to 32.
        num_threads (int, optional): _description_. Defaults to 4.
        device_id (int, optional): _description_. Defaults to 0.
        seed (int, optional): _description_. Defaults to -1.

    Returns:
        _type_: _description_
    """
    pipeline = Pipeline(batch_size=batch_size, num_threads=num_threads, device_id=device_id, seed=seed)
    with pipeline:
        images, _ = fn.readers.file(file_root='example/images')
        tensor_dict = {"images": images}
        for transform, kwargs in zip(transforms, params):
            tensor_dict = transform(tensor_dict, **kwargs)
        pipeline.set_outputs(*tuple(tensor_dict.values()))
    pipeline.build()
    return pipeline
