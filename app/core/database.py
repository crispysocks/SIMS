from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


def _get_server_url() -> str:
    """获取不指定数据库的 MySQL 连接 URL，用于创建数据库。"""
    return f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}"


def _ensure_database_exists() -> None:
    """如果配置的数据库不存在，则创建它。"""
    server_engine = create_engine(
        _get_server_url(),
        pool_pre_ping=True,
        isolation_level="AUTOCOMMIT",
    )
    with server_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {settings.DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
    server_engine.dispose()


# 确保数据库存在后再创建 engine
_ensure_database_exists()

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
    """在应用启动时初始化表结构（表不存在则创建），并确保存在默认管理员账号。"""
    import app.models.classes  # noqa: F401
    import app.models.employment  # noqa: F401
    import app.models.score  # noqa: F401
    import app.models.student  # noqa: F401
    import app.models.teacher  # noqa: F401
    import app.models.user  # noqa: F401

    Base.metadata.create_all(bind=engine)

    from app.models.user import User
    from app.core.security import md5_hash

    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == 'admin').first()
        if not admin:
            db.add(User(
                username='admin',
                password_hash=md5_hash('123456'),
                roles='admin,teacher',
                is_active=1,
            ))
            db.commit()
    finally:
        db.close()
