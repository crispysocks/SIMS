from datetime import date

from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Integer, Numeric, String

from app.core.database import Base


class Employment(Base):
    __tablename__ = 'employment'

    student_no = Column(String(20), ForeignKey('students.student_no', ondelete='CASCADE'), primary_key=True, comment='学生编号')
    employment_status = Column(Enum('待业', '在聘', '已离职'), default='待业', comment='就业状态')
    employment_open_time = Column(DateTime, comment='就业开放时间')
    offer_time = Column(DateTime, comment='offer下发时间')
    company_name = Column(String(100), comment='就业公司名称')
    salary = Column(Numeric(10, 2), comment='就业薪资')
    position = Column(String(50), comment='工作岗位')
    work_location = Column(String(100), comment='工作地点')
    contract_date = Column(Date, comment='签约日期')
    isdeleted = Column(Integer, default=0, comment='逻辑删除标记 0=正常 1=已删除')
