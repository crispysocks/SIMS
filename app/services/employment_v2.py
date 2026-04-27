from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.employment import Employment
from app.models.student import Student
from app.schemas.employment_v2 import (
    EmploymentCreate,
    EmploymentUpdate,
    EmploymentQuery,
    EmploymentSearchResponse,
)


def _check_student(db: Session, student_no: str) -> bool:
    """检查学生是否存在且未被删除。"""
    student = (
        db.query(Student)
        .filter(Student.student_no == student_no, Student.isdeleted == 0)
        .first()
    )
    return student is not None


def add_stu_test(db: Session, emp_model: EmploymentCreate):
    """添加学生就业信息。

    若该学生已有被软删除的记录，则复用该记录并更新字段。
    """
    if not _check_student(db, emp_model.student_no):
        return None

    existing = (
        db.query(Employment)
        .filter(Employment.student_no == emp_model.student_no)
        .first()
    )

    if existing:
        if existing.isdeleted == 0:
            return None

        existing.isdeleted = 0
        existing.employment_open_time = emp_model.employment_open_time
        existing.offer_time = emp_model.offer_time
        existing.company_name = emp_model.company_name
        existing.salary = emp_model.salary
        existing.position = emp_model.position
        existing.work_location = emp_model.work_location
        existing.employment_status = emp_model.employment_status or '在聘'
        db.commit()
        db.refresh(existing)
        return existing

    emp = Employment(
        student_no=emp_model.student_no,
        employment_open_time=emp_model.employment_open_time,
        offer_time=emp_model.offer_time,
        company_name=emp_model.company_name,
        salary=emp_model.salary,
        position=emp_model.position,
        work_location=emp_model.work_location,
        employment_status=emp_model.employment_status or '在聘',
        isdeleted=0,
    )
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp


def update_stu_test(db: Session, student_no: str, emp_model: EmploymentUpdate):
    """更新学生就业信息。"""
    emp = (
        db.query(Employment)
        .filter(Employment.student_no == student_no, Employment.isdeleted == 0)
        .first()
    )
    if not emp:
        return None

    update_data = emp_model.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(emp, key, value)
    db.commit()
    db.refresh(emp)
    return emp


def find_emp(db: Session, student_no: str):
    """根据学生编号查询就业信息。"""
    re = (
        db.query(Employment)
        .join(Student, Employment.student_no == Student.student_no)
        .filter(
            and_(
                Student.isdeleted == 0,
                Employment.student_no == student_no,
                Employment.isdeleted == 0,
            )
        )
        .first()
    )
    if re is None:
        return None

    data = {
        'student_no': re.student_no,
        'employment_open_time': re.employment_open_time,
        'offer_time': re.offer_time,
        'company_name': re.company_name,
        'salary': re.salary,
        'position': re.position,
        'work_location': re.work_location,
        'employment_status': re.employment_status,
    }
    return data


def find_list_emp(db: Session, class_no: str):
    """根据班级编号查询就业信息列表。"""
    re = (
        db.query(Employment, Student)
        .join(Student, Employment.student_no == Student.student_no)
        .filter(
            and_(
                Student.isdeleted == 0,
                Student.class_no == class_no,
                Employment.isdeleted == 0,
            )
        )
        .all()
    )
    if not re:
        return {'message': '您查找的班级不存在或该班级无就业信息'}

    data = [
        {
            'student_no': emp.student_no,
            'student_name': stu.name,
            'employment_open_time': emp.employment_open_time,
            'offer_time': emp.offer_time,
            'company_name': emp.company_name,
            'salary': emp.salary,
            'position': emp.position,
            'work_location': emp.work_location,
            'employment_status': emp.employment_status,
        }
        for emp, stu in re
    ]
    return data


def del_emp(db: Session, student_nos: List[str]):
    """软删除就业信息。"""
    emps = (
        db.query(Employment)
        .filter(
            and_(
                Employment.student_no.in_(student_nos),
                Employment.isdeleted == 0,
            )
        )
        .all()
    )
    if not emps:
        return {'message': '您要删除的学生不存在或已经被软删除'}

    for emp in emps:
        emp.isdeleted = 1
    db.commit()
    return {'message': '删除成功'}


def del_emp_back(db: Session, student_nos: List[str]):
    """恢复被软删除的就业信息。"""
    emps = (
        db.query(Employment)
        .filter(
            and_(
                Employment.student_no.in_(student_nos),
                Employment.isdeleted == 1,
            )
        )
        .all()
    )
    if not emps:
        return {'message': '您要恢复的学号都不存在或没有被软删除'}

    for emp in emps:
        emp.isdeleted = 0
    db.commit()
    return {'message': '恢复成功'}


def search_emp_list(db: Session, query: EmploymentQuery):
    """条件搜索就业信息。"""
    re = (
        db.query(Employment, Student.name, Student.class_no)
        .join(Student, Employment.student_no == Student.student_no)
    )

    if query.student_no is not None:
        re = re.filter(Employment.student_no == query.student_no)

    if query.company_name is not None:
        re = re.filter(Employment.company_name == query.company_name)

    if query.min_salary is not None:
        re = re.filter(Employment.salary >= query.min_salary)

    if query.max_salary is not None:
        re = re.filter(Employment.salary <= query.max_salary)

    if query.employment_status is not None:
        re = re.filter(Employment.employment_status == query.employment_status)

    if query.position is not None:
        re = re.filter(Employment.position == query.position)

    if query.work_location is not None:
        re = re.filter(Employment.work_location == query.work_location)

    results = re.filter(Employment.isdeleted == 0).all()

    return [
        EmploymentSearchResponse(
            student_no=emp.student_no,
            student_name=student_name,
            class_no=class_no,
            company_name=emp.company_name or '',
            salary=emp.salary,
            employment_open_time=emp.employment_open_time,
            offer_time=emp.offer_time,
            position=emp.position,
            work_location=emp.work_location,
            employment_status=emp.employment_status or '待业',
        )
        for emp, student_name, class_no in results
    ]
