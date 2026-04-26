from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base  # 修改这里

Base = declarative_base()

class Employment(Base):
    __tablename__ = "employment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer)
    open_time = Column(Date)
    offer_time = Column(Date)
    company = Column(String(100))
    salary = Column(Integer)
    status = Column(Integer, default=1)  # 同时修复 default 值