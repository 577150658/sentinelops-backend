from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Target(Base):
    __tablename__ = "targets"

    id: Mapped[str] = mapped_column(String(16), primary_key=True)
    target: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(16), default="域名")
    owner: Mapped[str] = mapped_column(String(64), default="")
    status: Mapped[str] = mapped_column(String(16), default="待扫描")
    findings: Mapped[int] = mapped_column(Integer, default=0)
