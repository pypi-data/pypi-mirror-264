"""
Defines the Nebula REST API FastAPI app.
"""

import asyncio
import mimetypes
import os
import shutil
import sqlite3
from contextlib import asynccontextmanager
from functools import partial, wraps
from hashlib import sha256
from typing import Awaitable, Callable, Dict, List, Mapping, Optional, Tuple

import anyio
import asyncpg
import sqlalchemy as sa
import sqlalchemy.exc
import sqlalchemy.orm.exc
from nebula._vendor.fastapi import APIRouter, Depends, FastAPI, Request, status
from nebula._vendor.fastapi.encoders import jsonable_encoder
from nebula._vendor.fastapi.exceptions import RequestValidationError
from nebula._vendor.fastapi.middleware.cors import CORSMiddleware
from nebula._vendor.fastapi.middleware.gzip import GZipMiddleware
from nebula._vendor.fastapi.openapi.utils import get_openapi
from nebula._vendor.fastapi.responses import JSONResponse
from nebula._vendor.fastapi.staticfiles import StaticFiles
from nebula._vendor.starlette.exceptions import HTTPException

import nebula
import nebula.server.api as api
import nebula.server.services as services
import nebula.settings
from nebula._internal.compatibility.experimental import enabled_experiments
from nebula.client.constants import SERVER_API_VERSION
from nebula.logging import get_logger
from nebula.server.api.dependencies import EnforceMinimumAPIVersion
from nebula.server.exceptions import ObjectNotFoundError
from nebula.server.utilities.database import get_dialect
from nebula.server.utilities.server import method_paths_from_routes
from nebula.settings import (
    NEBULA_API_DATABASE_CONNECTION_URL,
    NEBULA_DEBUG_MODE,
    NEBULA_MEMO_STORE_PATH,
    NEBULA_MEMOIZE_BLOCK_AUTO_REGISTRATION,
    NEBULA_UI_SERVE_BASE,
)
from nebula.utilities.hashing import hash_objects

TITLE = "Nebula Server"
API_TITLE = "Nebula Nebula REST API"
UI_TITLE = "Nebula Nebula REST API UI"
API_VERSION = nebula.__version__

logger = get_logger("server")

enforce_minimum_version = EnforceMinimumAPIVersion(
    # this should be <= SERVER_API_VERSION; clients that send
    # a version header under this value will be rejected
    minimum_api_version="0.8.0",
    logger=logger,
)


API_ROUTERS = (
    api.flows.router,
    api.flow_runs.router,
    api.task_runs.router,
    api.flow_run_states.router,
    api.task_run_states.router,
    api.flow_run_notification_policies.router,
    api.deployments.router,
    api.saved_searches.router,
    api.logs.router,
    api.concurrency_limits.router,
    api.concurrency_limits_v2.router,
    api.block_types.router,
    api.block_documents.router,
    api.workers.router,
    api.work_queues.router,
    api.artifacts.router,
    api.block_schemas.router,
    api.block_capabilities.router,
    api.collections.router,
    api.variables.router,
    api.csrf_token.router,
    api.ui.flow_runs.router,
    api.ui.schemas.router,
    api.ui.task_runs.router,
    api.admin.router,
    api.root.router,
)

SQLITE_LOCKED_MSG = "database is locked"


class SPAStaticFiles(StaticFiles):
    """
    Implementation of `StaticFiles` for serving single page applications.

    Adds `get_response` handling to ensure that when a resource isn't found the
    application still returns the index.
    """

    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except HTTPException:
            return await super().get_response("./index.html", scope)


class RequestLimitMiddleware:
    """
    A middleware that limits the number of concurrent requests handled by the API.

    This is a blunt tool for limiting SQLite concurrent writes which will cause failures
    at high volume. Ideally, we would only apply the limit to routes that perform
    writes.
    """

    def __init__(self, app, limit: float):
        self.app = app
        self._limiter = anyio.CapacityLimiter(limit)

    async def __call__(self, scope, receive, send) -> None:
        async with self._limiter:
            await self.app(scope, receive, send)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Provide a detailed message for request validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "exception_message": "Invalid request received.",
                "exception_detail": exc.errors(),
                "request_body": exc.body,
            }
        ),
    )


async def integrity_exception_handler(request: Request, exc: Exception):
    """Capture database integrity errors."""
    logger.error("Encountered exception in request:", exc_info=True)
    return JSONResponse(
        content={
            "detail": (
                "Data integrity conflict. This usually means a "
                "unique or foreign key constraint was violated. "
                "See server logs for details."
            )
        },
        status_code=status.HTTP_409_CONFLICT,
    )


def is_client_retryable_exception(exc: Exception):
    if isinstance(exc, sqlalchemy.exc.OperationalError) and isinstance(
        exc.orig, sqlite3.OperationalError
    ):
        if getattr(exc.orig, "sqlite_errorname", None) in {
            "SQLITE_BUSY",
            "SQLITE_BUSY_SNAPSHOT",
        } or SQLITE_LOCKED_MSG in getattr(exc.orig, "args", []):
            return True
        else:
            # Avoid falling through to the generic `DBAPIError` case below
            return False

    if isinstance(
        exc,
        (
            sqlalchemy.exc.DBAPIError,
            asyncpg.exceptions.QueryCanceledError,
            asyncpg.exceptions.ConnectionDoesNotExistError,
            asyncpg.exceptions.CannotConnectNowError,
            sqlalchemy.exc.InvalidRequestError,
            sqlalchemy.orm.exc.DetachedInstanceError,
        ),
    ):
        return True

    return False


def replace_placeholder_string_in_files(
    directory, placeholder, replacement, allowed_extensions=None
):
    """
    Recursively loops through all files in the given directory and replaces
    a placeholder string.
    """
    if allowed_extensions is None:
        allowed_extensions = [".txt", ".html", ".css", ".js", ".json", ".txt"]

    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in allowed_extensions):
                file_path = os.path.join(root, file)

                with open(file_path, "r", encoding="utf-8") as file:
                    file_data = file.read()

                file_data = file_data.replace(placeholder, replacement)

                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(file_data)


def copy_directory(directory, path):
    os.makedirs(path, exist_ok=True)
    for item in os.listdir(directory):
        source = os.path.join(directory, item)
        destination = os.path.join(path, item)

        if os.path.isdir(source):
            if os.path.exists(destination):
                shutil.rmtree(destination)
            shutil.copytree(source, destination, symlinks=True)
        else:
            shutil.copy2(source, destination)


async def custom_internal_exception_handler(request: Request, exc: Exception):
    """
    Log a detailed exception for internal server errors before returning.

    Send 503 for errors clients can retry on.
    """
    logger.error("Encountered exception in request:", exc_info=True)

    if is_client_retryable_exception(exc):
        return JSONResponse(
            content={"exception_message": "Service Unavailable"},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    return JSONResponse(
        content={"exception_message": "Internal Server Error"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def nebula_object_not_found_exception_handler(
    request: Request, exc: ObjectNotFoundError
):
    """Return 404 status code on object not found exceptions."""
    return JSONResponse(
        content={"exception_message": str(exc)}, status_code=status.HTTP_404_NOT_FOUND
    )


def create_api_app(
    router_prefix: Optional[str] = "",
    dependencies: Optional[List[Depends]] = None,
    health_check_path: str = "/health",
    version_check_path: str = "/version",
    fast_api_app_kwargs: dict = None,
    router_overrides: Mapping[str, Optional[APIRouter]] = None,
) -> FastAPI:
    """
    Create a FastAPI app that includes the Nebula REST API

    Args:
        router_prefix: a prefix to apply to all included routers
        dependencies: a list of global dependencies to add to each Nebula REST API router
        health_check_path: the health check route path
        fast_api_app_kwargs: kwargs to pass to the FastAPI constructor
        router_overrides: a mapping of route prefixes (i.e. "/admin") to new routers
            allowing the caller to override the default routers. If `None` is provided
            as a value, the default router will be dropped from the application.

    Returns:
        a FastAPI app that serves the Nebula REST API
    """
    fast_api_app_kwargs = fast_api_app_kwargs or {}
    api_app = FastAPI(title=API_TITLE, **fast_api_app_kwargs)
    api_app.add_middleware(GZipMiddleware)

    @api_app.get(health_check_path, tags=["Root"])
    async def health_check():
        return True

    @api_app.get(version_check_path, tags=["Root"])
    async def orion_info():
        return SERVER_API_VERSION

    # always include version checking
    if dependencies is None:
        dependencies = [Depends(enforce_minimum_version)]
    else:
        dependencies.append(Depends(enforce_minimum_version))

    routers = {router.prefix: router for router in API_ROUTERS}

    if router_overrides:
        for prefix, router in router_overrides.items():
            # We may want to allow this behavior in the future to inject new routes, but
            # for now this will be treated an as an exception
            if prefix not in routers:
                raise KeyError(
                    "Router override provided for prefix that does not exist:"
                    f" {prefix!r}"
                )

            # Drop the existing router
            existing_router = routers.pop(prefix)

            # Replace it with a new router if provided
            if router is not None:
                if prefix != router.prefix:
                    # We may want to allow this behavior in the future, but it will
                    # break expectations without additional routing and is banned for
                    # now
                    raise ValueError(
                        f"Router override for {prefix!r} defines a different prefix "
                        f"{router.prefix!r}."
                    )

                existing_paths = method_paths_from_routes(existing_router.routes)
                new_paths = method_paths_from_routes(router.routes)
                if not existing_paths.issubset(new_paths):
                    raise ValueError(
                        f"Router override for {prefix!r} is missing paths defined by "
                        f"the original router: {existing_paths.difference(new_paths)}"
                    )

                routers[prefix] = router

    for router in routers.values():
        api_app.include_router(router, prefix=router_prefix, dependencies=dependencies)

    return api_app


def create_ui_app(ephemeral: bool) -> FastAPI:
    ui_app = FastAPI(title=UI_TITLE)
    base_url = nebula.settings.NEBULA_UI_SERVE_BASE.value()
    stripped_base_url = base_url.rstrip("/")
    static_dir = (
        nebula.settings.NEBULA_UI_STATIC_DIRECTORY.value()
        or nebula.__ui_static_subpath__
    )
    reference_file_name = "UI_SERVE_BASE"

    if os.name == "nt":
        # Windows defaults to text/plain for .js files
        mimetypes.init()
        mimetypes.add_type("application/javascript", ".js")

    @ui_app.get(f"{stripped_base_url}/ui-settings")
    def ui_settings():
        return {
            "api_url": nebula.settings.NEBULA_UI_API_URL.value(),
            "flags": enabled_experiments(),
        }

    def reference_file_matches_base_url():
        reference_file_path = os.path.join(static_dir, reference_file_name)

        if os.path.exists(static_dir):
            try:
                with open(reference_file_path, "r") as f:
                    return f.read() == base_url
            except FileNotFoundError:
                return False
        else:
            return False

    def create_ui_static_subpath():
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)

        copy_directory(nebula.__ui_static_path__, static_dir)
        replace_placeholder_string_in_files(
            static_dir,
            "/NEBULA_UI_SERVE_BASE_REPLACE_PLACEHOLDER",
            stripped_base_url,
        )

        # Create a file to indicate that the static files have been copied
        # This is used to determine if the static files need to be copied again
        # when the server is restarted
        with open(os.path.join(static_dir, reference_file_name), "w") as f:
            f.write(base_url)

    ui_app.add_middleware(GZipMiddleware)

    if (
        os.path.exists(nebula.__ui_static_path__)
        and nebula.settings.NEBULA_UI_ENABLED.value()
        and not ephemeral
    ):
        # If the static files have already been copied, check if the base_url has changed
        # If it has, we delete the subpath directory and copy the files again
        if not reference_file_matches_base_url():
            create_ui_static_subpath()

        ui_app.mount(
            NEBULA_UI_SERVE_BASE.value(),
            SPAStaticFiles(directory=static_dir),
            name="ui_root",
        )

    return ui_app


APP_CACHE: Dict[Tuple[nebula.settings.Settings, bool], FastAPI] = {}


def _memoize_block_auto_registration(fn: Callable[[], Awaitable[None]]):
    """
    Decorator to handle skipping the wrapped function if the block registry has
    not changed since the last invocation
    """
    import toml

    import nebula.plugins
    from nebula.blocks.core import Block
    from nebula.server.models.block_registration import _load_collection_blocks_data
    from nebula.utilities.dispatch import get_registry_for_type

    @wraps(fn)
    async def wrapper(*args, **kwargs):
        if not NEBULA_MEMOIZE_BLOCK_AUTO_REGISTRATION.value():
            await fn(*args, **kwargs)
            return

        # Ensure collections are imported and have the opportunity to register types
        # before loading the registry
        nebula.plugins.load_nebula_collections()

        blocks_registry = get_registry_for_type(Block)
        collection_blocks_data = await _load_collection_blocks_data()
        current_blocks_loading_hash = hash_objects(
            blocks_registry,
            collection_blocks_data,
            NEBULA_API_DATABASE_CONNECTION_URL.value(),
            hash_algo=sha256,
        )

        memo_store_path = NEBULA_MEMO_STORE_PATH.value()
        try:
            if memo_store_path.exists():
                saved_blocks_loading_hash = toml.load(memo_store_path).get(
                    "block_auto_registration"
                )
                if (
                    saved_blocks_loading_hash is not None
                    and current_blocks_loading_hash == saved_blocks_loading_hash
                ):
                    if NEBULA_DEBUG_MODE.value():
                        logger.debug(
                            "Skipping block loading due to matching hash for block "
                            "auto-registration found in memo store."
                        )
                    return
        except Exception as exc:
            logger.warn(
                ""
                f"Unable to read memo_store.toml from {NEBULA_MEMO_STORE_PATH} during "
                f"block auto-registration: {exc!r}.\n"
                "All blocks will be registered."
            )

        await fn(*args, **kwargs)

        if current_blocks_loading_hash is not None:
            try:
                if not memo_store_path.exists():
                    memo_store_path.touch(mode=0o0600)

                memo_store_path.write_text(
                    toml.dumps({"block_auto_registration": current_blocks_loading_hash})
                )
            except Exception as exc:
                logger.warn(
                    "Unable to write to memo_store.toml at"
                    f" {NEBULA_MEMO_STORE_PATH} after block auto-registration:"
                    f" {exc!r}.\n Subsequent server start ups will perform block"
                    " auto-registration, which may result in slower server startup."
                )

    return wrapper


def create_app(
    settings: nebula.settings.Settings = None,
    ephemeral: bool = False,
    ignore_cache: bool = False,
) -> FastAPI:
    """
    Create an FastAPI app that includes the Nebula REST API and UI

    Args:
        settings: The settings to use to create the app. If not set, settings are pulled
            from the context.
        ignore_cache: If set, a new application will be created even if the settings
            match. Otherwise, an application is returned from the cache.
        ephemeral: If set, the application will be treated as ephemeral. The UI
            and services will be disabled.
    """
    settings = settings or nebula.settings.get_current_settings()
    cache_key = (settings.hash_key(), ephemeral)

    if cache_key in APP_CACHE and not ignore_cache:
        return APP_CACHE[cache_key]

    # TODO: Move these startup functions out of this closure into the top-level or
    #       another dedicated location
    async def run_migrations():
        """Ensure the database is created and up to date with the current migrations"""
        if nebula.settings.NEBULA_API_DATABASE_MIGRATE_ON_START:
            from nebula.server.database.dependencies import provide_database_interface

            db = provide_database_interface()
            await db.create_db()

    @_memoize_block_auto_registration
    async def add_block_types():
        """Add all registered blocks to the database"""
        if not nebula.settings.NEBULA_API_BLOCKS_REGISTER_ON_START:
            return

        from nebula.server.database.dependencies import provide_database_interface
        from nebula.server.models.block_registration import run_block_auto_registration

        db = provide_database_interface()
        session = await db.session()

        async with session:
            await run_block_auto_registration(session=session)

    async def start_services():
        """Start additional services when the Nebula REST API starts up."""

        if ephemeral:
            app.state.services = None
            return

        service_instances = []

        if nebula.settings.NEBULA_API_SERVICES_SCHEDULER_ENABLED.value():
            service_instances.append(services.scheduler.Scheduler())
            service_instances.append(services.scheduler.RecentDeploymentsScheduler())

        if nebula.settings.NEBULA_API_SERVICES_LATE_RUNS_ENABLED.value():
            service_instances.append(services.late_runs.MarkLateRuns())

        if nebula.settings.NEBULA_API_SERVICES_PAUSE_EXPIRATIONS_ENABLED.value():
            service_instances.append(services.pause_expirations.FailExpiredPauses())

        if nebula.settings.NEBULA_API_SERVICES_CANCELLATION_CLEANUP_ENABLED.value():
            service_instances.append(
                services.cancellation_cleanup.CancellationCleanup()
            )

        if nebula.settings.NEBULA_SERVER_ANALYTICS_ENABLED.value():
            service_instances.append(services.telemetry.Telemetry())

        if nebula.settings.NEBULA_API_SERVICES_FLOW_RUN_NOTIFICATIONS_ENABLED.value():
            service_instances.append(
                services.flow_run_notifications.FlowRunNotifications()
            )

        if nebula.settings.NEBULA_EXPERIMENTAL_ENABLE_TASK_SCHEDULING.value():
            service_instances.append(services.task_scheduling.TaskSchedulingTimeouts())

        loop = asyncio.get_running_loop()

        app.state.services = {
            service: loop.create_task(service.start()) for service in service_instances
        }

        for service, task in app.state.services.items():
            logger.info(f"{service.name} service scheduled to start in-app")
            task.add_done_callback(partial(on_service_exit, service))

    async def stop_services():
        """Ensure services are stopped before the Nebula REST API shuts down."""
        if hasattr(app.state, "services") and app.state.services:
            await asyncio.gather(*[service.stop() for service in app.state.services])
            try:
                await asyncio.gather(
                    *[task.stop() for task in app.state.services.values()]
                )
            except Exception:
                # `on_service_exit` should handle logging exceptions on exit
                pass

    @asynccontextmanager
    async def lifespan(app):
        try:
            await run_migrations()
            await add_block_types()
            await start_services()
            yield
        finally:
            await stop_services()

    def on_service_exit(service, task):
        """
        Added as a callback for completion of services to log exit
        """
        try:
            # Retrieving the result will raise the exception
            task.result()
        except Exception:
            logger.error(f"{service.name} service failed!", exc_info=True)
        else:
            logger.info(f"{service.name} service stopped!")

    app = FastAPI(
        title=TITLE,
        version=API_VERSION,
        lifespan=lifespan,
    )
    api_app = create_api_app(
        fast_api_app_kwargs={
            "exception_handlers": {
                # NOTE: FastAPI special cases the generic `Exception` handler and
                #       registers it as a separate middleware from the others
                Exception: custom_internal_exception_handler,
                RequestValidationError: validation_exception_handler,
                sa.exc.IntegrityError: integrity_exception_handler,
                ObjectNotFoundError: nebula_object_not_found_exception_handler,
            }
        },
    )
    ui_app = create_ui_app(ephemeral)

    # middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Limit the number of concurrent requests when using a SQLite database to reduce
    # chance of errors where the database cannot be opened due to a high number of
    # concurrent writes
    if (
        get_dialect(nebula.settings.NEBULA_API_DATABASE_CONNECTION_URL.value()).name
        == "sqlite"
    ):
        app.add_middleware(RequestLimitMiddleware, limit=100)

    if nebula.settings.NEBULA_SERVER_CSRF_PROTECTION_ENABLED.value():
        app.add_middleware(api.middleware.CsrfMiddleware)

    api_app.mount(
        "/static",
        StaticFiles(
            directory=os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "static"
            )
        ),
        name="static",
    )
    app.api_app = api_app
    app.mount("/api", app=api_app, name="api")
    app.mount("/", app=ui_app, name="ui")

    def openapi():
        """
        Convenience method for extracting the user facing OpenAPI schema from the API app.

        This method is attached to the global public app for easy access.
        """
        partial_schema = get_openapi(
            title=API_TITLE,
            version=API_VERSION,
            routes=api_app.routes,
        )
        new_schema = partial_schema.copy()
        new_schema["paths"] = {}
        for path, value in partial_schema["paths"].items():
            new_schema["paths"][f"/api{path}"] = value

        new_schema["info"]["x-logo"] = {"url": "static/nebula-logo-mark-gradient.png"}
        return new_schema

    app.openapi = openapi

    APP_CACHE[cache_key] = app
    return app
