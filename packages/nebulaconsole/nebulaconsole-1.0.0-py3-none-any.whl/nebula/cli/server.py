"""
Command line interface for working with Nebula
"""
import os
import textwrap
from functools import partial

import anyio
import anyio.abc
import typer

import nebula
from nebula.cli._types import NebulaTyper, SettingsOption
from nebula.cli._utilities import exit_with_error, exit_with_success
from nebula.cli.root import app
from nebula.logging import get_logger
from nebula.settings import (
    NEBULA_API_SERVICES_LATE_RUNS_ENABLED,
    NEBULA_API_SERVICES_SCHEDULER_ENABLED,
    NEBULA_LOGGING_SERVER_LEVEL,
    NEBULA_SERVER_ANALYTICS_ENABLED,
    NEBULA_SERVER_API_HOST,
    NEBULA_SERVER_API_KEEPALIVE_TIMEOUT,
    NEBULA_SERVER_API_PORT,
    NEBULA_UI_ENABLED,
)
from nebula.utilities.asyncutils import run_sync_in_worker_thread
from nebula.utilities.processutils import (
    get_sys_executable,
    run_process,
    setup_signal_handlers_server,
)

server_app = NebulaTyper(
    name="server",
    help="Commands for interacting with a self-hosted Nebula server instance.",
)
database_app = NebulaTyper(
    name="database", help="Commands for interacting with the database."
)
server_app.add_typer(database_app)
app.add_typer(server_app)

logger = get_logger(__name__)


def generate_welcome_blurb(base_url, ui_enabled: bool):
    blurb = textwrap.dedent(
        r"""
        ███╗   ██╗███████╗██████╗ ██╗   ██╗██╗      █████╗ 
        ████╗  ██║██╔════╝██╔══██╗██║   ██║██║     ██╔══██╗
        ██╔██╗ ██║█████╗  ██████╔╝██║   ██║██║     ███████║
        ██║╚██╗██║██╔══╝  ██╔══██╗██║   ██║██║     ██╔══██║
        ██║ ╚████║███████╗██████╔╝╚██████╔╝███████╗██║  ██║
        ╚═╝  ╚═══╝╚══════╝╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝

        Configure Nebula to communicate with the server with:

            nebula config set NEBULA_API_URL={api_url}

        View the API reference documentation at {docs_url}
        """
    ).format(api_url=base_url + "/api", docs_url=base_url + "/docs")

    visit_dashboard = textwrap.dedent(
        f"""
        Check out the dashboard at {base_url}
        """
    )

    dashboard_not_built = textwrap.dedent(
        """
        The dashboard is not built. It looks like you're on a development version.
        See `nebula dev` for development commands.
        """
    )

    dashboard_disabled = textwrap.dedent(
        """
        The dashboard is disabled. Set `NEBULA_UI_ENABLED=1` to re-enable it.
        """
    )

    if not os.path.exists(nebula.__ui_static_path__):
        blurb += dashboard_not_built
    elif not ui_enabled:
        blurb += dashboard_disabled
    else:
        blurb += visit_dashboard

    return blurb


@server_app.command()
async def start(
    host: str = SettingsOption(NEBULA_SERVER_API_HOST),
    port: int = SettingsOption(NEBULA_SERVER_API_PORT),
    keep_alive_timeout: int = SettingsOption(NEBULA_SERVER_API_KEEPALIVE_TIMEOUT),
    log_level: str = SettingsOption(NEBULA_LOGGING_SERVER_LEVEL),
    scheduler: bool = SettingsOption(NEBULA_API_SERVICES_SCHEDULER_ENABLED),
    analytics: bool = SettingsOption(
        NEBULA_SERVER_ANALYTICS_ENABLED, "--analytics-on/--analytics-off"
    ),
    late_runs: bool = SettingsOption(NEBULA_API_SERVICES_LATE_RUNS_ENABLED),
    ui: bool = SettingsOption(NEBULA_UI_ENABLED),
):
    """Start a Nebula server instance"""

    server_env = os.environ.copy()
    server_env["NEBULA_API_SERVICES_SCHEDULER_ENABLED"] = str(scheduler)
    server_env["NEBULA_SERVER_ANALYTICS_ENABLED"] = str(analytics)
    server_env["NEBULA_API_SERVICES_LATE_RUNS_ENABLED"] = str(late_runs)
    server_env["NEBULA_API_SERVICES_UI"] = str(ui)
    server_env["NEBULA_LOGGING_SERVER_LEVEL"] = log_level

    base_url = f"http://{host}:{port}"

    async with anyio.create_task_group() as tg:
        app.console.print(generate_welcome_blurb(base_url, ui_enabled=ui))
        app.console.print("\n")

        server_process_id = await tg.start(
            partial(
                run_process,
                command=[
                    get_sys_executable(),
                    "-m",
                    "uvicorn",
                    "--app-dir",
                    # quote wrapping needed for windows paths with spaces
                    f'"{nebula.__module_path__.parent}"',
                    "--factory",
                    "nebula.server.api.server:create_app",
                    "--host",
                    str(host),
                    "--port",
                    str(port),
                    "--timeout-keep-alive",
                    str(keep_alive_timeout),
                ],
                env=server_env,
                stream_output=True,
            )
        )

        # Explicitly handle the interrupt signal here, as it will allow us to
        # cleanly stop the uvicorn server. Failing to do that may cause a
        # large amount of anyio error traces on the terminal, because the
        # SIGINT is handled by Typer/Click in this process (the parent process)
        # and will start shutting down subprocesses:
        # https://github.com/kozmoai/server/issues/2475

        setup_signal_handlers_server(
            server_process_id, "the Nebula server", app.console.print
        )

    app.console.print("Server stopped!")


@database_app.command()
async def reset(yes: bool = typer.Option(False, "--yes", "-y")):
    """Drop and recreate all Nebula database tables"""
    from nebula.server.database.dependencies import provide_database_interface

    db = provide_database_interface()
    engine = await db.engine()
    if not yes:
        confirm = typer.confirm(
            "Are you sure you want to reset the Nebula database located "
            f'at "{engine.url!r}"? This will drop and recreate all tables.'
        )
        if not confirm:
            exit_with_error("Database reset aborted")
    app.console.print("Downgrading database...")
    await db.drop_db()
    app.console.print("Upgrading database...")
    await db.create_db()
    exit_with_success(f'Nebula database "{engine.url!r}" reset!')


@database_app.command()
async def upgrade(
    yes: bool = typer.Option(False, "--yes", "-y"),
    revision: str = typer.Option(
        "head",
        "-r",
        help=(
            "The revision to pass to `alembic upgrade`. If not provided, runs all"
            " migrations."
        ),
    ),
    dry_run: bool = typer.Option(
        False,
        help=(
            "Flag to show what migrations would be made without applying them. Will"
            " emit sql statements to stdout."
        ),
    ),
):
    """Upgrade the Nebula database"""
    from nebula.server.database.alembic_commands import alembic_upgrade
    from nebula.server.database.dependencies import provide_database_interface

    db = provide_database_interface()
    engine = await db.engine()

    if not yes:
        confirm = typer.confirm(
            f"Are you sure you want to upgrade the Nebula database at {engine.url!r}?"
        )
        if not confirm:
            exit_with_error("Database upgrade aborted!")

    app.console.print("Running upgrade migrations ...")
    await run_sync_in_worker_thread(alembic_upgrade, revision=revision, dry_run=dry_run)
    app.console.print("Migrations succeeded!")
    exit_with_success(f"Nebula database at {engine.url!r} upgraded!")


@database_app.command()
async def downgrade(
    yes: bool = typer.Option(False, "--yes", "-y"),
    revision: str = typer.Option(
        "-1",
        "-r",
        help=(
            "The revision to pass to `alembic downgrade`. If not provided, "
            "downgrades to the most recent revision. Use 'base' to run all "
            "migrations."
        ),
    ),
    dry_run: bool = typer.Option(
        False,
        help=(
            "Flag to show what migrations would be made without applying them. Will"
            " emit sql statements to stdout."
        ),
    ),
):
    """Downgrade the Nebula database"""
    from nebula.server.database.alembic_commands import alembic_downgrade
    from nebula.server.database.dependencies import provide_database_interface

    db = provide_database_interface()

    engine = await db.engine()

    if not yes:
        confirm = typer.confirm(
            "Are you sure you want to downgrade the Nebula "
            f"database at {engine.url!r}?"
        )
        if not confirm:
            exit_with_error("Database downgrade aborted!")

    app.console.print("Running downgrade migrations ...")
    await run_sync_in_worker_thread(
        alembic_downgrade, revision=revision, dry_run=dry_run
    )
    app.console.print("Migrations succeeded!")
    exit_with_success(f"Nebula database at {engine.url!r} downgraded!")


@database_app.command()
async def revision(
    message: str = typer.Option(
        None,
        "--message",
        "-m",
        help="A message to describe the migration.",
    ),
    autogenerate: bool = False,
):
    """Create a new migration for the Nebula database"""
    from nebula.server.database.alembic_commands import alembic_revision

    app.console.print("Running migration file creation ...")
    await run_sync_in_worker_thread(
        alembic_revision,
        message=message,
        autogenerate=autogenerate,
    )
    exit_with_success("Creating new migration file succeeded!")


@database_app.command()
async def stamp(revision: str):
    """Stamp the revision table with the given revision; don't run any migrations"""
    from nebula.server.database.alembic_commands import alembic_stamp

    app.console.print("Stamping database with revision ...")
    await run_sync_in_worker_thread(alembic_stamp, revision=revision)
    exit_with_success("Stamping database with revision succeeded!")
