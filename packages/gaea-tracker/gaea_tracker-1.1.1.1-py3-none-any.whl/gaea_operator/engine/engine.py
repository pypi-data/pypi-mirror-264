#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : trainer.py
@Author        : yanxiaodong
@Date          : 2022/11/28
@Description   :
"""
import functools
import logging
import time
import warnings
import weakref
from collections import OrderedDict, defaultdict
from collections.abc import Mapping
from typing import (Any, Callable, Dict, Generator, Iterable, Iterator, List,
                    Optional, Tuple, Union)

from gaea_operator.plugin import DataLoader

from .events import (CallableEventWithFilter, EventEnum, Events, EventsList,
                     RemovableEventHandle, State)
from .mixins import Serializable
from .utils import _check_signature, _to_hours_mins_secs


class Engine(Serializable):
    """
    Runs a given ``process_function`` over each batch of a dataset, emitting events as it goes.

    Args:
        process_function: A function receiving a handle to the engine and the current batch
            in each iteration, and returns data to be stored in the engine's state.

    Attributes:
        state: object that is used to pass internal and user-defined state between event handlers.
            It is created with the engine and its attributes (e.g. ``state.iteration``, ``state.epoch`` etc) are reset
            on every :meth:`Engine.run`.
        last_event_name: last event name triggered by the engine.
    """

    _state_dict_all_req_keys = ("epoch_length", "max_epochs")
    _state_dict_one_of_opt_keys = ("iteration", "epoch")

    # Flag to disable engine._internal_run as generator feature for BC
    interrupt_resume_enabled = True

    def __init__(self, process_function: Optional[Callable[["Engine", Any], Any]] = None):
        self._event_handlers = defaultdict(list)  # type: Dict[Any, List]
        self.logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
        self._process_function = process_function
        self.last_event_name = None  # type: Optional[Events]
        self.should_terminate = False
        self.should_terminate_single_epoch = False
        self.should_interrupt = False
        self.state = State()
        self._state_dict_user_keys = []  # type: List[str]
        self._allowed_events = []  # type: List[EventEnum]

        self._dataloader_iter = None  # type: Optional[Iterator[Any]]
        self._init_iter = None  # type: Optional[int]

        self.register_events(*Events)

        if self._process_function is None:
            self.logger.info("Process function is `None`, when running must be given a processing function")
        else:
            _check_signature(process_function, "process_function", self, None)

        # generator provided by self._internal_run_as_gen
        self._internal_run_generator = None  # type: Optional[Generator]

    def register_events(
        self, *event_names: Union[List[str], List[EventEnum]], event_to_attr: Optional[dict] = None
    ) -> None:
        """Add events that can be fired.

        Registering an event will let the user trigger these events at any point.
        This opens the door to make the :meth:`~Engine.run` loop even more configurable.

        By default, the events from :class:`~Events` are registered.

        Args:
            event_names: Defines the name of the event being supported. New events can be a str
                or an object derived from :class:`~EventEnum`. See example below.
            event_to_attr: A dictionary to map an event to a state attribute.
        """
        if not (event_to_attr is None or isinstance(event_to_attr, dict)):
            raise ValueError(f"Expected event_to_attr to be dictionary. Got {type(event_to_attr)}.")

        for index, e in enumerate(event_names):
            if not isinstance(e, (str, EventEnum)):
                raise TypeError(f"Value at {index} of event_names should be a str or EventEnum, but given {e}")
            self._allowed_events.append(e)
            if event_to_attr and e in event_to_attr:
                State.event_to_attr[e] = event_to_attr[e]
        # we need to update state attributes associated with new custom events
        self.state._update_attrs()

    def _handler_wrapper(self, handler: Callable, event_name: Any, event_filter: Callable) -> Callable:
        # signature of the following wrapper will be inspected during registering to check if engine is necessary
        # we have to build a wrapper with relevant signature : solution is functools.wraps
        @functools.wraps(handler)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            event = self.state.get_event_attrib_value(event_name)
            if event_filter(self, event):
                return handler(*args, **kwargs)

        # setup input handler as parent to make has_event_handler work
        setattr(wrapper, "_parent", weakref.ref(handler))
        return wrapper

    def _assert_allowed_event(self, event_name: Any) -> None:
        if event_name not in self._allowed_events:
            self.logger.error(f"attempt to add event handler to an invalid event {event_name}")
            raise ValueError(f"Event {event_name} is not a valid event for this {self.__class__.__name__}.")

    def add_event_handler(self, event_name: Any, handler: Callable, *args: Any, **kwargs: Any) -> RemovableEventHandle:
        """Add an event handler to be executed when the specified event is fired.

        Args:
            event_name: An event or a list of events to attach the handler. Valid events are
                from :class:`~Events` or any ``event_name`` added by :meth:`~Engine.register_events`.
            handler: the callable event handler that should be invoked. No restrictions on its signature.
                The first argument can be optionally `engine`, the :class:`~Engine` object, handler is bound to.
            args: optional args to be passed to ``handler``.
            kwargs: optional keyword args to be passed to ``handler``.

        Returns:
            :class:`~RemovableEventHandle`, which can be used to remove the handler.
        """
        if isinstance(event_name, EventsList):
            for e in event_name:
                self.add_event_handler(e, handler, *args, **kwargs)
            return RemovableEventHandle(event_name, handler, self)
        if isinstance(event_name, CallableEventWithFilter) and event_name.filter is not None:
            event_filter = event_name.filter
            handler = self._handler_wrapper(handler, event_name, event_filter)

        self._assert_allowed_event(event_name)

        event_args = ()  # type: Tuple[Any, ...]
        if event_name == Events.EXCEPTION_RAISED:
            event_args += (Exception(),)
        elif event_name == Events.TERMINATE_SINGLE_EPOCH:
            event_args += (0,)

        try:
            _check_signature(handler, "handler", self, *(event_args + args), **kwargs)
            self._event_handlers[event_name].append((handler, (self,) + args, kwargs))
        except ValueError:
            _check_signature(handler, "handler", *(event_args + args), **kwargs)
            self._event_handlers[event_name].append((handler, args, kwargs))
        self.logger.debug(f"Added handler for event {event_name}")

        return RemovableEventHandle(event_name, handler, self)

    def has_event_handler(self, handler: Callable, event_name: Optional[Any] = None) -> bool:
        """
        Check if the specified event has the specified handler.

        Args:
            handler: the callable event handler.
            event_name: The event the handler attached to. Set this
                to ``None`` to search all events.
        """
        if event_name is not None:
            if event_name not in self._event_handlers:
                return False
            events = [event_name]  # type: Union[List[Any], Dict[Any, List]]
        else:
            events = self._event_handlers
        for e in events:
            for h, _, _ in self._event_handlers[e]:
                if self._compare_handlers(handler, h):
                    return True
        return False

    @staticmethod
    def _compare_handlers(user_handler: Callable, registered_handler: Callable) -> bool:
        if hasattr(registered_handler, "_parent"):
            registered_handler = registered_handler._parent()  # type: ignore[attr-defined]
        return registered_handler == user_handler

    def remove_event_handler(self, handler: Callable, event_name: Any) -> None:
        """
        Remove event handler `handler` from registered handlers of the engine

        Args:
            handler: the callable event handler that should be removed
            event_name: The event the handler attached to.

        """
        if event_name not in self._event_handlers:
            raise ValueError(f"Input event name '{event_name}' does not exist")

        new_event_handlers = [
            (h, args, kwargs)
            for h, args, kwargs in self._event_handlers[event_name]
            if not self._compare_handlers(handler, h)
        ]
        if len(new_event_handlers) == len(self._event_handlers[event_name]):
            raise ValueError(f"Input handler '{handler}' is not found among registered event handlers")
        self._event_handlers[event_name] = new_event_handlers

    def on(self, event_name: Any, *args: Any, **kwargs: Any) -> Callable:
        """
        Decorator shortcut for :meth:`~Engine.add_event_handler`.

        Args:
            event_name: An event to attach the handler to. Valid events are from :class:`~Events`
                or any ``event_name`` added by :meth:`~Engine.register_events`.
            args: optional args to be passed to `handler`.
            kwargs: optional keyword args to be passed to `handler`.
        """

        def decorator(f: Callable) -> Callable:
            self.add_event_handler(event_name, f, *args, **kwargs)
            return f

        return decorator

    def _fire_event(self, event_name: Any, *event_args: Any, **event_kwargs: Any) -> None:
        """
        Execute all the handlers associated with given event.

        This method executes all handlers associated with the event
        `event_name`. Optional positional and keyword arguments can be used to
        pass arguments to **all** handlers added with this event. These
        arguments updates arguments passed using :meth:`~Engine.add_event_handler`.

        Args:
            event_name: event for which the handlers should be executed. Valid
                events are from :class:`~Events` or any `event_name` added by :meth:`~Engine.register_events`.
            *event_args: optional args to be passed to all handlers.
            **event_kwargs: optional keyword args to be passed to all handlers.
        """
        self.logger.debug(f"{self.state.epoch} | {self.state.iteration}, Firing handlers for event {event_name}")
        self.last_event_name = event_name
        for func, args, kwargs in self._event_handlers[event_name]:
            kwargs.update(event_kwargs)
            first, others = ((args[0],), args[1:]) if (args and args[0] == self) else ((), args)
            func(*first, *(event_args + others), **kwargs)

    def fire_event(self, event_name: Any) -> None:
        """
        Execute all the handlers associated with given event.

        This method executes all handlers associated with the event
        `event_name`. This is the method used in :meth:`~Engine.run` to call the
        core events found in :class:`~Events`.

        Custom events can be fired if they have been registered before with
        :meth:`~Engine.register_events`. The engine `state` attribute should be used
        to exchange "dynamic" data among `process_function` and handlers.

        This method is called automatically for core events. If no custom
        events are used in the engine, there is no need for the user to call
        the method.

        Args:
            event_name: event for which the handlers should be executed. Valid
                events are from :class:`~Events` or any `event_name` added by :meth:`~Engine.register_events`.
        """
        self._assert_allowed_event(event_name)
        return self._fire_event(event_name)

    def interrupt(self) -> None:
        """
        Sends interrupt signal to the engine, so that it interrupts the run after
        the current iteration. The run can be resumed by calling
        :meth:`~Engine.run`. Data iteration will continue from the interrupted state.
        """
        if not self.interrupt_resume_enabled:
            raise RuntimeError(
                "Engine 'interrupt/resume' feature is disabled. "
                "Please, set Engine.interrupt_resume_enabled=True to enable it"
            )

        self.logger.info("interrupt signaled. Engine will interrupt the run after current iteration is finished.")
        self.should_interrupt = True

    def terminate(self) -> None:
        """
        Sends terminate signal to the engine, so that it terminates completely the run. The run is
        terminated after the event on which ``terminate`` method was called. The following events are triggered:

        - ...
        - Terminating event
        - :attr:`~Events.TERMINATE`
        - :attr:`~Events.COMPLETED`

        """
        self.logger.info("Terminate signaled. Engine will stop after current iteration is finished.")
        self.should_terminate = True

    def terminate_epoch(self) -> None:
        """
        Sends terminate signal to the engine, so that it terminates the current epoch. The run
        continues from the next epoch. The following events are triggered:

        - ...
        - Event on which ``terminate_epoch`` method is called
        - :attr:`~Events.TERMINATE_SINGLE_EPOCH`
        - :attr:`~Events.EPOCH_COMPLETED`
        - :attr:`~Events.EPOCH_STARTED`
        - ...
        """
        self.logger.info(
            "Terminate current epoch is signaled. "
            "Current epoch iteration will stop after current iteration is finished."
        )
        self.should_terminate_single_epoch = True

    def _handle_exception(self, e: BaseException) -> None:
        if Events.EXCEPTION_RAISED in self._event_handlers:
            self._fire_event(Events.EXCEPTION_RAISED, e)
        else:
            raise e

    @property
    def state_dict_user_keys(self) -> List:
        return self._state_dict_user_keys

    def add_once_state(self, name: str, value: Any):
        """
        engine's state add a new attr
        """
        setattr(self.state, name, value)

    def state_dict(self) -> OrderedDict:
        """
        Returns a dictionary containing engine's state: "seed", "epoch_length", "max_epochs" and "iteration" and
        other state values defined by `engine.state_dict_user_keys`

        Returns:
            OrderedDict:
                a dictionary containing engine's state

        """
        keys = self._state_dict_all_req_keys + (self._state_dict_one_of_opt_keys[0],)  # type: Tuple[str, ...]
        keys += tuple(self._state_dict_user_keys)
        return OrderedDict([(k, getattr(self.state, k)) for k in keys])

    def load_state_dict(self, state_dict: Mapping) -> None:
        """
        Setups engine from `state_dict`.

        State dictionary should contain keys: `iteration` or `epoch` and `max_epochs`, `epoch_length` and
        `seed`. If `engine.state_dict_user_keys` contains keys, they should be also present in the state dictionary.
        Iteration and epoch values are 0-based: the first iteration or epoch is zero.

        This method does not remove any custom attributs added by user.

        Args:
            state_dict: a dict with parameters
        """
        super(Engine, self).load_state_dict(state_dict)

        for k in self._state_dict_user_keys:
            if k not in state_dict:
                raise ValueError(
                    f"Required user state attribute '{k}' is absent in provided state_dict '{state_dict.keys()}'"
                )
        self.state.max_epochs = state_dict["max_epochs"]
        self.state.epoch_length = state_dict["epoch_length"]
        for k in self._state_dict_user_keys:
            setattr(self.state, k, state_dict[k])

        if "iteration" in state_dict:
            self.state.iteration = state_dict["iteration"]
            self.state.epoch = 0
            if self.state.epoch_length is not None:
                self.state.epoch = self.state.iteration // self.state.epoch_length
        elif "epoch" in state_dict:
            self.state.epoch = state_dict["epoch"]
            if self.state.epoch_length is None:
                raise ValueError(
                    "If epoch is provided in the state dict, epoch_length should not be None. "
                    f"Input state_dict: {state_dict}"
                )
            self.state.iteration = self.state.epoch_length * self.state.epoch

    @staticmethod
    def _is_done(state: State) -> bool:
        is_done_count = (
            state.epoch_length is not None
            and state.max_epochs is not None
            and state.iteration >= state.epoch_length * state.max_epochs
        )
        is_done_epochs = state.max_epochs is not None and state.epoch >= state.max_epochs
        return is_done_count or is_done_epochs

    def set_data(self, data: Union[Iterable, DataLoader]) -> None:
        """
        Method to set data. After calling the method the next batch passed to `processing_function` is
        from newly provided data. Please, note that epoch length is not modified.

        Args:
            data: Collection of batches allowing repeated iteration (e.g., list or `DataLoader`).
        """
        self.state.dataloader = data
        self._dataloader_iter = iter(self.state.dataloader)

    def run(
        self,
        data: Optional[Iterable] = None,
        max_epochs: Optional[int] = None,
        epoch_length: Optional[int] = None,
    ) -> State:
        """
        Runs the ``process_function`` over the passed data.

        Engine has a state and the following logic is applied in this function:

        - At the first call, new state is defined by `max_epochs`, `epoch_length`, `seed`, if provided.
          A timer for total and per-epoch time is initialized when Events.STARTED is handled.
        - If state is already defined such that there are iterations to run until `max_epochs` and no input arguments
          provided, state is kept and used in the function.
        - If state is defined and engine is "done" (no iterations to run until `max_epochs`), a new state is defined.
        - If state is defined, engine is NOT "done", then input arguments if provided override defined state.

        Args:
            data: Collection of batches allowing repeated iteration (e.g., list or `DataLoader`). If not provided, then
                ``epoch_length`` is required and ``batch`` argument of ``process_function`` will be ``None``.
            max_epochs: Max epochs to run for (default: None).
                If a new state should be created (first run or run again from ended engine), it's default value is 1.
                If run is resuming from a state, provided `max_epochs` will be taken into account and should be larger
                than `engine.state.max_epochs`.
            epoch_length: Number of iterations to count as one epoch. By default, it can be set as
                `len(data)`. If `data` is an iterator and `epoch_length` is not set, then it will be automatically
                determined as the iteration on which data iterator raises `StopIteration`.
                This argument should not change if run is resuming from a state.

        Returns:
            State: output state.
        """
        if data is not None and not isinstance(data, Iterable):
            raise TypeError("Argument data should be iterable")

        if self.state.max_epochs is not None:
            # Check and apply overridden parameters
            if max_epochs is not None:
                if max_epochs < self.state.epoch:
                    raise ValueError(
                        "Argument max_epochs should be greater than or equal to the start "
                        f"epoch defined in the state: {max_epochs} vs {self.state.epoch}. "
                        "Please, set engine.state.max_epochs = None "
                        "before calling engine.run() in order to restart the training from the beginning."
                    )
                self.state.max_epochs = max_epochs
            if epoch_length is not None:
                if epoch_length != self.state.epoch_length:
                    raise ValueError(
                        "Argument epoch_length should be same as in the state, "
                        f"but given {epoch_length} vs {self.state.epoch_length}"
                    )

        if self.state.max_epochs is None or (self._is_done(self.state) and self._internal_run_generator is None):
            # Create new state
            if max_epochs is None:
                max_epochs = 1
            if epoch_length is None:
                if data is None:
                    raise ValueError("epoch_length should be provided if data is None")

                epoch_length = self._get_data_length(data)
                if epoch_length is not None and epoch_length < 1:
                    raise ValueError("Input data has zero size. Please provide non-empty data")

            self.state.iteration = 0
            self.state.epoch = 0
            self.state.max_epochs = max_epochs
            self.state.epoch_length = epoch_length
            # Reset generator if previously used
            self._internal_run_generator = None
            self.logger.info(f"Engine run starting with max_epochs={max_epochs}.")
        else:
            self.logger.info(
                f"Engine run resuming from iteration {self.state.iteration}, "
                f"epoch {self.state.epoch} until {self.state.max_epochs} epochs"
            )
            if self.state.epoch_length is None and data is None:
                raise ValueError("epoch_length should be provided if data is None")

            if self.should_terminate:
                # If engine was terminated and now is resuming from terminated state
                # we need to initialize iter_counter as 0
                self._init_iter = 0

        if self._dataloader_iter is None:
            self.state.dataloader = data

        if self.interrupt_resume_enabled:
            return self._internal_run()
        else:
            return self._internal_run_legacy()

    @staticmethod
    def _init_timers(state: State) -> None:
        state.times[Events.EPOCH_COMPLETED.name] = 0.0
        state.times[Events.COMPLETED.name] = 0.0

    def _get_data_length(self, data: Iterable) -> Optional[int]:
        try:
            if hasattr(data, "__len__"):
                return len(data)  # type: ignore[arg-type]
        except TypeError:
            # _InfiniteConstantSampler can raise a TypeError on DataLoader length of a IterableDataset
            pass
        return None

    def _setup_dataloader_iter(self) -> None:
        if self.state.dataloader is None:
            if self.state.epoch_length is None:
                raise RuntimeError(
                    "Internal error, self.state.epoch_length is None. "
                    "Please, file an issue if you encounter this error."
                )
            self._dataloader_iter = _get_none_data_iter(self.state.epoch_length)
        else:
            self._dataloader_iter = iter(self.state.dataloader)

    def _setup_engine(self) -> None:
        self._setup_dataloader_iter()

        if self._init_iter is None:
            iteration = self.state.iteration
            # Below we define initial counter value for _run_once_on_dataset to measure a single epoch
            if self.state.epoch_length is not None:
                iteration %= self.state.epoch_length
            self._init_iter = iteration

    def _internal_run(self) -> State:
        if self._internal_run_generator is None:
            self._internal_run_generator = self._internal_run_as_gen()
        try:
            return next(self._internal_run_generator)
        except StopIteration as out:
            self._internal_run_generator = None
            return out.value

    def _internal_run_as_gen(self) -> Generator:
        self.should_terminate = self.should_terminate_single_epoch = self.should_interrupt = False
        self._init_timers(self.state)
        try:
            try:
                start_time = time.time()
                self._fire_event(Events.STARTED)
                yield from self._maybe_terminate_or_interrupt()

                while not self._is_done(self.state) and not self.should_terminate:
                    self.state.epoch += 1
                    handlers_start_time = time.time()
                    self._fire_event(Events.EPOCH_STARTED)
                    epoch_time_taken = time.time() - handlers_start_time
                    yield from self._maybe_terminate_or_interrupt()

                    if self._dataloader_iter is None:
                        self._setup_engine()

                    epoch_time_taken += yield from self._run_once_on_dataset_as_gen()

                    # time is available for handlers but must be updated after fire
                    self.state.times[Events.EPOCH_COMPLETED.name] = epoch_time_taken

                    handlers_start_time = time.time()
                    self._fire_event(Events.EPOCH_COMPLETED)
                    epoch_time_taken += time.time() - handlers_start_time
                    # update time wrt handlers
                    self.state.times[Events.EPOCH_COMPLETED.name] = epoch_time_taken
                    yield from self._maybe_terminate_or_interrupt()

                    hours, mins, secs = _to_hours_mins_secs(epoch_time_taken)
                    self.logger.info(
                        f"Epoch[{self.state.epoch}] Complete. Time taken: {hours:02d}:{mins:02d}:{secs:06.3f}"
                    )

            except _EngineTerminateException:
                self._fire_event(Events.TERMINATE)

            time_taken = time.time() - start_time
            # time is available for handlers but must be updated after fire
            self.state.times[Events.COMPLETED.name] = time_taken
            handlers_start_time = time.time()
            self._fire_event(Events.COMPLETED)
            time_taken += time.time() - handlers_start_time
            # update time wrt handlers
            self.state.times[Events.COMPLETED.name] = time_taken
            hours, mins, secs = _to_hours_mins_secs(time_taken)
            self.logger.info(f"Engine run complete. Time taken: {hours:02d}:{mins:02d}:{secs:06.3f}")

        except BaseException as e:
            self._dataloader_iter = None
            self.logger.error(f"Engine run is terminating due to exception: {e}")
            self._handle_exception(e)

        self._dataloader_iter = None
        return self.state

    def _maybe_terminate_or_interrupt(self) -> Generator:
        if self.should_terminate:
            raise _EngineTerminateException()

        if self.should_terminate_single_epoch:
            raise _EngineTerminateSingleEpochException()

        if self.should_interrupt:
            self._fire_event(Events.INTERRUPT)
            self.should_interrupt = False
            yield self.state

    def _run_once_on_dataset_as_gen(self) -> Generator[State, None, float]:
        start_time = time.time()

        # We need to setup iter_counter > 0 if we resume from an iteration
        iter_counter = 0 if self._init_iter is None else self._init_iter
        self._init_iter = None
        should_exit = False
        try:
            if self._dataloader_iter is None:
                raise RuntimeError(
                    "Internal error, self._dataloader_iter is None. "
                    "Please, file an issue if you encounter this error."
                )

            while True:
                self.state.batch = self.state.output = None
                try:
                    # Avoid Events.GET_BATCH_STARTED triggered twice when data iter is restarted
                    if self.last_event_name != Events.DATALOADER_STOP_ITERATION:
                        self._fire_event(Events.GET_BATCH_STARTED)
                        yield from self._maybe_terminate_or_interrupt()

                    iter_data_start_time = time.time()
                    self.state.batch = next(self._dataloader_iter)
                    self.state.times[Events.ITERATION_STARTED.name] = time.time() - iter_data_start_time

                    self._fire_event(Events.GET_BATCH_COMPLETED)
                    yield from self._maybe_terminate_or_interrupt()

                    iter_counter += 1
                    should_exit = False
                except (StopIteration, RuntimeError):
                    # Define self.state.epoch_length if it is not yet set
                    if self.state.epoch_length is None:
                        # Define epoch length and stop the epoch
                        self.state.epoch_length = iter_counter
                        break

                    # Should exit while loop if we can not iterate
                    if should_exit:
                        if not self._is_done(self.state) and self.state.max_epochs is not None:
                            total_iters = self.state.epoch_length * self.state.max_epochs
                            warnings.warn(
                                "Data iterator can not provide data anymore but required total number of "
                                "iterations to run is not reached. "
                                f"Current iteration: {self.state.iteration} vs Total iterations to run : {total_iters}"
                            )
                        break

                    self._fire_event(Events.DATALOADER_STOP_ITERATION)
                    yield from self._maybe_terminate_or_interrupt()

                    self._setup_dataloader_iter()
                    should_exit = True

                    continue

                self.state.iteration += 1
                self._fire_event(Events.ITERATION_STARTED)
                yield from self._maybe_terminate_or_interrupt()

                self.state.output = self._process_function(self, self.state.batch)
                self.state.times[Events.ITERATION_COMPLETED.name] = time.time() - iter_data_start_time
                self._fire_event(Events.ITERATION_COMPLETED)
                yield from self._maybe_terminate_or_interrupt()

                if self.state.epoch_length is not None and iter_counter == self.state.epoch_length:
                    break

        except _EngineTerminateSingleEpochException:
            self._fire_event(Events.TERMINATE_SINGLE_EPOCH, iter_counter=iter_counter)
            self.should_terminate_single_epoch = False
            self._setup_dataloader_iter()

        except _EngineTerminateException as e:
            # we need to reraise this exception such that it is not handled
            # as a general exception by the code below
            raise e

        except Exception as e:
            self.logger.error(f"Current run is terminating due to exception: {e}")
            self._handle_exception(e)

        return time.time() - start_time

    def _maybe_terminate_legacy(self) -> None:
        if self.should_terminate:
            raise _EngineTerminateException()

        if self.should_terminate_single_epoch:
            raise _EngineTerminateSingleEpochException()

    def _internal_run_legacy(self) -> State:
        # internal_run without generator for BC
        self.should_terminate = self.should_terminate_single_epoch = self.should_interrupt = False
        self._init_timers(self.state)
        try:
            try:
                start_time = time.time()
                self._fire_event(Events.STARTED)
                self._maybe_terminate_legacy()

                while not self._is_done(self.state) and not self.should_terminate:
                    self.state.epoch += 1
                    handlers_start_time = time.time()
                    self._fire_event(Events.EPOCH_STARTED)
                    epoch_time_taken = time.time() - handlers_start_time
                    self._maybe_terminate_legacy()

                    if self._dataloader_iter is None:
                        self._setup_engine()

                    epoch_time_taken += self._run_once_on_dataset_legacy()

                    # time is available for handlers but must be updated after fire
                    self.state.times[Events.EPOCH_COMPLETED.name] = epoch_time_taken

                    handlers_start_time = time.time()
                    self._fire_event(Events.EPOCH_COMPLETED)
                    epoch_time_taken += time.time() - handlers_start_time
                    # update time wrt handlers
                    self.state.times[Events.EPOCH_COMPLETED.name] = epoch_time_taken
                    self._maybe_terminate_legacy()

                    hours, mins, secs = _to_hours_mins_secs(epoch_time_taken)
                    self.logger.info(
                        f"Epoch[{self.state.epoch}] Complete. Time taken: {hours:02d}:{mins:02d}:{secs:06.3f}"
                    )

            except _EngineTerminateException:
                self._fire_event(Events.TERMINATE)

            time_taken = time.time() - start_time
            # time is available for handlers but must be updated after fire
            self.state.times[Events.COMPLETED.name] = time_taken
            handlers_start_time = time.time()
            self._fire_event(Events.COMPLETED)
            time_taken += time.time() - handlers_start_time
            # update time wrt handlers
            self.state.times[Events.COMPLETED.name] = time_taken
            hours, mins, secs = _to_hours_mins_secs(time_taken)
            self.logger.info(f"Engine run complete. Time taken: {hours:02d}:{mins:02d}:{secs:06.3f}")

        except BaseException as e:
            self._dataloader_iter = None
            self.logger.error(f"Engine run is terminating due to exception: {e}")
            self._handle_exception(e)

        self._dataloader_iter = None
        return self.state

    def _run_once_on_dataset_legacy(self) -> float:
        start_time = time.time()

        # We need to setup iter_counter > 0 if we resume from an iteration
        iter_counter = 0 if self._init_iter is None else self._init_iter
        self._init_iter = None
        should_exit = False
        try:
            if self._dataloader_iter is None:
                raise RuntimeError(
                    "Internal error, self._dataloader_iter is None. "
                    "Please, file an issue if you encounter this error."
                )

            while True:
                self.state.batch = self.state.output = None
                try:
                    # Avoid Events.GET_BATCH_STARTED triggered twice when data iter is restarted
                    if self.last_event_name != Events.DATALOADER_STOP_ITERATION:
                        self._fire_event(Events.GET_BATCH_STARTED)
                        self._maybe_terminate_legacy()

                    self.state.batch = next(self._dataloader_iter)
                    self._fire_event(Events.GET_BATCH_COMPLETED)
                    self._maybe_terminate_legacy()

                    iter_counter += 1
                    should_exit = False
                except (StopIteration, RuntimeError):
                    # Define self.state.epoch_length if it is not yet set
                    if self.state.epoch_length is None:
                        # Define epoch length and stop the epoch
                        self.state.epoch_length = iter_counter
                        break

                    # Should exit while loop if we can not iterate
                    if should_exit:
                        if not self._is_done(self.state) and self.state.max_epochs is not None:
                            total_iters = self.state.epoch_length * self.state.max_epochs
                            warnings.warn(
                                "Data iterator can not provide data anymore but required total number of "
                                "iterations to run is not reached. "
                                f"Current iteration: {self.state.iteration} vs Total iterations to run : {total_iters}"
                            )
                        break

                    self._fire_event(Events.DATALOADER_STOP_ITERATION)
                    self._maybe_terminate_legacy()

                    self._setup_dataloader_iter()
                    should_exit = True

                    continue

                self.state.iteration += 1
                self._fire_event(Events.ITERATION_STARTED)
                self._maybe_terminate_legacy()

                self.state.output = self._process_function(self, self.state.batch)
                self._fire_event(Events.ITERATION_COMPLETED)
                self._maybe_terminate_legacy()

                if self.state.epoch_length is not None and iter_counter == self.state.epoch_length:
                    break

        except _EngineTerminateSingleEpochException:
            self._fire_event(Events.TERMINATE_SINGLE_EPOCH, iter_counter=iter_counter)
            self.should_terminate_single_epoch = False
            self._setup_dataloader_iter()

        except _EngineTerminateException as e:
            # we need to reraise this exception such that it is not handled
            # as a general exception by the code below
            raise e

        except Exception as e:
            self.logger.error(f"Current run is terminating due to exception: {e}")
            self._handle_exception(e)

        return time.time() - start_time


def _get_none_data_iter(size: int) -> Iterator:
    # Sized iterator for data as None
    for _ in range(size):
        yield None


class _EngineTerminateSingleEpochException(Exception):
    """
    Exception associated with Terminate Single Epoch event
    """
    pass


class _EngineTerminateException(Exception):
    """
    Exception associated with Terminate event
    """
    pass
