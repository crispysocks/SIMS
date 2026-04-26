from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import CurrentUser, get_current_user, require_role
from app.schemas.student import StudentCreate, StudentListResponse, StudentRead, StudentUpdate
from app.services import student as student_service

router = APIRouter(prefix='/api/students', tags=['学生管理'])


@router.get('/', response_model=StudentListResponse)
def get_students(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str | None = Query(default=None),
    class_id: int | None = Query(default=None),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """分页查询学生列表。"""
    return student_service.list_students(db, page, page_size, keyword, class_id)


@router.get('/{student_id}', response_model=StudentRead)
def get_student(
    student_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """查询单个学生详情。"""
    return StudentRead.model_validate(student_service.get_student_or_404(db, student_id))


@router.post('/', response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(
    data: StudentCreate,
    current_user: CurrentUser = Depends(require_role(['admin', 'teacher'])),
    db: Session = Depends(get_db),
):
    """创建新的学生记录。"""
    return student_service.create_student(db, data)


@router.put('/{student_id}', response_model=StudentRead)
def update_student(
    student_id: int,
    data: StudentUpdate,
    current_user: CurrentUser = Depends(require_role(['admin', 'teacher'])),
    db: Session = Depends(get_db),
):
    """更新指定学生信息。"""
    return student_service.update_student(db, student_id, data)


@router.delete('/{student_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: int,
    current_user: CurrentUser = Depends(require_role(['admin'])),
    db: Session = Depends(get_db),
):
    """逻辑删除指定学生。"""
    student_service.delete_student(db, student_id)
    return None


@router.post('/restore')
def restore_students(
    student_ids: list[int],
    current_user: CurrentUser = Depends(require_role(['admin'])),
    db: Session = Depends(get_db),
):
    """批量恢复被删除的学生。"""
    return student_service.restore_students(db, student_ids)
