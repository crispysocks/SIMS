from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.testing import in_

from file.db_model.employment_project import Employment
from file.db_model.student_project import Student_BASE
from file.pdc_model.employment import EmploymentCreate, EmploymentUpdate, EmploymentQuery, EmploymentSearchResponse
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session


# # 全局：获取当前登录用户+权限
# def get_current_user(username: str, password: str, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == username, User.password == password).first()
#     if not user:
#         raise HTTPException(status_code=401, detail="用户名或密码错误")
#     return user
#
# # 专属：仅超级管理员可访问（删除接口专用）
# def only_admin(user: dict = Depends(get_current_user)):
#     if user.role != "admin":
#         raise HTTPException(status_code=403, detail="权限不足，无法删除")
#     return user
def check_student(db:Session,student_id:int):
    a=db.query(Employment.student_id==student_id)
    if a:
        return True
    return False


def add_stu_test(db: Session, emp_model: EmploymentCreate):
    a = check_student(db, emp_model.student_id)
    if not a:
        return None
    emp = Employment(student_id=emp_model.student_id,
                     open_time=emp_model.open_time,
                     offer_time=emp_model.offer_time,
                     company=emp_model.company,
                     salary=emp_model.salary
                     )
    a=check_student(db,emp.student_id)


def update_stu_test(db: Session, student_id: int, emp_model: EmploymentUpdate):
    emp = db.query(Employment).filter(Employment.student_id == student_id).first()
    if not emp:
        return None

    if emp_model.salary is not None:
        emp.salary = emp_model.salary
    if emp_model.company is not None:
        emp.company = emp_model.company
    if emp_model.offer_time is not None:
        emp.offer_time = emp_model.offer_time
    if emp_model.open_time is not None:
        emp.open_time = emp_model.open_time
    db.commit()
    db.refresh(emp)
    return emp


def find_emp(db: Session, student_id: int):
    re = db.query(Employment) \
        .join(Student_BASE, Employment.student_id == Student_BASE.student_id) \
        .filter(
        and_(Student_BASE.status == 1, Employment.student_id == student_id,Employment.status ==1)
    ).first()
    if re is None:
        return {"message": "您查找的学生就业信息不存在或已被删除"}

    data = {"student_id": re.student_id, "open_date": re.open_time, "offer_date": re.offer_time,
             "company": re.company, "salary": re.salary}
    return data

def find_list_emp(db:Session,class_id:int):
    re =db.query(Employment,Student_BASE)\
        .join(Student_BASE,Employment.student_id==Student_BASE.student_id)\
        .filter(
        and_(Student_BASE.status==1,Student_BASE.class_id == class_id)
    ).all()
    if not re:
        return {"message":"您查找的班级不存在"}

    data=[{"student_id": i.Employment.student_id,"student_name":i.Student_BASE.student_name
              , "open_date": i.Employment.open_time, "offer_date": i.Employment.offer_time,
             "company": i.Employment.company, "salary": i.Employment.salary} for i in re]

    return data


#软删除
def del_emp(db: Session, student_id: List[int]):  # 注意参数是 List
    emps = db.query(Employment).filter(
        and_(Employment.student_id.in_(student_id), Employment.status == 1)
    ).all()
    if not emps:
        return {"message": "您要删除的学生不存在或已经被软删除"}

    for emp in emps:  # 遍历每个记录
        emp.status = 0
    db.commit()
    return {"message": "删除成功"}

#被软删除的状态恢复
def del_emp_back(db:Session,student_id:List[int]):
    emps = db.query(Employment).filter(
        and_(Employment.student_id.in_(student_id), Employment.status == 0)
    ).all()
    if not emps:
        return {"messgae":"您要恢复的学号都不存在或没有被软删除"}
    for emp in emps:
        emp.status =1
    db.commit()
    return {"message":"恢复成功"}


def search_emp_list(db:Session,query:EmploymentQuery):
    re =db.query(Employment,
                Student_BASE.student_name
                 ,Student_BASE.class_id).join(Student_BASE,Employment.student_id==Student_BASE.student_id)

    if query.student_id is not None:
        re=re.filter(Employment.student_id==query.student_id)

    if query.company is not None:
        re=re.filter(Employment.company == query.company)

    if query.min_salary is not None:
        re=re.filter(Employment.salary >=query.min_salary)

    if query.max_salary is not None:
        re=re.filter(Employment.salary <=query.max_salary)

    re.filter(Employment.status==1).all()

    return [
        EmploymentSearchResponse(
            student_id=emp.student_id,
            student_name=student_name,
            class_id=class_id,
            company=emp.company,
            salary=emp.salary,
            open_time=emp.open_time,
            offer_time=emp.offer_time
        )
        for emp, student_name, class_id in re
    ]


