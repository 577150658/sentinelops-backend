from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AIModel(Base):
    __tablename__ = "ai_models"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    kind: Mapped[str] = mapped_column(String(16))       # cloud / local
    endpoint: Mapped[str] = mapped_column(String(128))
    latency: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(16), default="offline")
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
