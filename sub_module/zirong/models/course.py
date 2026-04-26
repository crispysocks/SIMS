from sqlalchemy import Column, Integer, String
from app.database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(100), nullable=False, comment='课程名称')

    def __repr__(self):
        return f"<Course(id={self.id}, name='{self.course_name}')>"