#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : cli.py
@Author        : yanxiaodong
@Date          : 2023/6/6
@Description   :
"""
import json
import os
from typing import Any, Callable, Optional, List
import importlib

import yaml
from jsonargparse import ArgumentParser, ActionConfigFile, Namespace

from gaea_operator.trainer import TrainerArgument, StrategyArgument
from gaea_operator.data.source.base import DatasetArgument
from gaea_operator.handlers.metric_logger import ExperimentTrackerArgument
from gaea_operator.utils import MOUNT_PATH, PRODUCT_PATH, FILESYSTEM
from gaea_operator.distributed import setup_spawn_params, Parallel, set_model_type
from gaea_operator.user import UserSetting


class GaeaArgumentParser(ArgumentParser):
    """
    Extension of jsonargparse's ArgumentParser for Training and Evaluating.
    """

    def __init__(self,
                 *args: Any,
                 description: str = "Gaea trainer command line tool",
                 env_prefix: str = "GAEA",
                 default_env: bool = True,
                 default_config_files: Optional[List[str]] = ['config.yaml'],
                 **kwargs: Any) -> None:
        super(GaeaArgumentParser, self).__init__(*args,
                                                 description=description,
                                                 env_prefix=env_prefix,
                                                 default_env=default_env,
                                                 default_config_files=default_config_files,
                                                 **kwargs)

        self.env_prefix = env_prefix
        self.trainer_nested_key = 'trainer'
        self.dataset_nested_key = 'dataset'
        self.experiment_nested_key = 'experiment'
        self.strategy_nested_key = 'strategy'
        self.default_nested_key = 'default'
        self.user_nested_key = 'user'

        # 设置环境变量
        if default_env:
            self._init_env()

        # 通过class设置parser arguments
        self.setup_parser()

    def _init_env(self) -> None:
        # ppl 与 参数映射定义
        if os.environ.get('JOB_NAME', None) is not None:
            os.environ['RUN_NAME'] = os.environ['JOB_NAME']

        experiment_env_names = ('EXPERIMENT_KIND', 'EXPERIMENT_NAME', 'TRACKING_URI', 'RUN_NAME')
        dataset_env_names = ('DATASET_URI',)
        trainer_env_names = ('BACKEND',)
        default_env_names = ('BASE_MODEL_URI', 'OUTPUT_URI', 'DEBUG')
        user_env_names = ('AK', 'SK', 'ENDPOINT')

        env_names = {self.trainer_nested_key: trainer_env_names,
                     self.dataset_nested_key: dataset_env_names,
                     self.experiment_nested_key: experiment_env_names,
                     self.default_nested_key: default_env_names,
                     self.user_nested_key: user_env_names,
                     }

        for nested_key in env_names:
            if nested_key == self.default_nested_key:
                for name in env_names[nested_key]:
                    if os.environ.get(name, None) is not None:
                        new_name = self.env_prefix + '_' + name
                        os.environ[new_name] = os.environ[name]
            else:
                for name in env_names[nested_key]:
                    if os.environ.get(name, None) is not None:
                        new_name = self.env_prefix + '_' + nested_key.upper() + '__' + name
                        os.environ[new_name] = os.environ[name]

    def _set_env(self, config: Namespace) -> None:
        config = config.as_dict()
        for name, value in config.items():
            if isinstance(value, dict):
                for subname, subvalue in value.items():
                    new_name = self.env_prefix + '_' + name.upper() + '__' + subname.upper()
                    if os.environ.get(new_name, 'no_env_name') == 'no_env_name':
                        os.environ[new_name] = str(subvalue)
            else:
                new_name = self.env_prefix + '_' + name.upper()
                if os.environ.get(new_name, 'no_env_name') == 'no_env_name':
                    os.environ[new_name] = str(value)

    def setup_parser(self) -> None:
        self.add_argument('-c',
                          '--config',
                          action=ActionConfigFile,
                          help='Path to a configuration file in yaml format')
        self.add_argument('--debug',
                          type=bool,
                          default=False,
                          help='Debug')
        self.add_argument('--output_uri',
                          type=str,
                          default='.',
                          help='Output dir for model checkpoint or eval predict')
        self.add_argument('--base_model_uri',
                          type=str,
                          help='Base model uri for pretrain or eval')
        self.add_argument('--is_copy_log',
                          type=bool,
                          default=True,
                          help='Copy log to fs')

        self.add_argument('--parameter_uri.train',
                          type=str,
                          default='parameters.yaml',
                          help='Build model config for train')
        self.add_argument('--parameter_uri.eval',
                          type=str,
                          help='Build model config for eval')

        self.add_argument('--module',
                          type=str,
                          nargs='*',
                          default=None,
                          help='Custom function'
                          )

        self.add_class_arguments(TrainerArgument, nested_key=self.trainer_nested_key, fail_untyped=False,
                                 instantiate=False, sub_configs=False)

        self.add_class_arguments(StrategyArgument, nested_key=self.strategy_nested_key, fail_untyped=False,
                                 instantiate=False, sub_configs=False)

        self.add_class_arguments(DatasetArgument, nested_key=self.dataset_nested_key, fail_untyped=False,
                                 instantiate=False, sub_configs=False)

        self.add_class_arguments(ExperimentTrackerArgument, nested_key=self.experiment_nested_key, fail_untyped=False,
                                 instantiate=False, sub_configs=False)

        self.add_class_arguments(UserSetting, nested_key=self.user_nested_key, fail_untyped=False,
                                 instantiate=False, sub_configs=False)

    def _join_mount_path(self, config):
        config.output_uri = os.path.join(MOUNT_PATH, config.output_uri)
        if config.base_model_uri and len(config.base_model_uri) > 0:
            config.base_model_uri = os.path.join(MOUNT_PATH, config.base_model_uri)
        dataset_uri = config.dataset.dataset_uri.split(',')
        for i in range(len(dataset_uri)):
            dataset_uri[i] = os.path.join(MOUNT_PATH, dataset_uri[i])
        config.dataset.dataset_uri = ','.join(dataset_uri)

        return config

    def parse_arguments(self) -> Namespace:
        config = self.parse_args()

        self._set_env(config=config)

        config = self._join_mount_path(config=config)

        if not os.path.exists(config.output_uri):
            os.makedirs(config.output_uri)
        self.save(config, os.path.join(config.output_uri, 'config.yaml'), skip_none=False, overwrite=True)

        if 'validation_split' in config.dataset.as_dict():
            validation_split = config.dataset.validation_split.strip('{').strip('}')
            validation_split = validation_split.split(':')
            config.dataset.validation_split = {validation_split[0]: validation_split[1]}

            if "dataset_names" in config.dataset.validation_split:
                from gaea_operator.plugins import artifact_client, compute_client

                assert artifact_client is not None, "When get data uri, the artifact_client must be not None."

                dataset_names = config.dataset.validation_split.pop("dataset_names")
                dataset_uri = self._parse_dataset_name_get_uri(dataset_names=dataset_names)

                config.dataset.validation_split["dataset_uri"] = dataset_uri

        if config.dataset.dataset_names is not None and len(config.dataset.dataset_names) > 0:
            dataset_uri = self._parse_dataset_name_get_uri(dataset_names=config.dataset.dataset_names)

            config.dataset.dataset_uri = dataset_uri

        return config

    def _parse_dataset_name_get_uri(self, dataset_names: str):
        from gaea_operator.plugins import artifact_client, compute_client

        assert artifact_client is not None, "When get data uri, the artifact_client must be not None."
        dataset_names = dataset_names.split(",")
        dataset_uri = []
        # 通过 windmill sdk 获取name对应的数据路径,
        for name in dataset_names:
            workspace_id = name.split("/")[1]
            name = name.split("/versions/")
            version = name[1].split("/")[0]
            response = artifact_client.get_artifact(version=version, object_name=name[0])
            assert response.parent_name is not None, "Artifact get response {} parent name is none, " \
                                                     "please check your version {} and object name {}".format(response,
                                                                                                              version,
                                                                                                              name[0])
            guest_name = response.parent_name
            if compute_client is not None:
                fs_response = compute_client.suggest_filesystem(guest_name=guest_name, workspace_id=workspace_id)
                assert len(fs_response.file_systems) > 0, "Suggest response length is zero, " \
                                                          "please check your workspace_id: {} and guest_name: {}". \
                    format(workspace_id, guest_name)
                file_system = fs_response.file_systems[0]
                os.environ["FS_ENDPOINT"] = file_system.kind + "://" + file_system.endpoint + "/"
                uri = os.path.relpath(response.uri, file_system.kind + "://" + file_system.endpoint)
            else:
                uri = response.uri
            meta_file = os.path.join(MOUNT_PATH, uri, "meta.yaml")
            with open(meta_file, "r") as f:
                meta = yaml.load(f, Loader=yaml.Loader)
            for path in meta["paths"]:
                if compute_client is not None:
                    path = os.path.relpath(path, file_system.kind + "://" + file_system.endpoint)

                dataset_uri.append(path)
        dataset_uri = list(set(dataset_uri))

        return ",".join(dataset_uri)

    def instantiate_function(self, config: Namespace):
        if config.module is not None:
            for name in config.module:
                module = importlib.import_module(name)
                config = getattr(module, name)(config)

        return config

    def instantiate_user_setting(self, config: Namespace):
        from gaea_operator.user import UserSetting
        UserSetting(**config.user.as_dict())


def entry(func: Callable, backend: str = None, args: GaeaArgumentParser = None):
    """
    Run the same code across all supported distributed backends in a seamless manner.
    """
    if args is None:
        args = GaeaArgumentParser()

    config = args.parse_arguments()

    # 日志处理
    if config.is_copy_log:
        source_log_dir = 'log'
        dest_log_dir = os.path.join(PRODUCT_PATH, 'log')
    else:
        source_log_dir = os.path.join(PRODUCT_PATH, 'log')
        dest_log_dir = os.path.join(PRODUCT_PATH, 'log')
    os.environ['GAEA_LOG_DIR'] = source_log_dir

    config = args.instantiate_function(config)
    args.instantiate_user_setting(config)

    if backend is not None:
        config.trainer.backend = backend

    backend = config.trainer.backend
    model_type = config.trainer.model_type

    spawn_params = setup_spawn_params(backend=backend, **config.strategy)

    if spawn_params['nproc_per_node'] == 1 and config.debug:
        set_model_type(value=model_type)
        func(config)
    else:
        with Parallel(backend=backend, model_type=model_type, is_copy_log=config.is_copy_log,
                      source_log_dir=source_log_dir, dest_log_dir=dest_log_dir, **spawn_params) as parallel:
            parallel.run(func=func, args=config)
