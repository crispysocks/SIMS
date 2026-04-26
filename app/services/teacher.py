from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.teacher import Course, Teacher
from app.schemas.teacher import (
    CourseCreate,
    CourseRead,
    CourseUpdate,
    TeacherCreate,
    TeacherRead,
    TeacherUpdate,
)


def list_teachers(db: Session) -> list[TeacherRead]:
    """查询所有在职老师。"""
    items = db.query(Teacher).filter(Teacher.status == 1).order_by(Teacher.id).all()
    return [TeacherRead.model_validate(item) for item in items]


def get_teacher_or_404(db: Session, teacher_id: int) -> Teacher:
    """按主键查询老师，不存在时抛出异常。"""
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id, Teacher.status == 1).first()
    if not teacher:
        raise HTTPException(status_code=404, detail='老师不存在')
    return teacher


def create_teacher(db: Session, data: TeacherCreate) -> TeacherRead:
    """创建新的老师信息。"""
    teacher = Teacher(**data.model_dump())
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return TeacherRead.model_validate(teacher)


def update_teacher(db: Session, teacher_id: int, data: TeacherUpdate) -> TeacherRead:
    """更新指定老师的信息。"""
    teacher = get_teacher_or_404(db, teacher_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(teacher, key, value)
    db.commit()
    db.refresh(teacher)
    return TeacherRead.model_validate(teacher)


def delete_teacher(db: Session, teacher_id: int) -> None:
    """对指定老师执行逻辑删除，并校验课程关联。"""
    teacher = get_teacher_or_404(db, teacher_id)
    has_course = db.query(Course).filter(Course.teacher_id == teacher_id).first()
    if has_course:
        raise HTTPException(status_code=400, detail='该老师仍有关联课程，无法删除')
    teacher.status = 0
    db.commit()


def list_courses(db: Session) -> list[CourseRead]:
    """查询所有课程，并附带老师姓名。"""
    result = []
    for course in db.query(Course).order_by(Course.id).all():
        teacher = db.query(Teacher).filter(Teacher.id == course.teacher_id).first()
        result.append(
            CourseRead(
                id=course.id,
                course_name=course.course_name,
                teacher_id=course.teacher_id,
                teacher_name=teacher.name if teacher else None,
            )
        )
    return result


def get_course_or_404(db: Session, course_id: int) -> Course:
    """按主键查询课程，不存在时抛出异常。"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail='课程不存在')
    return course


def create_course(db: Session, data: CourseCreate) -> CourseRead:
    """创建课程并校验授课老师是否存在。"""
    teacher = get_teacher_or_404(db, data.teacher_id)
    course = Course(**data.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return CourseRead(
        id=course.id,
        course_name=course.course_name,
        teacher_id=course.teacher_id,
        teacher_name=teacher.name,
    )


def update_course(db: Session, course_id: int, data: CourseUpdate) -> CourseRead:
    """更新指定课程的信息。"""
    course = get_course_or_404(db, course_id)
    payload = data.model_dump(exclude_unset=True)
    if 'teacher_id' in payload:
        get_teacher_or_404(db, payload['teacher_id'])
    for key, value in payload.items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    teacher = db.query(Teacher).filter(Teacher.id == course.teacher_id).first()
    return CourseRead(
        id=course.id,
        course_name=course.course_name,
        teacher_id=course.teacher_id,
        teacher_name=teacher.name if teacher else None,
    )


def delete_course(db: Session, course_id: int) -> None:
    """删除指定课程。"""
    course = get_course_or_404(db, course_id)
    db.delete(course)
    db.commit()


def get_courses_by_teacher(db: Session, teacher_id: int) -> list[CourseRead]:
    """查询指定老师所授课程。"""
    teacher = get_teacher_or_404(db, teacher_id)
    items = db.query(Course).filter(Course.teacher_id == teacher_id).order_by(Course.id).all()
    return [
        CourseRead(
            id=item.id,
            course_name=item.course_name,
            teacher_id=item.teacher_id,
            teacher_name=teacher.name,
        )
        for item in items
    ]
