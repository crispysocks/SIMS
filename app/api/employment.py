from decimal import Decimal

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import require_role
from app.schemas.employment import (
    AvgSalaryByGroup,
    EmploymentCreate,
    EmploymentRead,
    EmploymentUpdate,
)
from app.schemas.response import ApiResponse
from app.services import employment as employment_service

router = APIRouter(
    prefix='/employment',
    tags=['就业管理v1'],
)


@router.get('/students/{student_no}')
def get_student_employment(
    student_no: str,
    db: Session = Depends(get_db),
) -> ApiResponse[EmploymentRead]:
    """查询单个学生的就业信息。"""
    result = employment_service.get_employment_by_student(db, student_no)
    return ApiResponse(message='查询成功', data=result)


@router.get('/class/{class_no}')
def get_class_employment(
    class_no: str,
    db: Session = Depends(get_db),
) -> ApiResponse[list[EmploymentRead]]:
    """查询班级学生的就业信息。"""
    data = employment_service.get_employment_by_class(db, class_no)
    return ApiResponse(message='查询成功', data=data)


@router.post('/students/{student_no}', dependencies=[Depends(require_role(['admin', 'teacher']))])
def create_student_employment(
    student_no: str,
    data: EmploymentCreate,
    db: Session = Depends(get_db),
) -> ApiResponse[EmploymentRead]:
    """新增学生就业信息。"""
    result = employment_service.create_employment(db, student_no, data)
    return ApiResponse(message='添加成功', data=result)


@router.put('/students/{student_no}', dependencies=[Depends(require_role(['admin', 'teacher']))])
def update_student_employment(
    student_no: str,
    data: EmploymentUpdate,
    db: Session = Depends(get_db),
) -> ApiResponse[EmploymentRead]:
    """更新学生就业信息。"""
    result = employment_service.update_employment(db, student_no, data)
    return ApiResponse(message='更新成功', data=result)


@router.delete('/students/{student_no}', dependencies=[Depends(require_role(['admin']))])
def delete_student_employment(
    student_no: str,
    db: Session = Depends(get_db),
) -> ApiResponse[None]:
    """逻辑删除学生就业信息。"""
    employment_service.delete_employment(db, student_no)
    return ApiResponse(message='删除成功', data=None)


@router.get('/salary')
def get_employment_by_min_salary(
    min_salary: Decimal = Query(..., ge=0, description='最低薪资'),
    db: Session = Depends(get_db),
) -> ApiResponse[list[EmploymentRead]]:
    """查询薪资大于等于指定值的就业记录。"""
    data = employment_service.get_employment_by_min_salary(db, min_salary)
    return ApiResponse(message='查询成功', data=data)


@router.get('/avg-salary')
def get_avg_salary(
    group_by: str | None = Query(default=None, description='分组维度：class-班级，gender-性别'),
    db: Session = Depends(get_db),
) -> ApiResponse[list[AvgSalaryByGroup]]:
    """查询就业成员平均工资，支持按班级或性别分组。"""
    data = employment_service.get_avg_salary_by_group(db, group_by)
    return ApiResponse(message='查询成功', data=data)


@router.get('/status/{status}')
def get_employment_by_status(
    status: int,
    db: Session = Depends(get_db),
) -> ApiResponse[list[EmploymentRead]]:
    """按状态查询就业记录，1=正常，0=已删除。"""
    data = employment_service.get_employment_by_status(db, status)
    return ApiResponse(message='查询成功', data=data)
