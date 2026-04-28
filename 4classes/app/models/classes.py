# 导入创建表需要的工具：列、整数、字符串、日期、时间
from sqlalchemy import Column, Integer, String, Date, DateTime

from datetime import datetime

# 导入父类，所有表都必须继承这个
from core.database import Base

# 创建班级表
class ClassInfo(Base):
    # 数据库里的表名
    __tablename__ = "class_info"

    # 班级ID，主键，自动增加
    class_id = Column(Integer, primary_key=True, autoincrement=True)
    # 班级名字，不能为空，最长50字符
    class_name = Column(String(50), nullable=False)
    # 开课时间，可以不填
    start_time = Column(Date, default=None)
    # 班主任ID，可以不填
    head_teacher_id = Column(Integer, default=None)
    # 逻辑删除，0=未删，1=已删，默认0
    is_deleted = Column(Integer, default=0)
    # 创建时间，新增时自动填当前时间
    create_time = Column(DateTime, default=datetime.now)
    # 更新时间，修改时在service里手动更新
    update_time = Column(DateTime, default=None)