from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.employment import Employment
from app.models.score import Score
from app.models.student import Student


def find_students_by_age(db: Session, age: int = 30) -> list[dict]:
    """查询年龄大于等于指定值的学生。"""
    items = db.query(Student).filter(Student.status == 1, Student.age >= age).all()
    return [
        {
            'student_id': item.id,
            'student_no': item.student_no,
            'student_name': item.name,
            'class_id': item.class_id,
            'age': item.age,
        }
        for item in items
    ]


def get_class_gender_stats(db: Session) -> list[dict]:
    """统计每个班级的总人数和男女数量。"""
    rows = (
        db.query(
            Student.class_id,
            func.count(Student.id).label('total'),
            func.sum(case((Student.gender == '男', 1), else_=0)).label('boy_count'),
            func.sum(case((Student.gender == '女', 1), else_=0)).label('girl_count'),
        )
        .filter(Student.status == 1)
        .group_by(Student.class_id)
        .order_by(Student.class_id)
        .all()
    )
    return [
        {
            'class_id': row.class_id,
            'total': row.total,
            'boy_count': row.boy_count or 0,
            'girl_count': row.girl_count or 0,
        }
        for row in rows
    ]


def get_students_always_above_score(db: Session, score: int = 80) -> list[dict]:
    """查询每次考试成绩都高于指定分数的学生。"""
    failed_subquery = db.query(Score.student_id).filter(Score.status == 1, Score.score <= score)
    rows = (
        db.query(Student.id, Student.name, Score.score)
        .join(Score, Score.student_id == Student.id)
        .filter(Student.status == 1, Score.status == 1, Student.id.not_in(failed_subquery))
        .order_by(Student.id)
        .all()
    )
    return [
        {'student_id': row.id, 'student_name': row.name, 'student_score': row.score}
        for row in rows
    ]


def get_students_failed_twice_or_more(db: Session) -> list[dict]:
    """查询两次及以上不及格的学生及对应成绩。"""
    failed_ids = (
        db.query(Score.student_id)
        .filter(Score.status == 1, Score.score < 60)
        .group_by(Score.student_id)
        .having(func.count(Score.id) >= 2)
        .subquery()
    )
    rows = (
        db.query(Student.name, Student.class_id, Score.score)
        .join(Score, Score.student_id == Student.id)
        .filter(Student.status == 1, Score.status == 1, Score.score < 60, Student.id.in_(failed_ids))
        .order_by(Student.class_id, Student.id)
        .all()
    )
    return [
        {'student_name': row.name, 'class_id': row.class_id, 'score': row.score}
        for row in rows
    ]


def get_class_avg_scores_by_exam(db: Session) -> list[dict]:
    """统计每个班级的平均成绩并按分数倒序排列。"""
    rows = (
        db.query(Student.class_id, func.avg(Score.score).label('avg_score'))
        .join(Score, Score.student_id == Student.id)
        .filter(Student.status == 1, Score.status == 1)
        .group_by(Student.class_id)
        .order_by(func.avg(Score.score).desc())
        .all()
    )
    return [{'class_id': row.class_id, 'avg_score': float(row.avg_score)} for row in rows]


def get_top_salary_students(db: Session) -> list[dict]:
    """统计就业薪资最高的前五名学生。"""
    rows = (
        db.query(Student.name, Student.class_id, Employment.offer_date, Employment.company_name, Employment.salary)
        .join(Employment, Employment.student_id == Student.id)
        .filter(Student.status == 1, Employment.status == 1)
        .order_by(Employment.salary.desc())
        .limit(5)
        .all()
    )
    return [
        {
            'name': row.name,
            'class_id': row.class_id,
            'offer_date': row.offer_date,
            'company_name': row.company_name,
            'salary': float(row.salary) if row.salary is not None else None,
        }
        for row in rows
    ]


def get_student_offer_duration(db: Session) -> list[dict]:
    """统计每个学生的就业时长。"""
    rows = (
        db.query(Student.id, Student.name, func.datediff(Employment.offer_date, Employment.open_date).label('days'))
        .join(Employment, Employment.student_id == Student.id)
        .filter(Student.status == 1, Employment.status == 1)
        .all()
    )
    return [
        {'student_id': row.id, 'student_name': row.name, 'duration_days': row.days}
        for row in rows
    ]


def get_class_avg_offer_duration(db: Session) -> list[dict]:
    """统计每个班级的平均就业时长。"""
    rows = (
        db.query(
            Student.class_id,
            func.avg(func.datediff(Employment.offer_date, Employment.open_date)).label('avg_days'),
        )
        .join(Employment, Employment.student_id == Student.id)
        .filter(Student.status == 1, Employment.status == 1, Employment.open_date.is_not(None))
        .group_by(Student.class_id)
        .order_by(Student.class_id)
        .all()
    )
    return [
        {'class_id': row.class_id, 'avg_time': float(row.avg_days) if row.avg_days is not None else None}
        for row in rows
    ]
