from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(16), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    phase: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32), default="queued")
    risk: Mapped[str] = mapped_column(String(16), default="low")
    agent: Mapped[str] = mapped_column(String(64), default="")
    progress: Mapped[int] = mapped_column(Integer, default=0)
    command: Mapped[str] = mapped_column(String(512), default="")

    # 新增字段
    depends_on: Mapped[str] = mapped_column(String(128), default="")
    source: Mapped[str] = mapped_column(String(16), default="template")
