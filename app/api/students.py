# ============================================================
# students.py —— 学生管理接口模块
# ============================================================
# 这个文件提供学生信息的增删改查接口，包括：
#   1. 获取所有学生列表
#   2. 按姓名模糊搜索学生
#   3. 按班级查询学生
#   4. 新增学生
#   5. 批量软删除学生
#   6. 批量恢复已删除的学生
#   7. 获取单个学生详情
#   8. 修改学生信息
#
# 学生模块的权限控制：
#   - 查询：任何人都可以
#   - 新增、修改、删除、恢复：仅 admin
# ============================================================

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import require_role
from app.schemas.response import ApiResponse
from app.schemas.student import StudentCreate, StudentRead, StudentUpdate
from app.services.student import (
    add_student_db,
    chick_status,
    chick_student,
    delete_back_db,
    delete_student_db,
    get_student_by_class_db,
    get_student_db,
    get_students_db,
    search_student_db,
    update_student_db,
)
from app.models.student import Student

# 创建路由，所有以 /students 开头的请求都归这里处理
router = APIRouter(
    prefix='/students',
    tags=['学生基本信息管理模块'],
)


# ============================================================
# 1. 获取所有学生列表
# ============================================================

@router.get('/all', summary='获取学生列表')
async def students(db: Session = Depends(get_db)) -> ApiResponse[list[StudentRead]]:
    """
    获取系统中所有学生的列表。

    访问地址：GET /students/all

    参数：
        db: 数据库连接

    返回值：
        所有学生的信息列表
    """
    students = get_students_db(db)
    return ApiResponse(message='查询成功', data=[StudentRead.model_validate(s) for s in students])


# ============================================================
# 2. 按姓名模糊搜索学生
# ============================================================

@router.get('/search', summary='模糊查询')
def search_student(name: str, db: Session = Depends(get_db)) -> ApiResponse[list[StudentRead]]:
    """
    根据姓名模糊搜索学生。

    访问地址：GET /students/search?name=张
    例子：GET /students/search?name=张
        会返回姓名中包含"张"的所有学生（如张三、张四、李张等）

    参数：
        name: 姓名关键字
        db: 数据库连接

    返回值：
        匹配的学生列表
    """
    data = search_student_db(db, name)
    return ApiResponse(message='查询成功', data=[StudentRead.model_validate(s) for s in data])


# ============================================================
# 3. 按班级查询学生
# ============================================================

@router.get('/class/{class_no}', summary='按班级查询学生')
def get_student_class(class_no: str, db: Session = Depends(get_db)) -> ApiResponse[list[StudentRead]]:
    """
    查询某个班级的所有学生。

    访问地址：GET /students/class/{class_no}
    例子：GET /students/class/C001

    参数：
        class_no: 班级编号
        db: 数据库连接

    返回值：
        该班级的学生列表
    """
    data = get_student_by_class_db(db, class_no)
    return ApiResponse(message='查询成功', data=[StudentRead.model_validate(s) for s in data])


# ============================================================
# 4. 新增学生
# ============================================================

@router.post('/add', summary='创建一个新学生', dependencies=[Depends(require_role(['admin']))])
def add_student(new_student: StudentCreate, db: Session = Depends(get_db)) -> ApiResponse[StudentRead]:
    """
    新增一个学生。

    访问地址：POST /students/add
    权限：仅管理员可操作

    参数：
        new_student: 学生信息，包含学号、姓名、性别、班级等
        db: 数据库连接

    返回值：
        新增成功的学生信息

    可能的错误：
        - 400：该学号的学生已存在
    """
    result = add_student_db(db, Student(**new_student.model_dump()))
    if result is None:
        raise HTTPException(status_code=400, detail='学生已存在')
    return ApiResponse(message='添加成功', data=StudentRead.model_validate(result))


# ============================================================
# 5. 批量软删除学生
# ============================================================

@router.delete('/batch', summary='软删除', dependencies=[Depends(require_role(['admin']))])
def delete_student(no_list: List[str], db: Session = Depends(get_db)) -> ApiResponse[None]:
    """
    批量软删除学生。

    访问地址：DELETE /students/batch
    权限：仅管理员可操作
    请求体：['S001', 'S002', 'S003']

    参数：
        no_list: 学生编号列表
        db: 数据库连接

    返回值：
        删除成功的提示
    """
    for student_no in no_list:
        result = chick_student(db, student_no)
        if result is True:
            delete_student_db(db, student_no)
        elif result is False:
            continue
    return ApiResponse(message='删除成功', data=None)


# ============================================================
# 6. 批量恢复已删除的学生
# ============================================================

@router.put('/back', summary='恢复软删除的学生', dependencies=[Depends(require_role(['admin']))])
def back_student(no_list: List[str], db: Session = Depends(get_db)) -> ApiResponse[None]:
    """
    批量恢复已软删除的学生。

    访问地址：PUT /students/back
    权限：仅管理员可操作
    请求体：['S001', 'S002']

    参数：
        no_list: 要恢复的学生编号列表
        db: 数据库连接

    返回值：
        恢复成功的提示

    可能的错误：
        - 400：部分学生不存在或者未被删除
    """
    for student_no in no_list:
        result = chick_student(db, student_no)
        result1 = chick_status(db, student_no)
        if result is False or result1 is True:
            raise HTTPException(status_code=400, detail='部分学生不存在或者未被删除,请重新输入')

    for student_no in no_list:
        delete_back_db(db, student_no)
    return ApiResponse(message='恢复成功', data=None)


# ============================================================
# 7. 获取单个学生详情
# ============================================================

@router.get('/{student_no}', summary='获取单个学生信息')
async def get_anyony_student(student_no: str, db: Session = Depends(get_db)) -> ApiResponse[StudentRead]:
    """
    根据学号查询单个学生的详细信息。

    访问地址：GET /students/{student_no}
    例子：GET /students/S001

    参数：
        student_no: 学生编号
        db: 数据库连接

    返回值：
        该学生的详细信息

    可能的错误：
        - 400：学生不存在或已被删除
    """
    result = chick_student(db, student_no)
    if result is True:
        result = chick_status(db, student_no)
        if result is True:
            result1 = get_student_db(db, student_no)
            return ApiResponse(message='查询成功', data=StudentRead.model_validate(result1))
    raise HTTPException(status_code=400, detail='学生不存在或已被删除')


# ============================================================
# 8. 修改学生信息
# ============================================================

@router.put('/{student_no}', summary='修改某个学生信息', dependencies=[Depends(require_role(['admin']))])
def update_student(student_no: str, update_student: StudentUpdate, db: Session = Depends(get_db)) -> ApiResponse[StudentRead]:
    """
    修改指定学生的信息。

    访问地址：PUT /students/{student_no}
    例子：PUT /students/S001
    权限：仅管理员可操作

    参数：
        student_no: 学生编号
        update_student: 要更新的字段
        db: 数据库连接

    返回值：
        修改后的学生信息

    可能的错误：
        - 400：学生不存在
    """
    result = chick_student(db, student_no)
    if result is True:
        update_student_db(db, student_no, update_student)
        result1 = get_student_db(db, student_no)
        return ApiResponse(message='修改成功', data=StudentRead.model_validate(result1))
    raise HTTPException(status_code=400, detail='学生不存在')
