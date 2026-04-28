# ============================================================
# teachers.py —— 教师管理接口模块
# ============================================================
# 这个文件提供教师信息的增删改查接口，包括：
#   1. 获取所有教师列表
#   2. 创建教师
#   3. 获取单个教师详情
#   4. 更新教师信息
#   5. 批量删除教师
#   6. 按姓名或性别搜索教师
#   7. 按性别统计教师数量及比例
#
# 教师模块的权限控制：
#   - 查询：任何人都可以
#   - 创建、更新、删除：仅 admin
# ============================================================

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import require_role
from app.schemas.teacher import TeacherCreate, TeacherRead, TeacherUpdate, TeacherGenderStat
from app.schemas.response import ApiResponse
from app.services import teacher as teacher_service

# 创建路由，所有以 /teachers 开头的请求都归这里处理
router = APIRouter(
    prefix='/teachers',
    tags=['教师管理模块'],
)


# ============================================================
# 1. 获取所有教师列表
# ============================================================

@router.get('', summary='获取教师列表')
def list_teachers(db: Session = Depends(get_db)) -> ApiResponse[list[TeacherRead]]:
    """
    获取系统中所有教师的列表。

    访问地址：GET /teachers

    参数：
        db: 数据库连接

    返回值：
        所有教师的信息列表
    """
    data = teacher_service.list_teachers(db)
    return ApiResponse(message='查询成功', data=data)


# ============================================================
# 2. 创建教师
# ============================================================

@router.post(
    '',
    summary='创建教师',
    dependencies=[Depends(require_role(['admin']))],
)
def create_teacher(data: TeacherCreate, db: Session = Depends(get_db)) -> ApiResponse[TeacherRead]:
    """
    新增一名教师。

    访问地址：POST /teachers
    状态码 201 表示"创建成功"
    权限：仅管理员可操作

    参数：
        data: 教师信息，包含教师编号、姓名、性别、联系方式等
        db: 数据库连接

    返回值：
        创建成功的教师信息
    """
    result = teacher_service.create_teacher(db, data)
    return ApiResponse(message='创建成功', data=result)


# ============================================================
# 3. 获取单个教师详情
# ============================================================

@router.get('/{teacher_no}', summary='获取教师详情')
def get_teacher(teacher_no: str, db: Session = Depends(get_db)) -> ApiResponse[TeacherRead]:
    """
    根据教师编号查询详细信息。

    访问地址：GET /teachers/{teacher_no}
    例子：GET /teachers/T001

    参数：
        teacher_no: 教师编号
        db: 数据库连接

    返回值：
        该教师的详细信息
    """
    result = teacher_service.get_teacher_by_no(db, teacher_no)
    return ApiResponse(message='查询成功', data=result)


# ============================================================
# 4. 更新教师信息
# ============================================================

@router.put('/{teacher_no}', summary='更新教师信息', dependencies=[Depends(require_role(['admin']))])
def update_teacher(
    teacher_no: str,
    data: TeacherUpdate,
    db: Session = Depends(get_db),
) -> ApiResponse[TeacherRead]:
    """
    修改指定教师的信息。

    访问地址：PUT /teachers/{teacher_no}
    例子：PUT /teachers/T001
    权限：仅管理员可操作

    参数：
        teacher_no: 教师编号
        data: 要更新的字段
        db: 数据库连接

    返回值：
        更新后的教师信息
    """
    result = teacher_service.update_teacher(db, teacher_no, data)
    return ApiResponse(message='更新成功', data=result)


# ============================================================
# 5. 批量删除教师
# ============================================================

@router.delete('', summary='批量删除教师', dependencies=[Depends(require_role(['admin']))])
def delete_teachers(teacher_nos: list[str], db: Session = Depends(get_db)) -> ApiResponse[list[TeacherRead]]:
    """
    批量删除教师。

    访问地址：DELETE /teachers
    权限：仅管理员可操作
    请求体：['T001', 'T002']

    参数：
        teacher_nos: 教师编号列表
        db: 数据库连接

    返回值：
        被删除的教师信息列表
    """
    result = teacher_service.delete_teachers(db, teacher_nos)
    return ApiResponse(message='删除成功', data=result)


# ============================================================
# 6. 按姓名或性别搜索教师
# ============================================================

@router.get('/search/by-name-or-gender', summary='按姓名或性别搜索教师')
def search_teachers(
    name: str | None = None,
    gender: str | None = None,
    db: Session = Depends(get_db),
) -> ApiResponse[list[TeacherRead]]:
    """
    根据姓名或性别搜索教师。

    访问地址：GET /teachers/search/by-name-or-gender?name=王&gender=男

    参数：
        name: 姓名关键字（可选，模糊匹配）
        gender: 性别（可选，如'男'、'女'）
        db: 数据库连接

    返回值：
        符合条件的教师列表
    """
    data = teacher_service.search_teachers(db, name=name, gender=gender)
    return ApiResponse(message='查询成功', data=data)


# ============================================================
# 7. 按性别统计教师数量及比例
# ============================================================

@router.get('/stats/gender', summary='按性别统计教师数量及比例')
def gender_stats(db: Session = Depends(get_db)) -> ApiResponse[list[TeacherGenderStat]]:
    """
    统计各性别的教师数量及占比。

    访问地址：GET /teachers/stats/gender

    参数：
        db: 数据库连接

    返回值：
        各性别的数量和比例，比如：
        [{ 'gender': '男', 'count': 10, 'percentage': 66.7 }]
    """
    data = teacher_service.gender_stats(db)
    return ApiResponse(message='查询成功', data=data)
