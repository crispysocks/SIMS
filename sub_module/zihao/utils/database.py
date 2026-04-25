# 1. 导入
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 2. 数据库连接信息（改成你自己的账号密码）
# 格式：mysql+pymysql://账号:密码@localhost:3306/数据库名
DATABASE = "mysql+pymysql://root:123456@localhost:3306/student"

# 3. 引擎 + 会话
engine = create_engine(DATABASE, echo=False)

SessionLocal = sessionmaker(bind=engine, autoflush=False)

# 通过会话工厂创建会话


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()