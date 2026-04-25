from typing import List

from fastapi import APIRouter, HTTPException

from Pydantic_model.student_model import Student_add, Student_response, Student_update
from dao.stu_dao import add_student_db, chick_student, get_student_db, get_students_db, student_response, \
    update_student_db, delete_student_db, delete_back_db, chick_status, get_student_by_class_db, search_student_db
from db_model.students_model import Students

# 统一前缀
stu_router = APIRouter(prefix="/students",tags=["学⽣基本信息管理模块"])


# GET /students # 获取学生列表
@stu_router.get("/all",summary='获取学生列表')
async def students():
    students = get_students_db()
    return {'message':'查询成功','data':students}

@stu_router.get('/search',summary='模糊查询')
def search_student(name:str):
    data = search_student_db(name)

    return {'message': '查询成功', 'data': data}

 # 获取某个学生信息
@stu_router.get("/{id}",summary='获取单个学生信息')
async def get_anyony_student(id:int):
    result = chick_student(id)
    if result == True:#表示有这个学生
        result = chick_status(id)
        if result == True:
        #读取数据库该学生信息
            result1 = get_student_db(id)
            response = student_response(result1)
            return {'message':'查询成功','student':response}
    raise HTTPException(status_code=400, detail="学生不存在或已被删除")

# POST /students # 创建新学生
@stu_router.post("/add",response_model=Student_response,summary='创建一个新学生')
def add_student(new_student: Student_add):
    result = chick_student(new_student.student_id)
    if result == True:#有这个学生
        raise HTTPException(status_code=400, detail="学生已存在")
    #添加学生进入数据库
    add_student_db(Students(**new_student.dict()))
    # new_student.dict() → 得到前端传的参数字典
    # Students(**字典) → 转成数据库能识别的ORM对象
    # 把这个对象传给add_student_db才能存入数据库
    return student_response(new_student)




# PUT /students/{id} # 修改某个学生信息
@stu_router.put("/{id}",summary='修改某个学生信息')
def update_student(id: int,update_student: Student_update):
    result = chick_student(id)
    if result == True:#Ture表示有这个学生
        #更新学生信息
        update_student_db(id, update_student)
        result1 = get_student_db(id)
        response = student_response(result1)
        return {'message': '修改成功', 'student': response}



#删除一个或多个学生信息，软删除，状态变为0
@stu_router.delete("/batch",summary='软删除')
def delete_student(id_list : List[int]):
    for id in id_list:
        result = chick_student(id)
        if result == True:
            delete_student_db(id)
        elif result == False:
            continue
    return {'message':'删除成功'}

# #删除学生信息，软删除，状态变为0
# @stu_router.delete("/{id}",summary='删除学生')
# def delete_student(id: int):
#     result = chick_student(id)
#     if result == False:#存在这个学生
#         delete_student_db(id)
#         return {'message':'删除成功'}

@stu_router.delete('/back',summary='恢复软删除的学生')
def back_student(id_list : List[int]):
    for id in id_list:
        result = chick_student(id)
        if result == False:
            raise HTTPException(status_code=400, detail="部分学生id不存在,请重新输入")

    for id in id_list:
        delete_student_db(id)
    return {'message':'恢复成功'}



@stu_router.get('/class/{id}',summary='按班级查询学生')
def get_student_class(id: int):
    data = get_student_by_class_db(id)

    return {'message':'查询成功','data':data}






