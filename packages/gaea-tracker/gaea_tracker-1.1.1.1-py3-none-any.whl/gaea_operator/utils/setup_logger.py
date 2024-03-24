#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : setup_logger.py    
@Author        : yanxiaodong
@Date          : 2022/11/29
@Description   :
"""
import logging
import os.path
from typing import Optional, TextIO


def setup_logger(
        name: Optional[str] = "gaea-operator",
        level: int = logging.INFO,
        stream: Optional[TextIO] = None,
        format: str = "[{}/{}] [%(process)d %(threadName)s] %(asctime)s %(name)s: %(lineno)d %(levelname)s: %(message)s",
        filepath: Optional[str] = None) -> logging.Logger:
    """
    Setups logger: name, level, format etc.
    Args:
        name: new name for the logger. If None, the standard logger is used.
        level: logging level, e.g. CRITICAL, ERROR, WARNING, INFO, DEBUG.
        stream: logging stream. If None, the standard stream is used (sys.stderr).
        format: logging format. By default, `%(asctime)s %(name)s %(levelname)s: %(message)s`.
        filepath: Optional logging file path. If not None, logs are written to the file.
    Returns:
        logging.Logger
    """
    # check if the logger already exists
    existing = name is None or name in logging.root.manager.loggerDict

    # if existing, get the logger otherwise create a new one
    logger = logging.getLogger(name)

    # Keep the existing configuration
    if existing:
        return logger

    import gaea_operator.distributed as idist

    distributed_rank = idist.get_rank()
    world_size = idist.get_world_size()

    # set distributed logger
    if distributed_rank == 0:
        logger.setLevel(level)
    else:
        logger.setLevel(logging.WARNING)

    formatter = logging.Formatter(format.format(distributed_rank, world_size))

    ch = logging.StreamHandler(stream=stream)
    if distributed_rank == 0:
        ch.setLevel(level)
    else:
        ch.setLevel(logging.WARNING)

    ch.setFormatter(formatter)
    logger.addHandler(ch)

    filepath = os.environ.get("GAEA_LOG_DIR", None)
    if filepath is not None:
        if not os.path.exists(filepath):
            os.makedirs(filepath, exist_ok=True)

        filepath = filepath + "/workerlog.{}".format(0)
        fh = logging.FileHandler(filepath)

        if distributed_rank == 0:
            fh.setLevel(level)
        else:
            fh.setLevel(logging.WARNING)

        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    # don't propagate to ancestors
    # the problem here is to attach handlers to loggers
    # should we provide a default configuration less open ?
    if name is not None:
        logger.propagate = False

    return logger
