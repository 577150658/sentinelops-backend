from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    time: Mapped[str] = mapped_column(String(16))
    actor: Mapped[str] = mapped_column(String(32))
    action: Mapped[str] = mapped_column(String(16))
    target: Mapped[str] = mapped_column(String(255))
    risk: Mapped[str] = mapped_column(String(16), default="low")
    hash: Mapped[str] = mapped_column(String(32))
    prev_hash: Mapped[str] = mapped_column(String(32), default="")
