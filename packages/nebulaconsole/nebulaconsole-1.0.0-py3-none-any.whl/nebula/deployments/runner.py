"""
Objects for creating and configuring deployments for flows using `serve` functionality.

Example:
    ```python
    import time
    from nebula import flow, serve


    @flow
    def slow_flow(sleep: int = 60):
        "Sleepy flow - sleeps the provided amount of time (in seconds)."
        time.sleep(sleep)


    @flow
    def fast_flow():
        "Fastest flow this side of the Mississippi."
        return


    if __name__ == "__main__":
        # to_deployment creates RunnerDeployment instances
        slow_deploy = slow_flow.to_deployment(name="sleeper", interval=45)
        fast_deploy = fast_flow.to_deployment(name="fast")

        serve(slow_deploy, fast_deploy)
    ```

"""

import enum
import importlib
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Union
from uuid import UUID

import pendulum
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, track
from rich.table import Table

from nebula._internal.concurrency.api import create_call, from_async
from nebula._internal.pydantic import HAS_PYDANTIC_V2
from nebula.runner.storage import RunnerStorage
from nebula.settings import (
    NEBULA_DEFAULT_DOCKER_BUILD_NAMESPACE,
    NEBULA_DEFAULT_WORK_POOL_NAME,
    NEBULA_UI_URL,
)
from nebula.utilities.collections import get_from_dict, isiterable

if HAS_PYDANTIC_V2:
    from pydantic.v1 import BaseModel, Field, PrivateAttr, root_validator, validator
else:
    from pydantic import BaseModel, Field, PrivateAttr, root_validator, validator

from nebula.client.orchestration import ServerType, get_client
from nebula.client.schemas.objects import MinimalDeploymentSchedule
from nebula.client.schemas.schedules import (
    SCHEDULE_TYPES,
    construct_schedule,
)
from nebula.deployments.schedules import (
    FlexibleScheduleList,
    create_minimal_deployment_schedule,
    normalize_to_minimal_deployment_schedules,
)
from nebula.events.schemas import DeploymentTrigger
from nebula.exceptions import (
    ObjectNotFound,
    NebulaHTTPStatusError,
)
from nebula.utilities.asyncutils import sync_compatible
from nebula.utilities.callables import ParameterSchema, parameter_schema
from nebula.utilities.dockerutils import (
    PushError,
    build_image,
    docker_client,
    generate_default_dockerfile,
    parse_image_tag,
    split_repository_path,
)
from nebula.utilities.slugify import slugify

if TYPE_CHECKING:
    from nebula.flows import Flow

__all__ = ["RunnerDeployment"]


class DeploymentApplyError(RuntimeError):
    """
    Raised when an error occurs while applying a deployment.
    """


class EntrypointType(enum.Enum):
    """
    Enum representing a entrypoint type.

    File path entrypoints are in the format: `path/to/file.py:function_name`.
    Module path entrypoints are in the format: `path.to.module.function_name`.
    """

    FILE_PATH = "file_path"
    MODULE_PATH = "module_path"


class RunnerDeployment(BaseModel):
    """
    A Nebula RunnerDeployment definition, used for specifying and building deployments.

    Attributes:
        name: A name for the deployment (required).
        version: An optional version for the deployment; defaults to the flow's version
        description: An optional description of the deployment; defaults to the flow's
            description
        tags: An optional list of tags to associate with this deployment; note that tags
            are used only for organizational purposes. For delegating work to agents,
            see `work_queue_name`.
        schedule: A schedule to run this deployment on, once registered
        is_schedule_active: Whether or not the schedule is active
        parameters: A dictionary of parameter values to pass to runs created from this
            deployment
        path: The path to the working directory for the workflow, relative to remote
            storage or, if stored on a local filesystem, an absolute path
        entrypoint: The path to the entrypoint for the workflow, always relative to the
            `path`
        parameter_openapi_schema: The parameter schema of the flow, including defaults.
        enforce_parameter_schema: Whether or not the Nebula API should enforce the
            parameter schema for this deployment.
        work_pool_name: The name of the work pool to use for this deployment.
        work_queue_name: The name of the work queue to use for this deployment's scheduled runs.
            If not provided the default work queue for the work pool will be used.
        job_variables: Settings used to override the values specified default base job template
            of the chosen work pool. Refer to the base job template of the chosen work pool for
            available settings.
    """

    class Config:
        arbitrary_types_allowed = True

    name: str = Field(..., description="The name of the deployment.")
    flow_name: Optional[str] = Field(
        None, description="The name of the underlying flow; typically inferred."
    )
    description: Optional[str] = Field(
        default=None, description="An optional description of the deployment."
    )
    version: Optional[str] = Field(
        default=None, description="An optional version for the deployment."
    )
    tags: List[str] = Field(
        default_factory=list,
        description="One of more tags to apply to this deployment.",
    )
    schedules: Optional[List[MinimalDeploymentSchedule]] = Field(
        default=None,
        description="The schedules that should cause this deployment to run.",
    )
    schedule: Optional[SCHEDULE_TYPES] = None
    paused: Optional[bool] = Field(
        default=None, description="Whether or not the deployment is paused."
    )
    is_schedule_active: Optional[bool] = Field(
        default=None, description="DEPRECATED: Whether or not the schedule is active."
    )
    parameters: Dict[str, Any] = Field(default_factory=dict)
    entrypoint: Optional[str] = Field(
        default=None,
        description=(
            "The path to the entrypoint for the workflow, relative to the `path`."
        ),
    )
    triggers: List[DeploymentTrigger] = Field(
        default_factory=list,
        description="The triggers that should cause this deployment to run.",
    )
    enforce_parameter_schema: bool = Field(
        default=False,
        description=(
            "Whether or not the Nebula API should enforce the parameter schema for"
            " this deployment."
        ),
    )
    storage: Optional[RunnerStorage] = Field(
        default=None,
        description=(
            "The storage object used to retrieve flow code for this deployment."
        ),
    )
    work_pool_name: Optional[str] = Field(
        default=None,
        description=(
            "The name of the work pool to use for this deployment. Only used when"
            " the deployment is registered with a built runner."
        ),
    )
    work_queue_name: Optional[str] = Field(
        default=None,
        description=(
            "The name of the work queue to use for this deployment. Only used when"
            " the deployment is registered with a built runner."
        ),
    )
    job_variables: Dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Job variables used to override the default values of a work pool"
            " base job template. Only used when the deployment is registered with"
            " a built runner."
        ),
    )
    _entrypoint_type: EntrypointType = PrivateAttr(
        default=EntrypointType.FILE_PATH,
    )
    _path: Optional[str] = PrivateAttr(
        default=None,
    )
    _parameter_openapi_schema: ParameterSchema = PrivateAttr(
        default_factory=ParameterSchema,
    )

    @property
    def entrypoint_type(self) -> EntrypointType:
        return self._entrypoint_type

    @validator("triggers", allow_reuse=True)
    def validate_automation_names(cls, field_value, values, field, config):
        """Ensure that each trigger has a name for its automation if none is provided."""
        for i, trigger in enumerate(field_value, start=1):
            if trigger.name is None:
                trigger.name = f"{values['name']}__automation_{i}"

        return field_value

    @root_validator(pre=True)
    def reconcile_paused(cls, values):
        paused = values.get("paused")
        is_schedule_active = values.get("is_schedule_active")

        if paused is not None:
            values["paused"] = paused
            values["is_schedule_active"] = not paused
        elif is_schedule_active is not None:
            values["paused"] = not is_schedule_active
            values["is_schedule_active"] = is_schedule_active
        else:
            values["paused"] = False
            values["is_schedule_active"] = True

        return values

    @root_validator(pre=True)
    def reconcile_schedules(cls, values):
        schedule = values.get("schedule")
        schedules = values.get("schedules")

        if schedules is None and schedule is not None:
            values["schedules"] = [create_minimal_deployment_schedule(schedule)]
        elif schedules is not None and len(schedules) > 0:
            values["schedules"] = normalize_to_minimal_deployment_schedules(schedules)

        return values

    @sync_compatible
    async def apply(
        self, work_pool_name: Optional[str] = None, image: Optional[str] = None
    ) -> UUID:
        """
        Registers this deployment with the API and returns the deployment's ID.

        Args:
            work_pool_name: The name of the work pool to use for this
                deployment.
            image: The registry, name, and tag of the Docker image to
                use for this deployment. Only used when the deployment is
                deployed to a work pool.

        Returns:
            The ID of the created deployment.
        """

        work_pool_name = work_pool_name or self.work_pool_name

        if image and not work_pool_name:
            raise ValueError(
                "An image can only be provided when registering a deployment with a"
                " work pool."
            )

        if self.work_queue_name and not work_pool_name:
            raise ValueError(
                "A work queue can only be provided when registering a deployment with"
                " a work pool."
            )

        if self.job_variables and not work_pool_name:
            raise ValueError(
                "Job variables can only be provided when registering a deployment"
                " with a work pool."
            )

        async with get_client() as client:
            flow_id = await client.create_flow_from_name(self.flow_name)

            create_payload = dict(
                flow_id=flow_id,
                name=self.name,
                work_queue_name=self.work_queue_name,
                work_pool_name=work_pool_name,
                version=self.version,
                paused=self.paused,
                schedules=self.schedules,
                parameters=self.parameters,
                description=self.description,
                tags=self.tags,
                path=self._path,
                entrypoint=self.entrypoint,
                storage_document_id=None,
                infrastructure_document_id=None,
                parameter_openapi_schema=self._parameter_openapi_schema.dict(),
                enforce_parameter_schema=self.enforce_parameter_schema,
            )

            if work_pool_name:
                create_payload["infra_overrides"] = self.job_variables
                if image:
                    create_payload["infra_overrides"]["image"] = image
                create_payload["path"] = None if self.storage else self._path
                create_payload["pull_steps"] = (
                    [self.storage.to_pull_step()] if self.storage else []
                )

            try:
                deployment_id = await client.create_deployment(**create_payload)
            except Exception as exc:
                if isinstance(exc, NebulaHTTPStatusError):
                    detail = exc.response.json().get("detail")
                    if detail:
                        raise DeploymentApplyError(detail) from exc
                raise DeploymentApplyError(
                    f"Error while applying deployment: {str(exc)}"
                ) from exc

            if client.server_type == ServerType.CLOUD:
                # The triggers defined in the deployment spec are, essentially,
                # anonymous and attempting truly sync them with cloud is not
                # feasible. Instead, we remove all automations that are owned
                # by the deployment, meaning that they were created via this
                # mechanism below, and then recreate them.
                await client.delete_resource_owned_automations(
                    f"nebula.deployment.{deployment_id}"
                )
                for trigger in self.triggers:
                    trigger.set_deployment_id(deployment_id)
                    await client.create_automation(trigger.as_automation())

            return deployment_id

    @staticmethod
    def _construct_deployment_schedules(
        interval: Optional[
            Union[Iterable[Union[int, float, timedelta]], int, float, timedelta]
        ] = None,
        anchor_date: Optional[Union[datetime, str]] = None,
        cron: Optional[Union[Iterable[str], str]] = None,
        rrule: Optional[Union[Iterable[str], str]] = None,
        timezone: Optional[str] = None,
        schedule: Optional[SCHEDULE_TYPES] = None,
        schedules: Optional[FlexibleScheduleList] = None,
    ) -> Union[List[MinimalDeploymentSchedule], FlexibleScheduleList]:
        """
        Construct a schedule or schedules from the provided arguments.

        This method serves as a unified interface for creating deployment
        schedules. If `schedules` is provided, it is directly returned. If
        `schedule` is provided, it is encapsulated in a list and returned. If
        `interval`, `cron`, or `rrule` are provided, they are used to construct
        schedule objects.

        Args:
            interval: An interval on which to schedule runs, either as a single
              value or as a list of values. Accepts numbers (interpreted as
              seconds) or `timedelta` objects. Each value defines a separate
              scheduling interval.
            anchor_date: The anchor date from which interval schedules should
              start. This applies to all intervals if a list is provided.
            cron: A cron expression or a list of cron expressions defining cron
              schedules. Each expression defines a separate cron schedule.
            rrule: An rrule string or a list of rrule strings for scheduling.
              Each string defines a separate recurrence rule.
            timezone: The timezone to apply to the cron or rrule schedules.
              This is a single value applied uniformly to all schedules.
            schedule: A singular schedule object, used for advanced scheduling
              options like specifying a timezone. This is returned as a list
              containing this single schedule.
            schedules: A pre-defined list of schedule objects. If provided,
              this list is returned as-is, bypassing other schedule construction
              logic.
        """

        num_schedules = sum(
            1
            for entry in (interval, cron, rrule, schedule, schedules)
            if entry is not None
        )
        if num_schedules > 1:
            raise ValueError(
                "Only one of interval, cron, rrule, schedule, or schedules can be provided."
            )
        elif num_schedules == 0:
            return []

        if schedules is not None:
            return schedules
        elif interval or cron or rrule:
            # `interval`, `cron`, and `rrule` can be lists of values. This
            # block figures out which one is not None and uses that to
            # construct the list of schedules via `construct_schedule`.
            parameters = [("interval", interval), ("cron", cron), ("rrule", rrule)]
            schedule_type, value = [
                param for param in parameters if param[1] is not None
            ][0]

            if not isiterable(value):
                value = [value]

            return [
                create_minimal_deployment_schedule(
                    construct_schedule(
                        **{
                            schedule_type: v,
                            "timezone": timezone,
                            "anchor_date": anchor_date,
                        }
                    )
                )
                for v in value
            ]
        else:
            return [create_minimal_deployment_schedule(schedule)]

    def _set_defaults_from_flow(self, flow: "Flow"):
        self._parameter_openapi_schema = parameter_schema(flow)

        if not self.version:
            self.version = flow.version
        if not self.description:
            self.description = flow.description

    @classmethod
    def from_flow(
        cls,
        flow: "Flow",
        name: str,
        interval: Optional[
            Union[Iterable[Union[int, float, timedelta]], int, float, timedelta]
        ] = None,
        cron: Optional[Union[Iterable[str], str]] = None,
        rrule: Optional[Union[Iterable[str], str]] = None,
        paused: Optional[bool] = None,
        schedules: Optional[FlexibleScheduleList] = None,
        schedule: Optional[SCHEDULE_TYPES] = None,
        is_schedule_active: Optional[bool] = None,
        parameters: Optional[dict] = None,
        triggers: Optional[List[DeploymentTrigger]] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        version: Optional[str] = None,
        enforce_parameter_schema: bool = False,
        work_pool_name: Optional[str] = None,
        work_queue_name: Optional[str] = None,
        job_variables: Optional[Dict[str, Any]] = None,
        entrypoint_type: EntrypointType = EntrypointType.FILE_PATH,
    ) -> "RunnerDeployment":
        """
        Configure a deployment for a given flow.

        Args:
            flow: A flow function to deploy
            name: A name for the deployment
            interval: An interval on which to execute the current flow. Accepts either a number
                or a timedelta object. If a number is given, it will be interpreted as seconds.
            cron: A cron schedule of when to execute runs of this flow.
            rrule: An rrule schedule of when to execute runs of this flow.
            paused: Whether or not to set this deployment as paused.
            schedules: A list of schedule objects defining when to execute runs of this deployment.
                Used to define multiple schedules or additional scheduling options like `timezone`.
            schedule: A schedule object of when to execute runs of this flow. Used for
                advanced scheduling options like timezone.
            is_schedule_active: Whether or not to set the schedule for this deployment as active. If
                not provided when creating a deployment, the schedule will be set as active. If not
                provided when updating a deployment, the schedule's activation will not be changed.
            triggers: A list of triggers that should kick of a run of this flow.
            parameters: A dictionary of default parameter values to pass to runs of this flow.
            description: A description for the created deployment. Defaults to the flow's
                description if not provided.
            tags: A list of tags to associate with the created deployment for organizational
                purposes.
            version: A version for the created deployment. Defaults to the flow's version.
            enforce_parameter_schema: Whether or not the Nebula API should enforce the
                parameter schema for this deployment.
            work_pool_name: The name of the work pool to use for this deployment.
            work_queue_name: The name of the work queue to use for this deployment's scheduled runs.
                If not provided the default work queue for the work pool will be used.
            job_variables: Settings used to override the values specified default base job template
                of the chosen work pool. Refer to the base job template of the chosen work pool for
                available settings.
        """
        constructed_schedules = cls._construct_deployment_schedules(
            interval=interval,
            cron=cron,
            rrule=rrule,
            schedule=schedule,
            schedules=schedules,
        )

        job_variables = job_variables or {}

        deployment = cls(
            name=Path(name).stem,
            flow_name=flow.name,
            schedule=schedule,
            schedules=constructed_schedules,
            is_schedule_active=is_schedule_active,
            paused=paused,
            tags=tags or [],
            triggers=triggers or [],
            parameters=parameters or {},
            description=description,
            version=version,
            enforce_parameter_schema=enforce_parameter_schema,
            work_pool_name=work_pool_name,
            work_queue_name=work_queue_name,
            job_variables=job_variables,
        )

        if not deployment.entrypoint:
            no_file_location_error = (
                "Flows defined interactively cannot be deployed. Check out the"
                " quickstart guide for help getting started:"
                " https://docs.nebula.io/latest/getting-started/quickstart"
            )
            ## first see if an entrypoint can be determined
            flow_file = getattr(flow, "__globals__", {}).get("__file__")
            mod_name = getattr(flow, "__module__", None)
            if entrypoint_type == EntrypointType.MODULE_PATH:
                if mod_name:
                    deployment.entrypoint = f"{mod_name}.{flow.__name__}"
                else:
                    raise ValueError(
                        "Unable to determine module path for provided flow."
                    )
            else:
                if not flow_file:
                    if not mod_name:
                        raise ValueError(no_file_location_error)
                    try:
                        module = importlib.import_module(mod_name)
                        flow_file = getattr(module, "__file__", None)
                    except ModuleNotFoundError as exc:
                        if "__nebula_loader__" in str(exc):
                            raise ValueError(
                                "Cannot create a RunnerDeployment from a flow that has been"
                                " loaded from an entrypoint. To deploy a flow via"
                                " entrypoint, use RunnerDeployment.from_entrypoint instead."
                            )
                        raise ValueError(no_file_location_error)
                    if not flow_file:
                        raise ValueError(no_file_location_error)

                # set entrypoint
                entry_path = (
                    Path(flow_file).absolute().relative_to(Path.cwd().absolute())
                )
                deployment.entrypoint = f"{entry_path}:{flow.fn.__name__}"

        if entrypoint_type == EntrypointType.FILE_PATH and not deployment._path:
            deployment._path = "."

        deployment._entrypoint_type = entrypoint_type

        cls._set_defaults_from_flow(deployment, flow)

        return deployment

    @classmethod
    def from_entrypoint(
        cls,
        entrypoint: str,
        name: str,
        interval: Optional[
            Union[Iterable[Union[int, float, timedelta]], int, float, timedelta]
        ] = None,
        cron: Optional[Union[Iterable[str], str]] = None,
        rrule: Optional[Union[Iterable[str], str]] = None,
        paused: Optional[bool] = None,
        schedules: Optional[FlexibleScheduleList] = None,
        schedule: Optional[SCHEDULE_TYPES] = None,
        is_schedule_active: Optional[bool] = None,
        parameters: Optional[dict] = None,
        triggers: Optional[List[DeploymentTrigger]] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        version: Optional[str] = None,
        enforce_parameter_schema: bool = False,
        work_pool_name: Optional[str] = None,
        work_queue_name: Optional[str] = None,
        job_variables: Optional[Dict[str, Any]] = None,
    ) -> "RunnerDeployment":
        """
        Configure a deployment for a given flow located at a given entrypoint.

        Args:
            entrypoint:  The path to a file containing a flow and the name of the flow function in
                the format `./path/to/file.py:flow_func_name`.
            name: A name for the deployment
            interval: An interval on which to execute the current flow. Accepts either a number
                or a timedelta object. If a number is given, it will be interpreted as seconds.
            cron: A cron schedule of when to execute runs of this flow.
            rrule: An rrule schedule of when to execute runs of this flow.
            paused: Whether or not to set this deployment as paused.
            schedules: A list of schedule objects defining when to execute runs of this deployment.
                Used to define multiple schedules or additional scheduling options like `timezone`.
            schedule: A schedule object of when to execute runs of this flow. Used for
                advanced scheduling options like timezone.
            is_schedule_active: Whether or not to set the schedule for this deployment as active. If
                not provided when creating a deployment, the schedule will be set as active. If not
                provided when updating a deployment, the schedule's activation will not be changed.
            triggers: A list of triggers that should kick of a run of this flow.
            parameters: A dictionary of default parameter values to pass to runs of this flow.
            description: A description for the created deployment. Defaults to the flow's
                description if not provided.
            tags: A list of tags to associate with the created deployment for organizational
                purposes.
            version: A version for the created deployment. Defaults to the flow's version.
            enforce_parameter_schema: Whether or not the Nebula API should enforce the
                parameter schema for this deployment.
            work_pool_name: The name of the work pool to use for this deployment.
            work_queue_name: The name of the work queue to use for this deployment's scheduled runs.
                If not provided the default work queue for the work pool will be used.
            job_variables: Settings used to override the values specified default base job template
                of the chosen work pool. Refer to the base job template of the chosen work pool for
                available settings.
        """
        from nebula.flows import load_flow_from_entrypoint

        job_variables = job_variables or {}
        flow = load_flow_from_entrypoint(entrypoint)

        constructed_schedules = cls._construct_deployment_schedules(
            interval=interval,
            cron=cron,
            rrule=rrule,
            schedule=schedule,
            schedules=schedules,
        )

        deployment = cls(
            name=Path(name).stem,
            flow_name=flow.name,
            schedule=schedule,
            schedules=constructed_schedules,
            paused=paused,
            is_schedule_active=is_schedule_active,
            tags=tags or [],
            triggers=triggers or [],
            parameters=parameters or {},
            description=description,
            version=version,
            entrypoint=entrypoint,
            enforce_parameter_schema=enforce_parameter_schema,
            work_pool_name=work_pool_name,
            work_queue_name=work_queue_name,
            job_variables=job_variables,
        )
        deployment._path = str(Path.cwd())

        cls._set_defaults_from_flow(deployment, flow)

        return deployment

    @classmethod
    @sync_compatible
    async def from_storage(
        cls,
        storage: RunnerStorage,
        entrypoint: str,
        name: str,
        interval: Optional[
            Union[Iterable[Union[int, float, timedelta]], int, float, timedelta]
        ] = None,
        cron: Optional[Union[Iterable[str], str]] = None,
        rrule: Optional[Union[Iterable[str], str]] = None,
        paused: Optional[bool] = None,
        schedules: Optional[FlexibleScheduleList] = None,
        schedule: Optional[SCHEDULE_TYPES] = None,
        is_schedule_active: Optional[bool] = None,
        parameters: Optional[dict] = None,
        triggers: Optional[List[DeploymentTrigger]] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        version: Optional[str] = None,
        enforce_parameter_schema: bool = False,
        work_pool_name: Optional[str] = None,
        work_queue_name: Optional[str] = None,
        job_variables: Optional[Dict[str, Any]] = None,
    ):
        """
        Create a RunnerDeployment from a flow located at a given entrypoint and stored in a
        local storage location.

        Args:
            entrypoint:  The path to a file containing a flow and the name of the flow function in
                the format `./path/to/file.py:flow_func_name`.
            name: A name for the deployment
            storage: A storage object to use for retrieving flow code. If not provided, a
                URL must be provided.
            interval: An interval on which to execute the current flow. Accepts either a number
                or a timedelta object. If a number is given, it will be interpreted as seconds.
            cron: A cron schedule of when to execute runs of this flow.
            rrule: An rrule schedule of when to execute runs of this flow.
            schedule: A schedule object of when to execute runs of this flow. Used for
                advanced scheduling options like timezone.
            is_schedule_active: Whether or not to set the schedule for this deployment as active. If
                not provided when creating a deployment, the schedule will be set as active. If not
                provided when updating a deployment, the schedule's activation will not be changed.
            triggers: A list of triggers that should kick of a run of this flow.
            parameters: A dictionary of default parameter values to pass to runs of this flow.
            description: A description for the created deployment. Defaults to the flow's
                description if not provided.
            tags: A list of tags to associate with the created deployment for organizational
                purposes.
            version: A version for the created deployment. Defaults to the flow's version.
            enforce_parameter_schema: Whether or not the Nebula API should enforce the
                parameter schema for this deployment.
            work_pool_name: The name of the work pool to use for this deployment.
            work_queue_name: The name of the work queue to use for this deployment's scheduled runs.
                If not provided the default work queue for the work pool will be used.
            job_variables: Settings used to override the values specified default base job template
                of the chosen work pool. Refer to the base job template of the chosen work pool for
                available settings.
        """
        from nebula.flows import load_flow_from_entrypoint

        constructed_schedules = cls._construct_deployment_schedules(
            interval=interval,
            cron=cron,
            rrule=rrule,
            schedule=schedule,
            schedules=schedules,
        )

        job_variables = job_variables or {}

        with tempfile.TemporaryDirectory() as tmpdir:
            storage.set_base_path(Path(tmpdir))
            await storage.pull_code()

            full_entrypoint = str(storage.destination / entrypoint)
            flow = await from_async.wait_for_call_in_new_thread(
                create_call(load_flow_from_entrypoint, full_entrypoint)
            )

        deployment = cls(
            name=Path(name).stem,
            flow_name=flow.name,
            schedule=schedule,
            schedules=constructed_schedules,
            paused=paused,
            is_schedule_active=is_schedule_active,
            tags=tags or [],
            triggers=triggers or [],
            parameters=parameters or {},
            description=description,
            version=version,
            entrypoint=entrypoint,
            enforce_parameter_schema=enforce_parameter_schema,
            storage=storage,
            work_pool_name=work_pool_name,
            work_queue_name=work_queue_name,
            job_variables=job_variables,
        )
        deployment._path = str(storage.destination).replace(
            tmpdir, "$STORAGE_BASE_PATH"
        )

        cls._set_defaults_from_flow(deployment, flow)

        return deployment


class DeploymentImage:
    """
    Configuration used to build and push a Docker image for a deployment.

    Attributes:
        name: The name of the Docker image to build, including the registry and
            repository.
        tag: The tag to apply to the built image.
        dockerfile: The path to the Dockerfile to use for building the image. If
            not provided, a default Dockerfile will be generated.
        **build_kwargs: Additional keyword arguments to pass to the Docker build request.
            See the [`docker-py` documentation](https://docker-py.readthedocs.io/en/stable/images.html#docker.models.images.ImageCollection.build)
            for more information.

    """

    def __init__(self, name, tag=None, dockerfile="auto", **build_kwargs):
        image_name, image_tag = parse_image_tag(name)
        if tag and image_tag:
            raise ValueError(
                f"Only one tag can be provided - both {image_tag!r} and {tag!r} were"
                " provided as tags."
            )
        namespace, repository = split_repository_path(image_name)
        # if the provided image name does not include a namespace (registry URL or user/org name),
        # use the default namespace
        if not namespace:
            namespace = NEBULA_DEFAULT_DOCKER_BUILD_NAMESPACE.value()
        # join the namespace and repository to create the full image name
        # ignore namespace if it is None
        self.name = "/".join(filter(None, [namespace, repository]))
        self.tag = tag or image_tag or slugify(pendulum.now("utc").isoformat())
        self.dockerfile = dockerfile
        self.build_kwargs = build_kwargs

    @property
    def reference(self):
        return f"{self.name}:{self.tag}"

    def build(self):
        full_image_name = self.reference
        build_kwargs = self.build_kwargs.copy()
        build_kwargs["context"] = Path.cwd()
        build_kwargs["tag"] = full_image_name
        build_kwargs["pull"] = build_kwargs.get("pull", True)

        if self.dockerfile == "auto":
            with generate_default_dockerfile():
                build_image(**build_kwargs)
        else:
            build_kwargs["dockerfile"] = self.dockerfile
            build_image(**build_kwargs)

    def push(self):
        with docker_client() as client:
            events = client.api.push(
                repository=self.name, tag=self.tag, stream=True, decode=True
            )
            for event in events:
                if "error" in event:
                    raise PushError(event["error"])


@sync_compatible
async def deploy(
    *deployments: RunnerDeployment,
    work_pool_name: Optional[str] = None,
    image: Optional[Union[str, DeploymentImage]] = None,
    build: bool = True,
    push: bool = True,
    print_next_steps_message: bool = True,
    ignore_warnings: bool = False,
) -> List[UUID]:
    """
    Deploy the provided list of deployments to dynamic infrastructure via a
    work pool.

    By default, calling this function will build a Docker image for the deployments, push it to a
    registry, and create each deployment via the Nebula API that will run the corresponding
    flow on the given schedule.

    If you want to use an existing image, you can pass `build=False` to skip building and pushing
    an image.

    Args:
        *deployments: A list of deployments to deploy.
        work_pool_name: The name of the work pool to use for these deployments. Defaults to
            the value of `NEBULA_DEFAULT_WORK_POOL_NAME`.
        image: The name of the Docker image to build, including the registry and
            repository. Pass a DeploymentImage instance to customize the Dockerfile used
            and build arguments.
        build: Whether or not to build a new image for the flow. If False, the provided
            image will be used as-is and pulled at runtime.
        push: Whether or not to skip pushing the built image to a registry.
        print_next_steps_message: Whether or not to print a message with next steps
            after deploying the deployments.

    Returns:
        A list of deployment IDs for the created/updated deployments.

    Examples:
        Deploy a group of flows to a work pool:

        ```python
        from nebula import deploy, flow

        @flow(log_prints=True)
        def local_flow():
            print("I'm a locally defined flow!")

        if __name__ == "__main__":
            deploy(
                local_flow.to_deployment(name="example-deploy-local-flow"),
                flow.from_source(
                    source="https://github.com/org/repo.git",
                    entrypoint="flows.py:my_flow",
                ).to_deployment(
                    name="example-deploy-remote-flow",
                ),
                work_pool_name="my-work-pool",
                image="my-registry/my-image:dev",
            )
        ```
    """
    work_pool_name = work_pool_name or NEBULA_DEFAULT_WORK_POOL_NAME.value()

    if not image and not all(
        d.storage or d.entrypoint_type == EntrypointType.MODULE_PATH
        for d in deployments
    ):
        raise ValueError(
            "Either an image or remote storage location must be provided when deploying"
            " a deployment."
        )

    if not work_pool_name:
        raise ValueError(
            "A work pool name must be provided when deploying a deployment. Either"
            " provide a work pool name when calling `deploy` or set"
            " `NEBULA_DEFAULT_WORK_POOL_NAME` in your profile."
        )

    if image and isinstance(image, str):
        image_name, image_tag = parse_image_tag(image)
        image = DeploymentImage(name=image_name, tag=image_tag)

    try:
        async with get_client() as client:
            work_pool = await client.read_work_pool(work_pool_name)
    except ObjectNotFound as exc:
        raise ValueError(
            f"Could not find work pool {work_pool_name!r}. Please create it before"
            " deploying this flow."
        ) from exc

    is_docker_based_work_pool = get_from_dict(
        work_pool.base_job_template, "variables.properties.image", False
    )
    is_block_based_work_pool = get_from_dict(
        work_pool.base_job_template, "variables.properties.block", False
    )
    # carve out an exception for block based work pools that only have a block in their base job template
    console = Console()
    if not is_docker_based_work_pool and not is_block_based_work_pool:
        if image:
            raise ValueError(
                f"Work pool {work_pool_name!r} does not support custom Docker images."
                " Please use a work pool with an `image` variable in its base job template"
                " or specify a remote storage location for the flow with `.from_source`."
                " If you are attempting to deploy a flow to a local process work pool,"
                " consider using `flow.serve` instead. See the documentation for more"
                " information: https://docs.nebula.io/latest/concepts/flows/#serving-a-flow"
            )
        elif work_pool.type == "process" and not ignore_warnings:
            console.print(
                "Looks like you're deploying to a process work pool. If you're creating a"
                " deployment for local development, calling `.serve` on your flow is a great"
                " way to get started. See the documentation for more information:"
                " https://docs.nebula.io/latest/concepts/flows/#serving-a-flow. "
                " Set `ignore_warnings=True` to suppress this message.",
                style="yellow",
            )

    is_managed_pool = work_pool.is_managed_pool
    if is_managed_pool:
        build = False
        push = False

    if image and build:
        with Progress(
            SpinnerColumn(),
            TextColumn(f"Building image {image.reference}..."),
            transient=True,
            console=console,
        ) as progress:
            docker_build_task = progress.add_task("docker_build", total=1)
            image.build()

            progress.update(docker_build_task, completed=1)
            console.print(
                f"Successfully built image {image.reference!r}", style="green"
            )

    if image and build and push:
        with Progress(
            SpinnerColumn(),
            TextColumn("Pushing image..."),
            transient=True,
            console=console,
        ) as progress:
            docker_push_task = progress.add_task("docker_push", total=1)

            image.push()

            progress.update(docker_push_task, completed=1)

        console.print(f"Successfully pushed image {image.reference!r}", style="green")

    deployment_exceptions = []
    deployment_ids = []
    image_ref = image.reference if image else None
    for deployment in track(
        deployments,
        description="Creating/updating deployments...",
        console=console,
        transient=True,
    ):
        try:
            deployment_ids.append(
                await deployment.apply(image=image_ref, work_pool_name=work_pool_name)
            )
        except Exception as exc:
            if len(deployments) == 1:
                raise
            deployment_exceptions.append({"deployment": deployment, "exc": exc})

    if deployment_exceptions:
        console.print(
            "Encountered errors while creating/updating deployments:\n",
            style="orange_red1",
        )
    else:
        console.print("Successfully created/updated all deployments!\n", style="green")

    complete_failure = len(deployment_exceptions) == len(deployments)

    table = Table(
        title="Deployments",
        show_lines=True,
    )

    table.add_column(header="Name", style="blue", no_wrap=True)
    table.add_column(header="Status", style="blue", no_wrap=True)
    table.add_column(header="Details", style="blue")

    for deployment in deployments:
        errored_deployment = next(
            (d for d in deployment_exceptions if d["deployment"] == deployment),
            None,
        )
        if errored_deployment:
            table.add_row(
                f"{deployment.flow_name}/{deployment.name}",
                "failed",
                str(errored_deployment["exc"]),
                style="red",
            )
        else:
            table.add_row(f"{deployment.flow_name}/{deployment.name}", "applied")
    console.print(table)

    if print_next_steps_message and not complete_failure:
        if not work_pool.is_push_pool and not work_pool.is_managed_pool:
            console.print(
                "\nTo execute flow runs from these deployments, start a worker in a"
                " separate terminal that pulls work from the"
                f" {work_pool_name!r} work pool:"
            )
            console.print(
                f"\n\t$ nebula worker start --pool {work_pool_name!r}",
                style="blue",
            )
        console.print(
            "\nTo trigger any of these deployments, use the"
            " following command:\n[blue]\n\t$ nebula deployment run"
            " [DEPLOYMENT_NAME]\n[/]"
        )

        if NEBULA_UI_URL:
            console.print(
                "\nYou can also trigger your deployments via the Nebula UI:"
                f" [blue]{NEBULA_UI_URL.value()}/deployments[/]\n"
            )

    return deployment_ids
