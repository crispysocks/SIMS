from sqlalchemy import Column, Integer, String, DateTime, func,ForeignKey
from Myproject.first_project.core.database import Base


class Teacher(Base):
    __tablename__ = "teacher"
    teacher_id = Column(Integer, primary_key=True, autoincrement=True,comment='老师id')
    teacher_name = Column(String(10),nullable=False,comment='老师姓名')
    subject = Column(String(5),nullable=False,comment='任职课程')
    gender = Column(String(5),nullable=True,comment='性别')
    phone_number=Column(String(20),nullable=True,comment='联系电话')
    status = Column(Integer, nullable=False,default=0,comment='逻辑删除，0是正常，1是离职')
    create_time=Column(DateTime,default=func.now(),comment='创建时间')
    update_time=Column(DateTime,default=func.now(),onupdate=func.now(),comment='更新时间')


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)