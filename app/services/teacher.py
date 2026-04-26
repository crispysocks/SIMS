from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate, TeacherUpdate


def get_teacher_by_no(db: Session, teacher_no: str) -> Teacher:
    teacher = db.query(Teacher).filter(Teacher.teacher_no == teacher_no).first()
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='教师不存在',
        )
    return teacher


def list_teachers(db: Session) -> list[Teacher]:
    return db.query(Teacher).filter(Teacher.isdeleted == 0).all()


def create_teacher(db: Session, data: TeacherCreate) -> Teacher:
    teacher = Teacher(**data.model_dump())
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher


def update_teacher(db: Session, teacher_no: str, data: TeacherUpdate) -> Teacher:
    teacher = get_teacher_by_no(db, teacher_no)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(teacher, field, value)
    db.commit()
    db.refresh(teacher)
    return teacher


def delete_teacher(db: Session, teacher_no: str) -> Teacher:
    teacher = get_teacher_by_no(db, teacher_no)
    teacher.isdeleted = 1
    db.commit()
    db.refresh(teacher)
    return teacher
