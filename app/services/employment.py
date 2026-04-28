# ============================================================
# services/employment.py —— 就业信息业务逻辑（v1 版）
# ============================================================
# 这个文件负责处理"就业信息"相关的具体业务操作。
#
# v1 版的特点：
#   - 面向单个学生的就业信息管理
#   - student_no 从 URL 参数传入
#   - 使用 HTTPException 抛出错误
#
# 包含的功能：
#   - 查询单个/班级学生的就业信息
#   - 新增、更新、删除就业信息
#   - 按薪资范围查询
#   - 分组统计平均工资
# ============================================================

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
    """
    查询单个学生的就业信息。

    如果该学生没有就业信息，抛出 404 错误。
    """
    employment = db.query(Employment).filter(
        Employment.student_no == student_no,
        Employment.isdeleted == 0,
    ).first()
    if not employment:
        raise HTTPException(status_code=404, detail='就业信息不存在')
    return EmploymentRead.model_validate(employment)


def get_employment_by_class(db: Session, class_no: str) -> list[EmploymentRead]:
    """
    查询指定班级的所有学生就业信息。

    通过 JOIN 关联学生表，筛选出该班级的学生。
    """
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
    """
    新增学生的就业信息。

    步骤：
        1. 检查学生是否存在
        2. 检查该学生是否已有就业信息
        3. 新建就业记录
    """
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
    """
    更新学生的就业信息。

    只更新前端传过来的字段（exclude_unset=True）。
    """
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
    """
    删除学生的就业信息（逻辑删除）。
    """
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
    """
    查询薪资大于等于指定值的就业记录。
    """
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
    """
    查询平均工资，支持按班级或性别分组。

    参数：
        group_by: 分组方式
            - 'class': 按班级分组
            - 'gender': 按性别分组
            - None: 不分组，返回总体平均

    返回值：
        每组的分组标识和平均薪资
    """
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
        # 按班级分组，group_key 是班级编号
        query = query.add_columns(Student.class_no.label('group_key')).group_by(Student.class_no)
    elif group_by == 'gender':
        # 按性别分组，group_key 是性别
        query = query.add_columns(Student.gender.label('group_key')).group_by(Student.gender)
    else:
        # 不分组，返回总体平均
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
    """
    按状态查询就业记录。

    参数：
        status: 0=已删除，1=正常
    """
    items = (
        db.query(Employment)
        .filter(Employment.isdeleted == status)
        .all()
    )
    return [EmploymentRead.model_validate(item) for item in items]
