from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from app.database import Base

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False, comment='老师姓名')
    # 外键：所属课程 ID，一个老师只能教一门课 (一对一)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, comment='所属课程ID')
    gender = Column(String(5), nullable=True, comment='性别')
    phone_number = Column(String(20), nullable=True, comment='联系电话')
    status = Column(Integer, nullable=False, default=0, comment='状态：0正常，1离职')
    create_time = Column(DateTime, default=func.now(), comment='创建时间')
    update_time = Column(DateTime, default=func.now(), onupdate=func.now(), comment='更新时间')
    avatar_path = Column(String(255), nullable=True, comment='头像路径')

    def __repr__(self):
        return f"<Teacher(id={self.id}, name='{self.name}')>"