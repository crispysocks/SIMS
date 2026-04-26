from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.employment import Employment
from app.models.student import Student
from app.schemas.employment import (
    AvgSalaryByGroup,
    EmploymentCreate,
    EmploymentRead,
    EmploymentUpdate,
)


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


def create_employment(
    db: Session,
    student_no: str,
    data: EmploymentCreate,
) -> EmploymentRead:
    """新增学生就业信息。"""
    student = db.query(Student).filter(Student.student_no == student_no, Student.isdeleted == 0).first()
    if not student:
        raise HTTPException(status_code=404, detail='学生不存在')
    existing = db.query(Employment).filter(Employment.student_no == student_no, Employment.isdeleted == 0).first()
    if existing:
        raise HTTPException(status_code=409, detail='该学生就业信息已存在')
    employment = Employment(
        student_no=student_no,
        **data.model_dump(),
    )
    db.add(employment)
    db.commit()
    db.refresh(employment)
    return EmploymentRead.model_validate(employment)


def update_employment(
    db: Session,
    student_no: str,
    data: EmploymentUpdate,
) -> EmploymentRead:
    """更新学生就业信息。"""
    employment = db.query(Employment).filter(
        Employment.student_no == student_no,
        Employment.isdeleted == 0,
    ).first()
    if not employment:
        raise HTTPException(status_code=404, detail='就业信息不存在')
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(employment, key, value)
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


def get_employment_by_min_salary(
    db: Session, min_salary: Decimal
) -> list[EmploymentRead]:
    """查询薪资大于等于指定值的就业记录。"""
    items = (
        db.query(Employment)
        .filter(
            Employment.salary >= min_salary,
            Employment.isdeleted == 0,
        )
        .all()
    )
    return [EmploymentRead.model_validate(item) for item in items]


def get_avg_salary_by_group(
    db: Session,
    group_by: str | None = None,
) -> list[AvgSalaryByGroup]:
    """查询平均工资，支持按班级或性别分组。"""
    query = (
        db.query(
            func.avg(Employment.salary).label('avg_salary'),
        )
        .join(Student, Employment.student_no == Student.student_no)
        .filter(
            Employment.isdeleted == 0,
            Student.isdeleted == 0,
            Employment.salary.isnot(None),
        )
    )

    if group_by == 'class':
        query = query.add_columns(Student.class_no.label('group_key')).group_by(Student.class_no)
    elif group_by == 'gender':
        query = query.add_columns(Student.gender.label('group_key')).group_by(Student.gender)
    else:
        result = query.first()
        avg = result.avg_salary if result else None
        return [AvgSalaryByGroup(group_key='all', avg_salary=avg)]

    results = query.all()
    return [
        AvgSalaryByGroup(group_key=r.group_key, avg_salary=r.avg_salary)
        for r in results
    ]


def get_employment_by_status(
    db: Session, status: int
) -> list[EmploymentRead]:
    """按状态查询就业记录，1=正常，0=已删除。"""
    items = (
        db.query(Employment)
        .filter(Employment.isdeleted == status)
        .all()
    )
    return [EmploymentRead.model_validate(item) for item in items]
