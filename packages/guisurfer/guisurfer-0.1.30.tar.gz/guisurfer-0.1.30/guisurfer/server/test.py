from typing import List, Annotated, Dict
import asyncio
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
from agentdesk.util import find_open_port
from agentdesk.proxy import ensure_ssh_proxy, cleanup_proxy

from guisurfer.server.models import V1UserProfile
from guisurfer.auth.transport import get_current_user
from guisurfer.server.key import SSHKeyPair


# TODO: pass headers?


async def connect():
    print("WS ssh_proxy started.")
    async with websockets.connect(f"ws://127.0.0.1:6090") as ws:
        print("WS WebSocket connected.")
        while True:
            try:
                print("\nDATA: ", await ws.recv())
            except asyncio.TimeoutError:
                # Handle timeout if no data is received from websockify
                print("WS timeout error")
                pass
            except websockets.exceptions.ConnectionClosed:
                # Handle connection closure
                print("WS connection closed")
                break
            except Exception as e:
                print(f"WS Error: {e}")
                raise


if __name__ == "__main__":
    asyncio.run(connect())
