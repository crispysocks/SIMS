from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import CurrentUser, get_current_user, require_role
from app.schemas.classes import ClassCreate, ClassRead, ClassUpdate
from app.services import classes as class_service

router = APIRouter(prefix='/api/classes', tags=['班级管理'])


@router.get('/', response_model=list[ClassRead])
def get_classes(
    class_name: str | None = Query(default=None),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """查询班级列表。"""
    return class_service.list_classes(db, class_name)


@router.post('/', response_model=ClassRead, status_code=status.HTTP_201_CREATED)
def create_class(
    data: ClassCreate,
    current_user: CurrentUser = Depends(require_role(['admin', 'teacher'])),
    db: Session = Depends(get_db),
):
    """创建新的班级。"""
    return class_service.create_class(db, data)


@router.put('/{class_id}', response_model=ClassRead)
def update_class(
    class_id: int,
    data: ClassUpdate,
    current_user: CurrentUser = Depends(require_role(['admin', 'teacher'])),
    db: Session = Depends(get_db),
):
    """更新指定班级信息。"""
    return class_service.update_class(db, class_id, data)


@router.delete('/{class_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_class(
    class_id: int,
    current_user: CurrentUser = Depends(require_role(['admin'])),
    db: Session = Depends(get_db),
):
    """逻辑删除指定班级。"""
    class_service.delete_class(db, class_id)
    return None
