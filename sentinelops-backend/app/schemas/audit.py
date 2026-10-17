from pydantic import BaseModel, ConfigDict


class AuditOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    time: str
    actor: str
    action: str
    target: str
    risk: str
    hash: str
