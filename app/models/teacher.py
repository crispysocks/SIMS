# ============================================================
# models/teacher.py —— 教师数据模型
# ============================================================
# 这个文件定义了"教师"这个数据表的结构。
#
# 教师表（teachers）存储了什么？
#   - 教师编号（主键）
#   - 姓名、性别
#   - 联系电话、电子邮箱
#   - 身份证号
#   - 出生日期、入职日期
#   - 授课科目
#   - 逻辑删除标记
# ============================================================

from datetime import date

from sqlalchemy import Column, Date, Enum, Integer, String, Text

from app.core.database import Base


class Teacher(Base):
    """
    教师信息模型，对应数据库里的 teachers 表。

    关系说明：
        - 教师表被班级表引用（班主任、授课老师）
        - 但教师表本身不直接引用其他表
    """

    __tablename__ = 'teachers'

    # ---------- 字段定义 ----------

    # 教师编号，主键
    teacher_no = Column(String(20), primary_key=True, comment='老师编号')

    name = Column(String(50), nullable=False, comment='老师姓名')

    gender = Column(Enum('男', '女'), nullable=False, comment='性别')

    phone = Column(String(20), comment='联系电话')

    email = Column(String(100), comment='电子邮箱')

    id_card = Column(String(18), comment='身份证号')

    birthday = Column(Date, comment='出生日期')

    hire_date = Column(Date, comment='入职日期')

    # 授课科目，比如 "Python"、"数据库"
    subject = Column(String(50), comment='授课科目')

    # 逻辑删除标记
    isdeleted = Column(Integer, default=0, comment='逻辑删除标记 0=正常 1=已删除')
