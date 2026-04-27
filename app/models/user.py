from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.core.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='用户ID')
    username = Column(String(50), unique=True, nullable=False, comment='登录账号')
    password_hash = Column(String(128), nullable=False, comment='密码MD5哈希值')
    roles = Column(String(100), nullable=False, default='teacher', comment='角色列表，逗号分隔')
    is_active = Column(Integer, default=1, nullable=False, comment='账号是否启用 1=启用 0=禁用')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
