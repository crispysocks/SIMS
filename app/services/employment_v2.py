# ============================================================
# services/employment_v2.py —— 就业信息业务逻辑（v2 版）
# ============================================================
# 这个文件是 employment.py 的升级版，支持更多功能。
#
# v2 和 v1 的区别：
#   - 支持批量操作（批量删除、批量恢复）
#   - student_no 在请求体里传入（不是 URL 参数）
#   - 支持灵活的条件搜索
#   - 返回的数据包含学生姓名和班级编号
#
# 包含的功能：
#   - 添加、更新、查询单个就业信息
#   - 按班级查询就业列表
#   - 批量删除、批量恢复
#   - 条件搜索
# ============================================================

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
    """
    检查学生是否存在且未被删除。

    返回值：
        True: 学生存在且正常
        False: 学生不存在或已删除
    """
    student = (
        db.query(Student)
        .filter(Student.student_no == student_no, Student.isdeleted == 0)
        .first()
    )
    return student is not None


def add_stu_test(db: Session, emp_model: EmploymentCreate):
    """
    添加学生就业信息。

    逻辑：
        1. 检查学生是否存在
        2. 检查是否已有就业记录
        3. 如果已有且已删除 → 恢复并更新
        4. 如果没有 → 新建记录

    返回值：
        成功：就业记录对象
        失败：None（学生不存在或记录已存在）
    """
    if not _check_student(db, emp_model.student_no):
        return None

    existing = (
        db.query(Employment)
        .filter(Employment.student_no == emp_model.student_no)
        .first()
    )

    if existing:
        # 如果记录已存在且未删除，返回 None（不允许重复）
        if existing.isdeleted == 0:
            return None

        # 如果记录已存在但已删除，恢复并更新
        existing.isdeleted = 0
        existing.employment_open_time = emp_model.employment_open_time
        existing.offer_time = emp_model.offer_time
        existing.company_name = emp_model.company_name
        existing.salary = emp_model.salary
        existing.position = emp_model.position
        existing.work_location = emp_model.work_location
        existing.employment_status = emp_model.employment_status
        db.commit()
        db.refresh(existing)
        return existing

    # 新建就业记录
    emp = Employment(
        student_no=emp_model.student_no,
        employment_open_time=emp_model.employment_open_time,
        offer_time=emp_model.offer_time,
        company_name=emp_model.company_name,
        salary=emp_model.salary,
        position=emp_model.position,
        work_location=emp_model.work_location,
        employment_status=emp_model.employment_status,
        isdeleted=0,
    )
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp


def update_stu_test(db: Session, student_no: str, emp_model: EmploymentUpdate):
    """
    更新学生就业信息。

    只更新传入的字段（逐个判断是否为 None）。
    """
    emp = (
        db.query(Employment)
        .filter(Employment.student_no == student_no, Employment.isdeleted == 0)
        .first()
    )
    if not emp:
        return None

    # 逐个字段判断，仅当传入的值不为 None 时才更新
    if emp_model.employment_open_time is not None:
        emp.employment_open_time = emp_model.employment_open_time
    if emp_model.offer_time is not None:
        emp.offer_time = emp_model.offer_time
    if emp_model.company_name is not None:
        emp.company_name = emp_model.company_name
    if emp_model.salary is not None:
        emp.salary = emp_model.salary
    if emp_model.position is not None:
        emp.position = emp_model.position
    if emp_model.work_location is not None:
        emp.work_location = emp_model.work_location
    if emp_model.employment_status is not None:
        emp.employment_status = emp_model.employment_status

    db.commit()
    db.refresh(emp)
    return emp


def find_emp(db: Session, student_no: str):
    """
    根据学生编号查询就业信息。

    返回值：
        就业记录对象，包含关联的学生信息
    """
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
    return re


def find_list_emp(db: Session, class_no: str):
    """
    根据班级编号查询该班所有学生的就业信息。

    返回值：
        包含学生姓名等关联信息的字典列表
    """
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

    # 把查询结果组装成字典列表
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
            'isdeleted': emp.isdeleted,
        }
        for emp, stu in re
    ]
    return data


def del_emp(db: Session, student_nos: List[str]):
    """
    批量软删除就业信息。

    参数：
        student_nos: 学生编号列表
    """
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
    """
    批量恢复被软删除的就业信息。

    参数：
        student_nos: 学生编号列表
    """
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
    """
    条件搜索就业信息。

    支持的条件：
        - student_no: 学生编号（精确匹配）
        - company_name: 公司名称（模糊匹配）
        - min_salary / max_salary: 薪资范围
        - employment_status: 就业状态
        - position: 岗位（模糊匹配）
        - work_location: 工作地点（模糊匹配）

    返回值：
        包含学生姓名和班级编号的 EmploymentSearchResponse 列表
    """
    re = (
        db.query(Employment, Student.name, Student.class_no)
        .join(Student, Employment.student_no == Student.student_no)
        .filter(Student.isdeleted == 0)
    )

    # 逐个条件判断，如果有值就加上过滤条件
    if query.student_no:
        re = re.filter(Employment.student_no == query.student_no)

    if query.company_name:
        re = re.filter(Employment.company_name.like(f'%{query.company_name}%'))

    if query.min_salary is not None:
        re = re.filter(Employment.salary >= query.min_salary)

    if query.max_salary is not None:
        re = re.filter(Employment.salary <= query.max_salary)

    if query.employment_status:
        re = re.filter(Employment.employment_status == query.employment_status)

    if query.position:
        re = re.filter(Employment.position.like(f'%{query.position}%'))

    if query.work_location:
        re = re.filter(Employment.work_location.like(f'%{query.work_location}%'))

    # 只返回未删除的记录
    results = re.filter(Employment.isdeleted == 0).all()

    # 把查询结果转成 Pydantic 模型列表
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
            isdeleted=emp.isdeleted,
        )
        for emp, student_name, class_no in results
    ]
