from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import require_role
from app.schemas.classes import ClassCreate, ClassRead, ClassUpdate
from app.schemas.response import ApiResponse
from app.services import classes as class_service

router = APIRouter(
    prefix='/classes',
    tags=['班级管理模块'],
)


# 1 分页+模糊查询 班级信息
@router.get('', summary='分页查询班级')
def get_class_list(
    skip: int = Query(0),
    limit: int = Query(10),
    class_name: Optional[str] = None,
    db: Session = Depends(get_db),
):
    classes, total = class_service.get_class_list(db, skip, limit, class_name)
    data = [ClassRead.model_validate(c) for c in classes]
    return ApiResponse(message='成功', data={'classes': data, 'total': total})


# 2 新增班级
@router.post('', summary='新增班级', status_code=status.HTTP_201_CREATED)
def create_class(
    data: ClassCreate,
    db: Session = Depends(get_db),
):
    cls = class_service.create_class(db, data)
    return ApiResponse(message='新增成功', data=ClassRead.model_validate(cls))


# 3 修改班级
@router.put('/{class_no}', summary='修改班级')
def update_class(
    class_no: str,
    data: ClassUpdate,
    db: Session = Depends(get_db),
):
    cls = class_service.update_class(db, class_no, data)
    return ApiResponse(message='修改成功', data=ClassRead.model_validate(cls))


# 4 删除班级
@router.delete('/{class_no}', summary='删除班级')
def delete_class(
    class_no: str,
    db: Session = Depends(get_db),
):
    class_service.delete_class(db, class_no)
    return ApiResponse(message='删除成功')


# 5 获取所有班级名称（固定路径，必须放在 /{class_no} 前面）
@router.get('/names', summary='只获取所有班级名称')
def get_class_names(
    db: Session = Depends(get_db),
):
    name_list = class_service.get_class_names(db)
    return ApiResponse(message='获取班级名称成功', data={'names': name_list})


# 6 统计班级总数（固定路径，必须放在 /{class_no} 前面）
@router.get('/count', summary='统计班级总数')
def get_class_count(
    db: Session = Depends(get_db),
):
    total = class_service.get_class_total_count(db)
    return ApiResponse(message='成功', data={'total': total})


# 7 根据班级编号查询单个班级详情（动态路径，放最后）
@router.get('/{class_no}', summary='根据编号查询单个班级')
def get_class_by_id(
    class_no: str,
    db: Session = Depends(get_db),
):
    cls = class_service.get_class_by_id(db, class_no)
    if not cls:
        return ApiResponse(code=404, message='班级不存在', data=None)
    return ApiResponse(message='查询成功', data=ClassRead.model_validate(cls))
