from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import CurrentUser, get_current_user, require_role
from app.schemas.employment import EmploymentRead, EmploymentUpsert
from app.services import employment as employment_service

router = APIRouter(prefix='/api/employment', tags=['就业管理'])


@router.get('/students/{student_id}', response_model=EmploymentRead)
def get_student_employment(
    student_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """查询单个学生的就业信息。"""
    return employment_service.get_employment_by_student(db, student_id)


@router.get('/class/{class_id}', response_model=list[EmploymentRead])
def get_class_employment(
    class_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """查询班级学生的就业信息。"""
    return employment_service.get_employment_by_class(db, class_id)


@router.post('/students/{student_id}', response_model=EmploymentRead)
def upsert_student_employment(
    student_id: int,
    data: EmploymentUpsert,
    current_user: CurrentUser = Depends(require_role(['admin', 'teacher'])),
    db: Session = Depends(get_db),
):
    """新增或更新学生就业信息。"""
    return employment_service.upsert_employment(db, student_id, data)


@router.delete('/students/{student_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_student_employment(
    student_id: int,
    current_user: CurrentUser = Depends(require_role(['admin'])),
    db: Session = Depends(get_db),
):
    """逻辑删除学生就业信息。"""
    employment_service.delete_employment(db, student_id)
    return None
