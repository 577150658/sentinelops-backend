from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[str] = mapped_column(String(16), primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    fmt: Mapped[str] = mapped_column(String(16), default="PDF")
    created: Mapped[str] = mapped_column(String(32))
    size: Mapped[str] = mapped_column(String(16), default="—")
    status: Mapped[str] = mapped_column(String(16), default="ready")
    content: Mapped[str] = mapped_column(Text, default="")
