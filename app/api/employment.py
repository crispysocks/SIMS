# ============================================================
# employment.py —— 就业管理 v1 接口模块
# ============================================================
# 这个文件提供就业信息的查询和管理接口，包括：
#   1. 查询单个学生的就业信息
#   2. 查询整个班级的就业信息
#   3. 新增、更新、删除学生就业信息
#   4. 按最低薪资筛选就业记录
#   5. 按班级或性别统计平均工资
#   6. 按状态查询就业记录
#
# 注意：删除是"逻辑删除"（软删除），不是真的从数据库删掉，
#       只是把状态标记为删除，方便以后恢复。
# ============================================================

# Decimal 是 Python 里用来精确表示小数的类型，适合处理金额（避免浮点数精度问题）
from decimal import Decimal

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import require_role
from app.schemas.employment import (
    AvgSalaryByGroup,
    EmploymentCreate,
    EmploymentRead,
    EmploymentUpdate,
)
from app.schemas.response import ApiResponse
from app.services import employment as employment_service

# 创建路由，所有以 /employment 开头的请求都归这里处理
router = APIRouter(
    prefix='/employment',
    tags=['就业管理v1'],
)


# ============================================================
# 查询单个学生的就业信息
# ============================================================

@router.get('/students/{student_no}')
def get_student_employment(
    student_no: str,
    db: Session = Depends(get_db),
) -> ApiResponse[EmploymentRead]:
    """
    查询单个学生的就业信息。

    访问地址：GET /employment/students/{student_no}
    例子：GET /employment/students/S001

    参数：
        student_no: 学生编号
        db: 数据库连接

    返回值：
        该学生的就业详细信息
    """
    result = employment_service.get_employment_by_student(db, student_no)
    return ApiResponse(message='查询成功', data=result)


# ============================================================
# 查询班级的就业信息
# ============================================================

@router.get('/class/{class_no}')
def get_class_employment(
    class_no: str,
    db: Session = Depends(get_db),
) -> ApiResponse[list[EmploymentRead]]:
    """
    查询某个班级所有学生的就业信息。

    访问地址：GET /employment/class/{class_no}
    例子：GET /employment/class/C001

    参数：
        class_no: 班级编号
        db: 数据库连接

    返回值：
        该班级所有学生的就业信息列表
    """
    data = employment_service.get_employment_by_class(db, class_no)
    return ApiResponse(message='查询成功', data=data)


# ============================================================
# 新增学生就业信息（需要 admin 或 teacher 权限）
# ============================================================

@router.post('/students/{student_no}', dependencies=[Depends(require_role(['admin', 'teacher']))])
def create_student_employment(
    student_no: str,
    data: EmploymentCreate,
    db: Session = Depends(get_db),
) -> ApiResponse[EmploymentRead]:
    """
    为指定学生新增就业信息。

    访问地址：POST /employment/students/{student_no}
    权限：仅管理员（admin）或老师（teacher）可操作

    参数：
        student_no: 学生编号
        data: 就业信息，包含公司、职位、薪资等
        db: 数据库连接

    返回值：
        新增成功的就业信息
    """
    result = employment_service.create_employment(db, student_no, data)
    return ApiResponse(message='添加成功', data=result)


# ============================================================
# 更新学生就业信息（需要 admin 或 teacher 权限）
# ============================================================

@router.put('/students/{student_no}', dependencies=[Depends(require_role(['admin', 'teacher']))])
def update_student_employment(
    student_no: str,
    data: EmploymentUpdate,
    db: Session = Depends(get_db),
) -> ApiResponse[EmploymentRead]:
    """
    更新指定学生的就业信息。

    访问地址：PUT /employment/students/{student_no}
    权限：仅管理员或老师可操作

    参数：
        student_no: 学生编号
        data: 要更新的就业信息字段
        db: 数据库连接

    返回值：
        更新后的就业信息
    """
    result = employment_service.update_employment(db, student_no, data)
    return ApiResponse(message='更新成功', data=result)


# ============================================================
# 删除学生就业信息（逻辑删除，需要 admin 权限）
# ============================================================

@router.delete('/students/{student_no}', dependencies=[Depends(require_role(['admin']))])
def delete_student_employment(
    student_no: str,
    db: Session = Depends(get_db),
) -> ApiResponse[None]:
    """
    删除指定学生的就业信息（逻辑删除）。

    访问地址：DELETE /employment/students/{student_no}
    权限：仅管理员可操作

    什么是逻辑删除？
        不是真的从数据库删掉，而是把状态标记为"已删除"，
        这样以后还能恢复，也能保留历史记录。

    参数：
        student_no: 学生编号
        db: 数据库连接

    返回值：
        删除成功的提示
    """
    employment_service.delete_employment(db, student_no)
    return ApiResponse(message='删除成功', data=None)


# ============================================================
# 按最低薪资筛选就业记录
# ============================================================

@router.get('/salary')
def get_employment_by_min_salary(
    min_salary: Decimal = Query(..., ge=0, description='最低薪资'),
    db: Session = Depends(get_db),
) -> ApiResponse[list[EmploymentRead]]:
    """
    查询薪资大于等于指定值的就业记录。

    访问地址：GET /employment/salary?min_salary=5000

    参数：
        min_salary: 最低薪资门槛，必须大于等于 0
        db: 数据库连接

    返回值：
        满足条件的就业记录列表
    """
    data = employment_service.get_employment_by_min_salary(db, min_salary)
    return ApiResponse(message='查询成功', data=data)


# ============================================================
# 按班级或性别统计平均工资
# ============================================================

@router.get('/avg-salary')
def get_avg_salary(
    group_by: str | None = Query(default=None, description='分组维度：class-班级，gender-性别'),
    db: Session = Depends(get_db),
) -> ApiResponse[list[AvgSalaryByGroup]]:
    """
    查询就业学生的平均工资，支持按不同维度分组统计。

    访问地址：GET /employment/avg-salary?group_by=class

    参数：
        group_by: 分组方式
            - 'class'：按班级分组，看每个班的平均薪资
            - 'gender'：按性别分组，看男女平均薪资对比
            - 不传：统计所有人的平均薪资
        db: 数据库连接

    返回值：
        分组统计结果列表
    """
    data = employment_service.get_avg_salary_by_group(db, group_by)
    return ApiResponse(message='查询成功', data=data)


# ============================================================
# 按状态查询就业记录
# ============================================================

@router.get('/status/{status}')
def get_employment_by_status(
    status: int,
    db: Session = Depends(get_db),
) -> ApiResponse[list[EmploymentRead]]:
    """
    按状态查询就业记录。

    访问地址：GET /employment/status/{status}
    例子：GET /employment/status/1

    参数：
        status: 状态码
            - 1：正常（未删除）
            - 0：已逻辑删除
        db: 数据库连接

    返回值：
        对应状态的就业记录列表
    """
    data = employment_service.get_employment_by_status(db, status)
    return ApiResponse(message='查询成功', data=data)
