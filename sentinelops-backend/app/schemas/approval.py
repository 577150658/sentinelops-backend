from pydantic import BaseModel, ConfigDict


class ApprovalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    taskId: str
    title: str
    desc: str
    command: str
    risk: str
