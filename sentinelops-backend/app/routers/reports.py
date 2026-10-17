from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.session import get_db
from app.db.models import Report

router = APIRouter(tags=["reports"])


@router.get("/reports")
def list_reports(db: Session = Depends(get_db)):
    return [
        {
            "id": r.id, "title": r.title, "fmt": r.fmt,
            "created": r.created, "size": r.size, "status": r.status,
        }
        for r in db.query(Report).order_by(Report.id.desc()).all()
    ]


@router.post("/reports/generate")
def generate_report(db: Session = Depends(get_db)):
    import time
    rid = "R-" + str(int(time.time()))[-4:]
    r = Report(
        id=rid, title="ENG-2041 即时报告", fmt="JSON",
        created=datetime.now().strftime("%Y-%m-%d"),
        size="—", status="ready",
        content='{"generated": true}',
    )
    db.add(r)
    db.commit()
    return {"ok": True, "id": rid, "title": r.title}


@router.get("/reports/{report_id}/download", response_class=PlainTextResponse)
def download_report(report_id: str, db: Session = Depends(get_db)):
    r = db.query(Report).filter(Report.id == report_id).first()
    if not r:
        raise HTTPException(404, "report not found")
    return r.content or "(empty)"
