from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.teacher import TeacherCreate, TeacherRead, TeacherUpdate
from app.services import teacher as teacher_service

router = APIRouter(prefix='/teachers', tags=['教师管理模块'])


@router.get('', response_model=list[TeacherRead], summary='获取教师列表')
def list_teachers(db: Session = Depends(get_db)) -> list[TeacherRead]:
    return teacher_service.list_teachers(db)


@router.post(
    '',
    response_model=TeacherRead,
    status_code=status.HTTP_201_CREATED,
    summary='创建教师',
)
def create_teacher(data: TeacherCreate, db: Session = Depends(get_db)) -> TeacherRead:
    return teacher_service.create_teacher(db, data)


@router.get('/{teacher_no}', response_model=TeacherRead, summary='获取教师详情')
def get_teacher(teacher_no: str, db: Session = Depends(get_db)) -> TeacherRead:
    return teacher_service.get_teacher_by_no(db, teacher_no)


@router.put('/{teacher_no}', response_model=TeacherRead, summary='更新教师信息')
def update_teacher(
    teacher_no: str,
    data: TeacherUpdate,
    db: Session = Depends(get_db),
) -> TeacherRead:
    return teacher_service.update_teacher(db, teacher_no, data)


@router.delete('/{teacher_no}', response_model=TeacherRead, summary='删除教师')
def delete_teacher(teacher_no: str, db: Session = Depends(get_db)) -> TeacherRead:
    return teacher_service.delete_teacher(db, teacher_no)
