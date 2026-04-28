# ============================================================
# services/teacher.py —— 教师业务逻辑
# ============================================================
# 这个文件负责处理"教师"相关的具体业务操作。
#
# 包含的功能：
#   - 查询单个教师、查询所有教师
#   - 新增教师（支持恢复已删除的记录）
#   - 更新教师信息
#   - 批量删除教师（逻辑删除）
#   - 按姓名和性别搜索教师
#   - 性别统计
# ============================================================

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate, TeacherUpdate


def get_teacher_by_no(db: Session, teacher_no: str) -> Teacher:
    """
    根据教师编号查询单个教师。

    如果教师不存在，抛出 404 错误。
    """
    teacher = db.query(Teacher).filter(Teacher.teacher_no == teacher_no).first()
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='教师不存在',
        )
    return teacher


def list_teachers(db: Session) -> list[Teacher]:
    """
    查询所有未删除的教师。
    """
    return db.query(Teacher).filter(Teacher.isdeleted == 0).all()


def create_teacher(db: Session, data: TeacherCreate) -> Teacher:
    """
    新增教师。

    逻辑：
        1. 检查教师编号是否已存在
        2. 如果存在且未删除 → 报错（编号冲突）
        3. 如果存在但已删除 → 恢复并更新信息
        4. 如果不存在 → 新建记录
    """
    existing = (
        db.query(Teacher)
        .filter(Teacher.teacher_no == data.teacher_no)
        .first()
    )

    if existing:
        # 如果教师已存在且未删除，报错
        if existing.isdeleted == 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='教师编号已存在',
            )

        # 如果教师已存在但已删除，恢复并更新
        existing.isdeleted = 0
        existing.name = data.name
        existing.gender = data.gender
        existing.phone = data.phone
        existing.email = data.email
        existing.id_card = data.id_card
        existing.birthday = data.birthday
        existing.hire_date = data.hire_date
        existing.subject = data.subject
        db.commit()
        db.refresh(existing)
        return existing

    # 新建教师记录
    teacher = Teacher(**data.model_dump())
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher


def update_teacher(db: Session, teacher_no: str, data: TeacherUpdate) -> Teacher:
    """
    更新教师信息。

    只更新前端传过来的字段。
    """
    teacher = get_teacher_by_no(db, teacher_no)
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(teacher, field, value)

    db.commit()
    db.refresh(teacher)
    return teacher


def delete_teachers(db: Session, teacher_nos: list[str]) -> list[Teacher]:
    """
    批量删除教师（逻辑删除）。

    参数：
        teacher_nos: 要删除的教师编号列表
    """
    teachers = (
        db.query(Teacher)
        .filter(Teacher.teacher_no.in_(teacher_nos), Teacher.isdeleted == 0)
        .all()
    )
    if not teachers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='未找到可删除的教师',
        )

    for teacher in teachers:
        teacher.isdeleted = 1
    db.commit()

    for teacher in teachers:
        db.refresh(teacher)
    return teachers


def search_teachers(db: Session, name: str | None = None, gender: str | None = None) -> list[Teacher]:
    """
    搜索教师。

    支持的条件：
        - name: 姓名模糊查询
        - gender: 性别精确匹配
    """
    query = db.query(Teacher).filter(Teacher.isdeleted == 0)

    if name:
        # like 是模糊查询，% 表示任意字符
        query = query.filter(Teacher.name.like(f'%{name}%'))

    if gender:
        query = query.filter(Teacher.gender == gender)

    return query.all()


def gender_stats(db: Session) -> list[dict]:
    """
    统计教师的性别分布。

    返回值：
        包含性别、数量、占比的字典列表
    """
    results = (
        db.query(Teacher.gender, func.count(Teacher.teacher_no).label('count'))
        .filter(Teacher.isdeleted == 0)
        .group_by(Teacher.gender)
        .all()
    )

    total = sum(r.count for r in results)

    return [
        {
            'gender': r.gender,
            'count': r.count,
            # round(..., 4) 保留 4 位小数
            'ratio': round(r.count / total, 4) if total else 0.0,
        }
        for r in results
    ]
