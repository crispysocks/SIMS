# ============================================================
# models/employment.py —— 就业信息数据模型
# ============================================================
# 这个文件定义了"就业信息"这个数据表的结构。
#
# 就业表（employment）存储了什么？
#   - 学生编号（主键，一个学生只有一条就业记录）
#   - 就业状态（待业、在聘、已离职）
#   - 就业时间、offer 时间
#   - 公司、职位、薪资、工作地点
#   - 逻辑删除标记
#
# 注意：
#   学生编号是主键，这意味着一个学生只能有一条就业记录。
#   如果学生换工作，应该更新这条记录，而不是新增。
# ============================================================

from datetime import date

from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Integer, Numeric, String

from app.core.database import Base


class Employment(Base):
    """
    就业信息模型，对应数据库里的 employment 表。

    关系说明：
        - student_no 关联到 students 表的 student_no
        - ondelete='CASCADE' 表示如果学生被删除，就业记录也一起删除
    """

    __tablename__ = 'employment'

    # ---------- 字段定义 ----------

    # 学生编号，既是主键也是外键
    # 一个学生只能有一条就业记录
    student_no = Column(
        String(20),
        ForeignKey('students.student_no', ondelete='CASCADE'),
        primary_key=True,
        comment='学生编号'
    )

    # Enum 表示这个字段只能从几个固定值中选择
    employment_status = Column(
        Enum('待业', '在聘', '已离职'),
        default='在聘',
        comment='就业状态'
    )

    # DateTime 包含日期和时间，比 Date 更精确
    employment_open_time = Column(DateTime, comment='就业开放时间')
    offer_time = Column(DateTime, comment='offer下发时间')

    company_name = Column(String(100), comment='就业公司名称')

    # Numeric(10, 2) 表示精确小数，总共 10 位，其中 2 位小数
    # 适合存储金额，避免浮点数精度问题
    salary = Column(Numeric(10, 2), comment='就业薪资')

    position = Column(String(50), comment='工作岗位')
    work_location = Column(String(100), comment='工作地点')

    # 逻辑删除标记
    isdeleted = Column(Integer, default=0, comment='逻辑删除标记 0=正常 1=已删除')
