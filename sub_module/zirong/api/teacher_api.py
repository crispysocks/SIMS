from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.teacher import TeacherCreate, TeacherUpdate, CourseCreate, CourseUpdate
from app.schemas.common import APIResponse
from app.services.teacher_service import TeacherService
from app.services.course_service import CourseService
from app.services.avatar_service import AvatarService

router = APIRouter(prefix="/api", tags=["老师及课程管理"])

# ========== 老师接口 ==========
@router.get("/teachers/", response_model=APIResponse[list])
async def get_teachers(db: Session = Depends(get_db)):
    service = TeacherService(db)
    return service.get_all_teachers()

@router.post("/teachers/", response_model=APIResponse[dict], status_code=201)
async def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    service = TeacherService(db)
    return service.create_teacher(teacher.model_dump())

@router.get("/teachers/{teacher_id}", response_model=APIResponse[dict])
async def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    service = TeacherService(db)
    return service.get_teacher(teacher_id)

@router.put("/teachers/{teacher_id}", response_model=APIResponse[dict])
async def update_teacher(teacher_id: int, teacher: TeacherUpdate, db: Session = Depends(get_db)):
    service = TeacherService(db)
    return service.update_teacher(teacher_id, teacher.model_dump(exclude_unset=True))

@router.delete("/teachers/{teacher_id}", response_model=APIResponse[None])
async def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    service = TeacherService(db)
    return service.delete_teacher(teacher_id)

# ========== 课程接口 ==========
@router.get("/courses/", response_model=APIResponse[list])
async def get_courses(db: Session = Depends(get_db)):
    service = CourseService(db)
    return service.get_all_courses()

@router.post("/courses/", response_model=APIResponse[dict], status_code=201)
async def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    service = CourseService(db)
    return service.create_course(course.model_dump())

@router.get("/courses/{course_id}", response_model=APIResponse[dict])
async def get_course(course_id: int, db: Session = Depends(get_db)):
    service = CourseService(db)
    return service.get_course(course_id)

@router.put("/courses/{course_id}", response_model=APIResponse[dict])
async def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    service = CourseService(db)
    return service.update_course(course_id, course.model_dump(exclude_unset=True))

@router.delete("/courses/{course_id}", response_model=APIResponse[None])
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    service = CourseService(db)
    return service.delete_course(course_id)

@router.get("/teachers/{teacher_id}/courses", response_model=APIResponse[list])
async def get_teacher_courses(teacher_id: int, db: Session = Depends(get_db)):
    service = CourseService(db)
    return service.get_courses_by_teacher(teacher_id)

# ========== 头像接口 ==========
@router.post("/teachers/{teacher_id}/avatar", response_model=APIResponse[dict])
async def upload_avatar(teacher_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    service = AvatarService(db)
    return service.upload_avatar(teacher_id, file)

@router.get("/teachers/{teacher_id}/avatar", response_model=APIResponse[dict])
async def get_avatar(teacher_id: int, db: Session = Depends(get_db)):
    service = AvatarService(db)
    return service.get_avatar_path(teacher_id)

@router.delete("/teachers/{teacher_id}/avatar", response_model=APIResponse[None])
async def remove_avatar(teacher_id: int, db: Session = Depends(get_db)):
    service = AvatarService(db)
    return service.delete_avatar(teacher_id)