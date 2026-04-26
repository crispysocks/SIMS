from datetime import date

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text

from app.core.database import Base


class ClassInfo(Base):
    __tablename__ = 'classes'

    class_no = Column(String(20), primary_key=True, comment='班级编号')
    class_name = Column(String(50), nullable=False, comment='班级名称')
    class_open_time = Column(Date, nullable=False, comment='开课时间')
    head_teacher_no = Column(String(20), ForeignKey('teachers.teacher_no', ondelete='SET NULL'), comment='班主任编号')
    instructor_no = Column(String(20), ForeignKey('teachers.teacher_no', ondelete='SET NULL'), comment='授课老师编号')
    description = Column(String(500), comment='班级描述')
    isdeleted = Column(Integer, default=0, comment='逻辑删除标记 0=正常 1=已删除')
    created_at = Column(Date, nullable=False, comment='创建时间')
    updated_at = Column(Date, nullable=False, comment='更新时间')
