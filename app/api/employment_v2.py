# ============================================================
# employment_v2.py —— 就业管理 v2 接口模块
# ============================================================
# 这是就业管理的第二个版本接口，功能比 v1 更完善，包括：
#   1. 添加就业信息
#   2. 获取班级就业信息列表
#   3. 软删除就业信息（批量）
#   4. 批量恢复已删除的就业信息
#   5. 条件搜索就业信息
#   6. 更新就业信息
#   7. 获取单个学生的就业信息
#
# v2 和 v1 的区别：
#   - v2 支持批量操作（删除、恢复）
#   - v2 支持更灵活的条件搜索
#   - v2 的返回格式更统一
# ============================================================

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import require_role
from app.schemas.employment_v2 import (
    EmploymentCreate,
    EmploymentOut,
    EmploymentUpdate,
    EmploymentQuery,
    EmploymentSearchResponse,
)
from app.schemas.response import ApiResponse
from app.services import employment_v2 as employment_service

# 创建路由，所有以 /employment 开头的请求都归这里处理
# 注意：v1 和 v2 共用 /employment 前缀，但具体路径不同
router = APIRouter(
    prefix='/employment',
    tags=['就业管理v2'],
)


# ============================================================
# 1. 添加就业信息
# ============================================================

@router.post('', summary='添加就业信息', dependencies=[Depends(require_role(['admin', 'teacher']))])
def add_employment(
    data: EmploymentCreate,
    db: Session = Depends(get_db),
) -> ApiResponse[EmploymentOut]:
    """
    添加一条学生就业信息。

    访问地址：POST /employment
    权限：仅管理员或老师可操作

    参数：
        data: 就业信息，包含学生编号、公司、职位、薪资等
        db: 数据库连接

    返回值：
        添加成功的就业信息

    可能的错误：
        - 400：学生不存在，或该学生已有就业信息
    """
    result = employment_service.add_stu_test(db, data)
    if not result:
        raise HTTPException(status_code=400, detail='添加失败，学生不存在或就业信息已存在')
    return ApiResponse(message='添加成功', data=EmploymentOut.model_validate(result))


# ============================================================
# 2. 获取班级就业信息列表
# ============================================================

@router.get('/class/{class_no}', summary='获取班级就业信息列表')
def get_employment_by_class(
    class_no: str,
    db: Session = Depends(get_db),
) -> ApiResponse[list[EmploymentOut]]:
    """
    根据班级编号获取该班所有学生的就业信息。

    访问地址：GET /employment/class/{class_no}
    例子：GET /employment/class/C001

    参数：
        class_no: 班级编号
        db: 数据库连接

    返回值：
        该班级所有学生的就业信息列表
    """
    result = employment_service.find_list_emp(db, class_no)
    # 如果 service 返回的是错误消息字典，就包装成空列表返回
    if isinstance(result, dict) and 'message' in result:
        return ApiResponse(message=result['message'], data=[])
    return ApiResponse(message='查询成功', data=[EmploymentOut.model_validate(item) for item in result])


# ============================================================
# 3. 软删除就业信息（批量）
# ============================================================

@router.delete('', summary='软删除就业信息', dependencies=[Depends(require_role(['admin']))])
def delete_employment(
    student_nos: List[str],
    db: Session = Depends(get_db),
) -> ApiResponse[None]:
    """
    批量软删除学生的就业信息。

    访问地址：DELETE /employment
    权限：仅管理员可操作
    请求体：['S001', 'S002', 'S003']

    参数：
        student_nos: 学生编号列表，可以同时删除多个
        db: 数据库连接

    返回值：
        删除成功的提示
    """
    result = employment_service.del_emp(db, student_nos)
    if isinstance(result, dict) and 'message' in result:
        return ApiResponse(message=result['message'], data=None)
    return ApiResponse(message='删除成功', data=None)


# ============================================================
# 4. 批量恢复就业信息
# ============================================================

@router.put('/restore', summary='批量恢复就业信息', dependencies=[Depends(require_role(['admin']))])
def restore_employment(
    student_nos: List[str],
    db: Session = Depends(get_db),
) -> ApiResponse[None]:
    """
    批量恢复已软删除的就业信息。

    访问地址：PUT /employment/restore
    权限：仅管理员可操作
    请求体：['S001', 'S002']

    参数：
        student_nos: 要恢复的学生编号列表
        db: 数据库连接

    返回值：
        恢复成功的提示
    """
    result = employment_service.del_emp_back(db, student_nos)
    if isinstance(result, dict) and 'message' in result:
        return ApiResponse(message=result['message'], data=None)
    return ApiResponse(message='恢复成功', data=None)


# ============================================================
# 5. 条件搜索就业信息
# ============================================================

@router.post('/search', summary='条件搜索就业信息')
def search_employment(
    query: EmploymentQuery,
    db: Session = Depends(get_db),
) -> ApiResponse[List[EmploymentSearchResponse]]:
    """
    根据多种条件组合搜索就业信息。

    访问地址：POST /employment/search

    参数：
        query: 查询条件，可以包含：
            - 学生姓名（模糊匹配）
            - 班级编号
            - 公司名称（模糊匹配）
            - 薪资范围（最低、最高）
            - 就业状态
        db: 数据库连接

    返回值：
        符合条件的就业信息列表
    """
    result = employment_service.search_emp_list(db, query)
    return ApiResponse(message='查询成功', data=result)


# ============================================================
# 6. 更新就业信息
# ============================================================

@router.put('/{student_no}', summary='更新就业信息', dependencies=[Depends(require_role(['admin', 'teacher']))])
def update_employment(
    student_no: str,
    data: EmploymentUpdate,
    db: Session = Depends(get_db),
) -> ApiResponse[EmploymentOut]:
    """
    更新指定学生的就业信息。

    访问地址：PUT /employment/{student_no}
    例子：PUT /employment/S001
    权限：仅管理员或老师可操作

    参数：
        student_no: 学生编号
        data: 要更新的字段
        db: 数据库连接

    返回值：
        更新后的就业信息

    可能的错误：
        - 400：该学生的就业信息不存在
    """
    result = employment_service.update_stu_test(db, student_no, data)
    if not result:
        raise HTTPException(status_code=400, detail='更新失败，就业信息不存在')
    return ApiResponse(message='更新成功', data=EmploymentOut.model_validate(result))


# ============================================================
# 7. 获取单个学生就业信息
# ============================================================

@router.get('/{student_no}', summary='获取学生就业信息')
def get_employment_by_student(
    student_no: str,
    db: Session = Depends(get_db),
) -> ApiResponse[EmploymentOut]:
    """
    根据学生编号获取其就业信息。

    访问地址：GET /employment/{student_no}
    例子：GET /employment/S001

    参数：
        student_no: 学生编号
        db: 数据库连接

    返回值：
        该学生的就业详细信息

    可能的错误：
        - 404：未找到该学生的就业记录
    """
    result = employment_service.find_emp(db, student_no)
    if result is None:
        raise HTTPException(status_code=404, detail='未找到该学生就业记录')
    return ApiResponse(message='查询成功', data=EmploymentOut.model_validate(result))
