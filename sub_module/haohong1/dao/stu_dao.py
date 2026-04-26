from sqlalchemy import func, join, and_
from sqlalchemy.orm import Session
from file.db_model.student_project import Student_BASE, Score_BASE, Employment_BASE


# 查询所有 ≤30 岁的学员（返回 ORM 对象）
def find_stu(db: Session,age:int=30):
    return db.query(Student_BASE).filter(Student_BASE.age >= age).all()


# 统计每个班级人数、男女数量（返回普通查询结果）
def class_gender_count(db: Session):
    result = db.query(
        Student_BASE.class_id,
        func.count(1).label("total"),
        func.sum(func.if_(Student_BASE.gender == "男", 1, 0)).label("boy_count"),
        func.sum(func.if_(Student_BASE.gender == "女", 1, 0)).label("girl_count")
    ).group_by(
        Student_BASE.class_id
    ).all()
    a = [{"class_id": s.class_id,
          "total": s.total,
          "boy_count": s.boy_count,
          "girl_count": s.girl_count
          } for s in result]
    return a


#查询每次考试成绩都在指定分数以上的学⽣的编号，姓名和成绩
def get_students_always_above_80(db: Session,score:int=80):
    #查询80分以下的学生编号
    re = db.query(Score_BASE.student_id).filter(Score_BASE.score <= score).all()
    #转换成列表
    res = [i.student_id for i in re]
    #查询语句
    result = db.query(Score_BASE.student_id, Score_BASE.score, Student_BASE.student_name) \
        .join(Student_BASE, Student_BASE.student_id == Score_BASE.student_id) \
        .filter(Score_BASE.student_id.notin_(res)).distinct().all()
    a = [{"student_id": s.student_id
             , "student_name": s.student_name
             , "student_score": s.score} for s in result]
    return a


#查询有两次以上不及格的学⽣的姓名，班级和不及格成绩
def get_students_failed_twice(db: Session):
    re = (db.query(Score_BASE.student_id)
          .filter(Score_BASE.score < 60)
          .group_by(Score_BASE.student_id).having(func.count(Score_BASE.student_id) >= 2).all())
    res = [i.student_id for i in re]

    result = db.query(Score_BASE.score, Student_BASE.student_name, Student_BASE.class_id, Student_BASE.student_id) \
        .join(Student_BASE, Student_BASE.student_id == Score_BASE.student_id) \
        .filter(
        and_(
            Score_BASE.score < 60,
            Score_BASE.student_id.in_(res)
        ))
    return [
        {
            "student_name": i.student_name,
            "class_id": i.class_id,
            "score": i.score
        }
        for i in result
    ]


#统计每次考试每个班级的平均分，按照从⾼到低排序
def get_avg_score_by_class_exam(db: Session):
    re = db.query(
        Student_BASE.class_id.label("班级ID"),
        func.avg(Score_BASE.score).label("平均分")
    ).join(
        Student_BASE,
        Student_BASE.student_id == Score_BASE.student_id
    ).group_by(
        Student_BASE.class_id
    ).order_by(
        # 按平均分 降序（从高到低）
        func.avg(Score_BASE.score).desc()
    ).all()

    result = [{"class_id": s.班级ID, "avg_socre": s.平均分} for s in re]
    return result


#统计就业薪资最⾼的前五名学⽣的姓名，班级和就业时间，就业公司
def get_class_avg_score_by_exam(db: Session):
    re = db.query(Student_BASE.student_name, Employment_BASE.company_name, Student_BASE.class_id,
                  Employment_BASE.offer_date) \
        .join(Student_BASE, Student_BASE.student_id == Employment_BASE.student_id) \
        .order_by(Employment_BASE.salary).limit(5).all()

    result = [{"name": i.student_name, "class": i.class_id,
               "offer_date": i.offer_date, "company_name": i.company_name} for i in re]
    return result


#统计每个学⽣的就业时⻓（offer下发时间-就业开放时间）
def get_stu_offer_time(db: Session):
    re = db.query(
        Student_BASE.student_id,
        func.datediff(Employment_BASE.offer_date, Employment_BASE.open_date).label('duration_days')
    ).join(
        Employment_BASE, Student_BASE.student_id == Employment_BASE.student_id
    ).all()

    res = [{"学生id": i.student_id, "时长": i.duration_days} for i in re]

    return res


#统计每个班级的平均就业时⻓（只统计进⼊就业阶段的学⽣，也就是有就业开放时间）
def get_class_offer_time(db: Session):
    re = db.query(Student_BASE.class_id,
             func.avg(func.datediff(Employment_BASE.offer_date, Employment_BASE.open_date)).label("aaa")
             ) \
        .join(Student_BASE, Student_BASE.student_id == Employment_BASE.student_id) \
        .group_by(Student_BASE.class_id)

    res=[{"class_id":i.class_id,"avg_time":i.aaa} for i in re]
    return res
