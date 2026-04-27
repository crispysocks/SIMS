import json
import os
from datetime import date, datetime

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


def _parse_date(value):
    """将 JSON 中的日期字符串解析为 date 或 datetime 对象。"""
    if value is None:
        return None
    if isinstance(value, str):
        if "T" in value:
            return datetime.fromisoformat(value)
        return date.fromisoformat(value)
    return value


def _load_sample_data() -> None:
    """如果配置启用，则加载示例数据并自动关闭开关。"""
    if not settings.LOAD_SAMPLE_DATA:
        return

    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_data.json")
    data_path = os.path.abspath(data_path)
    if not os.path.exists(data_path):
        return

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    from app.models.classes import ClassInfo
    from app.models.employment import Employment
    from app.models.score import Score
    from app.models.student import Student
    from app.models.teacher import Teacher

    db = SessionLocal()
    try:
        for item in data.get("teachers", []):
            item["birthday"] = _parse_date(item.get("birthday"))
            item["hire_date"] = _parse_date(item.get("hire_date"))
            if not db.query(Teacher).filter(Teacher.teacher_no == item["teacher_no"]).first():
                db.add(Teacher(**item))
        db.commit()

        for item in data.get("classes", []):
            item["class_open_time"] = _parse_date(item.get("class_open_time"))
            if not db.query(ClassInfo).filter(ClassInfo.class_no == item["class_no"]).first():
                db.add(ClassInfo(**item))
        db.commit()

        for item in data.get("students", []):
            item["entrance_time"] = _parse_date(item.get("entrance_time"))
            item["graduate_time"] = _parse_date(item.get("graduate_time"))
            if not db.query(Student).filter(Student.student_no == item["student_no"]).first():
                db.add(Student(**item))
        db.commit()

        for item in data.get("scores", []):
            item["exam_date"] = _parse_date(item.get("exam_date"))
            existing = db.query(Score).filter(
                Score.student_no == item["student_no"],
                Score.exam_no == item["exam_no"],
                Score.exam_name == item["exam_name"],
            ).first()
            if not existing:
                db.add(Score(**item))
        db.commit()

        for item in data.get("employments", []):
            item["employment_open_time"] = _parse_date(item.get("employment_open_time"))
            item["offer_time"] = _parse_date(item.get("offer_time"))
            if not db.query(Employment).filter(Employment.student_no == item["student_no"]).first():
                db.add(Employment(**item))
        db.commit()
    finally:
        db.close()

    _flip_load_sample_data_flag()


def _flip_load_sample_data_flag() -> None:
    """将 .env 文件中的 LOAD_SAMPLE_DATA 从 True 翻转为 False。"""
    import os

    env_path = os.path.join(os.getcwd(), ".env")
    if not os.path.exists(env_path):
        return

    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    flipped = False
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("LOAD_SAMPLE_DATA="):
            new_lines.append("LOAD_SAMPLE_DATA=False\n")
            flipped = True
        else:
            new_lines.append(line)

    if flipped:
        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

    settings.LOAD_SAMPLE_DATA = False


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

    _load_sample_data()
