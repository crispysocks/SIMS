# ============================================================
# services/classes.py —— 班级业务逻辑
# ============================================================
# 这个文件负责处理"班级"相关的具体业务操作。
#
# 什么是业务逻辑？
#   就是"做某件事的步骤"。
#   比如新增一个班级，需要：
#     1. 检查班级编号是否已存在
#     2. 如果存在但已删除，就恢复并更新
#     3. 如果不存在，就新建一条记录
#
# 为什么不把这些代码直接写在 api/classes.py 里？
#   - 接口层只负责"接收请求、返回响应"
#   - 业务逻辑层负责"具体怎么做"
#   - 这样分开后，业务逻辑可以在多个地方复用
# ============================================================

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.classes import ClassInfo
from app.schemas.classes import ClassCreate, ClassUpdate


# ---------- 1. 获取班级列表（支持分页和模糊查询） ----------
def get_class_list(db: Session, skip: int, limit: int, class_name: str | None = None):
    """
    获取班级列表。

    参数：
        db: 数据库会话
        skip: 跳过多少条记录（分页用）
        limit: 返回多少条记录（分页用）
        class_name: 班级名称关键字（模糊查询用，可选）

    返回值：
        (班级列表, 总数量)
    """
    # 先查询所有未删除的班级
    query = db.query(ClassInfo).filter(ClassInfo.isdeleted == 0)

    # 如果传了 class_name，就加上模糊查询条件
    # contains 表示"包含"，如查询"Python"会匹配"Python基础班"
    if class_name:
        query = query.filter(ClassInfo.class_name.contains(class_name))

    # count() 查询总数量（不受分页影响）
    total = query.count()

    # offset + limit 实现分页
    # 比如 skip=0, limit=10 表示取前 10 条
    classes = query.offset(skip).limit(limit).all()

    return classes, total


# ---------- 2. 新增班级 ----------
def create_class(db: Session, data: ClassCreate) -> ClassInfo:
    """
    新增一个班级。

    逻辑：
        1. 检查班级编号是否已存在
        2. 如果存在且未删除 → 报错（编号冲突）
        3. 如果存在但已删除 → 恢复并更新信息
        4. 如果不存在 → 新建记录
    """
    existing = (
        db.query(ClassInfo)
        .filter(ClassInfo.class_no == data.class_no)
        .first()
    )

    if existing:
        # 如果班级已存在且未删除，报错
        if existing.isdeleted == 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='班级编号已存在',
            )

        # 如果班级已存在但已删除，恢复它并更新信息
        existing.isdeleted = 0
        existing.class_name = data.class_name
        existing.class_open_time = data.class_open_time
        existing.head_teacher_no = data.head_teacher_no
        existing.instructor_no = data.instructor_no
        existing.description = data.description
        db.commit()
        db.refresh(existing)
        return existing

    # 新建班级记录
    # **data.model_dump() 把 Pydantic 模型转成字典，再传给 SQLAlchemy 模型
    class_info = ClassInfo(**data.model_dump())
    db.add(class_info)
    db.commit()
    db.refresh(class_info)
    return class_info


# ---------- 3. 修改班级 ----------
def update_class(db: Session, class_no: str, data: ClassUpdate) -> ClassInfo:
    """
    更新班级信息。

    参数：
        db: 数据库会话
        class_no: 要更新的班级编号
        data: 新的班级信息（只传要修改的字段）
    """
    # 查询未删除的班级
    cls = db.query(ClassInfo).filter(
        ClassInfo.class_no == class_no,
        ClassInfo.isdeleted == 0
    ).first()

    if not cls:
        raise HTTPException(status_code=404, detail='班级不存在')

    # exclude_unset=True 表示只获取前端传过来的字段
    # 这样前端没传的字段就不会被覆盖
    update_data = data.model_dump(exclude_unset=True)

    # 逐个字段更新
    for key, value in update_data.items():
        setattr(cls, key, value)

    db.commit()
    db.refresh(cls)

    return cls


# ---------- 4. 删除班级（逻辑删除） ----------
def delete_class(db: Session, class_no: str):
    """
    删除班级（逻辑删除）。

    逻辑删除只是把 isdeleted 标记为 1，数据还在数据库里。
    """
    cls = db.query(ClassInfo).filter(
        ClassInfo.class_no == class_no,
        ClassInfo.isdeleted == 0
    ).first()

    if not cls:
        raise HTTPException(status_code=404, detail='班级不存在')

    cls.isdeleted = 1
    db.commit()


# ---------- 5. 获取所有班级名称 ----------
def get_class_names(db: Session):
    """
    获取所有未删除班级的名称列表。

    返回值：
        ['Python基础班', 'Java进阶班', ...]
    """
    classes = db.query(ClassInfo).filter(ClassInfo.isdeleted == 0).all()
    return [cls.class_name for cls in classes]


# ---------- 6. 统计班级总数 ----------
def get_class_total_count(db: Session):
    """
    统计未删除的班级总数。
    """
    return db.query(ClassInfo).filter(ClassInfo.isdeleted == 0).count()


# ---------- 7. 根据编号查询单个班级 ----------
def get_class_by_id(db: Session, class_no: str):
    """
    根据班级编号查询单个班级信息。

    返回值：
        班级对象，如果不存在返回 None
    """
    return db.query(ClassInfo).filter(
        ClassInfo.class_no == class_no,
        ClassInfo.isdeleted == 0
    ).first()
