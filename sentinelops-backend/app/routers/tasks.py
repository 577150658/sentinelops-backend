from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Task, Approval, AuditLog
from app.schemas.task import TaskOut
from app.core.ws_manager import ws_manager

router = APIRouter(tags=["tasks"])


def _hash(prev: str, record: dict) -> str:
    import hashlib, json
    return hashlib.sha256(
        (json.dumps(record, sort_keys=True) + prev).encode()
    ).hexdigest()[:16]


def _append_audit(db: Session, actor: str, action: str, target: str, risk: str) -> None:
    last = db.query(AuditLog).order_by(AuditLog.id.desc()).first()
    prev = last.hash if last else "genesis"
    record = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "actor": actor,
        "action": action,
        "target": target,
    }
    db.add(AuditLog(
        time=record["time"], actor=actor, action=action,
        target=target, risk=risk, hash=_hash(prev, record), prev_hash=prev,
    ))


@router.get("/engagements/{eid}/tasks", response_model=list[TaskOut])
def list_tasks(eid: str, db: Session = Depends(get_db)):
    return db.query(Task).all()


class ApproveBody(BaseModel):
    actor: str = "approver"


@router.post("/tasks/{task_id}/approve")
async def approve_task(task_id: str, body: ApproveBody | None = None,
                       db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "task not found")
    if task.status != "blocked":
        raise HTTPException(400, f"task status={task.status}, cannot approve")

    task.status = "running"
    task.progress = 5
    db.query(Approval).filter(Approval.task_id == task_id).delete()
    _append_audit(db, (body.actor if body else "approver"),
                  "批准", f"task-{task_id}", task.risk)
    db.commit()

    await ws_manager.broadcast("task.progress",
                               {"taskId": task_id, "progress": 5})
    await ws_manager.broadcast("audit.log", {
        "time": datetime.now().strftime("%H:%M:%S"),
        "actor": "approver", "action": "批准",
        "target": f"task-{task_id}",
    })
    return {"ok": True, "taskId": task_id}


@router.post("/tasks/{task_id}/reject")
async def reject_task(task_id: str, body: ApproveBody | None = None,
                      db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "task not found")

    task.status = "rejected"
    db.query(Approval).filter(Approval.task_id == task_id).delete()
    _append_audit(db, (body.actor if body else "approver"),
                  "拒绝", f"task-{task_id}", task.risk)
    db.commit()

    await ws_manager.broadcast("audit.log", {
        "time": datetime.now().strftime("%H:%M:%S"),
        "actor": "approver", "action": "拒绝",
        "target": f"task-{task_id}",
    })
    return {"ok": True, "taskId": task_id}


class VerifyBody(BaseModel):
    name: str


@router.post("/tasks/verify")
async def create_verify_task(body: VerifyBody, db: Session = Depends(get_db)):
    import time
    vid = "V-" + str(int(time.time()))[-4:]
    _append_audit(db, "operator", "执行", f"{vid} · {body.name}", "medium")
    db.commit()
    await ws_manager.broadcast("audit.log", {
        "time": datetime.now().strftime("%H:%M:%S"),
        "actor": "operator", "action": "执行",
        "target": f"{vid} · {body.name}",
    })
    return {"id": vid, "name": body.name, "status": "pending_approval"}
