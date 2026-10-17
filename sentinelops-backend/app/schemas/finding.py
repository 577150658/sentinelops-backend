from pydantic import BaseModel, ConfigDict


class FindingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    severity: str
    title: str
    target: str
    status: str
    cvss: float
    tool: str
