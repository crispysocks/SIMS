from typing import List

from fastapi import APIRouter, HTTPException

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
    student_response,
    update_student_db,
)
from app.models.student import Student

router = APIRouter(prefix='/students', tags=['学生基本信息管理模块'])


@router.get('/all', summary='获取学生列表')
async def students():
    students = get_students_db()
    return {'message': '查询成功', 'data': students}


@router.get('/search', summary='模糊查询')
def search_student(name: str):
    data = search_student_db(name)
    return {'message': '查询成功', 'data': data}


@router.get('/{id}', summary='获取单个学生信息')
async def get_anyony_student(id: int):
    result = chick_student(id)
    if result is True:
        result = chick_status(id)
        if result is True:
            result1 = get_student_db(id)
            response = student_response(result1)
            return {'message': '查询成功', 'student': response}
    raise HTTPException(status_code=400, detail='学生不存在或已被删除')


@router.post('/add', response_model=StudentRead, summary='创建一个新学生')
def add_student(new_student: StudentCreate):
    result = chick_student(new_student.student_id)
    if result is True:
        raise HTTPException(status_code=400, detail='学生已存在')
    add_student_db(Student(**new_student.model_dump()))
    return student_response(new_student)


@router.put('/{id}', summary='修改某个学生信息')
def update_student(id: int, update_student: StudentUpdate):
    result = chick_student(id)
    if result is True:
        update_student_db(id, update_student)
        result1 = get_student_db(id)
        response = student_response(result1)
        return {'message': '修改成功', 'student': response}


@router.delete('/batch', summary='软删除')
def delete_student(id_list: List[int]):
    for id in id_list:
        result = chick_student(id)
        if result is True:
            delete_student_db(id)
        elif result is False:
            continue
    return {'message': '删除成功'}


@router.delete('/back', summary='恢复软删除的学生')
def back_student(id_list: List[int]):
    for id in id_list:
        result = chick_student(id)
        if result is False:
            raise HTTPException(status_code=400, detail='部分学生id不存在,请重新输入')

    for id in id_list:
        delete_back_db(id)
    return {'message': '恢复成功'}


@router.get('/class/{id}', summary='按班级查询学生')
def get_student_class(id: int):
    data = get_student_by_class_db(id)
    return {'message': '查询成功', 'data': data}
