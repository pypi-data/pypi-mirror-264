"""
Interface and implementations of various task runners.

[Task Runners](/concepts/task-runners/) in Nebula are responsible for managing the execution of Nebula task runs. Generally speaking, users are not expected to interact with task runners outside of configuring and initializing them for a flow.

Example:
    ```
    >>> from nebula import flow, task
    >>> from nebula.task_runners import SequentialTaskRunner
    >>> from typing import List
    >>>
    >>> @task
    >>> def say_hello(name):
    ...     print(f"hello {name}")
    >>>
    >>> @task
    >>> def say_goodbye(name):
    ...     print(f"goodbye {name}")
    >>>
    >>> @flow(task_runner=SequentialTaskRunner())
    >>> def greetings(names: List[str]):
    ...     for name in names:
    ...         say_hello(name)
    ...         say_goodbye(name)
    >>>
    >>> greetings(["arthur", "trillian", "ford", "marvin"])
    hello arthur
    goodbye arthur
    hello trillian
    goodbye trillian
    hello ford
    goodbye ford
    hello marvin
    goodbye marvin
    ```

    Switching to a `DaskTaskRunner`:
    ```
    >>> from nebula_dask.task_runners import DaskTaskRunner
    >>> flow.task_runner = DaskTaskRunner()
    >>> greetings(["arthur", "trillian", "ford", "marvin"])
    hello arthur
    goodbye arthur
    hello trillian
    hello ford
    goodbye marvin
    hello marvin
    goodbye ford
    goodbye trillian
    ```

For usage details, see the [Task Runners](/concepts/task-runners/) documentation.
"""
import abc
from contextlib import AsyncExitStack, asynccontextmanager
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Dict,
    Optional,
    Set,
    TypeVar,
)
from uuid import UUID

import anyio

from nebula._internal.concurrency.primitives import Event
from nebula.client.schemas.objects import State
from nebula.logging import get_logger
from nebula.states import exception_to_crashed_state
from nebula.utilities.collections import AutoEnum

if TYPE_CHECKING:
    import anyio.abc


T = TypeVar("T", bound="BaseTaskRunner")
R = TypeVar("R")


class TaskConcurrencyType(AutoEnum):
    SEQUENTIAL = AutoEnum.auto()
    CONCURRENT = AutoEnum.auto()
    PARALLEL = AutoEnum.auto()


CONCURRENCY_MESSAGES = {
    TaskConcurrencyType.SEQUENTIAL: "sequentially",
    TaskConcurrencyType.CONCURRENT: "concurrently",
    TaskConcurrencyType.PARALLEL: "in parallel",
}


class BaseTaskRunner(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self.logger = get_logger(f"task_runner.{self.name}")
        self._started: bool = False

    @property
    @abc.abstractmethod
    def concurrency_type(self) -> TaskConcurrencyType:
        pass  # noqa

    @property
    def name(self):
        return type(self).__name__.lower().replace("taskrunner", "")

    def duplicate(self):
        """
        Return a new task runner instance with the same options.
        """
        # The base class returns `NotImplemented` to indicate that this is not yet
        # implemented by a given task runner.
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        """
        Returns true if the task runners use the same options.
        """
        if type(other) == type(self) and (
            # Compare public attributes for naive equality check
            # Subclasses should implement this method with a check init option equality
            {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
            == {k: v for k, v in other.__dict__.items() if not k.startswith("_")}
        ):
            return True
        else:
            return NotImplemented

    @abc.abstractmethod
    async def submit(
        self,
        key: UUID,
        call: Callable[..., Awaitable[State[R]]],
    ) -> None:
        """
        Submit a call for execution and return a `NebulaFuture` that can be used to
        get the call result.

        Args:
            task_run: The task run being submitted.
            task_key: A unique key for this orchestration run of the task. Can be used
                for caching.
            call: The function to be executed
            run_kwargs: A dict of keyword arguments to pass to `call`

        Returns:
            A future representing the result of `call` execution
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def wait(self, key: UUID, timeout: float = None) -> Optional[State]:
        """
        Given a `NebulaFuture`, wait for its return state up to `timeout` seconds.
        If it is not finished after the timeout expires, `None` should be returned.

        Implementers should be careful to ensure that this function never returns or
        raises an exception.
        """
        raise NotImplementedError()

    @asynccontextmanager
    async def start(
        self: T,
    ) -> AsyncIterator[T]:
        """
        Start the task runner, preparing any resources necessary for task submission.

        Children should implement `_start` to prepare and clean up resources.

        Yields:
            The prepared task runner
        """
        if self._started:
            raise RuntimeError("The task runner is already started!")

        async with AsyncExitStack() as exit_stack:
            self.logger.debug("Starting task runner...")
            try:
                await self._start(exit_stack)
                self._started = True
                yield self
            finally:
                self.logger.debug("Shutting down task runner...")
                self._started = False

    async def _start(self, exit_stack: AsyncExitStack) -> None:
        """
        Create any resources required for this task runner to submit work.

        Cleanup of resources should be submitted to the `exit_stack`.
        """
        pass  # noqa

    def __str__(self) -> str:
        return type(self).__name__


class SequentialTaskRunner(BaseTaskRunner):
    """
    A simple task runner that executes calls as they are submitted.

    If writing synchronous tasks, this runner will always execute tasks sequentially.
    If writing async tasks, this runner will execute tasks sequentially unless grouped
    using `anyio.create_task_group` or `asyncio.gather`.
    """

    def __init__(self) -> None:
        super().__init__()
        self._results: Dict[str, State] = {}

    @property
    def concurrency_type(self) -> TaskConcurrencyType:
        return TaskConcurrencyType.SEQUENTIAL

    def duplicate(self):
        return type(self)()

    async def submit(
        self,
        key: UUID,
        call: Callable[..., Awaitable[State[R]]],
    ) -> None:
        # Run the function immediately and store the result in memory
        try:
            result = await call()
        except BaseException as exc:
            result = await exception_to_crashed_state(exc)

        self._results[key] = result

    async def wait(self, key: UUID, timeout: float = None) -> Optional[State]:
        return self._results[key]


class ConcurrentTaskRunner(BaseTaskRunner):
    """
    A concurrent task runner that allows tasks to switch when blocking on IO.
    Synchronous tasks will be submitted to a thread pool maintained by `anyio`.

    Example:
        ```
        Using a thread for concurrency:
        >>> from nebula import flow
        >>> from nebula.task_runners import ConcurrentTaskRunner
        >>> @flow(task_runner=ConcurrentTaskRunner)
        >>> def my_flow():
        >>>     ...
        ```
    """

    def __init__(self):
        # TODO: Consider adding `max_workers` support using anyio capacity limiters

        # Runtime attributes
        self._task_group: anyio.abc.TaskGroup = None
        self._result_events: Dict[UUID, Event] = {}
        self._results: Dict[UUID, Any] = {}
        self._keys: Set[UUID] = set()

        super().__init__()

    @property
    def concurrency_type(self) -> TaskConcurrencyType:
        return TaskConcurrencyType.CONCURRENT

    def duplicate(self):
        return type(self)()

    async def submit(
        self,
        key: UUID,
        call: Callable[[], Awaitable[State[R]]],
    ) -> None:
        if not self._started:
            raise RuntimeError(
                "The task runner must be started before submitting work."
            )

        if not self._task_group:
            raise RuntimeError(
                "The concurrent task runner cannot be used to submit work after "
                "serialization."
            )

        # Create an event to set on completion
        self._result_events[key] = Event()

        # Rely on the event loop for concurrency
        self._task_group.start_soon(self._run_and_store_result, key, call)

    async def wait(
        self,
        key: UUID,
        timeout: float = None,
    ) -> Optional[State]:
        if not self._task_group:
            raise RuntimeError(
                "The concurrent task runner cannot be used to wait for work after "
                "serialization."
            )

        return await self._get_run_result(key, timeout)

    async def _run_and_store_result(
        self, key: UUID, call: Callable[[], Awaitable[State[R]]]
    ):
        """
        Simple utility to store the orchestration result in memory on completion

        Since this run is occurring on the main thread, we capture exceptions to prevent
        task crashes from crashing the flow run.
        """
        try:
            result = await call()
        except BaseException as exc:
            result = await exception_to_crashed_state(exc)

        self._results[key] = result
        self._result_events[key].set()

    async def _get_run_result(
        self, key: UUID, timeout: float = None
    ) -> Optional[State]:
        """
        Block until the run result has been populated.
        """
        result = None  # retval on timeout

        # Note we do not use `asyncio.wrap_future` and instead use an `Event` to avoid
        # stdlib behavior where the wrapped future is cancelled if the parent future is
        # cancelled (as it would be during a timeout here)
        with anyio.move_on_after(timeout):
            await self._result_events[key].wait()
            result = self._results[key]

        return result  # timeout reached

    async def _start(self, exit_stack: AsyncExitStack):
        """
        Start the process pool
        """
        self._task_group = await exit_stack.enter_async_context(
            anyio.create_task_group()
        )

    def __getstate__(self):
        """
        Allow the `ConcurrentTaskRunner` to be serialized by dropping the task group.
        """
        data = self.__dict__.copy()
        data.update({k: None for k in {"_task_group"}})
        return data

    def __setstate__(self, data: dict):
        """
        When deserialized, we will no longer have a reference to the task group.
        """
        self.__dict__.update(data)
        self._task_group = None
