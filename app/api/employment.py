from decimal import Decimal

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import CurrentUser, get_current_user, require_role
from app.schemas.employment import (
    AvgSalaryByGroup,
    EmploymentCreate,
    EmploymentRead,
    EmploymentUpdate,
)
from app.services import employment as employment_service

router = APIRouter(prefix='/employment', tags=['就业管理v1'])


@router.get('/students/{student_no}', response_model=EmploymentRead)
def get_student_employment(
    student_no: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """查询单个学生的就业信息。"""
    return employment_service.get_employment_by_student(db, student_no)


@router.get('/class/{class_no}', response_model=list[EmploymentRead])
def get_class_employment(
    class_no: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """查询班级学生的就业信息。"""
    return employment_service.get_employment_by_class(db, class_no)


@router.post('/students/{student_no}', response_model=EmploymentRead)
def create_student_employment(
    student_no: str,
    data: EmploymentCreate,
    current_user: CurrentUser = Depends(require_role(['admin', 'teacher'])),
    db: Session = Depends(get_db),
):
    """新增学生就业信息。"""
    return employment_service.create_employment(db, student_no, data)


@router.put('/students/{student_no}', response_model=EmploymentRead)
def update_student_employment(
    student_no: str,
    data: EmploymentUpdate,
    current_user: CurrentUser = Depends(require_role(['admin', 'teacher'])),
    db: Session = Depends(get_db),
):
    """更新学生就业信息。"""
    return employment_service.update_employment(db, student_no, data)


@router.delete('/students/{student_no}', status_code=status.HTTP_204_NO_CONTENT)
def delete_student_employment(
    student_no: str,
    current_user: CurrentUser = Depends(require_role(['admin'])),
    db: Session = Depends(get_db),
):
    """逻辑删除学生就业信息。"""
    employment_service.delete_employment(db, student_no)
    return None


@router.get('/salary', response_model=list[EmploymentRead])
def get_employment_by_min_salary(
    min_salary: Decimal = Query(..., ge=0, description='最低薪资'),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """查询薪资大于等于指定值的就业记录。"""
    return employment_service.get_employment_by_min_salary(db, min_salary)


@router.get('/avg-salary', response_model=list[AvgSalaryByGroup])
def get_avg_salary(
    group_by: str | None = Query(default=None, description='分组维度：class-班级，gender-性别'),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """查询就业成员平均工资，支持按班级或性别分组。"""
    return employment_service.get_avg_salary_by_group(db, group_by)


@router.get('/status/{status}', response_model=list[EmploymentRead])
def get_employment_by_status(
    status: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """按状态查询就业记录，1=正常，0=已删除。"""
    return employment_service.get_employment_by_status(db, status)
