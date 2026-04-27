from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

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
    existing = (
        db.query(Teacher)
        .filter(Teacher.teacher_no == data.teacher_no)
        .first()
    )

    if existing:
        if existing.isdeleted == 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='教师编号已存在',
            )

        existing.isdeleted = 0
        existing.name = data.name
        existing.gender = data.gender
        existing.phone = data.phone
        existing.email = data.email
        existing.id_card = data.id_card
        existing.birthday = data.birthday
        existing.hire_date = data.hire_date
        existing.subject = data.subject
        db.commit()
        db.refresh(existing)
        return existing

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


def delete_teachers(db: Session, teacher_nos: list[str]) -> list[Teacher]:
    teachers = (
        db.query(Teacher)
        .filter(Teacher.teacher_no.in_(teacher_nos), Teacher.isdeleted == 0)
        .all()
    )
    if not teachers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='未找到可删除的教师',
        )
    for teacher in teachers:
        teacher.isdeleted = 1
    db.commit()
    for teacher in teachers:
        db.refresh(teacher)
    return teachers


def search_teachers(db: Session, name: str | None = None, gender: str | None = None) -> list[Teacher]:
    query = db.query(Teacher).filter(Teacher.isdeleted == 0)
    if name:
        query = query.filter(Teacher.name.like(f'%{name}%'))
    if gender:
        query = query.filter(Teacher.gender == gender)
    return query.all()


def gender_stats(db: Session) -> list[dict]:
    results = (
        db.query(Teacher.gender, func.count(Teacher.teacher_no).label('count'))
        .filter(Teacher.isdeleted == 0)
        .group_by(Teacher.gender)
        .all()
    )
    total = sum(r.count for r in results)
    return [
        {
            'gender': r.gender,
            'count': r.count,
            'ratio': round(r.count / total, 4) if total else 0.0,
        }
        for r in results
    ]
