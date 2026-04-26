from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.employment import Employment
from app.models.student import Student
from app.schemas.employment import EmploymentRead, EmploymentUpsert


def get_employment_by_student(db: Session, student_id: int) -> EmploymentRead:
    """查询单个学生的就业信息。"""
    employment = db.query(Employment).filter(
        Employment.student_id == student_id,
        Employment.status == 1,
    ).first()
    if not employment:
        raise HTTPException(status_code=404, detail='就业信息不存在')
    return EmploymentRead.model_validate(employment)


def get_employment_by_class(db: Session, class_id: int) -> list[EmploymentRead]:
    """查询指定班级的就业信息列表。"""
    items = db.query(Employment).filter(
        Employment.class_id == class_id,
        Employment.status == 1,
    ).all()
    return [EmploymentRead.model_validate(item) for item in items]


def upsert_employment(
    db: Session,
    student_id: int,
    data: EmploymentUpsert,
) -> EmploymentRead:
    """新增或更新学生就业信息，并同步冗余字段。"""
    student = db.query(Student).filter(Student.id == student_id, Student.status == 1).first()
    if not student:
        raise HTTPException(status_code=404, detail='学生不存在')
    employment = db.query(Employment).filter(Employment.student_id == student_id).first()
    if employment:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(employment, key, value)
        employment.student_name = student.name
        employment.class_id = student.class_id
        employment.status = 1
    else:
        employment = Employment(
            student_id=student.id,
            student_name=student.name,
            class_id=student.class_id,
            **data.model_dump(),
        )
        db.add(employment)
    db.commit()
    db.refresh(employment)
    return EmploymentRead.model_validate(employment)


def delete_employment(db: Session, student_id: int) -> None:
    """对指定学生的就业信息执行逻辑删除。"""
    employment = db.query(Employment).filter(
        Employment.student_id == student_id,
        Employment.status == 1,
    ).first()
    if not employment:
        raise HTTPException(status_code=404, detail='就业信息不存在')
    employment.status = 0
    db.commit()
