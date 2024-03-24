from nebula._vendor.fastapi import Depends, Query, status
from nebula._vendor.starlette.exceptions import HTTPException

from nebula.logging import get_logger
from nebula.server import models, schemas
from nebula.server.database.dependencies import provide_database_interface
from nebula.server.database.interface import NebulaDBInterface
from nebula.server.utilities.server import NebulaRouter
from nebula.settings import NEBULA_SERVER_CSRF_PROTECTION_ENABLED

logger = get_logger("server.api")

router = NebulaRouter(prefix="/csrf-token")


@router.get("")
async def create_csrf_token(
    db: NebulaDBInterface = Depends(provide_database_interface),
    client: str = Query(..., description="The client to create a CSRF token for"),
) -> schemas.core.CsrfToken:
    """Create or update a CSRF token for a client"""
    if NEBULA_SERVER_CSRF_PROTECTION_ENABLED.value() is False:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="CSRF protection is disabled.",
        )

    async with db.session_context(begin_transaction=True) as session:
        token = await models.csrf_token.create_or_update_csrf_token(
            session=session, client=client
        )
        await models.csrf_token.delete_expired_tokens(session=session)

    return token
