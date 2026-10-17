from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Target

router = APIRouter(tags=["targets"])


class TargetOut(BaseModel):
    id: str
    target: str
    type: str
    owner: str
    status: str
    findings: int

    class Config:
        from_attributes = True


class TargetCreate(BaseModel):
    target: str
    type: str = "域名"
    owner: str = ""


@router.get("/engagements/{eid}/targets", response_model=list[TargetOut])
def list_targets(eid: str, db: Session = Depends(get_db)):
    return db.query(Target).all()


@router.post("/engagements/{eid}/targets")
def create_target(eid: str, body: TargetCreate, db: Session = Depends(get_db)):
    import time
    tid = "TG-" + str(int(time.time()))[-4:]
    t = Target(
        id=tid,
        target=body.target,
        type=body.type or "域名",
        owner=body.owner or "",
        status="待扫描",
        findings=0,
    )
    db.add(t)
    db.commit()
    return {
        "ok": True,
        "id": tid,
        "target": t.target,
        "type": t.type,
        "owner": t.owner,
        "status": t.status,
        "findings": t.findings,
    }


@router.delete("/targets/{target_id}")
def delete_target(target_id: str, db: Session = Depends(get_db)):
    t = db.query(Target).filter(Target.id == target_id).first()
    if t:
        db.delete(t)
        db.commit()
    return {"ok": True, "id": target_id}
