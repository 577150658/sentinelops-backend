from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import AuditLog
from app.schemas.audit import AuditOut

router = APIRouter(tags=["audit"])


@router.get("/engagements/{eid}/audit", response_model=list[AuditOut])
def list_audit(eid: str, db: Session = Depends(get_db)):
    return db.query(AuditLog).order_by(AuditLog.id.desc()).all()
