from typing import TYPE_CHECKING, Any, Optional, Set
from uuid import UUID

import orjson
import pydantic

from nebula._internal.pydantic import HAS_PYDANTIC_V2
from nebula.client.utilities import inject_client
from nebula.context import FlowRunContext
from nebula.exceptions import NebulaHTTPStatusError
from nebula.utilities.asyncutils import sync_compatible

if TYPE_CHECKING:
    from nebula.client.orchestration import NebulaClient


if HAS_PYDANTIC_V2:
    from nebula._internal.pydantic.v2_schema import is_v2_model


def ensure_flow_run_id(flow_run_id: Optional[UUID] = None) -> UUID:
    if flow_run_id:
        return flow_run_id

    context = FlowRunContext.get()
    if context is None or context.flow_run is None:
        raise RuntimeError("Must either provide a flow run ID or be within a flow run.")

    return context.flow_run.id


@sync_compatible
async def create_flow_run_input_from_model(
    key: str,
    model_instance: pydantic.BaseModel,
    flow_run_id: Optional[UUID] = None,
    sender: Optional[str] = None,
):
    if sender is None:
        context = FlowRunContext.get()
        if context is not None and context.flow_run is not None:
            sender = f"nebula.flow-run.{context.flow_run.id}"

    if HAS_PYDANTIC_V2 and is_v2_model(model_instance):
        json_safe = orjson.loads(model_instance.model_dump_json())
    else:
        json_safe = orjson.loads(model_instance.json())

    await create_flow_run_input(
        key=key, value=json_safe, flow_run_id=flow_run_id, sender=sender
    )


@sync_compatible
@inject_client
async def create_flow_run_input(
    key: str,
    value: Any,
    flow_run_id: Optional[UUID] = None,
    sender: Optional[str] = None,
    client: "NebulaClient" = None,
):
    """
    Create a new flow run input. The given `value` will be serialized to JSON
    and stored as a flow run input value.

    Args:
        - key (str): the flow run input key
        - value (Any): the flow run input value
        - flow_run_id (UUID): the, optional, flow run ID. If not given will
          default to pulling the flow run ID from the current context.
    """
    flow_run_id = ensure_flow_run_id(flow_run_id)

    await client.create_flow_run_input(
        flow_run_id=flow_run_id,
        key=key,
        sender=sender,
        value=orjson.dumps(value).decode(),
    )


@sync_compatible
@inject_client
async def filter_flow_run_input(
    key_prefix: str,
    limit: int = 1,
    exclude_keys: Optional[Set[str]] = None,
    flow_run_id: Optional[UUID] = None,
    client: "NebulaClient" = None,
):
    if exclude_keys is None:
        exclude_keys = set()

    flow_run_id = ensure_flow_run_id(flow_run_id)

    return await client.filter_flow_run_input(
        flow_run_id=flow_run_id,
        key_prefix=key_prefix,
        limit=limit,
        exclude_keys=exclude_keys,
    )


@sync_compatible
@inject_client
async def read_flow_run_input(
    key: str, flow_run_id: Optional[UUID] = None, client: "NebulaClient" = None
) -> Any:
    """Read a flow run input.

    Args:
        - key (str): the flow run input key
        - flow_run_id (UUID): the flow run ID
    """
    flow_run_id = ensure_flow_run_id(flow_run_id)

    try:
        value = await client.read_flow_run_input(flow_run_id=flow_run_id, key=key)
    except NebulaHTTPStatusError as exc:
        if exc.response.status_code == 404:
            return None
        raise
    else:
        return orjson.loads(value)


@sync_compatible
@inject_client
async def delete_flow_run_input(
    key: str, flow_run_id: Optional[UUID] = None, client: "NebulaClient" = None
):
    """Delete a flow run input.

    Args:
        - flow_run_id (UUID): the flow run ID
        - key (str): the flow run input key
    """

    flow_run_id = ensure_flow_run_id(flow_run_id)

    await client.delete_flow_run_input(flow_run_id=flow_run_id, key=key)
