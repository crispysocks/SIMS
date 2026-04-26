from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.classes import ClassInfo
from app.schemas.classes import ClassCreate, ClassRead, ClassUpdate


def list_classes(db: Session, class_name: str | None = None) -> list[ClassRead]:
    """查询班级列表，并支持按班级名称模糊筛选。"""
    query = db.query(ClassInfo).filter(ClassInfo.is_deleted == 0)
    if class_name:
        query = query.filter(ClassInfo.class_name.contains(class_name))
    return [ClassRead.model_validate(item) for item in query.order_by(ClassInfo.class_id).all()]


def get_class_or_404(db: Session, class_id: int) -> ClassInfo:
    """按主键查询班级，不存在时抛出异常。"""
    class_info = db.query(ClassInfo).filter(
        ClassInfo.class_id == class_id,
        ClassInfo.is_deleted == 0,
    ).first()
    if not class_info:
        raise HTTPException(status_code=404, detail='班级不存在')
    return class_info


def create_class(db: Session, data: ClassCreate) -> ClassRead:
    """创建新的班级信息。"""
    existing = db.query(ClassInfo).filter(
        ClassInfo.class_name == data.class_name,
        ClassInfo.is_deleted == 0,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail='班级名称已存在')
    class_info = ClassInfo(**data.model_dump())
    db.add(class_info)
    db.commit()
    db.refresh(class_info)
    return ClassRead.model_validate(class_info)


def update_class(db: Session, class_id: int, data: ClassUpdate) -> ClassRead:
    """更新指定班级信息。"""
    class_info = get_class_or_404(db, class_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(class_info, key, value)
    db.commit()
    db.refresh(class_info)
    return ClassRead.model_validate(class_info)


def delete_class(db: Session, class_id: int) -> None:
    """对指定班级执行逻辑删除。"""
    class_info = get_class_or_404(db, class_id)
    class_info.is_deleted = 1
    db.commit()
