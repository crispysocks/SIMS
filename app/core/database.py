from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE,
    pool_recycle=settings.DB_POOL_RECYCLE,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """提供数据库会话依赖。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """在应用启动时初始化表结构。"""
    import app.models.classes  # noqa: F401
    import app.models.employment  # noqa: F401
    import app.models.score  # noqa: F401
    import app.models.student  # noqa: F401
    import app.models.teacher  # noqa: F401

    Base.metadata.create_all(bind=engine)
