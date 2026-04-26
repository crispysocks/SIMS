from datetime import date

from sqlalchemy import Column, Date, Enum, Integer, String, Text

from app.core.database import Base


class Teacher(Base):
    __tablename__ = 'teachers'

    teacher_no = Column(String(20), primary_key=True, comment='老师编号')
    name = Column(String(50), nullable=False, comment='老师姓名')
    gender = Column(Enum('男', '女'), nullable=False, comment='性别')
    phone = Column(String(20), comment='联系电话')
    email = Column(String(100), comment='电子邮箱')
    id_card = Column(String(18), comment='身份证号')
    birthday = Column(Date, comment='出生日期')
    hire_date = Column(Date, comment='入职日期')
    subject = Column(String(50), comment='授课科目')
    isdeleted = Column(Integer, default=0, comment='逻辑删除标记 0=正常 1=已删除')
    created_at = Column(Date, nullable=False, comment='创建时间')
    updated_at = Column(Date, nullable=False, comment='更新时间')
