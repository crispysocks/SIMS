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

router = APIRouter(
    prefix='/students',
    tags=['学生基本信息管理模块'],
)


@router.get('/all', summary='获取学生列表')
async def students(db: Session = Depends(get_db)) -> ApiResponse[list[StudentRead]]:
    students = get_students_db(db)
    return ApiResponse(message='查询成功', data=[StudentRead.model_validate(s) for s in students])


@router.get('/search', summary='模糊查询')
def search_student(name: str, db: Session = Depends(get_db)) -> ApiResponse[list[StudentRead]]:
    data = search_student_db(db, name)
    return ApiResponse(message='查询成功', data=[StudentRead.model_validate(s) for s in data])


@router.get('/class/{class_no}', summary='按班级查询学生')
def get_student_class(class_no: str, db: Session = Depends(get_db)) -> ApiResponse[list[StudentRead]]:
    data = get_student_by_class_db(db, class_no)
    return ApiResponse(message='查询成功', data=[StudentRead.model_validate(s) for s in data])


@router.post('/add', summary='创建一个新学生', dependencies=[Depends(require_role(['admin']))])
def add_student(new_student: StudentCreate, db: Session = Depends(get_db)) -> ApiResponse[StudentRead]:
    result = chick_student(db, new_student.student_no)
    if result is True:
        raise HTTPException(status_code=400, detail='学生已存在')
    add_student_db(db, Student(**new_student.model_dump()))
    return ApiResponse(message='添加成功', data=StudentRead.model_validate(new_student))


@router.delete('/batch', summary='软删除', dependencies=[Depends(require_role(['admin']))])
def delete_student(no_list: List[str], db: Session = Depends(get_db)) -> ApiResponse[None]:
    for student_no in no_list:
        result = chick_student(db, student_no)
        if result is True:
            delete_student_db(db, student_no)
        elif result is False:
            continue
    return ApiResponse(message='删除成功', data=None)


@router.delete('/back', summary='恢复软删除的学生', dependencies=[Depends(require_role(['admin']))])
def back_student(no_list: List[str], db: Session = Depends(get_db)) -> ApiResponse[None]:
    for student_no in no_list:
        result = chick_student(db, student_no)
        if result is False:
            raise HTTPException(status_code=400, detail='部分学生编号不存在,请重新输入')

    for student_no in no_list:
        delete_back_db(db, student_no)
    return ApiResponse(message='恢复成功', data=None)


@router.get('/{student_no}', summary='获取单个学生信息')
async def get_anyony_student(student_no: str, db: Session = Depends(get_db)) -> ApiResponse[StudentRead]:
    result = chick_student(db, student_no)
    if result is True:
        result = chick_status(db, student_no)
        if result is True:
            result1 = get_student_db(db, student_no)
            return ApiResponse(message='查询成功', data=StudentRead.model_validate(result1))
    raise HTTPException(status_code=400, detail='学生不存在或已被删除')


@router.put('/{student_no}', summary='修改某个学生信息', dependencies=[Depends(require_role(['admin']))])
def update_student(student_no: str, update_student: StudentUpdate, db: Session = Depends(get_db)) -> ApiResponse[StudentRead]:
    result = chick_student(db, student_no)
    if result is True:
        update_student_db(db, student_no, update_student)
        result1 = get_student_db(db, student_no)
        return ApiResponse(message='修改成功', data=StudentRead.model_validate(result1))
    raise HTTPException(status_code=400, detail='学生不存在')
