#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : events.py    
@Author        : yanxiaodong
@Date          : 2022/11/28
@Description   :
"""
import numbers
import weakref
from enum import Enum
from types import DynamicClassAttribute
from typing import (Any, Callable, Dict, Iterable, Iterator, List, Optional,
                    Union)

from gaea_operator.plugin import DataLoader

from .utils import _check_signature


class CallableEventWithFilter(object):
    """
    Single Event containing a filter, specifying whether the event should
    be run at the current event (if the event type is correct)

    Args:
        value: The actual enum value. Only needed for internal use. Do not touch!
        event_filter: A function taking the engine and the current event value as input and returning a
            boolean to indicate whether this event should be executed. Defaults to None, which will result to a
            function that always returns `True`
        name: The enum-name of the current object. Only needed for internal use. Do not touch!
    """

    def __init__(self, value: str, event_filter: Optional[Callable] = None, name: Optional[str] = None) -> None:
        self.filter = event_filter

        if not hasattr(self, "_value_"):
            self._value_ = value

        if not hasattr(self, "_name_") and name is not None:
            self._name_ = name

    # copied to be compatible to enum
    @DynamicClassAttribute
    def name(self) -> str:
        """The name of the Enum member."""
        return self._name_

    @DynamicClassAttribute
    def value(self) -> str:
        """The value of the Enum member."""
        return self._value_

    def __call__(
        self, event_filter: Optional[Callable] = None, every: Optional[int] = None, once: Optional[int] = None
    ) -> "CallableEventWithFilter":
        """
        Makes the event class callable and accepts either an arbitrary callable as filter
        (which must take in the engine and current event value and return a boolean) or an every or once value

        Args:
            event_filter: a filter function to check if the event should be executed when
                the event type was fired
            every: a value specifying how often the event should be fired
            once: a value specifying when the event should be fired (if only once)

        Returns:
            CallableEventWithFilter: A new event having the same value but a different filter function
        """

        if not ((event_filter is not None) ^ (every is not None) ^ (once is not None)):
            raise ValueError("Only one of the input arguments should be specified")

        if (event_filter is not None) and not callable(event_filter):
            raise TypeError("Argument event_filter should be a callable")

        if (every is not None) and not (isinstance(every, numbers.Integral) and every > 0):
            raise ValueError("Argument every should be integer and greater than zero")

        if (once is not None) and not (isinstance(once, numbers.Integral) and once > 0):
            raise ValueError("Argument once should be integer and positive")

        if every is not None:
            if every == 1:
                # Just return the event itself
                event_filter = None
            else:
                event_filter = self.every_event_filter(every)

        if once is not None:
            event_filter = self.once_event_filter(once)

        # check signature:
        if event_filter is not None:
            _check_signature(event_filter, "event_filter", "engine", "event")

        return CallableEventWithFilter(self.value, event_filter, self.name)

    @staticmethod
    def every_event_filter(every: int) -> Callable:
        """A wrapper for every event filter."""

        def wrapper(engine: "Engine", event: int) -> bool:
            if event % every == 0:
                return True
            return False

        return wrapper

    @staticmethod
    def once_event_filter(once: int) -> Callable:
        """A wrapper for once event filter."""

        def wrapper(engine: "Engine", event: int) -> bool:
            if event == once:
                return True
            return False

        return wrapper

    def __repr__(self) -> str:
        out = f"Events.{self.name}"
        if self.filter is not None:
            out += f"(filter={self.filter})"
        return out

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, CallableEventWithFilter):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        else:
            return NotImplemented

    def __hash__(self) -> int:
        return hash(self._name_)

    def __or__(self, other: Any) -> "EventsList":
        return EventsList() | self | other


class EventEnum(CallableEventWithFilter, Enum):
    """
    Base class for all :class:`~Events`. User defined custom events should also inherit this class.
    """

    pass


class Events(EventEnum):
    """Events that are fired by the :class:`~Engine` during execution. Built-in events:

    - STARTED : triggered when engine's run is started
    - EPOCH_STARTED : triggered when the epoch is started
    - GET_BATCH_STARTED : triggered before next batch is fetched
    - GET_BATCH_COMPLETED : triggered after the batch is fetched
    - ITERATION_STARTED : triggered when an iteration is started
    - ITERATION_COMPLETED : triggered when the iteration is ended

    - DATALOADER_STOP_ITERATION : engine's specific event triggered when dataloader has no more data to provide

    - EXCEPTION_RAISED : triggered when an exception is encountered
    - TERMINATE_SINGLE_EPOCH : triggered when the run is about to end the current epoch,
      after receiving a :meth:`~terminate_epoch()` or :meth:`~Engine.terminate()` call.

    - TERMINATE : triggered when the run is about to end completely, after receiving :meth:`~terminate()` call.

    - EPOCH_COMPLETED : triggered when the epoch is ended. Note that this is triggered even
      when :meth:`Engine.terminate_epoch()` is called.
    - COMPLETED : triggered when engine's run is completed
    """

    EPOCH_STARTED = "epoch_started"
    """triggered when the epoch is started."""
    EPOCH_COMPLETED = "epoch_completed"
    """Event attribute indicating epoch is ended."""

    STARTED = "started"
    """triggered when engine's run is started."""
    COMPLETED = "completed"
    """triggered when engine's run is completed"""

    ITERATION_STARTED = "iteration_started"
    """triggered when an iteration is started."""
    ITERATION_COMPLETED = "iteration_completed"
    """triggered when the iteration is ended."""
    EXCEPTION_RAISED = "exception_raised"
    """triggered when an exception is encountered."""

    GET_BATCH_STARTED = "get_batch_started"
    """triggered before next batch is fetched."""
    GET_BATCH_COMPLETED = "get_batch_completed"
    """triggered after the batch is fetched."""

    DATALOADER_STOP_ITERATION = "dataloader_stop_iteration"
    """engine's specific event triggered when dataloader has no more data to provide"""
    TERMINATE = "terminate"
    """triggered when the run is about to end completely, after receiving terminate() call."""
    TERMINATE_SINGLE_EPOCH = "terminate_single_epoch"
    """triggered when the run is about to end the current epoch,
    after receiving a terminate_epoch() call."""
    INTERRUPT = "interrupt"
    """triggered when the run is interrupted, after receiving interrupt() call."""

    def __or__(self, other: Any) -> "EventsList":
        return EventsList() | self | other


class EventsList:
    """
    Collection of events stacked by operator `__or__`.
    """

    def __init__(self) -> None:
        self._events = []  # type: List[Union[Events, CallableEventWithFilter]]

    def _append(self, event: Union[Events, CallableEventWithFilter]) -> None:
        if not isinstance(event, (Events, CallableEventWithFilter)):
            raise TypeError(f"Argument event should be Events or CallableEventWithFilter, got: {type(event)}")
        self._events.append(event)

    def __getitem__(self, item: int) -> Union[Events, CallableEventWithFilter]:
        return self._events[item]

    def __iter__(self) -> Iterator[Union[Events, CallableEventWithFilter]]:
        return iter(self._events)

    def __len__(self) -> int:
        return len(self._events)

    def __or__(self, other: Union[Events, CallableEventWithFilter]) -> "EventsList":
        self._append(event=other)
        return self


class State(object):
    """An object that is used to pass internal and user-defined state between event handlers. By default, state
    contains the following attributes:

    .. code-block:: python

        state.iteration         # 1-based, the first iteration is 1
        state.epoch             # 1-based, the first epoch is 1
        state.seed              # seed to set at each epoch
        state.dataloader        # data passed to engine
        state.epoch_length      # optional length of an epoch
        state.max_epochs        # number of epochs to run
        state.batch             # batch passed to `process_function`
        state.output            # output of `process_function` after a single iteration
        state.metrics           # dictionary with defined metrics if any
        state.times             # dictionary with total and per-epoch times fetched on
                                # keys: Events.EPOCH_COMPLETED.name and Events.COMPLETED.name

    Args:
        kwargs: keyword arguments to be defined as State attributes.
    """

    event_to_attr = {
        Events.GET_BATCH_STARTED: "iteration",
        Events.GET_BATCH_COMPLETED: "iteration",
        Events.ITERATION_STARTED: "iteration",
        Events.ITERATION_COMPLETED: "iteration",
        Events.EPOCH_STARTED: "epoch",
        Events.EPOCH_COMPLETED: "epoch",
        Events.STARTED: "epoch",
        Events.COMPLETED: "epoch",
    }  # type: Dict[Union[str, "Events", "CallableEventWithFilter"], str]

    def __init__(self, **kwargs: Any) -> None:
        self.iteration = 0
        self.epoch = 0
        self.epoch_length = None  # type: Optional[int]
        self.max_epochs = None  # type: Optional[int]
        self.output = None  # type: Optional[Any]
        self.batch = None  # type: Optional[int]
        self.metrics = {}  # type: Dict[str, Any]
        self.dataloader = None  # type: Optional[Union[DataLoader, Iterable[Any]]]
        self.seed = None  # type: Optional[int]
        self.times = {
            Events.EPOCH_COMPLETED.name: None,
            Events.COMPLETED.name: None,
            Events.ITERATION_STARTED.name: None,
            Events.ITERATION_COMPLETED.name: None,
        }  # type: Dict[str, Optional[float]]

        for k, v in kwargs.items():
            setattr(self, k, v)
        self._update_attrs()

    def _update_attrs(self) -> None:
        for value in self.event_to_attr.values():
            if not hasattr(self, value):
                setattr(self, value, 0)

    def get_event_attrib_value(self, event_name: Union[str, Events, CallableEventWithFilter]) -> int:
        """Get the value of Event attribute with given `event_name`."""
        if event_name not in State.event_to_attr:
            raise RuntimeError(f"Unknown event name '{event_name}'")
        return getattr(self, State.event_to_attr[event_name])

    def __repr__(self) -> str:
        s = "State:\n"
        for attr, value in self.__dict__.items():
            if not isinstance(value, (numbers.Number, str)):
                value = type(value)
            s += f"\t{attr}: {value}\n"
        return s


class RemovableEventHandle:
    """
    A weakref handle to remove a registered event.

    A handle that may be used to remove a registered event handler via the
    remove method, with-statement, or context manager protocol. Returned from
    :meth:`~Engine.add_event_handler`.

    Args:
        event_name: Registered event name.
        handler: Registered event handler, stored as weakref.
        engine: Target engine, stored as weakref.
    """

    def __init__(
        self, event_name: Union[CallableEventWithFilter, Enum, EventsList, Events], handler: Callable, engine: "Engine"
    ) -> None:
        self.event_name = event_name
        self.handler = weakref.ref(handler)
        self.engine = weakref.ref(engine)

    def remove(self) -> None:
        """Remove handler from engine."""
        handler = self.handler()
        engine = self.engine()

        if handler is None or engine is None:
            return

        if hasattr(handler, "_parent"):
            handler = handler._parent()  # type: ignore[attr-defined]
            if handler is None:
                raise RuntimeError(
                    "Internal error! Please fill an issue on https://github.com/pytorch/ignite/issues "
                    "if encounter this error. Thank you!"
                )

        if isinstance(self.event_name, EventsList):
            for e in self.event_name:
                if engine.has_event_handler(handler, e):
                    engine.remove_event_handler(handler, e)
        else:
            if engine.has_event_handler(handler, self.event_name):
                engine.remove_event_handler(handler, self.event_name)

    def __enter__(self) -> "RemovableEventHandle":
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        self.remove()
