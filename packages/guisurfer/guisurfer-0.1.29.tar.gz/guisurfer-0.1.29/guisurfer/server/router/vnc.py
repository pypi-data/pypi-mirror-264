from typing import List, Annotated, Dict
import asyncio
import traceback
import time

from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    WebSocket,
    WebSocketDisconnect,
    APIRouter,
    Query,
)
import asyncssh
from agentdesk import Desktop
from starlette.datastructures import Headers as StarletteHeaders
import websockets
from websockets import WebSocketClientProtocol
from agentdesk.util import find_open_port
from agentdesk.proxy import ensure_ssh_proxy, cleanup_proxy

from guisurfer.server.models import V1UserProfile
from guisurfer.auth.transport import get_current_user
from guisurfer.server.key import SSHKeyPair

router = APIRouter()


async def handle_client(websocket: WebSocket, ws: WebSocketClientProtocol):
    try:
        while True:
            data = await websocket.receive_bytes()
            await ws.send(data)
    except (WebSocketDisconnect, asyncio.CancelledError):
        print("Client WebSocket disconnected or cancelled.")


async def handle_websockify(websocket: WebSocket, ws: WebSocketClientProtocol):
    try:
        while True:
            data = await ws.recv()
            await websocket.send_bytes(data)
    except (websockets.exceptions.ConnectionClosed, asyncio.CancelledError):
        print("Websockify WebSocket disconnected or cancelled.")


async def ssh_proxy(
    websocket: WebSocket,
    host: str,
    username: str,
    private_ssh_key: str,
    ws_port: int = 6080,
    ssh_port: int = 22,
    headers: Dict[str, str] = {},
):
    reconnect_delay = 1
    try:
        print("WS establishing ssh connection...")
        local_port = find_open_port(6000, 8000)
        pid = ensure_ssh_proxy(
            local_port=local_port,
            remote_port=ws_port,
            ssh_host=host,
            ssh_key=private_ssh_key,
        )
        time.sleep(2)

        async with websockets.connect(f"ws://127.0.0.1:{local_port}") as ws:
            print("WS WebSocket connected.")

            # This block replaces your previous loop with asyncio.create_task
            try:
                tasks = [
                    asyncio.create_task(handle_client(websocket, ws)),
                    asyncio.create_task(handle_websockify(websocket, ws)),
                ]
                done, pending = await asyncio.wait(
                    tasks, return_when=asyncio.FIRST_EXCEPTION
                )

                # Cancel any pending tasks if one fails
                for task in pending:
                    task.cancel()
                # Check for exceptions and handle them
                for task in done:
                    if task.exception():
                        print(f"Task ended with exception: {task.exception()}")
                        break

            except Exception as e:
                print(f"WS Unhandled exception: {e}")
                raise
                # Handle specific cleanup or re-raise if necessary

    except Exception as e:
        print(f"WS Async Error: {e}")
        raise
    finally:
        try:
            cleanup_proxy(pid)
        except Exception as e:
            print(f"WS Cleanup error: {e}")


@router.websocket("/ws/vnc/{desktop_name}")
async def websocket_proxy(
    websocket: WebSocket,
    desktop_name: str,
    token: str = Query(...),
):
    try:
        current_user = await get_current_user(token)
        print("\nWS current_user: ", current_user)
        print("\nWS finding desktop: ", desktop_name)
        found = Desktop.find(owner_id=current_user.email, name=desktop_name.lower())
        if len(found) == 0:
            raise HTTPException(
                status_code=404, detail=f"Desktop {desktop_name} not found"
            )
        desktop = found[0]
        print("\nWS found desktop")

        print("\nWS finding key pair")
        found = SSHKeyPair.find(owner_id=current_user.email, public_key=desktop.ssh_key)
        if len(found) == 0:
            raise HTTPException(
                status_code=404, detail=f"SSH key for desktop {desktop_name} not found"
            )

        key_pair = found[0]
        print("\nWS found key pair")
        private_key = key_pair.decrypt_private_key(key_pair.private_key)
        # print("\nWS using private key: ", private_key)

        await websocket.accept()
    except Exception as e:
        print(f"WS Error: {e}")
        raise

    print("\nWS starting ssh proxy")
    # Proxy the WebSocket connection to the SSH connection
    send_headers = _filter_and_adjust_headers(websocket.headers, desktop.addr)

    try:
        await ssh_proxy(
            websocket=websocket,
            host=desktop.addr,
            username="agentsea",
            private_ssh_key=private_key,
            headers=send_headers,
        )
    except Exception as e:
        print(f"\nWS proxy Error: {e}")
        raise


def _filter_and_adjust_headers(headers: StarletteHeaders, addr: str) -> List[tuple]:
    filtered_headers = []
    for key, value in headers.items():
        key_lower = key.lower()
        if key_lower in [
            "sec-websocket-key",
            "sec-websocket-version",
            "sec-websocket-extensions",
            "cookie",
            "authorization",
        ]:
            continue
        if key_lower == "host":
            value = addr
        filtered_headers.append((key.encode("latin1"), value.encode("latin1")))
    return filtered_headers
