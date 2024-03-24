from typing import Optional

from nebula._vendor.fastapi import (
    WebSocket,
)
from nebula._vendor.starlette.status import (
    WS_1002_PROTOCOL_ERROR,
    WS_1008_POLICY_VIOLATION,
)
from nebula._vendor.starlette.websockets import WebSocketDisconnect
from websockets.exceptions import ConnectionClosed

NORMAL_DISCONNECT_EXCEPTIONS = (IOError, ConnectionClosed, WebSocketDisconnect)


async def accept_nebula_socket(websocket: WebSocket) -> Optional[WebSocket]:
    subprotocols = websocket.headers.get("Sec-WebSocket-Protocol", "").split(",")
    if "nebula" not in subprotocols:
        return await websocket.close(WS_1002_PROTOCOL_ERROR)

    await websocket.accept(subprotocol="nebula")

    try:
        # Websocket connections are authenticated via messages. The first
        # message is expected to be an auth message, and if any other type of
        # message is received then the connection will be closed.
        #
        # There is no authentication in Nebula Server, but the protocol requires
        # that we receive and return the auth message for compatibility with Nebula
        # Cloud.
        message = await websocket.receive_json()
        if message["type"] != "auth":
            return await websocket.close(WS_1008_POLICY_VIOLATION)

        await websocket.send_json({"type": "auth_success"})
        return websocket

    except NORMAL_DISCONNECT_EXCEPTIONS:
        # it's fine if a client disconnects either normally or abnormally
        return None
