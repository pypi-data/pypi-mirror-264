import io
import logging
import sys
import warnings
from builtins import print
from contextlib import contextmanager
from functools import lru_cache
from typing import TYPE_CHECKING, Dict, Optional, Union

import nebula
from nebula.exceptions import MissingContextError
from nebula.logging.filters import ObfuscateApiKeyFilter

if TYPE_CHECKING:
    from nebula.client.schemas import FlowRun as ClientFlowRun
    from nebula.client.schemas.objects import FlowRun, TaskRun
    from nebula.context import RunContext
    from nebula.flows import Flow
    from nebula.tasks import Task


class NebulaLogAdapter(logging.LoggerAdapter):
    """
    Adapter that ensures extra kwargs are passed through correctly; without this
    the `extra` fields set on the adapter would overshadow any provided on a
    log-by-log basis.

    See https://bugs.python.org/issue32732 — the Python team has declared that this is
    not a bug in the LoggingAdapter and subclassing is the intended workaround.
    """

    def process(self, msg, kwargs):
        kwargs["extra"] = {**(self.extra or {}), **(kwargs.get("extra") or {})}

        from nebula._internal.compatibility.deprecated import (
            NebulaDeprecationWarning,
            generate_deprecation_message,
        )

        if "send_to_orion" in kwargs["extra"]:
            warnings.warn(
                generate_deprecation_message(
                    'The "send_to_orion" option',
                    start_date="May 2023",
                    help='Use "send_to_api" instead.',
                ),
                NebulaDeprecationWarning,
                stacklevel=4,
            )

        return (msg, kwargs)

    def getChild(
        self, suffix: str, extra: Optional[Dict[str, str]] = None
    ) -> "NebulaLogAdapter":
        if extra is None:
            extra = {}

        return NebulaLogAdapter(
            self.logger.getChild(suffix),
            extra={
                **self.extra,
                **extra,
            },
        )


@lru_cache()
def get_logger(name: str = None) -> logging.Logger:
    """
    Get a `nebula` logger. These loggers are intended for internal use within the
    `nebula` package.

    See `get_run_logger` for retrieving loggers for use within task or flow runs.
    By default, only run-related loggers are connected to the `APILogHandler`.
    """
    parent_logger = logging.getLogger("nebula")

    if name:
        # Append the name if given but allow explicit full names e.g. "nebula.test"
        # should not become "nebula.nebula.test"
        if not name.startswith(parent_logger.name + "."):
            logger = parent_logger.getChild(name)
        else:
            logger = logging.getLogger(name)
    else:
        logger = parent_logger

    # Prevent the current API key from being logged in plain text
    obfuscate_api_key_filter = ObfuscateApiKeyFilter()
    logger.addFilter(obfuscate_api_key_filter)

    return logger


def get_run_logger(
    context: "RunContext" = None, **kwargs: str
) -> Union[logging.Logger, logging.LoggerAdapter]:
    """
    Get a Nebula logger for the current task run or flow run.

    The logger will be named either `nebula.task_runs` or `nebula.flow_runs`.
    Contextual data about the run will be attached to the log records.

    These loggers are connected to the `APILogHandler` by default to send log records to
    the API.

    Arguments:
        context: A specific context may be provided as an override. By default, the
            context is inferred from global state and this should not be needed.
        **kwargs: Additional keyword arguments will be attached to the log records in
            addition to the run metadata

    Raises:
        RuntimeError: If no context can be found
    """
    # Check for existing contexts
    task_run_context = nebula.context.TaskRunContext.get()
    flow_run_context = nebula.context.FlowRunContext.get()

    # Apply the context override
    if context:
        if isinstance(context, nebula.context.FlowRunContext):
            flow_run_context = context
        elif isinstance(context, nebula.context.TaskRunContext):
            task_run_context = context
        else:
            raise TypeError(
                f"Received unexpected type {type(context).__name__!r} for context. "
                "Expected one of 'None', 'FlowRunContext', or 'TaskRunContext'."
            )

    # Determine if this is a task or flow run logger
    if task_run_context:
        logger = task_run_logger(
            task_run=task_run_context.task_run,
            task=task_run_context.task,
            flow_run=flow_run_context.flow_run if flow_run_context else None,
            flow=flow_run_context.flow if flow_run_context else None,
            **kwargs,
        )
    elif flow_run_context:
        logger = flow_run_logger(
            flow_run=flow_run_context.flow_run, flow=flow_run_context.flow, **kwargs
        )
    elif (
        get_logger("nebula.flow_run").disabled
        and get_logger("nebula.task_run").disabled
    ):
        logger = logging.getLogger("null")
    else:
        raise MissingContextError("There is no active flow or task run context.")

    return logger


def flow_run_logger(
    flow_run: Union["FlowRun", "ClientFlowRun"],
    flow: Optional["Flow"] = None,
    **kwargs: str,
):
    """
    Create a flow run logger with the run's metadata attached.

    Additional keyword arguments can be provided to attach custom data to the log
    records.

    If the flow run context is available, see `get_run_logger` instead.
    """
    return NebulaLogAdapter(
        get_logger("nebula.flow_runs"),
        extra={
            **{
                "flow_run_name": flow_run.name if flow_run else "<unknown>",
                "flow_run_id": str(flow_run.id) if flow_run else "<unknown>",
                "flow_name": flow.name if flow else "<unknown>",
            },
            **kwargs,
        },
    )


def task_run_logger(
    task_run: "TaskRun",
    task: "Task" = None,
    flow_run: "FlowRun" = None,
    flow: "Flow" = None,
    **kwargs: str,
):
    """
    Create a task run logger with the run's metadata attached.

    Additional keyword arguments can be provided to attach custom data to the log
    records.

    If the task run context is available, see `get_run_logger` instead.

    If only the flow run context is available, it will be used for default values
    of `flow_run` and `flow`.
    """
    if not flow_run or not flow:
        flow_run_context = nebula.context.FlowRunContext.get()
        if flow_run_context:
            flow_run = flow_run or flow_run_context.flow_run
            flow = flow or flow_run_context.flow

    return NebulaLogAdapter(
        get_logger("nebula.task_runs"),
        extra={
            **{
                "task_run_id": str(task_run.id),
                "flow_run_id": str(task_run.flow_run_id),
                "task_run_name": task_run.name,
                "task_name": task.name if task else "<unknown>",
                "flow_run_name": flow_run.name if flow_run else "<unknown>",
                "flow_name": flow.name if flow else "<unknown>",
            },
            **kwargs,
        },
    )


@contextmanager
def disable_logger(name: str):
    """
    Get a logger by name and disables it within the context manager.
    Upon exiting the context manager, the logger is returned to its
    original state.
    """
    logger = logging.getLogger(name=name)

    # determine if it's already disabled
    base_state = logger.disabled
    try:
        # disable the logger
        logger.disabled = True
        yield
    finally:
        # return to base state
        logger.disabled = base_state


@contextmanager
def disable_run_logger():
    """
    Gets both `nebula.flow_run` and `nebula.task_run` and disables them
    within the context manager. Upon exiting the context manager, both loggers
    are returned to its original state.
    """
    with disable_logger("nebula.flow_run"), disable_logger("nebula.task_run"):
        yield


def print_as_log(*args, **kwargs):
    """
    A patch for `print` to send printed messages to the Nebula run logger.

    If no run is active, `print` will behave as if it were not patched.

    If `print` sends data to a file other than `sys.stdout` or `sys.stderr`, it will
    not be forwarded to the Nebula logger either.
    """
    from nebula.context import FlowRunContext, TaskRunContext

    context = TaskRunContext.get() or FlowRunContext.get()
    if (
        not context
        or not context.log_prints
        or kwargs.get("file") not in {None, sys.stdout, sys.stderr}
    ):
        return print(*args, **kwargs)

    logger = get_run_logger()

    # Print to an in-memory buffer; so we do not need to implement `print`
    buffer = io.StringIO()
    kwargs["file"] = buffer
    print(*args, **kwargs)

    # Remove trailing whitespace to prevent duplicates
    logger.info(buffer.getvalue().rstrip())


@contextmanager
def patch_print():
    """
    Patches the Python builtin `print` method to use `print_as_log`
    """
    import builtins

    original = builtins.print

    try:
        builtins.print = print_as_log
        yield
    finally:
        builtins.print = original
