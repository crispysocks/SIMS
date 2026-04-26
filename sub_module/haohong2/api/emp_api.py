from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from file.dao.emp_dao import add_stu_test, update_stu_test, find_emp, find_list_emp, del_emp, del_emp_back, \
    search_emp_list
from file.pdc_model.employment import EmploymentCreate, EmploymentUpdate, EmploymentSearchResponse, EmploymentQuery
from file.untils.database_util import get_db

emp_router1 = APIRouter()


@emp_router1.post('/employment',summary="添加就业信息",)
def add_employment(data: EmploymentCreate, db: Session = Depends(get_db)):
    """添加就业信息"""
    result = add_stu_test(db, data)
    if not result:
        raise HTTPException(status_code=400, detail="添加失败")
    return {"code": 200, "message": "添加成功", "data": result}


@emp_router1.put('/employment/{student_id}',summary="更新就业信息")
def update_employment(student_id: int, data: EmploymentUpdate, db: Session = Depends(get_db)):
    """更新就业信息"""
    result = update_stu_test(db, student_id, data)
    if not result:
        raise HTTPException(status_code=400, detail="添加失败")
    return {"code": 200, "message": "添加成功", "data": result}


@emp_router1.get('/employment/{student_id}',summary="获取学生就业信息")
def get_employment_by_student(student_id: int, db: Session = Depends(get_db)):
    """根据学生ID获取就业信息"""
    result = find_emp(db, student_id)
    if result is None:
        raise HTTPException(status_code=404, detail="未找到该学生就业记录")
    return {"code": 200, "message": "更新成功", "data": result}


@emp_router1.get('/employment/class/{class_id}', summary="获取班级就业信息列表")
def get_employment_by_class(class_id: int, db: Session = Depends(get_db)):
    """根据班级ID获取就业信息列表"""
    result = find_list_emp(db, class_id)
    return result


@emp_router1.delete('/employment',summary="软删除就业信息")
def delete_employment(student_id: List[int], db: Session = Depends(get_db)):
    result = del_emp(db, student_id)
    return result


@emp_router1.put('/employment/restore',summary="批量恢复就业信息")
def restore_employment(student_ids: List[int], db: Session = Depends(get_db)):
    result = del_emp_back(db, student_ids)
    return result

@emp_router1.post('/search_emp',summary="条件搜索就业信息",response_model=List[EmploymentSearchResponse])
def search_employment(query:EmploymentQuery,db:Session=Depends(get_db)):
    result = search_emp_list(db,query)
    return result