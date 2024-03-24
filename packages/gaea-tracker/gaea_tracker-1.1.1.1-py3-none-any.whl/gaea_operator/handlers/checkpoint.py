#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : checkpoint.py    
@Author        : yanxiaodong
@Date          : 2022/10/28
@Description   :
"""
import collections.abc as collections
import numbers
import os
import shutil
import tempfile
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from pathlib import Path
from typing import (Any, Callable, Dict, List, Mapping, NamedTuple, Optional,
                    Union)
import yaml

import gaea_operator.distributed as idist
from gaea_operator.engine import (PADDLE_BACKEND, TORCH_BACKEND, Engine,
                                  Events, Serializable)
from gaea_operator.handlers.model_ema import PaddleModelEMA, ModelEMA
from gaea_operator.metric.metric import BaseMetric
from gaea_operator.utils import MASTER_RANK
from .utils import paddle_load_pretrain_weight, paddle_load_resume_weight


class BaseSaveHandler(metaclass=ABCMeta):
    """
    Base class for save handlers

    """

    @abstractmethod
    def __call__(self, checkpoint: Mapping, filename: str, is_metadata: bool = False) -> None:
        """
        Method to save `checkpoint` with `filename`. Additionally, metadata dictionary is provided.

        Metadata contains:

        - `basename`: file prefix (if provided) with checkpoint name, e.g. `epoch_checkpoint`.
        - `score_name`: score name if provided, e.g `val_acc`.
        - `priority`: checkpoint priority value (higher is better), e.g. `12` or `0.6554435`

        Args:
            checkpoint: checkpoint dictionary to save.
            filename: filename associated with checkpoint.
            is_metadata: is or is not metadata.

        """

    @abstractmethod
    def remove(self, filename: str) -> None:
        """
        Method to remove saved checkpoint.

        Args:
            filename: filename associated with checkpoint.

        """


class Checkpoint(Serializable):
    """
    Checkpoint handler can be used to periodically save and load objects which have attribute
    ``state_dict/load_state_dict``.

    Args:
        to_save: Dictionary with the objects to save. Objects should have implemented ``state_dict`` and
            ``load_state_dict`` methods. .
        save_handler: String, method or callable class
            used to save engine and other provided objects. Function receives two objects: checkpoint as a dictionary
            and filename. If ``save_handler`` is callable class, it can
            inherit of :class:`~BaseSaveHandler` and optionally implement ``remove`` method
            to keep a fixed number of saved checkpoints. In case if user needs to save engine's checkpoint on a disk,
            ``save_handler`` can be defined with :class:`~DiskSaver` or a string specifying
            directory name can be passed to ``save_handler``.
        filename_prefix: Prefix for the file name to which objects will be saved. See Note for details.
        score_function: If not None, it should be a function taking a single argument,
            :class:`~Engine` object, and returning a score (`float`). Objects with highest scores
            will be retained.
        score_name: If ``score_function`` not None, it is possible to store its value using
            ``score_name``. If ``score_function`` is None, ``score_name`` can be used alone to define ``score_function``
            as ``Checkpoint.get_default_score_fn(score_name)`` by default.
        n_saved: Number of objects that should be kept on disk. Older files will be removed. If set to
            `None`, all objects are kept.
            Input of the function is ``(engine, event_name)``. Output of function should be an integer.
            Default is None, global_step based on attached engine. If provided, uses function output as global_step.
            To setup global step from another engine, please use :meth:`~handlers.global_step_from_engine`.
        filename_pattern: If ``filename_pattern`` is provided, this pattern will be used to render
            checkpoint filenames. If the pattern is not defined, the default pattern would be used. See Note for
            details.
        include_self: Whether to include the `state_dict` of this object in the checkpoint. If `True`, then
            there must not be another object in ``to_save`` with key ``checkpointer``.
        greater_or_equal: if `True`, the latest equally scored model is stored. Otherwise, the first model.
            Default, `False`.
        dataset_meta: Meta information of the dataset.
    """

    Item = NamedTuple("Item", [("priority", int), ("filename", str)])
    _state_dict_all_req_keys = ("saved",)

    def __init__(
            self,
            to_save: Mapping,
            save_handler: Union[str, Path, Callable, BaseSaveHandler],
            filename_prefix: Optional[str] = "",
            score_function: Optional[Callable] = None,
            score_name: Optional[str] = None,
            n_saved: Union[int, None] = 1,
            filename_pattern: Optional[str] = None,
            include_self: Optional[bool] = False,
            greater_or_equal: Optional[bool] = False,
            dataset_meta: Optional[Dict] = None,
    ):

        if not isinstance(to_save, collections.Mapping):
            raise TypeError(f"Argument `to_save` should be a dictionary, but given {type(to_save)}")

        self._check_objects(to_save, "state_dict")

        if include_self:
            if not isinstance(to_save, collections.MutableMapping):
                raise TypeError(
                    f"If `include_self` is True, then `to_save` must be mutable, but given {type(to_save)}."
                )

            if "checkpointer" in to_save:
                raise ValueError(f"Cannot have key 'checkpointer' if `include_self` is True: {to_save}")

        if not (
                isinstance(save_handler, str)
                or isinstance(save_handler, Path)
                or callable(save_handler)
                or isinstance(save_handler, BaseSaveHandler)
        ):
            raise TypeError(
                "Argument `save_handler` should be a string or Path object or callable or inherit from BaseSaveHandler"
            )

        self.to_save = to_save
        self.filename_prefix = filename_prefix
        if isinstance(save_handler, str) or isinstance(save_handler, Path):
            self.save_handler = DiskSaver(save_handler, create_dir=True)
        else:
            self.save_handler = save_handler  # type: ignore
        self.score_function = score_function
        self.score_name = score_name
        if self.score_name is not None and self.score_function is None:
            self.score_function = self.get_default_score_fn(self.score_name)
        self.n_saved = n_saved
        self.filename_pattern = filename_pattern
        self._saved = []  # type: List["Checkpoint.Item"]
        self.include_self = include_self
        self.greater_or_equal = greater_or_equal
        self.dataset_meta = dataset_meta
        self.module = idist.get_module()

        if self.module == PADDLE_BACKEND:
            self.ext = "pdparams"
        elif self.module == TORCH_BACKEND:
            self.ext = "pt"
        else:
            self.ext = "not_define"

    def _get_filename_pattern(self, global_step: Optional[int]) -> str:
        if self.filename_pattern is None:
            filename_pattern = self.setup_filename_pattern(
                with_prefix=len(self.filename_prefix) > 0,
                with_score=self.score_function is not None,
                with_score_name=self.score_name is not None,
                with_global_step=global_step is not None,
            )
        else:
            filename_pattern = self.filename_pattern
        return filename_pattern

    def reset(self) -> None:
        """
        Method to reset saved checkpoint names.

        Use this method if the engine will independently run multiple times.
        """
        self._saved = []

    @property
    def last_checkpoint(self) -> Optional[Union[str, Path]]:
        if len(self._saved) < 1:
            return None

        if not isinstance(self.save_handler, DiskSaver):
            return self._saved[-1].filename

        return self.save_handler.dirname / self._saved[-1].filename

    def _check_lt_n_saved(self, or_equal: bool = False) -> bool:
        if self.n_saved is None:
            return True
        return len(self._saved) < self.n_saved + int(or_equal)

    def _compare_fn(self, new: Union[int, float]) -> bool:
        if self.greater_or_equal:
            return new >= self._saved[-1].priority
        else:
            return new > self._saved[-1].priority

    def _save_checkpoint(self,
                         checkpoint: Dict,
                         priority: Union[int, float],
                         global_step: int,
                         pattern: Union[str, List] = None,
                         keys: Optional[List] = None):
        priority_str = f"{priority}" if isinstance(priority, numbers.Integral) else f"{priority:.4f}"

        name = "checkpoint"
        if len(checkpoint) == 1:
            for k in checkpoint:
                name = k
            checkpoint = checkpoint[name]
            if keys is not None and pattern is not None:
                pattern = pattern[keys.index(name)]

        filename_pattern = self._get_filename_pattern(global_step)

        _ext = self.ext
        if pattern is not None:
            _ext = pattern

        if isinstance(_ext, List):
            assert len(keys) == len(_ext), f"pattern: {pattern} length must be equal keys: {keys} length."
            filename = []
            for _e in _ext:
                filename_dict = {
                    "filename_prefix": self.filename_prefix,
                    "ext": _e,
                    "name": name,
                    "score_name": self.score_name,
                    "score": priority_str if (self.score_function is not None) else None,
                    "global_step": global_step,
                }
                filename.append(filename_pattern.format(**filename_dict))
        else:
            filename_dict = {
                "filename_prefix": self.filename_prefix,
                "ext": _ext,
                "name": name,
                "score_name": self.score_name,
                "score": priority_str if (self.score_function is not None) else None,
                "global_step": global_step,
            }
            filename = filename_pattern.format(**filename_dict)

        file_ext = os.path.splitext(filename) if isinstance(filename, str) else os.path.splitext(filename[0])
        try:
            index = list(map(lambda it: it.filename == file_ext[0], self._saved)).index(True)
            to_remove = True
        except ValueError:
            index = 0
            to_remove = not self._check_lt_n_saved()

        if to_remove:
            item = self._saved.pop(index)
            if isinstance(self.save_handler, BaseSaveHandler):
                self.save_handler.remove(item.filename)

        self._saved.append(Checkpoint.Item(priority, file_ext[0]))
        self._saved.sort(key=lambda it: it[0])

        if self.include_self:
            # Now that we've updated _saved, we can add our own state_dict.
            checkpoint["checkpointer"] = self.state_dict()

        if isinstance(filename, str):
            self.save_handler(checkpoint, filename)
        else:
            for i in range(len(filename)):
                self.save_handler(checkpoint[keys[i]], filename[i])

    def __call__(self, engine: Engine, global_step_transform: Optional[Callable] = None) -> None:
        global_step = None
        if global_step_transform is not None:
            global_step = global_step_transform(engine, engine.last_event_name)

        if self.score_function is not None:
            priority = self.score_function(engine)
            if not isinstance(priority, numbers.Number):
                raise ValueError("Output of score_function should be a number")
        else:
            if global_step is None:
                global_step = engine.state.get_event_attrib_value(Events.ITERATION_COMPLETED)
            priority = global_step

        if self._check_lt_n_saved() or self._compare_fn(priority):
            checkpoint = self._setup_checkpoint()
            self._save_checkpoint(checkpoint=checkpoint, priority=priority, global_step=global_step)

    def _setup_checkpoint(self, save_dict: Mapping = None) -> Dict[str, Dict[Any, Any]]:
        checkpoint = {}

        if save_dict is not None:
            for k, obj in save_dict.items():
                if isinstance(obj, List):
                    checkpoint[k] = [opt.state_dict() for opt in obj]
                else:
                    checkpoint[k] = obj.state_dict()

            return checkpoint

        if self.to_save is not None:
            for k, obj in self.to_save.items():
                if isinstance(obj, Dict):
                    checkpoint[k] = obj
                if hasattr(obj, 'state_dict'):
                    checkpoint[k] = obj.state_dict()

        return checkpoint

    @staticmethod
    def setup_filename_pattern(
            with_prefix: bool = True, with_score: bool = True, with_score_name: bool = True,
            with_global_step: bool = True
    ) -> str:
        """Helper method to get the default filename pattern for a checkpoint.

        Args:
            with_prefix: If True, the ``filename_prefix`` is added to the filename pattern:
                ``{filename_prefix}_{name}...``. Default, True.
            with_score: If True, ``score`` is added to the filename pattern: ``..._{score}.{ext}``.
                Default, True. At least one of ``with_score`` and ``with_global_step`` should be True.
            with_score_name: If True, ``score_name`` is added to the filename pattern:
                ``..._{score_name}={score}.{ext}``. If activated, argument ``with_score`` should be
                also True, otherwise an error is raised. Default, True.
            with_global_step: If True, ``{global_step}`` is added to the
                filename pattern: ``...{name}_{global_step}...``.
                At least one of ``with_score`` and ``with_global_step`` should be True.
        """
        filename_pattern = "{name}"

        if not (with_global_step or with_score):
            raise ValueError("At least one of with_score and with_global_step should be True.")

        if with_global_step:
            filename_pattern += "_{global_step}"

        if with_score_name and with_score:
            filename_pattern += "_{score_name}={score}"
        elif with_score:
            filename_pattern += "_{score}"
        elif with_score_name:
            raise ValueError("If with_score_name is True, with_score should be also True")

        if with_prefix:
            filename_pattern = "{filename_prefix}_" + filename_pattern

        filename_pattern += ".{ext}"
        return filename_pattern

    @staticmethod
    def _check_objects(objs: Mapping, attr: str) -> None:
        for k, obj in objs.items():
            if isinstance(obj, List):
                for i in range(len(obj)):
                    if not hasattr(obj[i], attr):
                        raise TypeError(f"Object {type(obj[i])} should have `{attr}` method")
            else:
                if not hasattr(obj, attr):
                    raise TypeError(f"Object {type(obj)} should have `{attr}` method")

    @staticmethod
    def get_default_score_fn(metric_name: str, score_sign: float = 1.0) -> Callable:
        """Helper method to get default score function based on the metric name.
        Args:
            metric_name: metric name to get the value from ``engine.state.metrics``.
            score_sign: sign of the score: 1.0 or -1.0. For error-like metrics, e.g. smaller is better,
                a negative score sign should be used (objects with larger score are retained). Default, 1.0.
        """
        if score_sign not in (1.0, -1.0):
            raise ValueError("Argument score_sign should be 1 or -1")

        def wrapper(engine: Engine) -> float:
            return score_sign * engine.state.metrics[metric_name]

        return wrapper

    def state_dict(self) -> "OrderedDict[str, List[Tuple[int, str]]]":
        """
        Method returns state dict with saved items: list of ``(priority, filename)`` pairs.
        Can be used to save internal state of the class.
        """
        return OrderedDict([("saved", [(p, f) for p, f in self._saved])])

    def load_state_dict(self, state_dict: Mapping) -> None:
        """
        Method replace internal state of the class with provided state dict data.

        Args:
            state_dict: a dict with "saved" key and list of ``(priority, filename)`` pairs as values.
        """
        super().load_state_dict(state_dict)
        self._saved = [Checkpoint.Item(p, f) for p, f in state_dict["saved"]]


class DiskSaver(BaseSaveHandler):
    """
    Handler that saves input checkpoint on a disk.
    Args:
        dirname: Directory path where the checkpoint will be saved
        atomic: if True, checkpoint is serialized to a temporary file, and then
            moved to final destination, so that files are guaranteed to not be damaged
            (for example if exception occurs during saving).
        create_dir: if True, will create directory ``dirname`` if it does not exist.
        require_empty: If True, will raise exception if there are any files in the directory ``dirname``.
    """

    def __init__(
            self,
            dirname: Union[str, Path],
            atomic: bool = True,
            create_dir: bool = True,
            require_empty: bool = True,
    ):
        assert dirname is not None, "Checkpoint save path must be set."
        self.dirname = Path(dirname).expanduser()
        self._atomic = atomic
        self.module = idist.get_module()

        if idist.get_rank() == MASTER_RANK:
            self._check_and_setup(self.dirname, create_dir, require_empty)

    @staticmethod
    def _check_and_setup(dirname: Path, create_dir: bool, require_empty: bool) -> None:
        if create_dir:
            if not dirname.exists():
                dirname.mkdir(parents=True)
        # Ensure that dirname exists
        if not dirname.exists():
            raise ValueError(f"Directory path '{dirname}' is not found")

        if require_empty:
            matched = [fname for fname in os.listdir(dirname) if fname.endswith((".pt", ".pdparams", ".json"))]
            if len(matched) > 0:
                raise ValueError(
                    f"Files {matched} with extension '.pt' or '.pdparams' are already present "
                    f"in the directory {dirname}. If you want to use this "
                    "directory anyway, pass `require_empty=False`."
                    ""
                )

    def __call__(self, checkpoint: Mapping, filename: str, is_metadata: bool = False) -> None:
        path = self.dirname / filename

        if is_metadata:
            if idist.get_rank() == MASTER_RANK:
                def save_yaml(obj, file, **configs):
                    with open(file, 'w') as f:
                        yaml.dump(obj, f, encoding='utf-8', allow_unicode=True, **configs)

                self._save_func(checkpoint=checkpoint, path=path, func=save_yaml)
        else:
            if self.module == PADDLE_BACKEND:
                import paddle
                self._save_func(checkpoint=checkpoint, path=path, func=paddle.save, symlink=True)
            if self.module == TORCH_BACKEND:
                import torch
                self._save_func(checkpoint=checkpoint, path=path, func=torch.save, symlink=True)

    def _save_func(self, checkpoint: Mapping, path: Path, func: Callable, symlink: bool = False) -> None:
        if not self._atomic:
            func(checkpoint, path)
        else:
            tmp = tempfile.NamedTemporaryFile(delete=False, dir=self.dirname)
            tmp_name = tmp.name
            try:
                func(checkpoint, tmp_name)
            except BaseException:
                tmp.close()
                os.remove(tmp_name)
                raise
            else:
                tmp.close()
                os.replace(tmp.name, path)
                # append group/others read mode
                # os.chmod(path, os.stat(path).st_mode | stat.S_IRGRP | stat.S_IROTH)
        # 通过软链接实现模型文件命名唯一
        if symlink:
            root, file = os.path.split(path)
            ext = os.path.splitext(path)[1]
            dst = os.path.join(root, 'best' + ext)
            try:
                os.remove(dst)
            except FileNotFoundError:
                pass
            
            try:
                os.symlink(os.path.abspath(path), os.path.abspath(dst))
            except OSError:
                shutil.copy(path, dst)

    def remove(self, filename: str) -> None:
        if idist.get_rank() == MASTER_RANK:
            for file in self.dirname.rglob("*"):
                if filename in str(file):
                    file.unlink()


class ModelCheckpoint(Checkpoint):
    """
    ModelCheckpoint handler.
    Args:
        dirname: Directory path where objects will be saved.
        categories: Dataset annotation category.
        filename_prefix: Prefix for the file names to which objects will be saved. See Notes of
            :class:`~Checkpoint` for more details.
        score_function: if not None, it should be a function taking a single argument, an
            :class:`~Engine` object, and return a score (`float`). Objects with highest scores
            will be retained.
        score_name: if ``score_function`` not None, it is possible to store its value using
            `score_name`. See Examples of :class:`~Checkpoint` for more details.
        n_saved: Number of objects that should be kept on disk. Older files will be removed. If set to
            `None`, all objects are kept.
        atomic: If True, objects are serialized to a temporary file, and then moved to final
            destination, so that files are guaranteed to not be damaged (for example if exception
            occurs during saving).
        require_empty: If True, will raise exception if there are any files starting with
            ``filename_prefix`` in the directory ``dirname``.
        create_dir: If True, will create directory ``dirname`` if it does not exist.
        global_step_transform: global step transform function to output a desired global step.
            Input of the function is `(engine, event_name)`. Output of function should be an integer.
            Default is None, global_step based on attached engine. If provided, uses function output as global_step.
            To setup global step from another engine, please use :meth:`~handlers.global_step_from_engine`.
        filename_pattern: If ``filename_pattern`` is provided, this pattern will be used to render
            checkpoint filenames. If the pattern is not defined, the default pattern would be used.
            See :class:`~ignite.handlers.checkpoint.Checkpoint` for details.
        include_self: Whether to include the `state_dict` of this object in the checkpoint. If `True`, then
            there must not be another object in ``to_save`` with key ``checkpointer``.
        greater_or_equal: if `True`, the latest equally scored model is stored. Otherwise, the first model.
            Default, `False`.
    """
    meta_file = "meta.yaml"
    config_file = "parameters.yaml"
    category_save_name = "labels"

    def __init__(
            self,
            dirname: Union[str, Path],
            categories: Optional[List],
            filename_prefix: str = "best",
            score_function: Optional[Callable] = None,
            score_name: Optional[str] = None,
            n_saved: Union[int, None] = 1,
            atomic: bool = True,
            require_empty: bool = False,
            create_dir: bool = True,
            filename_pattern: Optional[str] = None,
            include_self: bool = False,
            greater_or_equal: bool = True,
            metric: Optional[BaseMetric] = None
    ):
        disk_saver = DiskSaver(
            dirname,
            atomic=atomic,
            create_dir=create_dir,
            require_empty=require_empty
        )

        super(ModelCheckpoint, self).__init__(
            to_save={},
            save_handler=disk_saver,
            filename_prefix=filename_prefix,
            score_function=score_function,
            score_name=score_name,
            n_saved=n_saved,
            filename_pattern=filename_pattern,
            include_self=include_self,
            greater_or_equal=greater_or_equal,
            dataset_meta={self.category_save_name: categories}
        )
        self.metric = metric

    @property
    def last_checkpoint(self) -> Optional[Union[str, Path]]:
        if len(self._saved) < 1:
            return None

        if not isinstance(self.save_handler, DiskSaver):
            raise RuntimeError(f"Internal error, save_handler should be DiskSaver, but has {type(self.save_handler)}.")

        return self.save_handler.dirname / self._saved[-1].filename

    def attach_engine(self, engine: Engine,
                      global_step_transform: Optional[Callable] = None,
                      to_save: Optional[Mapping] = {}) -> None:
        """
        Attaching `self.__call__` method at COMPLETED.
        """
        if not isinstance(engine, Engine):
            raise TypeError(f"Argument engine should be class: `Engine`, but given {type(engine)}")

        if idist.get_rank() == MASTER_RANK:
            engine.add_event_handler(Events.COMPLETED, self.__call__, global_step_transform, to_save)

    @classmethod
    def load_checkpoint(cls,
                        model,
                        module: str,
                        resume_weight: Optional[str] = None,
                        pretrain_weight: Optional[str] = None,
                        optimizer: Optional[str] = None,
                        ema: Optional[ModelEMA] = None,):
        """
        Helper method to load model checkpoint.
        """
        if resume_weight is None and pretrain_weight is None:
            return 0

        if module == PADDLE_BACKEND:
            if resume_weight is not None:
                start_epoch = paddle_load_resume_weight(model, resume_weight, optimizer, ema)
            else:
                start_epoch = 0
                paddle_load_pretrain_weight(model, pretrain_weight)

            return start_epoch

    def __call__(self, engine: Engine, global_step_transform: Optional[Callable] = None, to_save: Dict = {}):
        self.to_save = to_save

        default_to_save = {}
        if hasattr(engine.state, "model"):
            default_to_save.update({"model": getattr(engine.state, "model")})
        if hasattr(engine.state, "optimizer"):
            default_to_save.update({"optimizer": getattr(engine.state, "optimizer")})

        self._check_objects(default_to_save, "state_dict")

        if global_step_transform is not None and not callable(global_step_transform):
            raise TypeError(f"global_step_transform should be a function, got {type(global_step_transform)} instead.")
        global_step = None
        if global_step_transform is not None:
            global_step = global_step_transform(engine, engine.last_event_name)

        if self.score_function is not None:
            priority = self.score_function(engine)
            if not isinstance(priority, numbers.Number):
                raise ValueError("Output of score_function should be a number")
        else:
            if global_step is None:
                global_step = engine.state.get_event_attrib_value(Events.ITERATION_COMPLETED)
            priority = global_step

        if self._check_lt_n_saved() or self._compare_fn(priority):
            # 保存指标
            if self.metric is not None:
                self.metric.save(dirname=self.save_handler.dirname)
            # meta文件保存，保存类别等信息
            metadata = {
                "priority": priority,
                "experiment_name": os.environ.get("GAEA_EXPERIMENT__EXPERIMENT_NAME", ""),
                "job_name": os.environ.get("GAEA_EXPERIMENT__RUN_NAME", ""),
                "experiment_run_id": os.environ.get("GAEA_EXPERIMENT__RUN_ID", "")
            }
            if isinstance(self.dataset_meta, Dict):
                metadata.update(self.dataset_meta)

            meta_filename = self.meta_file
            self.save_handler(checkpoint=metadata, filename=meta_filename, is_metadata=True)

            # 保存 `self.to_save` to yaml 文件
            config = self._setup_checkpoint()
            name = "config"
            if len(config) == 1:
                for k in config:
                    name = k
                config = config[name]

            config_filename = self.config_file
            self.save_handler(checkpoint=config, filename=config_filename, is_metadata=True)

            # 不同的框架文件保存格式不同，保持和框架默认使用方式
            # torch 把model.state_dict 和 optimizer.state_dict 保存在一个文件
            # paddle 把model.state_dict 和 optimizer.state_dict 分别保存
            checkpoint = self._setup_checkpoint(save_dict=default_to_save)
            if self.module == TORCH_BACKEND:
                self._save_checkpoint(checkpoint=checkpoint, priority=priority, global_step=global_step)

            if self.module == PADDLE_BACKEND:
                if hasattr(engine.state, PaddleModelEMA.name):
                    checkpoint.update({PaddleModelEMA.name: getattr(engine.state, PaddleModelEMA.name)})

                all_key_list = ["model", "optimizer", PaddleModelEMA.name]
                all_pattern_list = ["pdparams", "pdopt", "pdema"]
                pattern = []
                keys = []

                for k in checkpoint:
                    keys.append(k)
                    pattern.append(all_pattern_list[all_key_list.index(k)])

                self._save_checkpoint(checkpoint=checkpoint, priority=priority,
                                      global_step=global_step, pattern=pattern, keys=keys)
