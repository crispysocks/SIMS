# ============================================================
# models/student.py —— 学生数据模型
# ============================================================
# 这个文件定义了"学生"这个数据表的结构。
#
# 学生表（students）存储了什么？
#   - 学生编号（主键）
#   - 班级编号（外键，关联到班级表）
#   - 姓名、性别、年龄
#   - 籍贯、毕业院校、专业、学历
#   - 入学时间、毕业时间
#   - 顾问姓名、联系电话、身份证号
#   - 逻辑删除标记
# ============================================================

from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String

from app.core.database import Base


class Student(Base):
    """
    学生信息模型，对应数据库里的 students 表。

    关系说明：
        - class_no 关联到 classes 表的 class_no
        - ondelete='RESTRICT' 表示如果还有学生属于这个班级，
          就不允许删除这个班级（防止误删）
    """

    __tablename__ = 'students'

    # ---------- 字段定义 ----------

    # 学生编号，主键
    student_no = Column(String(20), primary_key=True, comment='学生编号')

    # 班级编号，外键
    class_no = Column(
        String(20),
        ForeignKey('classes.class_no', ondelete='RESTRICT'),
        nullable=False,
        comment='班级编号'
    )

    name = Column(String(50), nullable=False, comment='学生姓名')

    # 籍贯，即家乡所在地
    birth_place = Column(String(100), comment='籍贯')

    graduate_school = Column(String(100), comment='毕业院校')
    major = Column(String(50), comment='专业')

    entrance_time = Column(Date, nullable=False, comment='入学时间')
    graduate_time = Column(Date, comment='毕业时间')

    # Enum 表示只能从给定的几个值中选择
    education = Column(Enum('专科', '本科', '硕士'), comment='学历')

    # 顾问姓名，招生或负责跟进的顾问
    advisor_name = Column(String(50), comment='顾问姓名')

    age = Column(Integer, comment='年龄')

    gender = Column(Enum('男', '女'), nullable=False, comment='性别')

    phone = Column(String(20), comment='联系电话')

    # 身份证号，18 位
    id_card = Column(String(18), comment='身份证号')

    # 逻辑删除标记
    isdeleted = Column(Integer, default=0, comment='逻辑删除标记 0=正常 1=已删除')
