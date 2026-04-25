from fastapi import FastAPI,Depends
import uvicorn
from sqlalchemy.orm import Session
from Myproject.first_project.core import config as teachers_db
from Myproject.first_project.schemas.teacher_info import TeacherCreate,TeacherUpdate,CourseCreate,CourseUpdate
from Myproject.first_project.Services import teacher_services
app = FastAPI(description='老师信息及任课信息的管理')


def get_db():
    db = teachers_db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#获取所有老师
@app.get("/teachers/", tags=["老师管理"])
async def get_teachers(db: Session = Depends(get_db)):
    # 创建TeacherService实例（关键更新）
    service = teacher_services.TeacherService(db)
    # 通过services层获取数据（关键更新）
    teachers = teacher_services.get_all_teachers()
    return teachers


## 4.2 创建老师
@app.post("/teachers/", tags=["老师管理"])
async def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    # 通过services层处理创建逻辑（关键更新）
    service = teacher_services.TeacherService(db)
    return service.create_teacher(teacher.dict())


## 4.3 获取单个老师
@app.get("/teachers/{teacher_id}", tags=["老师管理"])
async def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    # 通过services层获取数据（关键更新）
    service = teacher_services.TeacherService(db)
    return service.get_teacher(teacher_id)

# 4.4 更新老师
@app.put("/teachers/{teacher_id}", tags=["老师管理"])
async def update_teacher(teacher_id: int, teacher: TeacherUpdate, db: Session = Depends(get_db)):
    service = teacher_services.TeacherService(db)
    return service.update_teacher(teacher_id, teacher.dict(exclude_unset=True))

## 4.5 删除老师
@app.delete("/teachers/{teacher_id}", tags=["老师管理"])
async def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    service = teacher_services.TeacherService(db)
    return service.delete_teacher(teacher_id)

# 5. 课程模块CRUD
## 5.1 获取所有课程
@app.get("/courses/", tags=["课程管理"])
async def get_courses(db: Session = Depends(get_db)):
    service = teacher_services.CourseService(db)
    courses = teacher_services.get_all_courses()
    return courses

## 5.2 创建课程
@app.post("/courses/", tags=["课程管理"])
async def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    service = teacher_services.CourseService(db)
    return service.create_course(course.dict())

## 5.3 获取单个课程
@app.get("/courses/{course_id}", tags=["课程管理"])
async def get_course(course_id: int, db: Session = Depends(get_db)):
    service = teacher_services.CourseService(db)
    return service.get_course(course_id)

## 5.4 更新课程
@app.put("/courses/{course_id}", tags=["课程管理"])
async def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    service = teacher_services.CourseService(db)
    return service.update_course(course_id, course.dict(exclude_unset=True))

## 5.5 删除课程
@app.delete("/courses/{course_id}", tags=["课程管理"])
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    service = teacher_services.CourseService(db)
    return service.delete_course(course_id)

## 5.6 获取指定老师的课程
@app.get("/teachers/{teacher_id}/courses", tags=["课程管理"])
async def get_teacher_courses(teacher_id: int, db: Session = Depends(get_db)):
    service = teacher_services.CourseService(db)
    return service.get_courses_by_teacher(teacher_id)


if __name__ == "__main__":
    uvicorn.run('teacher_api:app', host="127.0.0.1", port=8080)