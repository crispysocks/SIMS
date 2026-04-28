# ============================================================
# models/user.py —— 用户数据模型
# ============================================================
# 这个文件定义了"系统用户"这个数据表的结构。
#
# 用户表（users）存储了什么？
#   - 用户ID（自增主键）
#   - 登录账号（唯一，不能重复）
#   - 密码哈希值（加密后的密码，不是明文）
#   - 角色列表（逗号分隔，如 "admin,teacher"）
#   - 账号是否启用
#   - 创建时间
#
# 注意：
#   用户表和学生表/教师表是分开的！
#   - 学生、教师是"业务数据"，存储真实的人员信息
#   - 用户是"系统账号"，用于登录和管理权限
#   一个人可以既是学生/教师，又是系统用户。
# ============================================================

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.core.database import Base


class User(Base):
    """
    系统用户模型，对应数据库里的 users 表。

    用途：
        用于登录系统和控制权限，
        和学生表、教师表没有直接的外键关系。
    """

    __tablename__ = 'users'

    # ---------- 字段定义 ----------

    # 用户ID，自增主键
    # autoincrement=True 表示数据库会自动分配递增的数字
    id = Column(Integer, primary_key=True, autoincrement=True, comment='用户ID')

    # 登录账号，unique=True 表示不能重复
    username = Column(String(50), unique=True, nullable=False, comment='登录账号')

    # 密码的 MD5 哈希值，不能存明文密码！
    password_hash = Column(String(128), nullable=False, comment='密码MD5哈希值')

    # 角色列表，用逗号分隔
    # 例如：'admin'、'teacher'、'admin,teacher'
    # 系统会根据这个字段判断用户能做什么操作
    roles = Column(String(100), nullable=False, default='teacher', comment='角色列表，逗号分隔')

    # 账号状态：1 表示启用，0 表示禁用
    # 禁用的账号无法登录
    is_active = Column(Integer, default=1, nullable=False, comment='账号是否启用 1=启用 0=禁用')

    # 创建时间，默认是当前时间
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
