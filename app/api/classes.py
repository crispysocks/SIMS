from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import require_role
from app.schemas.classes import ClassCreate, ClassRead, ClassReadDetail, ClassUpdate
from app.schemas.response import ApiResponse
from app.services import classes as class_service

router = APIRouter(
    prefix='/classes',
    tags=['班级管理模块'],
)


@router.get('', summary='获取班级列表')
def list_classes(db: Session = Depends(get_db)) -> ApiResponse[list[ClassRead]]:
    data = class_service.list_classes(db)
    return ApiResponse(message='查询成功', data=data)


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    summary='创建班级',
    dependencies=[Depends(require_role(['admin']))],
)
def create_class(data: ClassCreate, db: Session = Depends(get_db)) -> ApiResponse[ClassRead]:
    result = class_service.create_class(db, data)
    return ApiResponse(message='创建成功', data=result)


@router.get('/{class_no}', summary='获取班级详情')
def get_class(class_no: str, db: Session = Depends(get_db)) -> ApiResponse[ClassReadDetail]:
    result = class_service.get_class_by_no(db, class_no)
    return ApiResponse(message='查询成功', data=result)


@router.put('/{class_no}', summary='更新班级信息', dependencies=[Depends(require_role(['admin']))])
def update_class(
    class_no: str,
    data: ClassUpdate,
    db: Session = Depends(get_db),
) -> ApiResponse[ClassRead]:
    result = class_service.update_class(db, class_no, data)
    return ApiResponse(message='更新成功', data=result)


@router.delete('/{class_no}', summary='删除班级', dependencies=[Depends(require_role(['admin']))])
def delete_class(class_no: str, db: Session = Depends(get_db)) -> ApiResponse[ClassRead]:
    result = class_service.delete_class(db, class_no)
    return ApiResponse(message='删除成功', data=result)
