from fastapi import WebSocket
from typing import Any


class WSManager:
    """管理所有活跃的 WebSocket 连接，广播事件到前端"""

    def __init__(self) -> None:
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self.active.append(ws)
        print(f"[WS] connected, total={len(self.active)}")

    def disconnect(self, ws: WebSocket) -> None:
        if ws in self.active:
            self.active.remove(ws)
        print(f"[WS] disconnected, total={len(self.active)}")

    async def broadcast(self, event_type: str, payload: dict[str, Any]) -> None:
        """向前端推送事件，格式与前端 WSMock.emit 对齐"""
        message = {"type": event_type, "payload": payload}
        dead: list[WebSocket] = []
        for ws in self.active:
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)


ws_manager = WSManager()
