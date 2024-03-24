from contextlib import AsyncExitStack
from typing import (
    Any,
    Dict,
    Iterable,
    Optional,
)

import anyio
from typing_extensions import Literal

from nebula._internal.concurrency.api import create_call, from_async, from_sync
from nebula.client.orchestration import NebulaClient
from nebula.client.schemas.objects import TaskRun
from nebula.context import EngineContext
from nebula.engine import (
    begin_task_map,
    get_task_call_return_value,
    wait_for_task_runs_and_report_crashes,
)
from nebula.futures import NebulaFuture
from nebula.results import ResultFactory
from nebula.task_runners import BaseTaskRunner
from nebula.tasks import Task
from nebula.utilities.asyncutils import sync_compatible

EngineReturnType = Literal["future", "state", "result"]


@sync_compatible
async def submit_autonomous_task_run_to_engine(
    task: Task,
    task_run: TaskRun,
    task_runner: BaseTaskRunner,
    parameters: Optional[Dict[str, Any]] = None,
    wait_for: Optional[Iterable[NebulaFuture]] = None,
    mapped: bool = False,
    return_type: EngineReturnType = "future",
    client: Optional[NebulaClient] = None,
) -> NebulaFuture:
    async with AsyncExitStack() as stack:
        parameters = parameters or {}
        with EngineContext(
            flow=None,
            flow_run=None,
            autonomous_task_run=task_run,
            task_runner=task_runner,
            client=client,
            parameters=parameters,
            result_factory=await ResultFactory.from_autonomous_task(task),
            background_tasks=await stack.enter_async_context(anyio.create_task_group()),
        ) as flow_run_context:
            begin_run = create_call(
                begin_task_map if mapped else get_task_call_return_value,
                task=task,
                flow_run_context=flow_run_context,
                parameters=parameters,
                wait_for=wait_for,
                return_type=return_type,
                task_runner=task_runner,
            )
            if task.isasync:
                future_result_or_state = await from_async.wait_for_call_in_loop_thread(
                    begin_run
                )
            else:
                future_result_or_state = from_sync.wait_for_call_in_loop_thread(
                    begin_run
                )

            if return_type == "future":
                await wait_for_task_runs_and_report_crashes(
                    task_run_futures=[future_result_or_state],
                    client=client,
                )
            return future_result_or_state
