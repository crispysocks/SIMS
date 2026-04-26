from sqlalchemy import Column, Date, Integer, String

from app.core.database import Base


class Student(Base):
    """学生基础信息模型。"""

    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    student_no = Column(String(32), unique=True, nullable=False, comment='学生编号')
    class_id = Column(Integer, nullable=False, comment='班级编号')
    name = Column(String(50), nullable=False, comment='学生姓名')
    hometown = Column(String(100), nullable=True, comment='籍贯')
    graduate_school = Column(String(100), nullable=True, comment='毕业院校')
    major = Column(String(50), nullable=True, comment='专业')
    enroll_date = Column(Date, nullable=True, comment='入学时间')
    graduate_date = Column(Date, nullable=True, comment='毕业时间')
    education = Column(String(20), nullable=True, comment='学历')
    advisor_id = Column(Integer, nullable=True, comment='顾问编号')
    age = Column(Integer, nullable=True, comment='年龄')
    gender = Column(String(10), nullable=True, comment='性别')
    status = Column(Integer, nullable=False, default=1, comment='状态 1正常 0删除')
