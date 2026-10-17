from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[str] = mapped_column(String(16), primary_key=True)
    icon: Mapped[str] = mapped_column(String(8), default="📦")
    name: Mapped[str] = mapped_column(String(64))
    version: Mapped[str] = mapped_column(String(16))
    author: Mapped[str] = mapped_column(String(64))
    desc: Mapped[str] = mapped_column(Text)
    tags: Mapped[str] = mapped_column(String(255), default="")  # 逗号分隔
    risk: Mapped[str] = mapped_column(String(16), default="low")
    tools: Mapped[int] = mapped_column(Integer, default=0)
    runs: Mapped[int] = mapped_column(Integer, default=0)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
