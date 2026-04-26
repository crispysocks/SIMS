from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from file.untils.database_util import get_db
from file.dao.stu_dao import find_stu, class_gender_count, get_students_always_above_80, get_students_failed_twice, \
    get_avg_score_by_class_exam, get_class_avg_score_by_exam, get_stu_offer_time, get_class_offer_time

emp_router = APIRouter()

# 1. 查询学生
@emp_router.get("/statistics/list1",summary='查询所有超过指定岁数的学员的信息')
def get_stu(age:int,db: Session = Depends(get_db)):
    data = find_stu(db,age)
    return {"code": 200, "data": data}

# 2. 统计班级性别数量
@emp_router.get("/statistics/list2",summary='统计每个班级的⼈数以及男⽣⼥⽣的⼈数')
def get_count(db: Session = Depends(get_db)):
    data = class_gender_count(db)
    return {"code": 200, "data": data}

#3.查询每在多少分以上的学⽣的编号，姓名和成绩，默认80
@emp_router.get("/statistics/list3", summary='查询每次考试成绩都在指定分数以上的学⽣的编号，姓名和成绩,默认80分')
def get_count(score:int,db: Session = Depends(get_db)):
    data = get_students_always_above_80(db,score)
    return {"code": 200, "data": data}

#4.查询有两次以上不及格的学⽣的姓名，班级和不及格成绩
@emp_router.get("/statistics/list4",summary='查询有两次以上不及格的学⽣的姓名，班级和不及格成绩')
def get_count(db: Session = Depends(get_db)):
    data = get_students_failed_twice(db)
    return {"code": 200, "data": data}

#5统计每次考试每个班级的平均分，按照从⾼到低排序
@emp_router.get("/statistics/list5",summary='统计每次考试每个班级的平均分，按照从⾼到低排序')
def get_count(db: Session = Depends(get_db)):
    data = get_avg_score_by_class_exam(db)
    return {"code": 200, "data": data}

@emp_router.get("/statistics/list6",summary='统计就业薪资最⾼的前五名学⽣的姓名，班级和就业时间，就业公司')
def get_count(db: Session = Depends(get_db)):
    data = get_class_avg_score_by_exam(db)
    return {"code": 200, "data": data}

@emp_router.get("/statistics/list7",summary='统计每个学⽣的就业时⻓（offer下发时间-就业开放时间）')
def get_count(db: Session = Depends(get_db)):
    data = get_stu_offer_time(db)
    return {"code": 200, "data": data}

@emp_router.get("/statistics/list8",summary='统计每个班级的平均就业时⻓（只统计进⼊就业阶段的学⽣，也就是有就业开放时间）')
def get_count(db: Session = Depends(get_db)):
    data = get_class_offer_time(db)
    return {"code": 200, "data": data}