from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.employment import Employment
from app.models.student import Student
from app.schemas.employment import EmploymentRead, EmploymentUpsert


def get_employment_by_student(db: Session, student_no: str) -> EmploymentRead:
    """查询单个学生的就业信息。"""
    employment = db.query(Employment).filter(
        Employment.student_no == student_no,
        Employment.isdeleted == 0,
    ).first()
    if not employment:
        raise HTTPException(status_code=404, detail='就业信息不存在')
    return EmploymentRead.model_validate(employment)


def get_employment_by_class(db: Session, class_no: str) -> list[EmploymentRead]:
    """查询指定班级的就业信息列表。"""
    items = (
        db.query(Employment)
        .join(Student, Employment.student_no == Student.student_no)
        .filter(
            Student.class_no == class_no,
            Student.isdeleted == 0,
            Employment.isdeleted == 0,
        )
        .all()
    )
    return [EmploymentRead.model_validate(item) for item in items]


def upsert_employment(
    db: Session,
    student_no: str,
    data: EmploymentUpsert,
) -> EmploymentRead:
    """新增或更新学生就业信息。"""
    student = db.query(Student).filter(Student.student_no == student_no, Student.isdeleted == 0).first()
    if not student:
        raise HTTPException(status_code=404, detail='学生不存在')
    employment = db.query(Employment).filter(Employment.student_no == student_no).first()
    if employment:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(employment, key, value)
        employment.isdeleted = 0
    else:
        employment = Employment(
            student_no=student_no,
            **data.model_dump(),
        )
        db.add(employment)
    db.commit()
    db.refresh(employment)
    return EmploymentRead.model_validate(employment)


def delete_employment(db: Session, student_no: str) -> None:
    """对指定学生的就业信息执行逻辑删除。"""
    employment = db.query(Employment).filter(
        Employment.student_no == student_no,
        Employment.isdeleted == 0,
    ).first()
    if not employment:
        raise HTTPException(status_code=404, detail='就业信息不存在')
    employment.isdeleted = 1
    db.commit()
