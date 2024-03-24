"""
Routes for interacting with flow run state objects.
"""

from typing import List
from uuid import UUID

from nebula._vendor.fastapi import Depends, HTTPException, Path, status

import nebula.server.models as models
import nebula.server.schemas as schemas
from nebula.server.database.dependencies import provide_database_interface
from nebula.server.database.interface import NebulaDBInterface
from nebula.server.utilities.server import NebulaRouter

router = NebulaRouter(prefix="/flow_run_states", tags=["Flow Run States"])


@router.get("/{id}")
async def read_flow_run_state(
    flow_run_state_id: UUID = Path(
        ..., description="The flow run state id", alias="id"
    ),
    db: NebulaDBInterface = Depends(provide_database_interface),
) -> schemas.states.State:
    """
    Get a flow run state by id.
    """
    async with db.session_context() as session:
        flow_run_state = await models.flow_run_states.read_flow_run_state(
            session=session, flow_run_state_id=flow_run_state_id
        )
    if not flow_run_state:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Flow run state not found"
        )
    return flow_run_state


@router.get("/")
async def read_flow_run_states(
    flow_run_id: UUID,
    db: NebulaDBInterface = Depends(provide_database_interface),
) -> List[schemas.states.State]:
    """
    Get states associated with a flow run.
    """
    async with db.session_context() as session:
        return await models.flow_run_states.read_flow_run_states(
            session=session, flow_run_id=flow_run_id
        )
