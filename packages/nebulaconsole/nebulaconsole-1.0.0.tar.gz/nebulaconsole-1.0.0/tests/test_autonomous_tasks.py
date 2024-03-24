import asyncio
import inspect
import os
from pathlib import Path
from typing import AsyncGenerator, Iterable, Tuple
from unittest import mock

import pytest

import nebula.results
from nebula import Task, task, unmapped
from nebula.blocks.core import Block
from nebula.client.orchestration import NebulaClient, get_client
from nebula.client.schemas import TaskRun
from nebula.client.schemas.objects import StateType
from nebula.filesystems import LocalFileSystem
from nebula.results import ResultFactory
from nebula.server.api.task_runs import TaskQueue
from nebula.server.services.task_scheduling import TaskSchedulingTimeouts
from nebula.settings import (
    NEBULA_EXPERIMENTAL_ENABLE_TASK_SCHEDULING,
    NEBULA_LOCAL_STORAGE_PATH,
    NEBULA_TASK_SCHEDULING_DEFAULT_STORAGE_BLOCK,
    NEBULA_TASK_SCHEDULING_PENDING_TASK_TIMEOUT,
    temporary_settings,
)
from nebula.task_server import TaskServer
from nebula.utilities.asyncutils import sync_compatible
from nebula.utilities.hashing import hash_objects


@sync_compatible
async def result_factory_from_task(task) -> ResultFactory:
    return await ResultFactory.from_autonomous_task(task)


@pytest.fixture
def local_filesystem():
    block = LocalFileSystem(basepath="~/.nebula/storage/test")
    block.save("test-fs", overwrite=True)
    return block


@pytest.fixture(autouse=True)
def allow_experimental_task_scheduling():
    with temporary_settings(
        {
            NEBULA_EXPERIMENTAL_ENABLE_TASK_SCHEDULING: True,
        }
    ):
        yield


@pytest.fixture(autouse=True)
async def clear_scheduled_task_queues():
    TaskQueue.reset()
    yield
    TaskQueue.reset()


@pytest.fixture(autouse=True)
async def clear_cached_filesystems():
    nebula.results._default_task_scheduling_storages.clear()
    yield
    nebula.results._default_task_scheduling_storages.clear()


@pytest.fixture
def foo_task() -> Task:
    @task
    def foo(x: int) -> int:
        print(x)
        return x

    return foo


@pytest.fixture
def async_foo_task() -> Task:
    @task
    async def async_foo(x: int) -> int:
        print(x)
        return x

    return async_foo


@pytest.fixture
def foo_task_with_result_storage(foo_task, local_filesystem):
    return foo_task.with_options(result_storage=local_filesystem)


@pytest.fixture
def async_foo_task_with_result_storage(async_foo_task, local_filesystem):
    return async_foo_task.with_options(result_storage=local_filesystem)


def test_task_submission_fails_when_experimental_flag_off(foo_task):
    with temporary_settings({NEBULA_EXPERIMENTAL_ENABLE_TASK_SCHEDULING: False}):
        with pytest.raises(RuntimeError, match="Tasks cannot be run outside of a flow"):
            foo_task.submit(42)


def test_task_submission_with_parameters_uses_default_storage(foo_task):
    foo_task_without_result_storage = foo_task.with_options(result_storage=None)
    task_run = foo_task_without_result_storage.submit(42)

    result_factory = result_factory_from_task(foo_task)

    result_factory.read_parameters(task_run.state.state_details.task_parameters_id)


def test_task_submission_with_parameters_reuses_default_storage_block(
    foo_task: Task, tmp_path: Path
):
    with temporary_settings(
        {
            NEBULA_TASK_SCHEDULING_DEFAULT_STORAGE_BLOCK: "local-file-system/my-tasks",
            NEBULA_LOCAL_STORAGE_PATH: tmp_path / "some-storage",
        }
    ):
        # The block will not exist initially
        with pytest.raises(ValueError, match="Unable to find block document"):
            Block.load("local-file-system/my-tasks")

        foo_task_without_result_storage = foo_task.with_options(result_storage=None)
        task_run_a = foo_task_without_result_storage.submit(42)

        storage_before = Block.load("local-file-system/my-tasks")
        assert isinstance(storage_before, LocalFileSystem)
        assert storage_before.basepath == str(tmp_path / "some-storage")

        foo_task_without_result_storage = foo_task.with_options(result_storage=None)
        task_run_b = foo_task_without_result_storage.submit(24)

        storage_after = Block.load("local-file-system/my-tasks")
        assert isinstance(storage_after, LocalFileSystem)

        result_factory = result_factory_from_task(foo_task)
        assert result_factory.read_parameters(
            task_run_a.state.state_details.task_parameters_id
        ) == {"x": 42}
        assert result_factory.read_parameters(
            task_run_b.state.state_details.task_parameters_id
        ) == {"x": 24}


def test_task_submission_creates_a_scheduled_task_run(foo_task_with_result_storage):
    task_run = foo_task_with_result_storage.submit(42)
    assert task_run.state.is_scheduled()

    result_factory = result_factory_from_task(foo_task_with_result_storage)

    parameters = result_factory.read_parameters(
        task_run.state.state_details.task_parameters_id
    )

    assert parameters == dict(x=42)


async def test_sync_task_not_awaitable_in_async_context(foo_task):
    task_run = foo_task.submit(42)
    assert task_run.state.is_scheduled()

    result_factory = await result_factory_from_task(foo_task)

    parameters = await result_factory.read_parameters(
        task_run.state.state_details.task_parameters_id
    )

    assert parameters == dict(x=42)


async def test_async_task_submission_creates_a_scheduled_task_run(
    async_foo_task_with_result_storage,
):
    task_run = await async_foo_task_with_result_storage.submit(42)
    assert task_run.state.is_scheduled()

    result_factory = await result_factory_from_task(async_foo_task_with_result_storage)

    parameters = await result_factory.read_parameters(
        task_run.state.state_details.task_parameters_id
    )

    assert parameters == dict(x=42)


async def test_scheduled_tasks_are_enqueued_server_side(
    foo_task_with_result_storage: Task,
):
    task_run: TaskRun = foo_task_with_result_storage.submit(42)
    assert task_run.state.is_scheduled()

    enqueued: TaskRun = await TaskQueue.for_key(task_run.task_key).get()

    # The server-side task run through API-like serialization for comparison
    enqueued = TaskRun.parse_obj(enqueued.dict(json_compatible=True))

    # The server-side task run in the queue should be the same as the one returned
    # to the client, but some of the calculated fields will be populated server-side
    # after orchestration in a way that differs by microseconds, or the
    # created/updated dates are populated.

    assert task_run.state.created is None
    assert enqueued.state.created is not None
    task_run.state.created = enqueued.state.created

    assert task_run.state.updated is None
    assert enqueued.state.updated is not None
    task_run.state.updated = enqueued.state.updated

    assert task_run.estimated_start_time_delta is not None
    assert enqueued.estimated_start_time_delta is not None
    task_run.estimated_start_time_delta = enqueued.estimated_start_time_delta

    assert enqueued.dict() == task_run.dict()


@pytest.fixture
async def nebula_client() -> AsyncGenerator[NebulaClient, None]:
    async with get_client() as client:
        yield client


async def test_scheduled_tasks_are_restored_at_server_startup(
    foo_task_with_result_storage: Task, nebula_client: NebulaClient
):
    # run one iteration of the timeouts service
    service = TaskSchedulingTimeouts()
    await service.start(loops=1)

    # schedule a task
    task_run: TaskRun = foo_task_with_result_storage.submit(42)
    assert task_run.state.is_scheduled()

    # pull the task from the queue to make sure it's cleared; this simulates when a task
    # server pulls a task, then the nebula server dies
    enqueued: TaskRun = await TaskQueue.for_key(task_run.task_key).get()
    assert enqueued.id == task_run.id

    # verify there is no other task in queue
    with pytest.raises(asyncio.QueueEmpty):
        await TaskQueue.for_key(task_run.task_key).get_nowait()

    # Run another loop to show that the task is NOT re-enqueued after the first run
    await service.start(loops=1)

    with pytest.raises(asyncio.QueueEmpty):
        await TaskQueue.for_key(task_run.task_key).get_nowait()

    # now emulate that we've restarted the Nebula server by resetting the
    # TaskSchedulingTimeouts service
    service = TaskSchedulingTimeouts()
    await service.start(loops=1)

    # the task will still be SCHEDULED
    task_run = await nebula_client.read_task_run(task_run.id)
    assert task_run.state.type == StateType.SCHEDULED

    # ...and it should be re-enqueued
    enqueued: TaskRun = await TaskQueue.for_key(task_run.task_key).get()
    assert enqueued.id == task_run.id


async def test_stuck_pending_tasks_are_reenqueued(
    foo_task_with_result_storage: Task, nebula_client: NebulaClient
):
    task_run: TaskRun = foo_task_with_result_storage.submit(42)
    assert task_run.state.is_scheduled()

    # now we simulate a stuck task by having the TaskServer try to run it but fail
    server = TaskServer(foo_task_with_result_storage)
    with pytest.raises(ValueError):
        with mock.patch(
            "nebula.task_server.submit_autonomous_task_run_to_engine",
            side_effect=ValueError("woops"),
        ):
            await server.execute_task_run(task_run)

    # now the task will be in a stuck pending state
    task_run = await nebula_client.read_task_run(task_run.id)
    assert task_run.state.type == StateType.PENDING

    # now run an iteration of the TaskSchedulingTimeouts loop service with an absurdly
    # long timeout so that it will never happen
    with temporary_settings({NEBULA_TASK_SCHEDULING_PENDING_TASK_TIMEOUT: 1000000}):
        await TaskSchedulingTimeouts().start(loops=1)

    # the task will still be PENDING
    task_run = await nebula_client.read_task_run(task_run.id)
    assert task_run.state.type == StateType.PENDING

    # now run an iteration of the TaskSchedulingTimeouts loop service with a short
    # timeout so we can sleep past it and ensure that this task run will get picked up
    with temporary_settings({NEBULA_TASK_SCHEDULING_PENDING_TASK_TIMEOUT: 0.1}):
        await asyncio.sleep(0.2)
        await TaskSchedulingTimeouts().start(loops=1)

    # now the task will now be SCHEDULED
    task_run = await nebula_client.read_task_run(task_run.id)
    assert task_run.state.type == StateType.SCHEDULED

    # ...and it should be re-enqueued
    enqueued: TaskRun = await TaskQueue.for_key(task_run.task_key).get()
    assert enqueued.id == task_run.id


class TestCall:
    async def test_call(self, async_foo_task):
        result = await async_foo_task(42)

        assert result == 42

    async def test_call_with_return_state(self, async_foo_task):
        state = await async_foo_task(42, return_state=True)

        assert state.is_completed()

        assert await state.result() == 42


class TestMap:
    async def test_map(self, async_foo_task):
        task_runs = await async_foo_task.map([1, 2, 3])

        assert len(task_runs) == 3

        result_factory = await result_factory_from_task(async_foo_task)

        for i, task_run in enumerate(task_runs):
            assert task_run.state.is_scheduled()
            assert await result_factory.read_parameters(
                task_run.state.state_details.task_parameters_id
            ) == {"x": i + 1}

    async def test_map_with_implicitly_unmapped_kwargs(self):
        @task
        def bar(x: int, unmappable: int) -> Tuple[int, int]:
            return (x, unmappable)

        task_runs = bar.map([1, 2, 3], unmappable=42)

        assert len(task_runs) == 3

        result_factory = await result_factory_from_task(bar)

        for i, task_run in enumerate(task_runs):
            assert task_run.state.is_scheduled()
            assert await result_factory.read_parameters(
                task_run.state.state_details.task_parameters_id
            ) == {"x": i + 1, "unmappable": 42}

    async def test_async_map_with_implicitly_unmapped_kwargs(self):
        @task
        async def bar(x: int, unmappable: int) -> Tuple[int, int]:
            return (x, unmappable)

        task_runs = await bar.map([1, 2, 3], unmappable=42)

        assert len(task_runs) == 3

        result_factory = await result_factory_from_task(bar)

        for i, task_run in enumerate(task_runs):
            assert task_run.state.is_scheduled()
            assert await result_factory.read_parameters(
                task_run.state.state_details.task_parameters_id
            ) == {"x": i + 1, "unmappable": 42}

    async def test_map_with_explicit_unmapped_kwargs(self):
        @task
        def bar(x: int, mappable: Iterable) -> Tuple[int, Iterable]:
            return (x, mappable)

        task_runs = bar.map([1, 2, 3], mappable=unmapped(["some", "iterable"]))

        assert len(task_runs) == 3

        result_factory = await result_factory_from_task(bar)

        for i, task_run in enumerate(task_runs):
            assert task_run.state.is_scheduled()
            assert await result_factory.read_parameters(
                task_run.state.state_details.task_parameters_id
            ) == {"x": i + 1, "mappable": ["some", "iterable"]}

    async def test_async_map_with_explicit_unmapped_kwargs(self):
        @task
        async def bar(x: int, mappable: Iterable) -> Tuple[int, Iterable]:
            return (x, mappable)

        task_runs = await bar.map([1, 2, 3], mappable=unmapped(["some", "iterable"]))

        assert len(task_runs) == 3

        result_factory = await result_factory_from_task(bar)

        for i, task_run in enumerate(task_runs):
            assert task_run.state.is_scheduled()
            assert await result_factory.read_parameters(
                task_run.state.state_details.task_parameters_id
            ) == {"x": i + 1, "mappable": ["some", "iterable"]}


class TestTaskKey:
    def test_task_key_includes_qualname_and_source_file_hash(self):
        def some_fn():
            pass

        t = Task(fn=some_fn)
        source_file = os.path.abspath(inspect.getsourcefile(some_fn))
        task_origin_hash = hash_objects(t.name, source_file)
        assert t.task_key == f"{some_fn.__qualname__}-{task_origin_hash}"

    def test_task_key_handles_unknown_source_file(self, monkeypatch):
        def some_fn():
            pass

        monkeypatch.setattr(inspect, "getsourcefile", lambda x: None)
        t = Task(fn=some_fn)
        assert t.task_key == f"{some_fn.__qualname__}-unknown-source-file"
