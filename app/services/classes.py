from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.classes import ClassInfo
from app.schemas.classes import ClassCreate, ClassUpdate


# 1.分页 + 模糊查询  获取班级列表
def get_class_list(db: Session, skip: int, limit: int, class_name: str | None = None):
    query = db.query(ClassInfo).filter(ClassInfo.isdeleted == 0)

    if class_name:
        query = query.filter(ClassInfo.class_name.contains(class_name))

    total = query.count()
    classes = query.offset(skip).limit(limit).all()

    return classes, total


# 2.新增班级
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


# 3.修改班级
def update_class(db: Session, class_no: str, data: ClassUpdate) -> ClassInfo:
    cls = db.query(ClassInfo).filter(
        ClassInfo.class_no == class_no,
        ClassInfo.isdeleted == 0
    ).first()

    if not cls:
        raise HTTPException(status_code=404, detail='班级不存在')

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(cls, key, value)

    db.commit()
    db.refresh(cls)

    return cls


# 4.删除班级（逻辑删除）
def delete_class(db: Session, class_no: str):
    cls = db.query(ClassInfo).filter(
        ClassInfo.class_no == class_no,
        ClassInfo.isdeleted == 0
    ).first()

    if not cls:
        raise HTTPException(status_code=404, detail='班级不存在')

    cls.isdeleted = 1
    db.commit()


# 5.获取所有班级名称
def get_class_names(db: Session):
    classes = db.query(ClassInfo).filter(ClassInfo.isdeleted == 0).all()
    return [cls.class_name for cls in classes]


# 6.统计一共有多少班级
def get_class_total_count(db: Session):
    return db.query(ClassInfo).filter(ClassInfo.isdeleted == 0).count()


# 7.根据编号查单个班级
def get_class_by_id(db: Session, class_no: str):
    return db.query(ClassInfo).filter(
        ClassInfo.class_no == class_no,
        ClassInfo.isdeleted == 0
    ).first()
