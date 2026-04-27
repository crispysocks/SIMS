from datetime import date

from sqlalchemy import Column, Date, ForeignKey, Integer, String, PrimaryKeyConstraint

from app.core.database import Base


class Score(Base):
    __tablename__ = 'scores'

    student_no = Column(String(20), ForeignKey('students.student_no', ondelete='CASCADE'), nullable=False, comment='学生编号')
    exam_no = Column(Integer, nullable=False, comment='考核序次')
    score = Column(Integer, nullable=False, comment='成绩')
    exam_date = Column(Date, comment='考核日期')
    isdeleted = Column(Integer, default=0, comment='逻辑删除标记 0=正常 1=已删除')

    __table_args__ = (
        PrimaryKeyConstraint('student_no', 'exam_no'),
    )
