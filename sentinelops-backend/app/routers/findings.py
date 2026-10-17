from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Finding
from app.schemas.finding import FindingOut

router = APIRouter(tags=["findings"])


@router.get("/engagements/{eid}/findings", response_model=list[FindingOut])
def list_findings(eid: str, db: Session = Depends(get_db)):
    return db.query(Finding).all()
