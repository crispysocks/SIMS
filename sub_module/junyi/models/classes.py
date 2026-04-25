# 导入SQLAlchemy的字段类型：列、日期时间、整数、字符串、日期
from sqlalchemy import Column, DateTime, Integer, String, Date

# 导入Base基类，所有模型都要继承它
from app.core.database import Base

# 班级信息表，对应数据库里的 class_info 表
class ClassInfo(Base):
    # 数据库表名
    __tablename__ = "class_info"

    # 班级编号：主键、自增
    class_id = Column(Integer, primary_key=True, autoincrement=True, comment="班级编号")
    # 班级名称：字符串50位，不能为空
    class_name = Column(String(50), nullable=False, comment="班级名称")
    # 开课时间：日期类型
    start_time = Column(Date, default=None, comment="开课时间")
    # 班主任ID：整数
    head_teacher_id = Column(Integer, default=None, comment="班主任ID")
    # 逻辑删除：0=未删除，1=已删除
    is_deleted = Column(Integer, nullable=False, default=0, comment="逻辑删除")
    # 创建时间
    create_time = Column(DateTime, default=None, comment="创建时间")
    # 更新时间
    update_time = Column(DateTime, default=None, comment="更新时间")