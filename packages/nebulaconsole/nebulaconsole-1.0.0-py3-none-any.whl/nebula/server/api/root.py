"""
Contains the `hello` route for testing and healthcheck purposes.
"""
from nebula._vendor.fastapi import Depends, status
from nebula._vendor.fastapi.responses import JSONResponse

from nebula.server.database.dependencies import provide_database_interface
from nebula.server.database.interface import NebulaDBInterface
from nebula.server.utilities.server import NebulaRouter

router = NebulaRouter(prefix="", tags=["Root"])


@router.get("/hello")
async def hello():
    """Say hello!"""
    return "👋"


@router.get("/ready")
async def perform_readiness_check(
    db: NebulaDBInterface = Depends(provide_database_interface),
):
    is_db_connectable = await db.is_db_connectable()

    if is_db_connectable:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "OK"},
        )

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"message": "Database is not available"},
    )
