"""
Routes for interacting with block capabilities.
"""
from typing import List

from nebula._vendor.fastapi import Depends

from nebula.server import models
from nebula.server.database.dependencies import (
    NebulaDBInterface,
    provide_database_interface,
)
from nebula.server.utilities.server import NebulaRouter

router = NebulaRouter(prefix="/block_capabilities", tags=["Block capabilities"])


@router.get("/")
async def read_available_block_capabilities(
    db: NebulaDBInterface = Depends(provide_database_interface),
) -> List[str]:
    async with db.session_context() as session:
        return await models.block_schemas.read_available_block_capabilities(
            session=session
        )
