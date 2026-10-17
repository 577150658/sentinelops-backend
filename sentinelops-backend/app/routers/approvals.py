from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Approval
from app.schemas.approval import ApprovalOut

router = APIRouter(tags=["approvals"])


@router.get("/engagements/{eid}/approvals", response_model=list[ApprovalOut])
def list_approvals(eid: str, db: Session = Depends(get_db)):
    rows = db.query(Approval).all()
    return [
        ApprovalOut(
            id=r.id, taskId=r.task_id, title=r.title,
            desc=r.desc, command=r.command, risk=r.risk,
        )
        for r in rows
    ]
