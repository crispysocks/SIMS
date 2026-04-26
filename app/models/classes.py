from sqlalchemy import Column, Date, DateTime, Integer, String, func

from app.core.database import Base


class ClassInfo(Base):
    """班级信息模型。"""

    __tablename__ = 'class_info'

    class_id = Column(Integer, primary_key=True, autoincrement=True, comment='班级编号')
    class_name = Column(String(50), nullable=False, unique=True, comment='班级名称')
    start_time = Column(Date, nullable=True, comment='开课时间')
    head_teacher_id = Column(Integer, nullable=True, comment='班主任ID')
    lecturer_id = Column(Integer, nullable=True, comment='授课老师ID')
    is_deleted = Column(Integer, nullable=False, default=0, comment='逻辑删除标记')
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment='创建时间')
    update_time = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment='更新时间',
    )
