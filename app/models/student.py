from datetime import date

from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String

from app.core.database import Base


class Student(Base):
    __tablename__ = 'students'

    student_no = Column(String(20), primary_key=True, comment='学生编号')
    class_no = Column(String(20), ForeignKey('classes.class_no', ondelete='RESTRICT'), nullable=False, comment='班级编号')
    name = Column(String(50), nullable=False, comment='学生姓名')
    birth_place = Column(String(100), comment='籍贯')
    graduate_school = Column(String(100), comment='毕业院校')
    major = Column(String(50), comment='专业')
    entrance_time = Column(Date, nullable=False, comment='入学时间')
    graduate_time = Column(Date, comment='毕业时间')
    education = Column(String(20), comment='学历')
    advisor_name = Column(String(50), comment='顾问姓名')
    age = Column(Integer, comment='年龄')
    gender = Column(Enum('男', '女'), nullable=False, comment='性别')
    phone = Column(String(20), comment='联系电话')
    id_card = Column(String(18), comment='身份证号')
    isdeleted = Column(Integer, default=0, comment='逻辑删除标记 0=正常 1=已删除')
    created_at = Column(Date, nullable=False, comment='创建时间')
    updated_at = Column(Date, nullable=False, comment='更新时间')
