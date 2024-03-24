#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : launcher.py    
@Author        : yanxiaodong
@Date          : 2023/5/17
@Description   :
"""
import os
from typing import Optional, Any, Callable
import traceback
from argparse import Namespace
from threading import Thread
import shutil
import time

from .utils import _assert_backend, setup_spawn_params, spawn
from gaea_operator.utils import setup_logger, IMAGE_OBJECT_DETECTION, train_config


class Parallel(object):
    """
    Distributed launcher context manager to simplify distributed configuration setup for multiple backends.

    """

    def __init__(
            self,
            backend: Optional[str],
            model_type: Optional[str] = IMAGE_OBJECT_DETECTION,
            is_copy_log: Optional[bool] = True,
            source_log_dir: Optional[str] = None,
            dest_log_dir: Optional[str] = None,
            **spawn_kwargs: Any,
    ) -> None:
        _assert_backend(backend=backend)

        self.spawn_params = spawn_kwargs

        self.model_type = model_type
        self.backend = backend

        self.is_copy_log = is_copy_log
        self.source_log_dir = source_log_dir
        self.dest_log_dir = dest_log_dir

        self._logger = setup_logger(__name__ + "." + self.__class__.__name__)

    def __enter__(self):
        if self.spawn_params is not None:
            self._logger.info(f"Initialized distributed launcher with backend: '{self.backend}'")
            msg = "\n\t".join([f"{k}: {v}" for k, v in self.spawn_params.items()])
            self._logger.info(f"- Parameters to spawn processes: \n\t{msg}")

        thread = Thread(target=self._copy_logs)
        thread.daemon = True
        thread.start()

        return self

    def _copy_logs(self,) -> None:
        """
        Copy logs from source directory to destination directory.
        """
        if self.is_copy_log:
            while True:
                if os.path.exists(self.source_log_dir):
                    if not os.path.exists(self.dest_log_dir):
                        os.makedirs(self.dest_log_dir, exist_ok=True)
                    shutil.copytree(self.source_log_dir, self.dest_log_dir, dirs_exist_ok=True)

                time.sleep(15)

    def run(self, func: Callable, args: Namespace) -> None:
        """Execute ``func`` with provided arguments in distributed context.

        Args:
            func: function to execute.
            args: Simple object for storing attributes.
        """
        if self.spawn_params is not None:
            spawn(self.backend, self.model_type, func, args=args, **self.spawn_params)

    def __exit__(self, exc_type, exc_value, traceback):
        if self.is_copy_log:
            if os.path.exists(self.source_log_dir):
                if not os.path.exists(self.dest_log_dir):
                    os.makedirs(self.dest_log_dir, exist_ok=True)
                shutil.copytree(self.source_log_dir, self.dest_log_dir, dirs_exist_ok=True)

        if exc_type is not None:
            self._logger.error(exc_type, exc_value, traceback)


def entry(func: Callable, args: Namespace):
    """
    Run the same code across all supported distributed backends in a seamless manner.
    """
    logger = setup_logger()
    try:
        config, _, _ = train_config(args.config, args.override)
        backend = config["backend"]
        model_type = config["model_type"]

        spawn_params = setup_spawn_params(**config)

        with Parallel(backend=backend, model_type=model_type, **spawn_params) as parallel:
            parallel.run(func=func, args=args)
    except Exception:
        logger.error(traceback.format_exc())
        for handle in logger.handlers:
            handle.close()
        exit(1)
