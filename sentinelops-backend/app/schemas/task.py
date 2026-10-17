from pydantic import BaseModel, ConfigDict


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    phase: str
    status: str
    risk: str
    agent: str
    progress: int
    command: str = ""
    depends_on: str = ""
    source: str = "template"
