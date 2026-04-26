from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import CurrentUser, get_current_user, require_role
from app.schemas.teacher import (
    CourseCreate,
    CourseRead,
    CourseUpdate,
    TeacherCreate,
    TeacherRead,
    TeacherUpdate,
)
from app.services import teacher as teacher_service

router = APIRouter(tags=['教师与课程管理'])


@router.get('/api/teachers', response_model=list[TeacherRead])
def get_teachers(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """查询老师列表。"""
    return teacher_service.list_teachers(db)


@router.post('/api/teachers', response_model=TeacherRead, status_code=status.HTTP_201_CREATED)
def create_teacher(
    data: TeacherCreate,
    current_user: CurrentUser = Depends(require_role(['admin'])),
    db: Session = Depends(get_db),
):
    """创建老师信息。"""
    return teacher_service.create_teacher(db, data)


@router.put('/api/teachers/{teacher_id}', response_model=TeacherRead)
def update_teacher(
    teacher_id: int,
    data: TeacherUpdate,
    current_user: CurrentUser = Depends(require_role(['admin'])),
    db: Session = Depends(get_db),
):
    """更新老师信息。"""
    return teacher_service.update_teacher(db, teacher_id, data)


@router.delete('/api/teachers/{teacher_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher(
    teacher_id: int,
    current_user: CurrentUser = Depends(require_role(['admin'])),
    db: Session = Depends(get_db),
):
    """逻辑删除老师。"""
    teacher_service.delete_teacher(db, teacher_id)
    return None


@router.get('/api/courses', response_model=list[CourseRead])
def get_courses(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """查询课程列表。"""
    return teacher_service.list_courses(db)


@router.post('/api/courses', response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(
    data: CourseCreate,
    current_user: CurrentUser = Depends(require_role(['admin'])),
    db: Session = Depends(get_db),
):
    """创建课程。"""
    return teacher_service.create_course(db, data)


@router.put('/api/courses/{course_id}', response_model=CourseRead)
def update_course(
    course_id: int,
    data: CourseUpdate,
    current_user: CurrentUser = Depends(require_role(['admin'])),
    db: Session = Depends(get_db),
):
    """更新课程信息。"""
    return teacher_service.update_course(db, course_id, data)


@router.delete('/api/courses/{course_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int,
    current_user: CurrentUser = Depends(require_role(['admin'])),
    db: Session = Depends(get_db),
):
    """删除课程。"""
    teacher_service.delete_course(db, course_id)
    return None


@router.get('/api/teachers/{teacher_id}/courses', response_model=list[CourseRead])
def get_teacher_courses(
    teacher_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """查询指定老师所授课程。"""
    return teacher_service.get_courses_by_teacher(db, teacher_id)
