from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentRead, StudentUpdate


def list_students(
    db: Session,
    page: int,
    page_size: int,
    keyword: str | None = None,
    class_id: int | None = None,
) -> dict:
    """分页查询学生列表，并支持关键字和班级筛选。"""
    query = db.query(Student).filter(Student.status == 1)
    if keyword:
        query = query.filter(
            (Student.name.contains(keyword)) | (Student.student_no.contains(keyword))
        )
    if class_id is not None:
        query = query.filter(Student.class_id == class_id)
    total = query.count()
    items = query.order_by(Student.id).offset((page - 1) * page_size).limit(page_size).all()
    return {
        'total': total,
        'items': [StudentRead.model_validate(item) for item in items],
        'page': page,
        'page_size': page_size,
    }


def get_student_or_404(db: Session, student_id: int) -> Student:
    """按主键查询学生，不存在时抛出异常。"""
    student = db.query(Student).filter(Student.id == student_id, Student.status == 1).first()
    if not student:
        raise HTTPException(status_code=404, detail='学生不存在')
    return student


def create_student(db: Session, data: StudentCreate) -> StudentRead:
    """创建新的学生记录，必要时恢复已逻辑删除的数据。"""
    try:
        existing = db.query(Student).filter(Student.student_no == data.student_no).first()
        if existing and existing.status == 1:
            raise HTTPException(status_code=400, detail='学生编号已存在')
        if existing and existing.status == 0:
            for key, value in data.model_dump().items():
                setattr(existing, key, value)
            existing.status = 1
            db.commit()
            db.refresh(existing)
            return StudentRead.model_validate(existing)
        student = Student(**data.model_dump())
        db.add(student)
        db.commit()
        db.refresh(student)
        return StudentRead.model_validate(student)
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail='数据库操作失败')


def update_student(db: Session, student_id: int, data: StudentUpdate) -> StudentRead:
    """更新指定学生信息。"""
    try:
        student = get_student_or_404(db, student_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(student, key, value)
        db.commit()
        db.refresh(student)
        return StudentRead.model_validate(student)
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail='数据库操作失败')


def delete_student(db: Session, student_id: int) -> None:
    """对指定学生执行逻辑删除。"""
    student = get_student_or_404(db, student_id)
    student.status = 0
    db.commit()


def restore_students(db: Session, student_ids: list[int]) -> dict:
    """批量恢复已逻辑删除的学生。"""
    restored = 0
    for student_id in student_ids:
        student = db.query(Student).filter(Student.id == student_id).first()
        if student and student.status == 0:
            student.status = 1
            restored += 1
    db.commit()
    return {'restored': restored}
