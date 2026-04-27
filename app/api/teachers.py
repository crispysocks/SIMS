from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import require_role
from app.schemas.teacher import TeacherCreate, TeacherRead, TeacherUpdate
from app.schemas.response import ApiResponse
from app.services import teacher as teacher_service

router = APIRouter(
    prefix='/teachers',
    tags=['教师管理模块'],
)


@router.get('', summary='获取教师列表')
def list_teachers(db: Session = Depends(get_db)) -> ApiResponse[list[TeacherRead]]:
    data = teacher_service.list_teachers(db)
    return ApiResponse(message='查询成功', data=data)


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    summary='创建教师',
    dependencies=[Depends(require_role(['admin']))],
)
def create_teacher(data: TeacherCreate, db: Session = Depends(get_db)) -> ApiResponse[TeacherRead]:
    result = teacher_service.create_teacher(db, data)
    return ApiResponse(message='创建成功', data=result)


@router.get('/{teacher_no}', summary='获取教师详情')
def get_teacher(teacher_no: str, db: Session = Depends(get_db)) -> ApiResponse[TeacherRead]:
    result = teacher_service.get_teacher_by_no(db, teacher_no)
    return ApiResponse(message='查询成功', data=result)


@router.put('/{teacher_no}', summary='更新教师信息', dependencies=[Depends(require_role(['admin']))])
def update_teacher(
    teacher_no: str,
    data: TeacherUpdate,
    db: Session = Depends(get_db),
) -> ApiResponse[TeacherRead]:
    result = teacher_service.update_teacher(db, teacher_no, data)
    return ApiResponse(message='更新成功', data=result)


@router.delete('/{teacher_no}', summary='删除教师', dependencies=[Depends(require_role(['admin']))])
def delete_teacher(teacher_no: str, db: Session = Depends(get_db)) -> ApiResponse[TeacherRead]:
    result = teacher_service.delete_teacher(db, teacher_no)
    return ApiResponse(message='删除成功', data=result)
