from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Approval(Base):
    __tablename__ = "approvals"

    id: Mapped[str] = mapped_column(String(16), primary_key=True)
    task_id: Mapped[str] = mapped_column(String(16), index=True)
    title: Mapped[str] = mapped_column(String(255))
    desc: Mapped[str] = mapped_column(String(512))
    command: Mapped[str] = mapped_column(String(512))
    risk: Mapped[str] = mapped_column(String(16))
