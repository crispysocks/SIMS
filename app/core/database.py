# ============================================================
# database.py —— 数据库连接管理模块
# ============================================================
# 这个文件负责管理数据库的连接、会话和表结构初始化。
#
# 主要功能：
#   1. 自动创建数据库（如果不存在）
#   2. 创建数据库连接引擎（engine）
#   3. 提供数据库会话（SessionLocal）
#   4. 定义 ORM 基类（Base），所有数据表模型都继承它
#   5. 提供 get_db() 函数，供接口函数获取数据库连接
#   6. 加载示例数据（如果配置开启）
#   7. 初始化数据库表结构和默认管理员账号
#
# 什么是 ORM？
#   ORM（对象关系映射）让你可以用 Python 类来操作数据库表，
#   不用直接写 SQL 语句。比如：
#       db.query(Student).filter(Student.name == '张三').first()
#   等价于 SQL：SELECT * FROM student WHERE name = '张三';
# ============================================================

import json      # 用来读取 sample_data.json
import os        # 用来处理文件路径
from datetime import date, datetime  # 用来处理日期格式转换

# SQLAlchemy 核心工具
# create_engine: 创建数据库连接引擎
# text: 把字符串变成安全的 SQL 语句
from sqlalchemy import create_engine, text
# declarative_base: 创建 ORM 基类
# sessionmaker: 创建会话工厂
from sqlalchemy.orm import declarative_base, sessionmaker

# 导入配置，获取数据库连接地址等信息
from app.core.config import settings


# ============================================================
# 辅助函数：获取服务器连接 URL（不指定数据库）
# ============================================================

def _get_server_url() -> str:
    """
    获取不指定数据库的 MySQL 连接地址。

    用途：
        创建数据库时，需要先连接到 MySQL 服务器（不连具体数据库），
        然后执行 CREATE DATABASE 命令。
    """
    return f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}"


# ============================================================
# 辅助函数：确保数据库存在
# ============================================================

def _ensure_database_exists() -> None:
    """
    如果配置的数据库不存在，则自动创建它。

    为什么需要这个？
        新环境部署时，数据库可能还没创建，
        这个函数会在程序启动时自动建好数据库，省去手动创建的步骤。
    """
    # 创建一个临时引擎，连接到 MySQL 服务器（不指定数据库）
    server_engine = create_engine(
        _get_server_url(),
        pool_pre_ping=True,           # 连接前 ping 一下，确保连接可用
        isolation_level="AUTOCOMMIT", # 自动提交模式，CREATE DATABASE 需要
    )
    with server_engine.connect() as conn:
        # 执行 SQL：如果不存在就创建数据库，使用 utf8mb4 编码（支持中文和表情符号）
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {settings.DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
    # 用完关闭临时引擎
    server_engine.dispose()


# 程序启动时立即执行：确保数据库存在
_ensure_database_exists()


# ============================================================
# 创建数据库引擎和会话
# ============================================================

# engine 是数据库连接引擎，负责管理所有数据库连接
# pool_pre_ping=True: 使用前检查连接是否还活着，死了就换新的
# pool_size: 连接池里保持的连接数
# pool_recycle: 连接多久后强制回收，防止 MySQL 超时断开
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE,
    pool_recycle=settings.DB_POOL_RECYCLE,
)

# SessionLocal 是一个"工厂"，用来创建数据库会话
# autocommit=False: 不会自动提交，需要手动调用 db.commit()
# autoflush=False: 不会自动刷新，需要手动调用 db.flush()
# bind=engine: 绑定到上面创建的引擎
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 是 ORM 基类，所有数据表模型（如 Student、Teacher）都要继承这个类
# 继承后，SQLAlchemy 就知道这个类对应数据库里的一张表
Base = declarative_base()


# ============================================================
# 提供数据库会话（供接口函数使用）
# ============================================================

def get_db():
    """
    提供数据库会话的生成器函数。

    用法：
        在接口函数的参数里写：db: Session = Depends(get_db)
        FastAPI 会自动调用这个函数，把 db 传进来。

    为什么用 yield？
        这是 Python 的生成器语法，配合 try...finally 可以确保
        无论接口执行成功还是报错，数据库连接都会被关闭。
    """
    db = SessionLocal()   # 创建一个新的会话
    try:
        yield db          # 把会话交给接口函数使用
    finally:
        db.close()        # 接口结束后关闭会话，释放连接


# ============================================================
# 辅助函数：解析日期字符串
# ============================================================

def _parse_date(value):
    """
    把 JSON 里的日期字符串转成 Python 的 date 或 datetime 对象。

    参数：
        value: 可能是字符串（如 "2023-01-01"）、None，或已经是日期对象

    返回值：
        对应的 date 或 datetime 对象，如果 value 是 None 则返回 None
    """
    if value is None:
        return None
    if isinstance(value, str):
        # 如果字符串里包含 "T"，说明是 datetime 格式（如 "2023-01-01T12:00:00"）
        if "T" in value:
            return datetime.fromisoformat(value)
        # 否则是 date 格式（如 "2023-01-01"）
        return date.fromisoformat(value)
    return value


# ============================================================
# 加载示例数据
# ============================================================

def _load_sample_data() -> None:
    """
    如果配置启用，则从 sample_data.json 加载测试数据。

    用途：
        新环境部署时，自动填充一些测试数据，方便演示和开发。

    注意：
        加载完成后会自动把 .env 里的 LOAD_SAMPLE_DATA 改成 False，
        防止下次启动时重复导入。
    """
    if not settings.LOAD_SAMPLE_DATA:
        return

    # 计算 sample_data.json 的绝对路径
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_data.json")
    data_path = os.path.abspath(data_path)
    if not os.path.exists(data_path):
        return

    # 读取 JSON 文件
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 导入各个模型类
    from app.models.classes import ClassInfo
    from app.models.employment import Employment
    from app.models.score import Score
    from app.models.student import Student
    from app.models.teacher import Teacher

    # 创建会话并导入数据
    db = SessionLocal()
    try:
        # 导入教师数据
        for item in data.get("teachers", []):
            item["birthday"] = _parse_date(item.get("birthday"))
            item["hire_date"] = _parse_date(item.get("hire_date"))
            # 如果数据库里已经有这个教师，就跳过（避免重复）
            if not db.query(Teacher).filter(Teacher.teacher_no == item["teacher_no"]).first():
                db.add(Teacher(**item))
        db.commit()

        # 导入班级数据
        for item in data.get("classes", []):
            item["class_open_time"] = _parse_date(item.get("class_open_time"))
            if not db.query(ClassInfo).filter(ClassInfo.class_no == item["class_no"]).first():
                db.add(ClassInfo(**item))
        db.commit()

        # 导入学生数据
        for item in data.get("students", []):
            item["entrance_time"] = _parse_date(item.get("entrance_time"))
            item["graduate_time"] = _parse_date(item.get("graduate_time"))
            if not db.query(Student).filter(Student.student_no == item["student_no"]).first():
                db.add(Student(**item))
        db.commit()

        # 导入成绩数据
        for item in data.get("scores", []):
            item["exam_date"] = _parse_date(item.get("exam_date"))
            # 成绩用学生编号 + 考试序次联合判断是否重复
            existing = db.query(Score).filter(
                Score.student_no == item["student_no"],
                Score.exam_no == item["exam_no"],
            ).first()
            if not existing:
                db.add(Score(**item))
        db.commit()

        # 导入就业数据
        for item in data.get("employments", []):
            item["employment_open_time"] = _parse_date(item.get("employment_open_time"))
            item["offer_time"] = _parse_date(item.get("offer_time"))
            if not db.query(Employment).filter(Employment.student_no == item["student_no"]).first():
                db.add(Employment(**item))
        db.commit()
    finally:
        db.close()

    # 导入完成后，把开关关掉
    _flip_load_sample_data_flag()


# ============================================================
# 辅助函数：关闭示例数据开关
# ============================================================

def _flip_load_sample_data_flag() -> None:
    """
    把 .env 文件里的 LOAD_SAMPLE_DATA 从 True 改成 False。

    为什么要改？
        防止每次启动都重复导入示例数据。
    """
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

    # 如果找到了配置项，就写回文件
    if flipped:
        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

    # 同时更新内存中的配置
    settings.LOAD_SAMPLE_DATA = False


# ============================================================
# 初始化数据库
# ============================================================

def init_db() -> None:
    """
    应用启动时初始化数据库。

    做三件事：
    1. 导入所有模型模块（让 SQLAlchemy 知道有哪些表）
    2. 创建所有表（如果表不存在）
    3. 检查并创建默认管理员账号（admin/123456）
    4. 加载示例数据（如果配置开启）
    """
    # noqa: F401 表示"虽然导入了但没直接用，不要报警告"
    # 导入这些模型是为了让 SQLAlchemy 注册它们，知道要创建哪些表
    import app.models.classes  # noqa: F401
    import app.models.employment  # noqa: F401
    import app.models.score  # noqa: F401
    import app.models.student  # noqa: F401
    import app.models.teacher  # noqa: F401
    import app.models.user  # noqa: F401

    # 根据所有继承 Base 的模型类，在数据库里创建对应的表
    Base.metadata.create_all(bind=engine)

    # 导入 User 模型和密码加密工具
    from app.models.user import User
    from app.core.security import md5_hash

    # 创建会话，检查是否需要创建默认管理员
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == 'admin').first()
        if not admin:
            # 如果不存在 admin 账号，就创建一个
            db.add(User(
                username='admin',
                password_hash=md5_hash('123456'),  # 默认密码 123456
                roles='admin,teacher',              # 同时拥有管理员和老师权限
                is_active=1,                        # 账号启用状态
            ))
            db.commit()
    finally:
        db.close()

    # 最后加载示例数据（如果开启了开关）
    _load_sample_data()
