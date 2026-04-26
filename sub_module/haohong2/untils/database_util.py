#确认数据库地址
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE = 'mysql+pymysql://root:123456@localhost/test'
# 生成引擎
engine = create_engine(DATABASE,pool_size=5)
# 创建表模型基类

# 创建会话工厂
session = sessionmaker(bind=engine)
db = session()

def get_db():
    try:
        yield db
    finally:
        db.close()