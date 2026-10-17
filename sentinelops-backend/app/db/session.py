from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base import Base

# SQLite 需要 check_same_thread=False 允许跨线程访问
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """创建所有表并填充种子数据"""
    from app.db import models  # noqa: F401  确保模型已注册
    Base.metadata.create_all(bind=engine)

    from app.db.seed import seed_if_empty
    seed_if_empty()
