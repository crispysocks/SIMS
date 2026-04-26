from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.employment import Employment
from app.models.score import Score
from app.models.student import Student


def find_students_by_age(db: Session, age: int = 30) -> list[dict]:
    """查询年龄大于等于指定值的学生。"""
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
    """统计每个班级的总人数和男女数量。"""
    rows = (
        db.query(
            Student.class_no,
            func.count(Student.student_no).label('total'),
            func.sum(case((Student.gender == '男', 1), else_=0)).label('boy_count'),
            func.sum(case((Student.gender == '女', 1), else_=0)).label('girl_count'),
        )
        .filter(Student.isdeleted == 0)
        .group_by(Student.class_no)
        .order_by(Student.class_no)
        .all()
    )
    return [
        {
            'class_no': row.class_no,
            'total': row.total,
            'boy_count': row.boy_count or 0,
            'girl_count': row.girl_count or 0,
        }
        for row in rows
    ]


def get_students_always_above_score(db: Session, score: int = 80) -> list[dict]:
    """查询每次考试成绩都高于指定分数的学生。"""
    failed_subquery = db.query(Score.student_no).filter(Score.isdeleted == 0, Score.score <= score)
    rows = (
        db.query(Student.student_no, Student.name, Score.score)
        .join(Score, Score.student_no == Student.student_no)
        .filter(Student.isdeleted == 0, Score.isdeleted == 0, Student.student_no.not_in(failed_subquery))
        .order_by(Student.student_no)
        .all()
    )
    return [
        {'student_no': row.student_no, 'student_name': row.name, 'student_score': float(row.score)}
        for row in rows
    ]


def get_students_failed_twice_or_more(db: Session) -> list[dict]:
    """查询两次及以上不及格的学生及对应成绩。"""
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

    rows = (
        db.query(Student.name, Student.class_no, Score.score)
        .join(Score, Score.student_no == Student.student_no)
        .filter(
            Student.isdeleted == 0,
            Score.isdeleted == 0,
            Score.score < 60,
            Student.student_no.in_(failed_ids)
        )
        .order_by(Student.class_no, Student.student_no)
        .all()
    )

    return [
        {'student_name': row.name, 'class_no': row.class_no, 'score': float(row.score)}
        for row in rows
    ]


def get_class_avg_scores_by_exam(db: Session) -> list[dict]:
    """统计每个班级的平均成绩并按分数倒序排列。"""
    rows = (
        db.query(Student.class_no, func.avg(Score.score).label('avg_score'))
        .join(Score, Score.student_no == Student.student_no)
        .filter(Student.isdeleted == 0, Score.isdeleted == 0)
        .group_by(Student.class_no)
        .order_by(func.avg(Score.score).desc())
        .all()
    )
    return [{'class_no': row.class_no, 'avg_score': float(row.avg_score)} for row in rows]


def get_top_salary_students(db: Session) -> list[dict]:
    """统计就业薪资最高的前五名学生。"""
    rows = (
        db.query(Student.name, Student.class_no, Employment.offer_time, Employment.company_name, Employment.salary)
        .join(Employment, Employment.student_no == Student.student_no)
        .filter(Student.isdeleted == 0, Employment.isdeleted == 0)
        .order_by(Employment.salary.desc())
        .limit(5)
        .all()
    )
    return [
        {
            'name': row.name,
            'class_no': row.class_no,
            'offer_time': row.offer_time,
            'company_name': row.company_name,
            'salary': float(row.salary) if row.salary is not None else None,
        }
        for row in rows
    ]


def get_student_offer_duration(db: Session) -> list[dict]:
    """统计每个学生的就业时长（offer_time - employment_open_time 的天数差）。"""
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
        {'student_no': row.student_no, 'student_name': row.name, 'duration_days': row.days}
        for row in rows
    ]


def get_class_avg_offer_duration(db: Session) -> list[dict]:
    """统计每个班级的平均就业时长。"""
    rows = (
        db.query(
            Student.class_no,
            func.avg(
                func.timestampdiff(func.text('day'), Employment.employment_open_time, Employment.offer_time)
            ).label('avg_days'),
        )
        .join(Employment, Employment.student_no == Student.student_no)
        .filter(Student.isdeleted == 0, Employment.isdeleted == 0, Employment.employment_open_time.is_not(None))
        .group_by(Student.class_no)
        .order_by(Student.class_no)
        .all()
    )
    return [
        {'class_no': row.class_no, 'avg_time': float(row.avg_days) if row.avg_days is not None else None}
        for row in rows
    ]
