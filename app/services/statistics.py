# ============================================================
# services/statistics.py —— 统计分析业务逻辑
# ============================================================
# 这个文件负责处理各种统计查询。
#
# 统计分析的特点：
#   - 只查询数据，不修改数据
#   - 通常使用 SQL 的聚合函数（COUNT、AVG、SUM 等）
#   - 经常需要 JOIN 多张表
#
# 包含的统计功能：
#   - 按年龄查询学生
#   - 班级性别统计
#   - 每次考试都高于某分数的学生
#   - 两次及以上不及格的学生
#   - 班级平均成绩
#   - 就业薪资最高的学生
#   - 就业时长统计
# ============================================================

from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.classes import ClassInfo
from app.models.employment import Employment
from app.models.score import Score
from app.models.student import Student


def find_students_by_age(db: Session, age: int = 30) -> list[dict]:
    """
    查询年龄大于等于指定值的学生。

    默认查询年龄 >= 30 的学生。
    """
    items = db.query(Student).filter(Student.isdeleted == 0, Student.age >= age).all()
    return [
        {
            'student_no': item.student_no,
            'name': item.name,
            'class_no': item.class_no,
            'age': item.age,
        }
        for item in items
    ]


def get_class_gender_stats(db: Session) -> list[dict]:
    """
    统计每个班级的总人数和男女数量。

    使用 case 语句在 SQL 中实现条件计数：
        - gender == '男' 时计 1，否则计 0
        - 然后 SUM 就是男生总数
    """
    rows = (
        db.query(
            Student.class_no,
            ClassInfo.class_name,
            func.count(Student.student_no).label('total'),
            func.sum(case((Student.gender == '男', 1), else_=0)).label('male_count'),
            func.sum(case((Student.gender == '女', 1), else_=0)).label('female_count'),
        )
        .join(ClassInfo, Student.class_no == ClassInfo.class_no)
        .filter(Student.isdeleted == 0, ClassInfo.isdeleted == 0)
        .group_by(Student.class_no, ClassInfo.class_name)
        .order_by(Student.class_no)
        .all()
    )
    return [
        {
            'class_no': row.class_no,
            'class_name': row.class_name,
            'total': row.total,
            'male_count': row.male_count or 0,
            'female_count': row.female_count or 0,
        }
        for row in rows
    ]


def get_students_always_above_score(db: Session, score: int = 80) -> list[dict]:
    """
    查询每次考试成绩都高于指定分数的学生。

    实现思路：
        1. 先找出有成绩 <= 指定分数的学生（子查询）
        2. 再查询不在这些学生中的记录
    """
    # 子查询：找出有不及格记录的学生
    failed_subquery = db.query(Score.student_no).filter(Score.isdeleted == 0, Score.score <= score)

    rows = (
        db.query(Student.student_no, Student.name, Student.class_no)
        .join(Score, Score.student_no == Student.student_no)
        .filter(
            Student.isdeleted == 0,
            Score.isdeleted == 0,
            # not_in 表示"不在这个列表里"
            Student.student_no.not_in(failed_subquery)
        )
        .group_by(Student.student_no, Student.name, Student.class_no)
        .order_by(Student.student_no)
        .all()
    )
    return [
        {'student_no': row.student_no, 'name': row.name, 'class_no': row.class_no}
        for row in rows
    ]


def get_students_failed_twice_or_more(db: Session) -> list[dict]:
    """
    查询两次及以上不及格（< 60 分）的学生。

    实现思路：
        1. 按学生分组，统计不及格次数
        2. 用 HAVING 筛选次数 >= 2 的学生
        3. 返回学生基本信息
    """
    # 第一步：找出不及格次数 >= 2 的学生
    failed_ids_result = (
        db.query(Score.student_no)
        .filter(Score.isdeleted == 0, Score.score < 60)
        .group_by(Score.student_no)
        .having(func.count(Score.student_no) >= 2)
        .all()
    )
    failed_ids = [row.student_no for row in failed_ids_result]

    if not failed_ids:
        return []

    # 第二步：查询这些学生的基本信息
    rows = (
        db.query(Student.student_no, Student.name, Student.class_no)
        .filter(
            Student.isdeleted == 0,
            Student.student_no.in_(failed_ids)
        )
        .order_by(Student.class_no, Student.student_no)
        .all()
    )

    return [
        {'student_no': row.student_no, 'name': row.name, 'class_no': row.class_no}
        for row in rows
    ]


def get_class_avg_scores_by_exam(db: Session) -> list[dict]:
    """
    统计每个班级的平均成绩，并按分数从高到低排列。
    """
    rows = (
        db.query(Student.class_no, ClassInfo.class_name, func.avg(Score.score).label('avg_score'))
        .join(Score, Score.student_no == Student.student_no)
        .join(ClassInfo, Student.class_no == ClassInfo.class_no)
        .filter(Student.isdeleted == 0, Score.isdeleted == 0, ClassInfo.isdeleted == 0)
        .group_by(Student.class_no, ClassInfo.class_name)
        .order_by(func.avg(Score.score).desc())
        .all()
    )
    return [
        {'class_no': row.class_no, 'class_name': row.class_name, 'avg_score': float(row.avg_score)}
        for row in rows
    ]


def get_top_salary_students(db: Session) -> list[dict]:
    """
    统计就业薪资最高的前五名学生。

    使用 limit(5) 限制只返回前 5 条。
    """
    rows = (
        db.query(Student.student_no, Student.name, Student.class_no, Employment.offer_time, Employment.company_name, Employment.salary, Employment.position)
        .join(Employment, Employment.student_no == Student.student_no)
        .filter(Student.isdeleted == 0, Employment.isdeleted == 0)
        .order_by(Employment.salary.desc())
        .limit(5)
        .all()
    )
    return [
        {
            'student_no': row.student_no,
            'name': row.name,
            'class_no': row.class_no,
            'offer_time': row.offer_time,
            'company': row.company_name,
            'salary': float(row.salary) if row.salary is not None else None,
            'position': row.position,
        }
        for row in rows
    ]


def get_student_offer_duration(db: Session) -> list[dict]:
    """
    统计每个学生的就业时长。

    就业时长 = offer_time - employment_open_time（天数差）

    使用 timestampdiff 计算两个日期的天数差。
    """
    rows = (
        db.query(
            Student.student_no,
            Student.name,
            func.timestampdiff(func.text('day'), Employment.employment_open_time, Employment.offer_time).label('days'),
        )
        .join(Employment, Employment.student_no == Student.student_no)
        .filter(Student.isdeleted == 0, Employment.isdeleted == 0)
        .all()
    )
    return [
        {'student_no': row.student_no, 'name': row.name, 'offer_duration_days': row.days}
        for row in rows
    ]


def get_class_avg_offer_duration(db: Session) -> list[dict]:
    """
    统计每个班级的平均就业时长。
    """
    rows = (
        db.query(
            Student.class_no,
            ClassInfo.class_name,
            func.avg(
                func.timestampdiff(func.text('day'), Employment.employment_open_time, Employment.offer_time)
            ).label('avg_days'),
        )
        .join(Employment, Employment.student_no == Student.student_no)
        .join(ClassInfo, Student.class_no == ClassInfo.class_no)
        .filter(
            Student.isdeleted == 0,
            Employment.isdeleted == 0,
            ClassInfo.isdeleted == 0,
            Employment.employment_open_time.is_not(None)  # 排除空值
        )
        .group_by(Student.class_no, ClassInfo.class_name)
        .order_by(Student.class_no)
        .all()
    )
    return [
        {
            'class_no': row.class_no,
            'class_name': row.class_name,
            'avg_offer_duration_days': float(row.avg_days) if row.avg_days is not None else None
        }
        for row in rows
    ]
