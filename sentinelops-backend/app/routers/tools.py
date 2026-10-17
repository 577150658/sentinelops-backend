from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Tool

router = APIRouter(tags=["tools"])


@router.get("/tools")
def list_tools(db: Session = Depends(get_db)):
    return [
        {
            "id": t.id, "endpoint": t.endpoint, "tools": t.tools,
            "permission": t.permission, "signature": t.signature,
            "lastCall": t.last_call, "enabled": t.enabled,
        }
        for t in db.query(Tool).all()
    ]


@router.post("/tools/{tool_id}/toggle")
def toggle_tool(tool_id: str, db: Session = Depends(get_db)):
    t = db.query(Tool).filter(Tool.id == tool_id).first()
    if not t:
        raise HTTPException(404, "tool not found")
    t.enabled = not t.enabled
    db.commit()
    return {"ok": True, "id": tool_id, "enabled": t.enabled}

# ============================================================
# 注册工具接口
# ============================================================
from pydantic import BaseModel


class ToolCreate(BaseModel):
    endpoint: str
    tools: str = ""
    permission: str = "扫描"
    signature: str = "待校验"


@router.post("/tools")
def create_tool(body: ToolCreate, db: Session = Depends(get_db)):
    import time
    tid = "T-" + str(int(time.time()))[-4:]
    t = Tool(
        id=tid,
        endpoint=body.endpoint,
        tools=body.tools,
        permission=body.permission,
        signature=body.signature,
        last_call="—",
        enabled=False,
    )
    db.add(t)
    db.commit()
    return {
        "ok": True,
        "id": tid,
        "endpoint": t.endpoint,
        "enabled": t.enabled,
    }
