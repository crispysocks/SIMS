from fastapi import HTTPException
from sqlalchemy.orm import Session

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
    if data.remark is not None:
        score.remark = data.remark
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
