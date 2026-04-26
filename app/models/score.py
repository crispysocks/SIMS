from sqlalchemy import Column, Integer

from app.core.database import Base


class Score(Base):
    """???????"""

    __tablename__ = 'scores'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='??ID')
    student_id = Column(Integer, nullable=False, comment='??ID')
    exam_order = Column(Integer, nullable=False, comment='????')
    score = Column(Integer, nullable=False, comment='??')
    status = Column(Integer, nullable=False, default=1, comment='?? 1?? 0??')
