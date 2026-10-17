from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import AuditLog
from app.core.ws_manager import ws_manager

router = APIRouter(tags=["replay"])


def _hash(prev: str, record: dict) -> str:
    import hashlib, json
    return hashlib.sha256(
        (json.dumps(record, sort_keys=True) + prev).encode()
    ).hexdigest()[:16]


class ReplayBody(BaseModel):
    target: str
    request: str = ""
    modified: bool = False


@router.post("/traffic/replay")
async def replay_traffic(body: ReplayBody, db: Session = Depends(get_db)):
    last = db.query(AuditLog).order_by(AuditLog.id.desc()).first()
    prev = last.hash if last else "genesis"
    record = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "actor": "operator",
        "action": "执行",
        "target": f"replay · {body.target}",
    }
    db.add(AuditLog(
        time=record["time"], actor="operator", action="执行",
        target=record["target"], risk="medium",
        hash=_hash(prev, record), prev_hash=prev,
    ))
    db.commit()

    await ws_manager.broadcast("audit.log", record)

    return {
        "ok": True,
        "target": body.target,
        "modified": body.modified,
        "status": 200,
        "response": {"message": "模拟重放成功，真实实现需接入代理"},
    }
