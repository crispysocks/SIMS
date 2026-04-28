# ============================================================
# classes.py —— 班级管理接口模块
# ============================================================
# 这个文件提供班级相关的所有接口，包括：
#   1. 查询班级列表（支持分页和模糊搜索）
#   2. 新增班级
#   3. 修改班级信息
#   4. 删除班级
#   5. 获取所有班级名称（给下拉框用）
#   6. 统计班级总数
#   7. 查询单个班级详情
#
# 注意：接口的顺序很重要！
#   固定路径（如 /names、/count）要放在动态路径（如 /{class_no}）前面，
#   否则 FastAPI 会把 /names 当成 class_no="names" 来匹配。
# ============================================================

# Optional 表示一个类型可以是某种类型，也可以是 None（空）
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import require_role
from app.schemas.classes import ClassCreate, ClassRead, ClassUpdate
from app.schemas.response import ApiResponse
# 导入班级相关的业务逻辑函数，接口只负责"接请求"和"返回结果"，具体做事交给 service
from app.services import classes as class_service

# 创建路由，所有以 /classes 开头的请求都归这里处理
router = APIRouter(
    prefix='/classes',
    tags=['班级管理模块'],
)


# ============================================================
# 1. 分页查询班级列表（支持模糊搜索）
# ============================================================

@router.get('', summary='分页查询班级')
def get_class_list(
    skip: int = Query(0),           # 跳过多少条，从第几条开始查
    limit: int = Query(10),         # 最多返回多少条
    class_name: Optional[str] = None,  # 可选的班级名称模糊搜索关键字
    db: Session = Depends(get_db),
):
    """
    分页查询班级列表，支持按班级名称模糊搜索。

    访问地址：GET /classes?skip=0&limit=10&class_name=一班

    参数：
        skip: 跳过前面多少条记录（用于翻页）
        limit: 这一页最多显示多少条
        class_name: 班级名称关键字，不传就查全部
        db: 数据库连接

    返回值：
        { classes: 班级列表, total: 总数量 }
    """
    # 调用 service 层的函数去查数据库
    classes, total = class_service.get_class_list(db, skip, limit, class_name)

    # 把数据库模型转换成前端需要的格式（Pydantic 模型）
    # model_validate 是 Pydantic v2 的方法，用来把 ORM 对象转成字典-like 的对象
    data = [ClassRead.model_validate(c) for c in classes]

    return ApiResponse(message='成功', data={'classes': data, 'total': total})


# ============================================================
# 2. 新增班级
# ============================================================

@router.post('', summary='新增班级')
def create_class(
    data: ClassCreate,
    db: Session = Depends(get_db),
):
    """
    新增一个班级。

    访问地址：POST /classes
    状态码 201 表示"创建成功"。

    参数：
        data: 班级信息，包含班级编号、名称等
        db: 数据库连接

    返回值：
        新增成功的班级信息
    """
    cls = class_service.create_class(db, data)
    return ApiResponse(message='新增成功', data=ClassRead.model_validate(cls))


# ============================================================
# 3. 修改班级
# ============================================================

@router.put('/{class_no}', summary='修改班级')
def update_class(
    class_no: str,          # URL 路径里的参数，比如 /classes/C001
    data: ClassUpdate,
    db: Session = Depends(get_db),
):
    """
    修改指定班级的信息。

    访问地址：PUT /classes/{class_no}
    例子：PUT /classes/C001

    参数：
        class_no: 班级编号，从网址路径里获取
        data: 要修改的字段（不需要传全部字段，只传要改的）
        db: 数据库连接

    返回值：
        修改后的班级信息
    """
    cls = class_service.update_class(db, class_no, data)
    return ApiResponse(message='修改成功', data=ClassRead.model_validate(cls))


# ============================================================
# 4. 删除班级
# ============================================================

@router.delete('/{class_no}', summary='删除班级')
def delete_class(
    class_no: str,
    db: Session = Depends(get_db),
):
    """
    删除指定班级。

    访问地址：DELETE /classes/{class_no}

    参数：
        class_no: 班级编号
        db: 数据库连接

    返回值：
        删除成功的提示
    """
    class_service.delete_class(db, class_no)
    return ApiResponse(message='删除成功')


# ============================================================
# 5. 获取所有班级名称（固定路径，必须放在 /{class_no} 前面）
# ============================================================

@router.get('/names', summary='只获取所有班级名称')
def get_class_names(
    db: Session = Depends(get_db),
):
    """
    获取所有班级的名称列表。

    访问地址：GET /classes/names

    用途：
        前端下拉框需要显示所有班级名称时调用，数据量小，速度快。

    返回值：
        { names: ['一班', '二班', '三班'] }
    """
    name_list = class_service.get_class_names(db)
    return ApiResponse(message='获取班级名称成功', data={'names': name_list})


# ============================================================
# 6. 统计班级总数（固定路径，必须放在 /{class_no} 前面）
# ============================================================

@router.get('/count', summary='统计班级总数')
def get_class_count(
    db: Session = Depends(get_db),
):
    """
    统计系统中一共有多少个班级。

    访问地址：GET /classes/count

    返回值：
        { total: 10 }
    """
    total = class_service.get_class_total_count(db)
    return ApiResponse(message='成功', data={'total': total})


# ============================================================
# 7. 查询单个班级详情（动态路径，放最后）
# ============================================================

@router.get('/{class_no}', summary='根据编号查询单个班级')
def get_class_by_id(
    class_no: str,
    db: Session = Depends(get_db),
):
    """
    根据班级编号查询单个班级的详细信息。

    访问地址：GET /classes/{class_no}
    例子：GET /classes/C001

    参数：
        class_no: 班级编号
        db: 数据库连接

    返回值：
        班级详细信息，如果找不到返回 404
    """
    cls = class_service.get_class_by_id(db, class_no)
    if not cls:
        return ApiResponse(code=404, message='班级不存在', data=None)
    return ApiResponse(message='查询成功', data=ClassRead.model_validate(cls))
