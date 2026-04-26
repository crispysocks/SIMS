from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from app.core.database import Base


class Teacher(Base):
    """???????"""

    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='??ID')
    name = Column(String(50), nullable=False, comment='????')
    subject = Column(String(50), nullable=False, comment='????')
    gender = Column(String(10), nullable=True, comment='??')
    phone = Column(String(20), nullable=True, comment='????')
    status = Column(Integer, nullable=False, default=1, comment='?? 1?? 0??')
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment='????')
    update_time = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment='????',
    )


class Course(Base):
    """???????"""

    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='??ID')
    course_name = Column(String(100), nullable=False, comment='????')
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False, comment='????ID')
