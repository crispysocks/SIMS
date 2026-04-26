from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.score import Score
from app.models.student import Student
from app.schemas.score import ScoreCreate, ScoreRead, ScoreUpdate


def list_scores_by_student(db: Session, student_id: int) -> list[ScoreRead]:
    """查询指定学生的有效成绩列表。"""
    return [
        ScoreRead.model_validate(item)
        for item in db.query(Score)
        .filter(Score.student_id == student_id, Score.status == 1)
        .order_by(Score.exam_order)
        .all()
    ]


def create_score(db: Session, data: ScoreCreate) -> ScoreRead:
    """录入学生成绩并校验考核序次唯一性。"""
    student = db.query(Student).filter(Student.id == data.student_id, Student.status == 1).first()
    if not student:
        raise HTTPException(status_code=404, detail='学生不存在')
    existing = db.query(Score).filter(
        Score.student_id == data.student_id,
        Score.exam_order == data.exam_order,
        Score.status == 1,
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
        Score.student_id == data.student_id,
        Score.exam_order == data.exam_order,
        Score.status == 1,
    ).first()
    if not score:
        raise HTTPException(status_code=404, detail='成绩记录不存在')
    score.score = data.score
    db.commit()
    db.refresh(score)
    return ScoreRead.model_validate(score)


def delete_score(db: Session, student_id: int, exam_order: int) -> None:
    """逻辑删除指定学生某次考核成绩。"""
    score = db.query(Score).filter(
        Score.student_id == student_id,
        Score.exam_order == exam_order,
        Score.status == 1,
    ).first()
    if not score:
        raise HTTPException(status_code=404, detail='成绩记录不存在')
    score.status = 0
    db.commit()
