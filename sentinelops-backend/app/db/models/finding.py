from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[str] = mapped_column(String(16), primary_key=True)
    severity: Mapped[str] = mapped_column(String(16))
    title: Mapped[str] = mapped_column(String(255))
    target: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(16), default="pending")
    cvss: Mapped[float] = mapped_column(Float, default=0.0)
    tool: Mapped[str] = mapped_column(String(64), default="")
