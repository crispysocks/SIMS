from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import require_role
from app.schemas.classes import ClassCreate, ClassRead, ClassReadDetail, ClassUpdate
from app.services import classes as class_service

router = APIRouter(
    prefix='/classes',
    tags=['班级管理模块'],
)


@router.get('', response_model=list[ClassRead], summary='获取班级列表')
def list_classes(db: Session = Depends(get_db)) -> list[ClassRead]:
    return class_service.list_classes(db)


@router.post(
    '',
    response_model=ClassRead,
    status_code=status.HTTP_201_CREATED,
    summary='创建班级',
    dependencies=[Depends(require_role(['admin']))],
)
def create_class(data: ClassCreate, db: Session = Depends(get_db)) -> ClassRead:
    return class_service.create_class(db, data)


@router.get('/{class_no}', response_model=ClassReadDetail, summary='获取班级详情')
def get_class(class_no: str, db: Session = Depends(get_db)) -> ClassReadDetail:
    return class_service.get_class_by_no(db, class_no)


@router.put('/{class_no}', response_model=ClassRead, summary='更新班级信息', dependencies=[Depends(require_role(['admin']))])
def update_class(
    class_no: str,
    data: ClassUpdate,
    db: Session = Depends(get_db),
) -> ClassRead:
    return class_service.update_class(db, class_no, data)


@router.delete('/{class_no}', response_model=ClassRead, summary='删除班级', dependencies=[Depends(require_role(['admin']))])
def delete_class(class_no: str, db: Session = Depends(get_db)) -> ClassRead:
    return class_service.delete_class(db, class_no)
