from fastapi import HTTPException

from db_model.students_model import Students
from utils.database import get_db

def chick_status(new_student_id):#检查学生状态0返回false，1返回ture
    db = next(get_db())
    result = db.query(Students).all()
    for student in result:
        if student.student_id== new_student_id:
            if student.status == 0:
                return False
            else:
                return True


def chick_student(new_student_id):#查询学生是否存在，存在ture，不存在false
    db = next(get_db())
    result = db.query(Students).all()
    for student in result:
        if student.student_id == new_student_id:
            return True
    return False
def get_students_db():#获取所有学生信息，包括状态
    list1 = []
    db = next(get_db())
    result = db.query(Students).all()
    for student in result:
        bool1 = chick_status(student.student_id)
        if bool1 == True:
            list1.append(student)

    return list1

def get_student_db(student_id):#获取某个学生的信息
    db = next(get_db())
    result = db.query(Students).filter(Students.student_id == student_id).first()
    return result


# 公共响应体函数，返回学生信息（没有状态的信息）
def student_response(new_student):
    return {
        "student_id": new_student.student_id,
        "class_id": new_student.class_id,
        "student_name": new_student.student_name,
        "hometown": new_student.hometown,
        "graduate_school": new_student.graduate_school,
        "major": new_student.major,
        "enroll_date": new_student.enroll_date,
        "graduate_date": new_student.graduate_date,
        "education": new_student.education,
        "advisor_id": new_student.advisor_id,
        "age": new_student.age,
        "gender": new_student.gender
    }
def add_student_db(new_student):#添加单个学生
    db = next(get_db())
    db.add(new_student)# 添加
    db.commit()# 提交



def update_student_db(student_id, update_student):#更新学生的信息
    db = next(get_db())
    try:#更新学生信息
        db.query(Students).filter(Students.student_id == student_id).update({
            "class_id": update_student.class_id,
            "student_name": update_student.student_name,
            "hometown": update_student.hometown,
            "graduate_school": update_student.graduate_school,
            "major": update_student.major,
            "enroll_date": update_student.enroll_date,
            "graduate_date": update_student.graduate_date,
            "education": update_student.education,
            "advisor_id": update_student.advisor_id,
            "age": update_student.age,
            "gender": update_student.gender
        })
        db.commit()
        return True
    except:
        raise HTTPException(status_code=400, detail="更新失败")



def delete_student_db(student_id,delete_student = 0):#软删除学生的信息
    db = next(get_db())
    try:#更新学生信息
        db.query(Students).filter(Students.student_id == student_id).update({
            'status' :delete_student
        })
        db.commit()
        return True
    except:
        raise HTTPException(status_code=400, detail="删除失败")


def delete_back_db(student_id,delete_student = 1):#恢复软删除学生信息
    db = next(get_db())
    try:#更新学生信息
        db.query(Students).filter(Students.student_id == student_id).update({
            'status' :delete_student
        })
        db.commit()
        return True
    except:
        raise HTTPException(status_code=400, detail="恢复失败")




def get_student_by_class_db(class_id):
    db = next(get_db())
    data = db.query(Students).filter(Students.class_id==class_id).all()
    return data


def search_student_db(name):
    db = next(get_db())
    data = db.query(Students).filter(Students.student_name.like(f"%{name}%")).all()
    return data

