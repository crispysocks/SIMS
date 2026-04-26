from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.classes import ClassInfo
from app.schemas.classes import ClassCreate, ClassUpdate


def get_class_by_no(db: Session, class_no: str) -> ClassInfo:
    class_info = (
        db.query(ClassInfo)
        .filter(ClassInfo.class_no == class_no, ClassInfo.isdeleted == 0)
        .first()
    )
    if not class_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='班级不存在',
        )
    return class_info


def list_classes(db: Session) -> list[ClassInfo]:
    return db.query(ClassInfo).filter(ClassInfo.isdeleted == 0).all()


def create_class(db: Session, data: ClassCreate) -> ClassInfo:
    existing = (
        db.query(ClassInfo)
        .filter(ClassInfo.class_no == data.class_no)
        .first()
    )

    if existing:
        if existing.isdeleted == 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='班级编号已存在',
            )

        existing.isdeleted = 0
        existing.class_name = data.class_name
        existing.class_open_time = data.class_open_time
        existing.head_teacher_no = data.head_teacher_no
        existing.instructor_no = data.instructor_no
        existing.description = data.description
        db.commit()
        db.refresh(existing)
        return existing

    class_info = ClassInfo(**data.model_dump())
    db.add(class_info)
    db.commit()
    db.refresh(class_info)
    return class_info


def update_class(db: Session, class_no: str, data: ClassUpdate) -> ClassInfo:
    class_info = get_class_by_no(db, class_no)
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(class_info, field, value)
    db.commit()
    db.refresh(class_info)
    return class_info


def delete_class(db: Session, class_no: str) -> ClassInfo:
    class_info = get_class_by_no(db, class_no)
    class_info.isdeleted = 1
    db.commit()
    db.refresh(class_info)
    return class_info
