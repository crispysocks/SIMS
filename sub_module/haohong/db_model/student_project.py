from sqlalchemy import Integer, Column, String, Date, DECIMAL
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Student_BASE(Base):
    __tablename__ = 'student'

    student_id = Column(Integer, primary_key=True)
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
    class_id = Column(Integer)
    status = Column(String(10))

class Score_BASE(Base):
    __tablename__ = 'score'
    score_id = Column(Integer, primary_key=True)
    student_id=Column(Integer)
    exam_order=Column(Integer)
    subject =Column(String(30))
    score =Column(Integer)
    status =Column(Integer)

class Employment_BASE(Base):
    __tablename__ = 'employment'
    employment_id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    open_date = Column(Date)
    offer_date = Column(Date)
    company_name = Column(String(100))
    salary = Column(DECIMAL(10,2))
    status = Column(Integer)