"""
Command line interface for working with agent services
"""

import os
from functools import partial
from typing import List
from uuid import UUID

import anyio
import typer

import nebula
from nebula.agent import NebulaAgent
from nebula.cli._types import NebulaTyper, SettingsOption
from nebula.cli._utilities import exit_with_error
from nebula.cli.root import app
from nebula.client import get_client
from nebula.exceptions import ObjectNotFound
from nebula.settings import (
    NEBULA_AGENT_PREFETCH_SECONDS,
    NEBULA_AGENT_QUERY_INTERVAL,
    NEBULA_API_URL,
)
from nebula.utilities.processutils import setup_signal_handlers_agent
from nebula.utilities.services import critical_service_loop

agent_app = NebulaTyper(
    name="agent",
    help="Commands for starting and interacting with agent processes.",
    deprecated=True,
    deprecated_name="agent",
    deprecated_start_date="Mar 2024",
    deprecated_help="Use `nebula worker start` instead. Refer to the upgrade guide for more information: https://docs.nebula.io/latest/guides/upgrade-guide-agents-to-workers/. ",
)
app.add_typer(agent_app)


ascii_name = r"""
 ███╗   ██╗███████╗██████╗ ██╗   ██╗██╗      █████╗      █████╗  ██████╗ ███████╗███╗   ██╗████████╗
 ████╗  ██║██╔════╝██╔══██╗██║   ██║██║     ██╔══██╗    ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝
 ██╔██╗ ██║█████╗  ██████╔╝██║   ██║██║     ███████║    ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   
 ██║╚██╗██║██╔══╝  ██╔══██╗██║   ██║██║     ██╔══██║    ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   
 ██║ ╚████║███████╗██████╔╝╚██████╔╝███████╗██║  ██║    ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   
 ╚═╝  ╚═══╝╚══════╝╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   
                                                                                                   
"""


@agent_app.command()
async def start(
    # deprecated main argument
    work_queue: str = typer.Argument(
        None,
        show_default=False,
        help="DEPRECATED: A work queue name or ID",
    ),
    work_queues: List[str] = typer.Option(
        None,
        "-q",
        "--work-queue",
        help="One or more work queue names for the agent to pull from.",
    ),
    work_queue_prefix: List[str] = typer.Option(
        None,
        "-m",
        "--match",
        help=(
            "Dynamically matches work queue names with the specified prefix for the"
            " agent to pull from,for example `dev-` will match all work queues with a"
            " name that starts with `dev-`"
        ),
    ),
    work_pool_name: str = typer.Option(
        None,
        "-p",
        "--pool",
        help="A work pool name for the agent to pull from.",
    ),
    hide_welcome: bool = typer.Option(False, "--hide-welcome"),
    api: str = SettingsOption(NEBULA_API_URL),
    run_once: bool = typer.Option(
        False, help="Run the agent loop once, instead of forever."
    ),
    prefetch_seconds: int = SettingsOption(NEBULA_AGENT_PREFETCH_SECONDS),
    # deprecated tags
    tags: List[str] = typer.Option(
        None,
        "-t",
        "--tag",
        help=(
            "DEPRECATED: One or more optional tags that will be used to create a work"
            " queue. This option will be removed on 2023-02-23."
        ),
    ),
    limit: int = typer.Option(
        None,
        "-l",
        "--limit",
        help="Maximum number of flow runs to start simultaneously.",
    ),
):
    """
    Start an agent process to poll one or more work queues for flow runs.
    """
    work_queues = work_queues or []

    if work_queue is not None:
        # try to treat the work_queue as a UUID
        try:
            async with get_client() as client:
                q = await client.read_work_queue(UUID(work_queue))
                work_queue = q.name
        # otherwise treat it as a string name
        except (TypeError, ValueError):
            pass
        work_queues.append(work_queue)
        app.console.print(
            (
                "Agents now support multiple work queues. Instead of passing a single"
                " argument, provide work queue names with the `-q` or `--work-queue`"
                f" flag: `nebula agent start -q {work_queue}`\n"
            ),
            style="blue",
        )

    if not work_queues and not tags and not work_queue_prefix and not work_pool_name:
        exit_with_error("No work queues provided!", style="red")
    elif bool(work_queues) + bool(tags) + bool(work_queue_prefix) > 1:
        exit_with_error(
            "Only one of `work_queues`, `match`, or `tags` can be provided.",
            style="red",
        )
    if work_pool_name and tags:
        exit_with_error(
            "`tag` and `pool` options cannot be used together.", style="red"
        )

    if tags:
        work_queue_name = f"Agent queue {'-'.join(sorted(tags))}"
        app.console.print(
            (
                "`tags` are deprecated. For backwards-compatibility with old versions"
                " of Nebula, this agent will create a work queue named"
                f" `{work_queue_name}` that uses legacy tag-based matching. This option"
                " will be removed on 2023-02-23."
            ),
            style="red",
        )

        async with get_client() as client:
            try:
                work_queue = await client.read_work_queue_by_name(work_queue_name)
                if work_queue.filter is None:
                    # ensure the work queue has legacy (deprecated) tag-based behavior
                    await client.update_work_queue(filter=dict(tags=tags))
            except ObjectNotFound:
                # if the work queue doesn't already exist, we create it with tags
                # to enable legacy (deprecated) tag-matching behavior
                await client.create_work_queue(name=work_queue_name, tags=tags)

        work_queues = [work_queue_name]

    if not hide_welcome:
        if api:
            app.console.print(
                f"Starting v{nebula.__version__} agent connected to {api}..."
            )
        else:
            app.console.print(
                f"Starting v{nebula.__version__} agent with ephemeral API..."
            )

    agent_process_id = os.getpid()
    setup_signal_handlers_agent(agent_process_id, "the Nebula agent", app.console.print)

    async with NebulaAgent(
        work_queues=work_queues,
        work_queue_prefix=work_queue_prefix,
        work_pool_name=work_pool_name,
        prefetch_seconds=prefetch_seconds,
        limit=limit,
    ) as agent:
        if not hide_welcome:
            app.console.print(ascii_name)
            if work_pool_name:
                app.console.print(
                    "Agent started! Looking for work from "
                    f"work pool '{work_pool_name}'..."
                )
            elif work_queue_prefix:
                app.console.print(
                    "Agent started! Looking for work from "
                    f"queue(s) that start with the prefix: {work_queue_prefix}..."
                )
            else:
                app.console.print(
                    "Agent started! Looking for work from "
                    f"queue(s): {', '.join(work_queues)}..."
                )

        async with anyio.create_task_group() as tg:
            tg.start_soon(
                partial(
                    critical_service_loop,
                    agent.get_and_submit_flow_runs,
                    NEBULA_AGENT_QUERY_INTERVAL.value(),
                    printer=app.console.print,
                    run_once=run_once,
                    jitter_range=0.3,
                    backoff=4,  # Up to ~1 minute interval during backoff
                )
            )

            tg.start_soon(
                partial(
                    critical_service_loop,
                    agent.check_for_cancelled_flow_runs,
                    NEBULA_AGENT_QUERY_INTERVAL.value() * 2,
                    printer=app.console.print,
                    run_once=run_once,
                    jitter_range=0.3,
                    backoff=4,
                )
            )

    app.console.print("Agent stopped!")
