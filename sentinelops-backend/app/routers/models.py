from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import AIModel

router = APIRouter(tags=["models"])


@router.get("/models")
def list_models(db: Session = Depends(get_db)):
    return [
        {
            "id": m.id, "name": m.name, "kind": m.kind,
            "endpoint": m.endpoint, "latency": m.latency,
            "status": m.status, "enabled": m.enabled,
        }
        for m in db.query(AIModel).all()
    ]


class ModelCreate(BaseModel):
    name: str
    kind: str = "local"
    endpoint: str


@router.post("/models")
def create_model(body: ModelCreate, db: Session = Depends(get_db)):
    import time
    mid = "M-" + str(int(time.time()))[-4:]
    m = AIModel(id=mid, name=body.name, kind=body.kind,
                endpoint=body.endpoint, latency=0, status="offline", enabled=True)
    db.add(m)
    db.commit()
    return {"ok": True, "id": mid}


@router.post("/models/{model_id}/test")
def test_model(model_id: str, db: Session = Depends(get_db)):
    m = db.query(AIModel).filter(AIModel.id == model_id).first()
    if not m:
        raise HTTPException(404, "model not found")
    # 模拟探测：真实实现应发一个 ping 请求
    import random
    m.latency = random.randint(200, 2000)
    m.status = "online"
    db.commit()
    return {"ok": True, "id": model_id, "latency": m.latency, "status": m.status}
