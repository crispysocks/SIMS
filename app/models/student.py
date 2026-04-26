from sqlalchemy import Column, Date, Integer, String

from app.core.database import Base


class Student(Base):
    __tablename__ = 'students'

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
