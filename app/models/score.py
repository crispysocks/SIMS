# ============================================================
# models/score.py —— 成绩数据模型
# ============================================================
# 这个文件定义了"成绩"这个数据表的结构。
#
# 成绩表（scores）存储了什么？
#   - 学生编号
#   - 考试序次（第几次考试）
#   - 分数
#   - 考试日期
#   - 逻辑删除标记
#
# 主键说明：
#   成绩表使用"联合主键"，由 student_no + exam_no 共同组成。
#   这意味着一个学生可以有多次考试的成绩，
#   但每次考试一个学生只有一条记录。
# ============================================================

from datetime import date

from sqlalchemy import Column, Date, ForeignKey, Integer, String, PrimaryKeyConstraint

from app.core.database import Base


class Score(Base):
    """
    成绩模型，对应数据库里的 scores 表。

    关系说明：
        - student_no 关联到 students 表的 student_no
        - ondelete='CASCADE' 表示学生被删除时，成绩记录也一起删除

    联合主键：
        - student_no + exam_no 共同作为主键
        - 这样可以确保一个学生每次考试只有一条成绩记录
    """

    __tablename__ = 'scores'

    # ---------- 字段定义 ----------

    student_no = Column(
        String(20),
        ForeignKey('students.student_no', ondelete='CASCADE'),
        nullable=False,
        comment='学生编号'
    )

    # 考试序次，比如 1 表示第一次考试，2 表示第二次考试
    exam_no = Column(Integer, nullable=False, comment='考核序次')

    score = Column(Integer, nullable=False, comment='成绩')

    exam_date = Column(Date, comment='考核日期')

    # 逻辑删除标记
    isdeleted = Column(Integer, default=0, comment='逻辑删除标记 0=正常 1=已删除')

    # ---------- 联合主键定义 ----------
    # __table_args__ 用来设置表级别的配置
    # PrimaryKeyConstraint 定义联合主键（支持多个字段组成联合主键）：学生编号 + 考试序次
    __table_args__ = (
        PrimaryKeyConstraint('student_no', 'exam_no'),
    )
