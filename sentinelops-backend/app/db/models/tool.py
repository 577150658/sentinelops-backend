from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Tool(Base):
    __tablename__ = "tools"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    endpoint: Mapped[str] = mapped_column(String(128))
    tools: Mapped[str] = mapped_column(String(128))
    permission: Mapped[str] = mapped_column(String(16))
    signature: Mapped[str] = mapped_column(String(16))
    last_call: Mapped[str] = mapped_column(String(16), default="—")
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
