from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Task, AuditLog
from app.core.ws_manager import ws_manager

router = APIRouter(tags=["emergency"])


def _hash(prev: str, record: dict) -> str:
    import hashlib, json
    return hashlib.sha256(
        (json.dumps(record, sort_keys=True) + prev).encode()
    ).hexdigest()[:16]


@router.post("/emergency-stop")
async def emergency_stop(db: Session = Depends(get_db)):
    db.query(Task).filter(Task.status == "running").update({"status": "stopped"})

    last = db.query(AuditLog).order_by(AuditLog.id.desc()).first()
    prev = last.hash if last else "genesis"
    record = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "actor": "operator", "action": "停止",
        "target": "所有沙箱任务",
    }
    db.add(AuditLog(
        time=record["time"], actor="operator", action="停止",
        target="所有沙箱任务", risk="high",
        hash=_hash(prev, record), prev_hash=prev,
    ))
    db.commit()

    await ws_manager.broadcast("audit.log", {
        "time": record["time"], "actor": "operator",
        "action": "停止", "target": "所有沙箱任务",
    })
    return {"ok": True}
