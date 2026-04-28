# ============================================================
# models/classes.py —— 班级数据模型
# ============================================================
# 这个文件定义了"班级"这个数据表的结构。
#
# 什么是数据模型？
#   数据模型是一个 Python 类，它告诉 SQLAlchemy：
#   "数据库里有一张表，表里有这些字段，每个字段是什么类型。"
#
#   SQLAlchemy 会根据这个类自动在数据库里创建对应的表，
#   也能把表里的数据读出来变成这个类的对象。
#
# 班级表（classes）存储了什么？
#   - 班级编号、班级名称
#   - 开课时间
#   - 班主任和授课老师的编号（关联到教师表）
#   - 班级描述
#   - 逻辑删除标记
# ============================================================

from datetime import date

# SQLAlchemy 的列定义工具
# Column: 定义一列
# String: 字符串类型
# Integer: 整数类型
# Date: 日期类型
# ForeignKey: 外键（关联到其他表）
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text

# 从 database.py 导入 Base，所有模型都要继承它
from app.core.database import Base


class ClassInfo(Base):
    """
    班级信息模型，对应数据库里的 classes 表。

    关系说明：
        - head_teacher_no（班主任）和 instructor_no（授课老师）
          都关联到 teachers 表的 teacher_no 字段
        - ondelete='SET NULL' 表示如果老师被删除，这两个字段会变成空，
          而不是把班级一起删掉
    """

    # __tablename__ 指定这个类对应数据库里的哪张表
    __tablename__ = 'classes'

    # ---------- 字段定义 ----------

    # primary_key=True 表示这是主键，唯一标识一条记录
    class_no = Column(String(20), primary_key=True, comment='班级编号')

    # nullable=False 表示这个字段不能为空
    class_name = Column(String(50), nullable=False, comment='班级名称')

    class_open_time = Column(Date, nullable=False, comment='开课时间')

    # ForeignKey 表示外键，关联到另一张表的主键
    # ondelete='SET NULL' 表示关联的记录删除时，这里设为 NULL
    head_teacher_no = Column(
        String(20),
        ForeignKey('teachers.teacher_no', ondelete='SET NULL'),
        comment='班主任编号'
    )

    instructor_no = Column(
        String(20),
        ForeignKey('teachers.teacher_no', ondelete='SET NULL'),
        comment='授课老师编号'
    )

    description = Column(String(500), comment='班级描述')

    # 逻辑删除标记：0 表示正常，1 表示已删除
    # 用逻辑删除而不是物理删除，可以保留历史数据，方便恢复
    isdeleted = Column(Integer, default=0, comment='逻辑删除标记 0=正常 1=已删除')
