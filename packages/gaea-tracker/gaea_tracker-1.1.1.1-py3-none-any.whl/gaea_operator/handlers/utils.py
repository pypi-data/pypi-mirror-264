#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : utils.py    
@Author        : yanxiaodong
@Date          : 2022/12/1
@Description   :
"""
import base64
import binascii
import hashlib
import os
import shutil
import sys
import tarfile
import time
import zipfile
from typing import Any, Callable, Dict, Optional

import numpy as np
import requests
import tqdm

from gaea_operator.engine import Engine, Events
from gaea_operator.handlers.model_ema import PaddleModelEMA
from gaea_operator.plugin import POptimizer, paddle, Layer
from gaea_operator.utils.misc import is_url
import gaea_operator.distributed as idist


def global_step_from_engine(engine: Engine, custom_event_name: Optional[Events] = None) -> Callable:
    """Helper method to setup `global_step_transform` function using another engine.
    This can be helpful for logging trainer epoch/iteration while output handler is attached to an evaluator.
    Args:
        engine: engine which state is used to provide the global step
        custom_event_name: registered event name. Optional argument, event name to use.
    Returns:
        global step based on provided engine
    """

    def wrapper(_: Any, event_name: Events) -> int:
        if custom_event_name is not None:
            event_name = custom_event_name
        return engine.state.get_event_attrib_value(event_name)

    return wrapper


WEIGHTS_HOME = os.path.expanduser("~/.cache/paddle/weights")
DOWNLOAD_RETRY_LIMIT = 3


def map_path(url, root_dir, path_depth=1):
    """
    parse path after download to decompress under root_dir.
    """
    assert path_depth > 0, 'path_depth should be a positive integer'
    dirname = url
    for _ in range(path_depth):
        dirname = os.path.dirname(dirname)
    fpath = os.path.relpath(url, dirname)

    zip_formats = ['.zip', '.tar', '.gz']
    for zip_format in zip_formats:
        fpath = fpath.replace(zip_format, '')
    return os.path.join(root_dir, fpath)


def _md5check(fullname, md5sum=None):
    if md5sum is None:
        return True

    md5 = hashlib.md5()
    with open(fullname, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    calc_md5sum = md5.hexdigest()

    if calc_md5sum != md5sum:
        return False
    return True


def _md5check_from_url(filename, url):
    req = requests.get(url, stream=True)
    content_md5 = req.headers.get('content-md5')
    req.close()
    if not content_md5 or _md5check(filename, binascii.hexlify(base64.b64decode(content_md5.strip('"'))).decode()):
        return True
    else:
        return False


def _check_exist_file_md5(filename, md5sum, url):
    return _md5check_from_url(filename, url) if md5sum is None and filename.endswith('pdparams') \
        else _md5check(filename, md5sum)


def _download(url, path, md5sum=None):
    if not os.path.exists(path):
        os.makedirs(path)

    fname = os.path.split(url)[-1]
    fullname = os.path.join(path, fname)
    retry_cnt = 0

    while not (os.path.exists(fullname) and _check_exist_file_md5(fullname, md5sum, url)):
        if retry_cnt < DOWNLOAD_RETRY_LIMIT:
            retry_cnt += 1
        else:
            raise RuntimeError("Download from {} failed, Retry limit reached".format(url))

        # NOTE: windows path join may incur \, which is invalid in url
        if sys.platform == "win32":
            url = url.replace('\\', '/')

        req = requests.get(url, stream=True)
        if req.status_code != 200:
            raise RuntimeError("Downloading from {} failed with code {}!".format(url, req.status_code))

        # For protecting download interupted, download to
        # tmp_fullname firstly, move tmp_fullname to fullname
        # after download finished
        tmp_fullname = fullname + "_tmp"
        total_size = req.headers.get('content-length')
        with open(tmp_fullname, 'wb') as f:
            if total_size:
                for chunk in tqdm.tqdm(
                        req.iter_content(chunk_size=1024),
                        total=(int(total_size) + 1023) // 1024,
                        unit='KB'):
                    f.write(chunk)
            else:
                for chunk in req.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        try:
            shutil.move(tmp_fullname, fullname)
        except FileNotFoundError:
            pass
    return fullname


def _download_dist(url: str, path: str, md5sum: Optional[str] = None):
    env = os.environ
    if 'PADDLE_TRAINERS_NUM' in env and 'PADDLE_TRAINER_ID' in env:
        # Mainly used to solve the problem of downloading data from
        # different machines in the case of multiple machines.
        # Different nodes will download data, and the same node
        # will only download data once.
        # Reference https://github.com/PaddlePaddle/PaddleClas/blob/release/2.5/ppcls/utils/download.py#L108
        rank_id_curr_node = idist.get_rank()
        num_trainers = idist.get_world_size()
        if num_trainers <= 1:
            return _download(url, path, md5sum)
        else:
            fname = os.path.split(url)[-1]
            fullname = os.path.join(path, fname)
            lock_path = fullname + '.download.lock'

            if not os.path.isdir(path):
                os.makedirs(path, exist_ok=True)

            if not os.path.exists(fullname):
                with open(lock_path, 'w'):  # touch
                    os.utime(lock_path, None)
                if rank_id_curr_node == 0:
                    _download(url, path, md5sum)
                    os.remove(lock_path)
                else:
                    while os.path.exists(lock_path):
                        time.sleep(0.5)
            return fullname
    else:
        return _download(url, path, md5sum)


def _move_and_merge_tree(src: str, dst: str):
    if not os.path.exists(dst):
        shutil.move(src, dst)
    elif os.path.isfile(src):
        shutil.move(src, dst)
    else:
        for fp in os.listdir(src):
            src_fp = os.path.join(src, fp)
            dst_fp = os.path.join(dst, fp)
            if os.path.isdir(src_fp):
                if os.path.isdir(dst_fp):
                    _move_and_merge_tree(src_fp, dst_fp)
                else:
                    shutil.move(src_fp, dst_fp)
            elif os.path.isfile(src_fp) and \
                    not os.path.isfile(dst_fp):
                shutil.move(src_fp, dst_fp)


def _decompress(fname: str):
    fpath = os.path.split(fname)[0]
    fpath_tmp = os.path.join(fpath, 'tmp')
    if os.path.isdir(fpath_tmp):
        shutil.rmtree(fpath_tmp)
        os.makedirs(fpath_tmp)

    if fname.find('tar') >= 0:
        with tarfile.open(fname) as tf:
            tf.extractall(path=fpath_tmp)
    elif fname.find('zip') >= 0:
        with zipfile.ZipFile(fname) as zf:
            zf.extractall(path=fpath_tmp)
    elif fname.find('.txt') >= 0:
        return
    else:
        raise TypeError("Unsupport compress file type {}".format(fname))

    for f in os.listdir(fpath_tmp):
        src_dir = os.path.join(fpath_tmp, f)
        dst_dir = os.path.join(fpath, f)
        _move_and_merge_tree(src_dir, dst_dir)

    shutil.rmtree(fpath_tmp)
    os.remove(fname)


def _decompress_dist(fname: str):
    env = os.environ
    if 'PADDLE_TRAINERS_NUM' in env and 'PADDLE_TRAINER_ID' in env:
        trainer_id = int(env['PADDLE_TRAINER_ID'])
        num_trainers = int(env['PADDLE_TRAINERS_NUM'])
        if num_trainers <= 1:
            _decompress(fname)
        else:
            lock_path = fname + '.decompress.lock'
            from paddle.distributed import ParallelEnv
            unique_endpoints = paddle.utils.download._get_unique_endpoints(ParallelEnv().trainer_endpoints[:])
            # NOTE(dkp): _decompress_dist always performed after
            # _download_dist, in _download_dist sub-trainers is waiting
            # for download lock file release with sleeping, if decompress
            # prograss is very fast and finished with in the sleeping gap
            # time, e.g in tiny dataset such as coco_ce, spine_coco, main
            # trainer may finish decompress and release lock file, so we
            # only craete lock file in main trainer and all sub-trainer
            # wait 1s for main trainer to create lock file, for 1s is
            # twice as sleeping gap, this waiting time can keep all
            # trainer pipeline in order
            # **change this if you have more elegent methods**
            if ParallelEnv().current_endpoint in unique_endpoints:
                with open(lock_path, 'w'):  # touch
                    os.utime(lock_path, None)
                _decompress(fname)
                os.remove(lock_path)
            else:
                time.sleep(1)
                while os.path.exists(lock_path):
                    time.sleep(0.5)
    else:
        _decompress(fname)


def get_weights_path(url: str, md5sum: Optional[str] = None, check_exist: Optional[bool] = True):
    """
    Get weights path from WEIGHTS_HOME, if not exists, download it from url.
    """
    # parse path after download to decompress under root_dir
    fullpath = map_path(url, WEIGHTS_HOME)

    if os.path.exists(fullpath) and check_exist:
        if not os.path.isfile(fullpath) or _check_exist_file_md5(fullpath, md5sum, url):
            return fullpath
        else:
            os.remove(fullpath)

    fullname = _download_dist(url, WEIGHTS_HOME, md5sum)

    # new weights format which postfix is 'pdparams' not need to decompress
    if os.path.splitext(fullname)[-1] not in ['.pdparams', '.yml']:
        _decompress_dist(fullname)

    return fullpath


def _strip_postfix(path: str):
    # 如果给定路径是文件夹，模型权重，优化器权重文件名必须相同
    if os.path.isdir(path):
        for file in os.listdir(path):
            file = os.path.join(path, file)
            if file.endswith(('.pdparams', '.pdopt', '.pdmodel')):
                path, ext = os.path.splitext(file)
                return path
        raise 'Unknown weights path: {}, weights file postfix must be in {}'.format(path,
                                                                                    ['.pdparams', '.pdopt', '.pdmodel'])

    # 如果给定是文件，可以不包含后缀
    path, ext = os.path.splitext(path)
    assert ext in ['', '.pdparams', '.pdopt', '.pdmodel'], 'Unknown postfix {} from weights'.format(ext)
    return path


def match_state_dict(model_state_dict: Dict, weight_state_dict: Dict):
    """
    Match between the model state dict and pretrained weight state dict.
    """

    model_keys = sorted(model_state_dict.keys())
    weight_keys = sorted(weight_state_dict.keys())

    def match(a, b):
        if b.startswith('backbone.res5'):
            # In Faster RCNN, res5 pretrained weights have prefix of backbone,
            # however, the corresponding model weights have difficult prefix,
            # bbox_head.
            b = b[9:]
        return a == b or a.endswith("." + b)

    match_matrix = np.zeros([len(model_keys), len(weight_keys)])
    for i, m_k in enumerate(model_keys):
        for j, w_k in enumerate(weight_keys):
            if match(m_k, w_k):
                match_matrix[i, j] = len(w_k)
    max_id = match_matrix.argmax(1)
    max_len = match_matrix.max(1)
    max_id[max_len == 0] = -1

    load_id = set(max_id)
    load_id.discard(-1)
    not_load_weight_name = []
    for idx in range(len(weight_keys)):
        if idx not in load_id:
            not_load_weight_name.append(weight_keys[idx])

    matched_keys = {}
    result_state_dict = {}
    for model_id, weight_id in enumerate(max_id):
        if weight_id == -1:
            continue
        model_key = model_keys[model_id]
        weight_key = weight_keys[weight_id]
        weight_value = weight_state_dict[weight_key]
        model_value_shape = list(model_state_dict[model_key].shape)

        if list(weight_value.shape) != model_value_shape:
            continue

        assert model_key not in result_state_dict
        result_state_dict[model_key] = weight_value
        if weight_key in matched_keys:
            raise ValueError('Ambiguity weight {} loaded, it matches at least '
                             '{} and {} in the model'.format(weight_key, model_key, matched_keys[weight_key]))
        matched_keys[weight_key] = model_key
    return result_state_dict


def paddle_load_pretrain_weight(model: Layer, pretrain_weight: str):
    if is_url(pretrain_weight):
        pretrain_weight = get_weights_path(pretrain_weight)
    else:
        # 拼接路径
        if os.path.isdir(pretrain_weight):
            if os.path.exists(os.path.join(pretrain_weight, 'best.pdparams')):
                pretrain_weight = os.path.join(pretrain_weight, 'best.pdparams')
            else:
                raise ValueError('pretrain_weight: {} is missing file `best.pdparams` for PaddlePaddle or `best.pt` for Torch,'
                                'please save model weight file in pretrain_weight.'.format(pretrain_weight))
        elif not os.path.isfile(pretrain_weight):
            raise ValueError('pretrain_weight: {} is not exist, please set a valid pretrain_weight.'.format(pretrain_weight))        

    path = _strip_postfix(pretrain_weight)
    if not (os.path.isdir(path) or os.path.isfile(path) or os.path.exists(path + '.pdparams')):
        raise ValueError("Model pretrain path `{}` does not exists. "
                         "If you don't want to load pretrain model, "
                         "please delete `pretrain_weights` field in "
                         "config file.".format(path))

    model_dict = model.state_dict()

    weights_path = path + '.pdparams'
    param_state_dict = paddle.load(weights_path)
    param_state_dict = match_state_dict(model_dict, param_state_dict)

    for k, v in param_state_dict.items():
        if isinstance(v, np.ndarray):
            v = paddle.to_tensor(v)
        if model_dict[k].dtype != v.dtype:
            param_state_dict[k] = v.astype(model_dict[k].dtype)

    model.set_dict(param_state_dict)


def paddle_load_resume_weight(model: Layer,
                              weight: str,
                              optimizer: Optional[POptimizer] = None,
                              ema: Optional[PaddleModelEMA] = None):
    if is_url(weight):
        weight = get_weights_path(weight)

    path = _strip_postfix(weight)
    pdparam_path = path + '.pdparams'
    if not os.path.exists(pdparam_path):
        raise ValueError('Model pretrain path {} does not exists.'.format(pdparam_path))

    if ema and os.path.exists(path + '.pdema'):
        # Exchange model and ema_model to load
        ema_state_dict = paddle.load(pdparam_path)
        param_state_dict = paddle.load(path + '.pdema')
    else:
        ema_state_dict = None
        param_state_dict = paddle.load(pdparam_path)

    model_dict = model.state_dict()
    pretrain_weight = {}
    incorrect_keys = 0

    for key, value in model_dict.items():
        if key in param_state_dict.keys():
            if isinstance(param_state_dict[key], np.ndarray):
                pretrain_weight[key] = paddle.to_tensor(param_state_dict[key])
            if value.dtype == param_state_dict[key].dtype:
                pretrain_weight[key] = param_state_dict[key]
            else:
                pretrain_weight[key] = param_state_dict[key].astype(value.dtype)
        else:
            incorrect_keys += 1

    assert incorrect_keys == 0, 'Load weight {} incorrectly, {} keys unmatched, please check again.'. \
        format(weight, incorrect_keys)

    model.set_dict(pretrain_weight)

    last_epoch = 0
    if optimizer is not None and os.path.exists(path + '.pdopt'):
        optim_state_dict = paddle.load(path + '.pdopt')
        # to solve resume bug, will it be fixed in paddle 2.0
        if isinstance(optimizer, list):
            for i in range(len(optimizer)):
                for key in optimizer[i].state_dict().keys():
                    if key not in optim_state_dict[i].keys():
                        optim_state_dict[i][key] = optimizer[i].state_dict()[key]
                if 'last_epoch' in optim_state_dict[i]:
                    last_epoch = optim_state_dict[i].pop('last_epoch')
                optimizer[i].set_state_dict(optim_state_dict[i])
        else:
            for key in optimizer.state_dict().keys():
                if key not in optim_state_dict.keys():
                    optim_state_dict[key] = optimizer.state_dict()[key]
            if 'last_epoch' in optim_state_dict:
                last_epoch = optim_state_dict.pop('last_epoch')
            optimizer.set_state_dict(optim_state_dict)

        if ema_state_dict is not None:
            ema.resume(ema_state_dict, optim_state_dict['LR_Scheduler']['last_epoch'])
    elif ema_state_dict is not None:
        ema.resume(ema_state_dict)

    return last_epoch
