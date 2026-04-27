from fastapi import HTTPException
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.classes import ClassInfo
from app.models.score import Score
from app.models.student import Student
from app.schemas.score import ScoreCreate, ScoreRead, ScoreUpdate


def list_scores_by_student(db: Session, student_no: str) -> list[ScoreRead]:
    """查询指定学生的有效成绩列表。"""
    return [
        ScoreRead.model_validate(item)
        for item in db.query(Score)
        .filter(Score.student_no == student_no, Score.isdeleted == 0)
        .order_by(Score.exam_no)
        .all()
    ]


def create_score(db: Session, data: ScoreCreate) -> ScoreRead:
    """录入学生成绩并校验考核序次唯一性。"""
    student = db.query(Student).filter(Student.student_no == data.student_no, Student.isdeleted == 0).first()
    if not student:
        raise HTTPException(status_code=404, detail='学生不存在')
    existing = db.query(Score).filter(
        Score.student_no == data.student_no,
        Score.exam_no == data.exam_no,
        Score.exam_name == data.exam_name,
        Score.isdeleted == 0,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail='该学生该次考核成绩已存在')
    score = Score(**data.model_dump())
    db.add(score)
    db.commit()
    db.refresh(score)
    return ScoreRead.model_validate(score)


def update_score(db: Session, data: ScoreUpdate) -> ScoreRead:
    """修改指定学生某次考核成绩。"""
    score = db.query(Score).filter(
        Score.student_no == data.student_no,
        Score.exam_no == data.exam_no,
        Score.exam_name == data.exam_name,
        Score.isdeleted == 0,
    ).first()
    if not score:
        raise HTTPException(status_code=404, detail='成绩记录不存在')
    score.score = data.score
    if data.exam_date is not None:
        score.exam_date = data.exam_date
    db.commit()
    db.refresh(score)
    return ScoreRead.model_validate(score)


def delete_score(db: Session, student_no: str, exam_no: int, exam_name: str) -> None:
    """逻辑删除指定学生某次考核成绩。"""
    score = db.query(Score).filter(
        Score.student_no == student_no,
        Score.exam_no == exam_no,
        Score.exam_name == exam_name,
        Score.isdeleted == 0,
    ).first()
    if not score:
        raise HTTPException(status_code=404, detail='成绩记录不存在')
    score.isdeleted = 1
    db.commit()


def get_exam_ranking(db: Session, exam_no: int, exam_name: str) -> list[dict]:
    """查询某次考试的学生成绩排名（同分同名次）。"""
    rows = (
        db.query(
            Student.student_no,
            Student.name.label('student_name'),
            Student.class_no,
            ClassInfo.class_name,
            Score.score,
        )
        .join(Score, Score.student_no == Student.student_no)
        .join(ClassInfo, ClassInfo.class_no == Student.class_no)
        .filter(
            Student.isdeleted == 0,
            Score.isdeleted == 0,
            ClassInfo.isdeleted == 0,
            Score.exam_no == exam_no,
            Score.exam_name == exam_name,
        )
        .order_by(Score.score.desc())
        .all()
    )
    result = []
    current_rank = 0
    prev_score = None
    for idx, row in enumerate(rows, start=1):
        if row.score != prev_score:
            current_rank = idx
            prev_score = row.score
        result.append({
            'student_no': row.student_no,
            'student_name': row.student_name,
            'class_no': row.class_no,
            'class_name': row.class_name,
            'score': row.score,
            'rank': current_rank,
        })
    return result


def get_progress_ranking(db: Session, limit: int = 20) -> list[dict]:
    """学生成绩进步榜：前后两次考试分差最大的学生。"""
    subquery = (
        db.query(
            Score.student_no,
            func.max(Score.exam_no).label('latest_exam_no'),
        )
        .filter(Score.isdeleted == 0)
        .group_by(Score.student_no)
        .subquery()
    )
    rows = (
        db.query(
            Student.student_no,
            Student.name.label('student_name'),
            Student.class_no,
            ClassInfo.class_name,
            Score.exam_no.label('previous_exam_no'),
            Score.exam_name.label('previous_exam_name'),
            Score.score.label('previous_score'),
            subquery.c.latest_exam_no,
        )
        .join(Score, Score.student_no == Student.student_no)
        .join(ClassInfo, ClassInfo.class_no == Student.class_no)
        .join(subquery, subquery.c.student_no == Student.student_no)
        .filter(
            Student.isdeleted == 0,
            Score.isdeleted == 0,
            ClassInfo.isdeleted == 0,
            Score.exam_no == subquery.c.latest_exam_no - 1,
        )
        .all()
    )
    result = []
    for row in rows:
        latest = db.query(Score).filter(
            Score.student_no == row.student_no,
            Score.exam_no == row.latest_exam_no,
            Score.isdeleted == 0,
        ).first()
        if latest:
            result.append({
                'student_no': row.student_no,
                'student_name': row.student_name,
                'class_no': row.class_no,
                'class_name': row.class_name,
                'previous_exam_no': row.previous_exam_no,
                'previous_exam_name': row.previous_exam_name,
                'previous_score': row.previous_score,
                'latest_exam_no': latest.exam_no,
                'latest_exam_name': latest.exam_name,
                'latest_score': latest.score,
                'score_diff': latest.score - row.previous_score,
            })
    result.sort(key=lambda x: x['score_diff'], reverse=True)
    return result[:limit]


def get_class_score_report(db: Session, exam_no: int, exam_name: str) -> list[dict]:
    """班级成绩报表：平均分、优秀率、及格率。"""
    rows = (
        db.query(
            Student.class_no,
            ClassInfo.class_name,
            Score.exam_no,
            Score.exam_name,
            func.count(Score.student_no).label('student_count'),
            func.avg(Score.score).label('avg_score'),
            func.sum(case((Score.score >= 85, 1), else_=0)).label('excellent_count'),
            func.sum(case((Score.score >= 60, 1), else_=0)).label('pass_count'),
        )
        .join(Score, Score.student_no == Student.student_no)
        .join(ClassInfo, ClassInfo.class_no == Student.class_no)
        .filter(
            Student.isdeleted == 0,
            Score.isdeleted == 0,
            ClassInfo.isdeleted == 0,
            Score.exam_no == exam_no,
            Score.exam_name == exam_name,
        )
        .group_by(Student.class_no, ClassInfo.class_name, Score.exam_no, Score.exam_name)
        .order_by(func.avg(Score.score).desc())
        .all()
    )
    report = []
    for row in rows:
        count = row.student_count or 0
        avg_score = float(row.avg_score) if row.avg_score is not None else 0.0
        excellent_count = row.excellent_count or 0
        pass_count = row.pass_count or 0
        report.append({
            'class_no': row.class_no,
            'class_name': row.class_name,
            'exam_no': row.exam_no,
            'exam_name': row.exam_name,
            'student_count': count,
            'avg_score': round(avg_score, 2),
            'excellent_rate': round(excellent_count / count, 4) if count else 0.0,
            'pass_rate': round(pass_count / count, 4) if count else 0.0,
            'excellent_count': excellent_count,
            'pass_count': pass_count,
        })
    return report
