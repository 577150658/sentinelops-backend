from pydantic import BaseModel


class SkillOut(BaseModel):
    id: str
    icon: str
    name: str
    version: str
    author: str
    desc: str
    tags: list[str]
    risk: str
    tools: int
    runs: int
    enabled: bool
