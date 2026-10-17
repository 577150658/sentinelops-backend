from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Skill
from app.schemas.skill import SkillOut

router = APIRouter(tags=["skills"])


@router.get("/skills", response_model=list[SkillOut])
def list_skills(db: Session = Depends(get_db)):
    rows = db.query(Skill).all()
    return [
        SkillOut(
            id=r.id, icon=r.icon, name=r.name, version=r.version,
            author=r.author, desc=r.desc,
            tags=[t for t in (r.tags or "").split(",") if t],
            risk=r.risk, tools=r.tools, runs=r.runs, enabled=r.enabled,
        )
        for r in rows
    ]
