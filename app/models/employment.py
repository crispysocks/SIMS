from sqlalchemy import Column, Date, Integer, Numeric, String

from app.core.database import Base


class Employment(Base):
    """?????????"""

    __tablename__ = 'employment'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='????ID')
    student_id = Column(Integer, nullable=False, unique=True, comment='??ID')
    student_name = Column(String(50), nullable=True, comment='??????')
    class_id = Column(Integer, nullable=True, comment='??????')
    open_date = Column(Date, nullable=True, comment='??????')
    offer_date = Column(Date, nullable=True, comment='offer????')
    company_name = Column(String(100), nullable=True, comment='??????')
    salary = Column(Numeric(10, 2), nullable=True, comment='????')
    status = Column(Integer, nullable=False, default=1, comment='?? 1?? 0??')
