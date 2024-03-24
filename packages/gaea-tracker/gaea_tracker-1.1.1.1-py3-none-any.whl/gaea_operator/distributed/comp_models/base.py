#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : base.py    
@Author        : yanxiaodong
@Date          : 2022/11/29
@Description   :
"""
from abc import ABCMeta, abstractmethod
from numbers import Number
from typing import Any, Callable, List, Optional, Sequence, Tuple, Union, Dict

from gaea_operator.engine import PADDLE_BACKEND, TORCH_BACKEND, Engine
from gaea_operator.plugin import (Device, Layer, Model, Module, Optimizer, fused_allreduce_gradients,
                                   PTensor, Tensor, TTensor, paddle, torch)
from gaea_operator.utils import IMAGE_CLASSIFICATION, IMAGE_OBJECT_DETECTION, SEMANTIC_SEGMENTATION


class ComputationModel(metaclass=ABCMeta):
    """
    Base class for distributed computation models and defines interface methods.
    This class is public and should be used for other custom derived distributed models.
    """
    def __init__(self, model_type: Optional[str] = None, backend: Optional[str] = None, **kwargs) -> None:
        self._model_type = model_type
        self._backend = backend

        self._nproc_per_node = None  # type: Optional[int]
        self._nnodes = None  # type: Optional[int]
        self._node = None  # type: Optional[int]
        self._module = None  # type: Optional[str]

    def _setup_attrs(self) -> None:
        if self._nproc_per_node is None:
            self._nproc_per_node = self._compute_nproc_per_node() if self.get_world_size() > 1 else 1
        if self._nnodes is None:
            self._nnodes = self.get_world_size() // self._nproc_per_node
        if self._node is None:
            self._node = self.get_rank() // self._nproc_per_node

    @property
    def module(self):
        return self._module

    @module.setter
    def module(self, value):
        self._module = value

    @property
    def backend(self):
        return self._backend

    @abstractmethod
    def is_initialized(self) -> bool:
        pass

    @abstractmethod
    def _compute_nproc_per_node(self) -> int:
        pass

    def get_model_type(self) -> str:
        return self._model_type

    def set_model_type(self, value) -> None:
        self._model_type = value

    @abstractmethod
    def get_local_rank(self) -> int:
        pass

    @abstractmethod
    def get_rank(self) -> int:
        pass

    @abstractmethod
    def get_world_size(self) -> int:
        pass

    @abstractmethod
    def get_nproc_per_node(self) -> int:
        pass

    @abstractmethod
    def get_nnodes(self) -> int:
        pass

    @abstractmethod
    def get_node_rank(self) -> int:
        pass

    @abstractmethod
    def device(self) -> Device:
        pass

    @abstractmethod
    def finalize(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def create_from_backend(backend: str, **kwargs: Any) -> "ComputationModel":
        pass

    def _collective_op(
            self, tensor: Union[Tensor, float, str], fn: Callable, *args: Any, **kwargs: Any
    ) -> Union[Tensor, float, str, List]:
        device = self.device()

        tensor_to_number = tensor_to_str = False
        retain = False
        if "retain" in kwargs:
            retain = kwargs.pop("retain")

        if isinstance(tensor, (Number, float)):
            tensor_to_number = True
            tensor = self._number_to_tensor(obj=tensor, device=device)
        if isinstance(tensor, str):
            tensor_to_str = True
            tensor = self._encode_str(tensor, device=device, retain=retain)

        tensor_device = None
        if isinstance(tensor, PTensor):
            if f"{tensor.place}" != f"{device}":
                tensor_device = tensor.place
                tensor = paddle.to_tensor(tensor, place=device)
        elif isinstance(tensor, TTensor):
            if tensor.device != device:
                tensor_device = tensor.device
                tensor = tensor.to(device)

        tensor = fn(tensor, *args, **kwargs)

        if tensor_device is not None:
            if isinstance(tensor, PTensor):
                if isinstance(tensor, List):
                    tensor_list = []
                    for value in tensor:
                        tensor_list.append(paddle.to_tensor(value, place=tensor_device))
                    tensor = tensor_list
                else:
                    tensor = paddle.to_tensor(tensor, place=tensor_device)
            else:
                if isinstance(tensor, List):
                    tensor_list = []
                    for value in tensor:
                        tensor_list.append(value.to(device=tensor_device))
                    tensor = tensor_list
                else:
                    tensor = tensor.to(device=tensor_device)

        if tensor_to_number:
            return self._tensor_to_number(tensor)
        if tensor_to_str:
            return self._decode_str(tensor)

        return tensor

    def all_reduce(self, tensor: Union[Tensor, float], op: str = "SUM") -> Union[Tensor, float]:
        """
        All reduce the given object from the current process group.
        Args:
            tensor: python object for all reduce.
            op: all reduce operation.
        """
        if not isinstance(tensor, (PTensor, TTensor, Number)):
            raise TypeError(f"Unhandled input type {type(tensor)}")

        return self._collective_op(tensor=tensor, fn=self._do_all_reduce, op=op)

    def all_gather(self, tensor: Union[Tensor, float, str]) -> Union[List[Tensor], List[float], List[str]]:
        """
        All gather the given object from the current process group.
        Args:
            tensor: python object for all gather.
        """
        if not isinstance(tensor, (PTensor, TTensor, Number, str, list)):
            raise TypeError(f"Unhandled input type {type(tensor)}")

        return self._collective_op(tensor=tensor, fn=self._do_all_gather)

    def broadcast(self, tensor: Union[Tensor, float, str], src: int = 0) -> Union[Tensor, float, str]:
        """
        Broadcast the given object from source process to the current process group.
        Args:
            tensor: python object for broadcast.
            src: The source rank index.
        """
        if not isinstance(tensor, (PTensor, TTensor, Number, str)):
            raise TypeError(f"Unhandled input type {type(tensor)}")

        return self._collective_op(tensor=tensor, fn=self._do_broadcast, retain=True, src=src)

    @abstractmethod
    def _number_to_tensor(self, obj: Union[Number, float], device: Union[str, Device]) -> Tensor:
        """
        Convert the given object to a tensor.
        """
        pass

    @abstractmethod
    def _tensor_to_number(self, obj: Union[List[Tensor], Tensor]) -> Union[List, Number, float]:
        """
        Convert a tensor to the given object.
        """
        pass

    @abstractmethod
    def _encode_str(self, obj: str, device: Union[str, Device], retain: Optional[bool] = False) -> Tensor:
        pass

    @abstractmethod
    def _decode_str(self, obj: Union[List[Tensor], Tensor]) -> List[str]:
        pass

    @abstractmethod
    def _do_all_reduce(self, tensor: Tensor, op: str = "SUM") -> Tensor:
        pass

    @abstractmethod
    def _do_all_gather(self, tensor: Tensor) -> Tensor:
        pass

    @abstractmethod
    def _do_broadcast(self, tensor: Tensor, src: int) -> Tensor:
        pass

    @abstractmethod
    def barrier(self) -> None:
        pass

    def auto_model(self, model: Model) -> Model:
        pass

    def auto_optim(self, optimizer: Optimizer) -> Optimizer:
        pass

    def training_step(self,
                      model: Model,
                      optimizer: Union[List[Optimizer], Optimizer],
                      loss_fn: Callable,
                      lr_scheduler: Union[List, Callable],
                      device: Device,
                      gradient_accumulation_steps: int):
        """
        Factory function for training.

        Args:
            model: the model to train.
            optimizer: the optimizer to use.
            lr_scheduler: the learning rate to use.
            loss_fn: the loss function to use.
            device: current device.
            gradient_accumulation_steps: Number of steps the gradients should be accumulated across.
        """
        if self._module == PADDLE_BACKEND:
            def paddle_update(engine: Engine, batch: Union[Dict, Sequence[Tensor]]) -> Number:
                model.train()
                # model forward
                if self._model_type == IMAGE_OBJECT_DETECTION:
                    batch['epoch_id'] = engine.state.epoch
                    outputs = model(batch)
                    loss = outputs['loss']
                elif self._model_type == IMAGE_CLASSIFICATION:
                    data = batch[0]
                    label = batch[1]
                    outputs = model(data)
                    loss_dict = loss_fn(outputs, label)
                    loss = loss_dict['loss']
                elif self._model_type == SEMANTIC_SEGMENTATION:
                    data = batch['img']
                    label = batch['label']
                    outputs = model(data)
                    loss = loss_fn(outputs, batch)
                else:
                    raise ValueError('Please your model type {}'.format(self._model_type))
                # model backward
                loss.backward()

                if engine.state.iteration % gradient_accumulation_steps == 0:
                    if isinstance(optimizer, List):
                        for i in range(len(optimizer)):
                            optimizer[i].step()
                    else:
                        optimizer.step()

                curr_lr = [optimizer[i].get_lr() for i in range(len(optimizer))] if isinstance(optimizer, List) \
                    else optimizer.get_lr()
                engine.add_once_state(
                    'learning_rate', sum(curr_lr) / len(curr_lr) if isinstance(curr_lr, List) else curr_lr)
                if lr_scheduler is not None:
                    if isinstance(lr_scheduler, List):
                        for i in range(len(lr_scheduler)):
                            if not getattr(lr_scheduler[i], 'by_epoch', False):
                                lr_scheduler[i].step()
                    else:
                        lr_scheduler.step()

                if (engine.state.iteration - 1) % gradient_accumulation_steps == 0:
                    if isinstance(optimizer, List):
                        for i in range(len(optimizer)):
                            optimizer[i].clear_grad()
                    else:
                        optimizer.clear_grad()

                return loss.item()

            update = paddle_update

        if self._module == TORCH_BACKEND:
            loss_fn = loss_fn.to(device)

            def torch_update(engine: Engine, batch: Union[Dict, Sequence[Tensor]]) -> Number:
                if (engine.state.iteration - 1) % gradient_accumulation_steps == 0:
                    optimizer.zero_grad()

                model.train()
                # model forward

                if self._model_type == IMAGE_OBJECT_DETECTION:
                    batch['epoch_id'] = engine.state.epoch
                    outputs = model(batch)
                    loss = outputs['loss']
                elif self._model_type == IMAGE_CLASSIFICATION:
                    data = batch[0].to(device, non_blocking=True)
                    label = batch[1].to(device, non_blocking=True)
                    outputs = model(data)
                    loss_dict = loss_fn(outputs, label)
                    loss = loss_dict['loss']
                else:
                    raise ValueError('Please your model type {}'.format(self._model_type))

                # model backward
                loss.backward()
                if engine.state.iteration % gradient_accumulation_steps == 0:
                    optimizer.step()

                if lr_scheduler is not None:
                    lr_scheduler.step()
                    curr_lr = lr_scheduler.get_lr()
                else:
                    curr_lr = optimizer.param_groups[0]['lr']
                engine.add_once_state('learning_rate', curr_lr)

                return loss.item()

            update = torch_update

        return update

    def amp_training_step(self,
                          model: Model,
                          optimizer: Union[List[Optimizer], Optimizer],
                          loss_fn: Callable,
                          lr_scheduler: Union[List, Callable],
                          device: Device,
                          gradient_accumulation_steps: int,
                          amp_param: dict):
        """
        Factory function for training.

        Args:
            model: the model to train.
            optimizer: the optimizer to use.
            lr_scheduler: the learning rate to use.
            loss_fn: the loss function to use.
            device: current device.
            gradient_accumulation_steps: Number of steps the gradients should be accumulated across.
            amp_param: The mixed precision mode param.
        """
        amp_level = amp_param.get('amp_level', 'O1')

        if self._module == PADDLE_BACKEND:
            AMP_RELATED_FLAGS_SETTING = {'FLAGS_max_inplace_grad_add': 8}
            if paddle.is_compiled_with_cuda():
                AMP_RELATED_FLAGS_SETTING.update({'FLAGS_cudnn_batchnorm_spatial_persistent': 1})
            paddle.set_flags(AMP_RELATED_FLAGS_SETTING)

            use_fused_allreduce_gradients = amp_param.get('use_fused_allreduce_gradients', False)
            custom_white_list = amp_param.get('custom_white_list', None)
            custom_black_list = amp_param.get('custom_black_list', None)
            init_loss_scaling = amp_param.get('init_loss_scaling', 1024)
            use_dynamic_loss_scaling = amp_param.get('use_dynamic_loss_scaling', False)

            enable = amp_param.get('enable', True)

            if amp_level == 'O2':
                model, optimizer = paddle.amp.decorate(models=model, optimizers=optimizer, level=amp_level)

            from paddle.amp import decorate
            scaler = paddle.amp.GradScaler(enable=enable, init_loss_scaling=init_loss_scaling,
                                           use_dynamic_loss_scaling=use_dynamic_loss_scaling)

            def paddle_update(engine: Engine, batch: Union[Dict, Sequence[Tensor]]) -> Number:
                model.train()
                # model forward
                if isinstance(model, paddle.DataParallel) and use_fused_allreduce_gradients:
                    with model.no_sync():
                        with paddle.amp.auto_cast(enable=enable, custom_white_list=custom_white_list,
                                                  custom_black_list=custom_black_list, level=amp_level):
                            # model forward
                            if self._model_type == IMAGE_OBJECT_DETECTION:
                                batch['epoch_id'] = engine.state.epoch
                                outputs = model(batch)
                                loss = outputs['loss']
                            elif self._model_type == IMAGE_CLASSIFICATION:
                                data = batch[0]
                                label = batch[1]
                                outputs = model(data)
                                loss_dict = loss_fn(outputs, label)
                                loss = loss_dict['loss']
                            else:
                                raise ValueError('Please your model type {}'.format(self._model_type))

                        # model backward
                        scaled_loss = scaler.scale(loss)
                        scaled_loss.backward()
                    fused_allreduce_gradients(list(model.parameters()), None)
                else:
                    with paddle.amp.auto_cast(enable=enable, custom_white_list=custom_white_list,
                                              custom_black_list=custom_black_list, level=amp_level):
                        # model forward
                        if self._model_type == IMAGE_OBJECT_DETECTION:
                            batch['epoch_id'] = engine.state.epoch
                            outputs = model(batch)
                            loss = outputs['loss']
                        elif self._model_type == IMAGE_CLASSIFICATION:
                            data = batch[0]
                            label = batch[1]
                            outputs = model(data)
                            loss_dict = loss_fn(outputs, label)
                            loss = loss_dict['loss']

                    # model backward
                    scaled_loss = scaler.scale(loss)
                    scaled_loss.backward()
                # in dygraph mode, optimizer.minimize is equal to optimizer.step
                if engine.state.iteration % gradient_accumulation_steps == 0:
                    if isinstance(optimizer, List):
                        for i in range(len(optimizer)):
                            scaler.minimize(optimizer[i], scaled_loss)
                    else:
                        scaler.minimize(optimizer, scaled_loss)

                curr_lr = [optimizer[i].get_lr() for i in range(len(optimizer))] if isinstance(optimizer, List) \
                    else optimizer.get_lr()
                engine.add_once_state(
                    'learning_rate', sum(curr_lr) / len(curr_lr) if isinstance(curr_lr, List) else curr_lr)

                if lr_scheduler is not None:
                    if isinstance(lr_scheduler, List):
                        for i in range(len(lr_scheduler)):
                            if not getattr(lr_scheduler[i], 'by_epoch', False):
                                lr_scheduler[i].step()
                    else:
                        lr_scheduler.step()

                if (engine.state.iteration - 1) % gradient_accumulation_steps == 0:
                    if isinstance(optimizer, List):
                        for i in range(len(optimizer)):
                            optimizer[i].clear_grad()
                    else:
                        optimizer.clear_grad()

                return loss.item()

            update = paddle_update

        if self._module == TORCH_BACKEND:
            loss_fn = loss_fn.to(device)

            def torch_update(engine: Engine, batch: Sequence[Tensor]) -> Number:
                if (engine.state.iteration - 1) % gradient_accumulation_steps == 0:
                    optimizer.zero_grad()

                # TODO: 补充toch混合精度训练

            update = torch_update

        return update

    def validating_step(self, model: Model, device: Device):
        """
        Factory function for validating.

        Args:
            model: the model to validate.
            device: current device.
        """
        if self._module == TORCH_BACKEND:
            def torch_update(engine: Engine, batch: Union[Dict, Sequence[Tensor]]) -> Union[Any, Tuple[Tensor]]:
                model.eval()
                with torch.no_grad():
                    if self._model_type == IMAGE_OBJECT_DETECTION:
                        outputs = model(batch)
                        img_id = batch['im_id']
                    elif self._model_type == IMAGE_CLASSIFICATION:
                        data = batch[0].to(device, non_blocking=True)
                        img_id = batch['im_id'].to(device, non_blocking=True)
                        outputs = model(data)
                    else:
                        raise ValueError('Please check your model type {}'.format(self._model_type))

                return outputs, img_id

            update = torch_update

        if self._module == PADDLE_BACKEND:
            def paddle_update(engine: Engine, batch: Union[Dict, Sequence[Tensor]]) -> Union[Any, Tuple[Tensor]]:
                model.eval()
                with paddle.no_grad():
                    if self._model_type == IMAGE_OBJECT_DETECTION:
                        outputs = model(batch)
                        img_id = batch['im_id']
                    elif self._model_type == IMAGE_CLASSIFICATION:
                        outputs = model(batch[0])
                        img_id = batch['im_id']
                    elif self._model_type == SEMANTIC_SEGMENTATION:
                        outputs = model(batch['img'])[0]
                        label = batch['label']
                        return outputs, label
                    else:
                        raise ValueError('Please check your model type {}'.format(self._model_type))

                return outputs, img_id

            update = paddle_update

        return update

    def amp_validating_step(self, model: Model, device: Device, amp_param: dict):
        """
        Factory function for validating.

        Args:
            model: the model to validate.
            device: current device.
            amp_param: The mixed precision mode param.
        """
        amp_level = amp_param.get('amp_level', 'O1')
        if self._module == TORCH_BACKEND:
            def torch_update(engine: Engine, batch: Sequence[Tensor]) -> Union[Any, Tuple[Tensor]]:
                # TODO: 补充toch混合精度训练
                pass

            update = torch_update

        if self._module == PADDLE_BACKEND:
            custom_white_list = amp_param.get('custom_white_list', None)
            custom_black_list = amp_param.get('custom_black_list', None)
            enable = amp_param.get('enable', True)

            if amp_level == 'O2':
                model, _ = paddle.amp.decorate(models=model, level=amp_level)

            def paddle_update(engine: Engine, batch: Union[Dict, Sequence[Tensor]]) -> Union[Any, Tuple[Tensor]]:
                model.eval()
                with paddle.no_grad():
                    with paddle.amp.auto_cast(enable=enable, custom_white_list=custom_white_list,
                                              custom_black_list=custom_black_list, level=amp_level):
                        if self._model_type == IMAGE_OBJECT_DETECTION:
                            outputs = model(batch)
                            img_id = batch['im_id']
                        else:
                            outputs = model(batch[0])
                            img_id = batch['im_id']
                return outputs, img_id

            update = paddle_update

        return update


class _SerialModel(ComputationModel):
    """
    Private class defines non-distributed computation model for code compatibility with other distributed models.
    """
    available_backends = ()

    def __init__(self, **kwargs: Any) -> None:
        super(_SerialModel, self).__init__(**kwargs)

    def is_initialized(self) -> bool:
        return True

    def get_local_rank(self) -> int:
        return 0

    def get_rank(self) -> int:
        return 0

    def get_world_size(self) -> int:
        return 1

    def get_nproc_per_node(self) -> int:
        return 1

    def get_nnodes(self) -> int:
        return 1

    def get_node_rank(self) -> int:
        return 0

    def device(self) -> Device:
        if self._module == PADDLE_BACKEND:
            if paddle.device.cuda.device_count() > 0:
                return paddle.set_device('gpu')
            return paddle.set_device('cpu')
        if self._module == TORCH_BACKEND:
            if torch.cuda.is_available():
                return torch.device('cuda')
            return torch.device('cpu')

    def finalize(self) -> None:
        pass

    def _compute_nproc_per_node(self) -> int:
        return 1

    @staticmethod
    def create_from_backend(model_type: str, backend: Optional[str] = None) -> "_SerialModel":
        return _SerialModel(model_type=model_type, backend=backend)

    def all_reduce(self, tensor: Union[Tensor, float], op: str = "SUM") -> Union[Tensor, float]:
        return tensor

    def all_gather(self, tensor: Union[Tensor, float, str]) -> Union[List[Tensor], List[float], List[str]]:
        return [tensor]

    def broadcast(self, tensor: Union[Tensor, float, str], src: int = 0) -> Union[Tensor, float, str]:
        return tensor

    def _do_all_reduce(self, tensor: Tensor, op: str = "SUM") -> Tensor:
        return tensor

    def _do_all_gather(self, tensor: Tensor) -> Tensor:
        return tensor

    def _do_broadcast(self, tensor: Tensor, src: int) -> Tensor:
        return tensor

    def _number_to_tensor(self, obj: Union[Number, float], device: Union[str, 'device']) -> Tensor:
        pass

    def _tensor_to_number(self, obj: Union[List[Tensor], Tensor]) -> Union[Number, float]:
        pass

    def _encode_str(self, obj: str, device: Union[str, 'device'], retain: Optional[bool] = False) -> Tensor:
        pass

    def _decode_str(self, obj: Union[List[Tensor], Tensor]) -> List[str]:
        pass

    def barrier(self) -> None:
        pass

    def auto_model(self, model: Model) -> Tuple[str, Model]:
        assert isinstance(model, Layer) or isinstance(model, Module), \
            f'model should paddle.nn.Layer or torch.nn.Module, but give {type(model)}'
        if isinstance(model, Layer):
            self._module = PADDLE_BACKEND
        if isinstance(model, Module):
            self._module = TORCH_BACKEND

        device = self.device()
        if self._module == TORCH_BACKEND:
            model = model.to(device)
        return self._module, model

    def auto_optim(self, optimizer: Optimizer) -> Optimizer:
        return optimizer
