from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Students(Base):
    # 指定真实表名
    __tablename__ = "students"

    # 表里的字段
    student_id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer)
    student_name = Column(String(50))
    hometown = Column(String(100))
    graduate_school = Column(String(100))
    major = Column(String(50))
    enroll_date = Column(Date)
    graduate_date = Column(Date)
    education = Column(String(20))
    advisor_id = Column(Integer)
    age = Column(Integer)
    gender = Column(String(10))
    status = Column(Integer)
