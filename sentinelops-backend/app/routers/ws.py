import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.ws_manager import ws_manager

ws_router = APIRouter()


@ws_router.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        # 心跳：每 30 秒发一次 ping，保持连接
        while True:
            try:
                await asyncio.wait_for(websocket.receive_text(), timeout=30)
            except asyncio.TimeoutError:
                await websocket.send_json({"type": "ping", "payload": {}})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception:
        ws_manager.disconnect(websocket)
