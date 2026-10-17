from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import AuditLog
from app.core.ws_manager import ws_manager

router = APIRouter(tags=["imports"])

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def _hash(prev: str, record: dict) -> str:
    import hashlib, json
    return hashlib.sha256(
        (json.dumps(record, sort_keys=True) + prev).encode()
    ).hexdigest()[:16]


@router.post("/imports/{kind}")
async def upload_file(kind: str, file: UploadFile = File(...),
                      db: Session = Depends(get_db)):
    # 保存到 uploads/
    safe_name = Path(file.filename or "unknown").name
    dst = UPLOAD_DIR / f"{kind}_{int(datetime.now().timestamp())}_{safe_name}"
    content = await file.read()
    dst.write_bytes(content)

    last = db.query(AuditLog).order_by(AuditLog.id.desc()).first()
    prev = last.hash if last else "genesis"
    record = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "actor": "operator",
        "action": "执行",
        "target": f"import · {kind} · {safe_name}",
    }
    db.add(AuditLog(
        time=record["time"], actor="operator", action="执行",
        target=record["target"], risk="low",
        hash=_hash(prev, record), prev_hash=prev,
    ))
    db.commit()

    await ws_manager.broadcast("audit.log", record)

    return {
        "ok": True, "kind": kind,
        "filename": safe_name, "size": len(content),
        "saved": str(dst),
    }
