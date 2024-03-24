#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : config.py    
@Author        : yanxiaodong
@Date          : 2022/12/20
@Description   :
"""
import os
import warnings
from typing import Any, Dict, List, Optional, Union, Callable, Tuple

import yaml


def parse_config(cfg_file: str) -> Dict:
    """
    It loads a config file
    
    :param cfg_file: The path to the config file
    :type cfg_file: str
    :return: A dictionary of the config file
    """
    with open(cfg_file, 'r') as f:
        yaml_config = yaml.load(f, Loader=yaml.SafeLoader)

    return yaml_config


def override(dl: Union[List, Dict], ks: List, v: Any):
    """
    It takes a dictionary or list, a list of keys, and a value, and recursively replaces the value at the end of the key
    list
    
    :param dl: the dict or list to be overridden
    :type dl: Union[List, Dict]
    :param ks: the keys of the dict or list
    :type ks: List
    :param v: the value to be set
    :type v: Any
    """

    def str2num(v):
        try:
            return eval(v)
        except Exception:
            return v

    assert isinstance(dl, (list, dict)), '{} should be a list or a dict'
    assert len(ks) > 0, 'lenght of keys should larger than 0'
    if isinstance(dl, list):
        k = str2num(ks[0])
        if len(ks) == 1:
            assert k < len(dl), 'index({}) out of range({})'.format(k, dl)
            dl[k] = str2num(v)
        else:
            override(dl[k], ks[1:], v)
    else:
        if len(ks) == 1:
            if not ks[0] in dl:
                warnings.warn('A new filed ({}) detected!'.format(ks[0]))
            dl[ks[0]] = str2num(v)
        else:
            override(dl[ks[0]], ks[1:], v)


def override_config(config: Dict, options: Optional[List] = None) -> Dict:
    """
    It takes a dictionary and a list of strings, and returns a dictionary
    
    :param config: The config dictionary to override
    :type config: Dict
    :param options: List of options to override the config
    :type options: Optional[List]
    :return: A dictionary with the values of the config file and the values of the command line options.
    """
    if options is not None:
        for opt in options:
            assert isinstance(opt, str), ('option({}) should be a str'.format(opt))
            assert "=" in opt, ('option({}) should contain a = to distinguish between key and value'.format(opt))
            pair = opt.split('=')
            assert len(pair) == 2, 'there can be only a = in the option'
            key, value = pair
            if value is not None and len(value) > 0:
                keys = key.split('.')
                override(config, keys, value)
    return config


def train_config(base_model_uri: str = '',
                 model_config_file: str = 'parameters.yaml',
                 config_load_callback: Optional[Callable] = None) -> Tuple:
    """
     Read config from file, and override the config with the overrides.

    :param model_config_file: base model file.
    :type model_config_file: Optional[str]
    :param model_config_file: model config file.
    :type model_config_file: Optional[str]
    :param config_load_callback: `config_load_callback` is a function that loads the configuration of
    a corresponding suite library.
    :return: a tuple containing three elements: the original config dictionary, the model config dictionary (if the
    `config_load_callback` parameter is not `None`), and the model config save dictionary (if the `config_load_callback`
    parameter is not `None`).
    """
    root_dir = os.getcwd()
    commit_id_file = os.path.join(root_dir, 'version.txt')
    if os.path.isfile(commit_id_file):
        commit_id = open(commit_id_file, 'r').read()
        os.environ['COMMIT_ID'] = commit_id

    model_config = {}
    model_config_save = {}
    if config_load_callback is not None:
        pretrain_weight, model_config, model_config_save = config_load_callback(model_config_file)

    base_model_uri = base_model_uri if base_model_uri and len(base_model_uri) > 0 else pretrain_weight

    return base_model_uri, model_config, model_config_save


def eval_config(base_model_uri: str,
                model_config_file: str = None,
                overrides: Optional[List] = None,
                config_load_callback: Optional[Callable] = None) -> Tuple:
    """
     Read config from file, and override the config with the overrides.

    :param file: the path to the config file.
    :type file: str
    :param overrides: a dictionary of parameters that will override the parameters in the config file.
    :type overrides: Optional[List]
    :param config_load_callback: `config_load_callback` is a function that loads the configuration of
    a corresponding suite library.
    :return: a tuple containing three elements: the original config dictionary, the model config dictionary (if the
    `config_load_callback` parameter is not `None`), and the model config save dictionary (if the `config_load_callback`
    parameter is not `None`).
    """
    root_dir = os.getcwd()
    commit_id_file = os.path.join(root_dir, 'version.txt')
    if os.path.isfile(commit_id_file):
        commit_id = open(commit_id_file, 'r').read()
        os.environ['COMMIT_ID'] = commit_id

    assert base_model_uri is not None and len(base_model_uri) > 0, 'base_model_uri is missing for model evaluation,'
    'please set base_model_uri using --model_base_path argument.'
    
    if os.path.isfile(base_model_uri):
        model_dir = os.path.dirname(base_model_uri)
    elif os.path.isdir(base_model_uri):
        model_dir = base_model_uri
    else:
        raise ValueError(f'base_model_uri: {base_model_uri} is not exist, please set correct path.')
    
    model_weight = base_model_uri

    if model_config_file is None:
        model_config_file = os.path.join(model_dir, 'parameters.yaml')

    categories = []
    meta_path = os.path.join(model_dir, 'meta.yaml')
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            meta_data = yaml.safe_load(f)
            if "labels" in meta_data:
                categories = meta_data["labels"]
            elif "categories" in meta_data:
                categories = meta_data["categories"]

    model_config = {}
    model_config_save = {}
    if config_load_callback is not None:
        _, model_config, model_config_save = config_load_callback(
            model_config_file,
            num_classes=len(categories) if len(categories) > 0 else None)

    model_config["categories"] = categories

    return model_weight, model_config, model_config_save
