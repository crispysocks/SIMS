from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import require_role
from app.schemas.employment_v2 import (
    EmploymentCreate,
    EmploymentOut,
    EmploymentUpdate,
    EmploymentQuery,
    EmploymentSearchResponse,
)
from app.schemas.response import ApiResponse
from app.services import employment_v2 as employment_service

router = APIRouter(
    prefix='/employment',
    tags=['就业管理v2'],
)


@router.post('', summary='添加就业信息', dependencies=[Depends(require_role(['admin', 'teacher']))])
def add_employment(
    data: EmploymentCreate,
    db: Session = Depends(get_db),
) -> ApiResponse[EmploymentOut]:
    """添加就业信息"""
    result = employment_service.add_stu_test(db, data)
    if not result:
        raise HTTPException(status_code=400, detail='添加失败，学生不存在或就业信息已存在')
    return ApiResponse(message='添加成功', data=EmploymentOut.model_validate(result))


@router.get('/class/{class_no}', summary='获取班级就业信息列表')
def get_employment_by_class(
    class_no: str,
    db: Session = Depends(get_db),
) -> ApiResponse[list[EmploymentOut]]:
    """根据班级编号获取就业信息列表"""
    result = employment_service.find_list_emp(db, class_no)
    if isinstance(result, dict) and 'message' in result:
        return ApiResponse(message=result['message'], data=[])
    return ApiResponse(message='查询成功', data=[EmploymentOut.model_validate(item) for item in result])


@router.delete('', summary='软删除就业信息', dependencies=[Depends(require_role(['admin']))])
def delete_employment(
    student_nos: List[str],
    db: Session = Depends(get_db),
) -> ApiResponse[None]:
    result = employment_service.del_emp(db, student_nos)
    if isinstance(result, dict) and 'message' in result:
        return ApiResponse(message=result['message'], data=None)
    return ApiResponse(message='删除成功', data=None)


@router.put('/restore', summary='批量恢复就业信息', dependencies=[Depends(require_role(['admin']))])
def restore_employment(
    student_nos: List[str],
    db: Session = Depends(get_db),
) -> ApiResponse[None]:
    result = employment_service.del_emp_back(db, student_nos)
    if isinstance(result, dict) and 'message' in result:
        return ApiResponse(message=result['message'], data=None)
    return ApiResponse(message='恢复成功', data=None)


@router.post('/search', summary='条件搜索就业信息')
def search_employment(
    query: EmploymentQuery,
    db: Session = Depends(get_db),
) -> ApiResponse[List[EmploymentSearchResponse]]:
    result = employment_service.search_emp_list(db, query)
    return ApiResponse(message='查询成功', data=result)


@router.put('/{student_no}', summary='更新就业信息', dependencies=[Depends(require_role(['admin', 'teacher']))])
def update_employment(
    student_no: str,
    data: EmploymentUpdate,
    db: Session = Depends(get_db),
) -> ApiResponse[EmploymentOut]:
    """更新就业信息"""
    result = employment_service.update_stu_test(db, student_no, data)
    if not result:
        raise HTTPException(status_code=400, detail='更新失败，就业信息不存在')
    return ApiResponse(message='更新成功', data=EmploymentOut.model_validate(result))


@router.get('/{student_no}', summary='获取学生就业信息')
def get_employment_by_student(
    student_no: str,
    db: Session = Depends(get_db),
) -> ApiResponse[EmploymentOut]:
    """根据学生编号获取就业信息"""
    result = employment_service.find_emp(db, student_no)
    if result is None:
        raise HTTPException(status_code=404, detail='未找到该学生就业记录')
    return ApiResponse(message='查询成功', data=EmploymentOut.model_validate(result))
