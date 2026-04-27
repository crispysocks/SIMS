from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.student import Student


def chick_status(db: Session, new_student_no: str):
    """检查学生状态，0返回False，1返回True。"""
    result = db.query(Student).all()
    for student in result:
        if student.student_no == new_student_no:
            if student.isdeleted == 1:
                return False
            else:
                return True


def chick_student(db: Session, new_student_no: str):
    """查询学生是否存在，存在返回True，不存在返回False。"""
    result = db.query(Student).all()
    for student in result:
        if student.student_no == new_student_no:
            return True
    return False


def get_students_db(db: Session):
    """获取所有学生信息，包括状态。"""
    list1 = []
    result = db.query(Student).all()
    for student in result:
        bool1 = chick_status(db, student.student_no)
        if bool1 is True:
            list1.append(student)
    return list1


def get_student_db(db: Session, student_no: str):
    """获取某个学生的信息。"""
    result = db.query(Student).filter(Student.student_no == student_no).first()
    return result


def student_response(new_student):
    """公共响应体函数，返回学生信息（没有状态的信息）。"""
    if new_student is None:
        return None
    return {
        'student_no': new_student.student_no,
        'class_no': new_student.class_no,
        'name': new_student.name,
        'birth_place': new_student.birth_place,
        'graduate_school': new_student.graduate_school,
        'major': new_student.major,
        'entrance_time': new_student.entrance_time,
        'graduate_time': new_student.graduate_time,
        'education': new_student.education,
        'advisor_name': new_student.advisor_name,
        'age': new_student.age,
        'gender': new_student.gender,
        'phone': new_student.phone,
        'id_card': new_student.id_card,
    }


def add_student_db(db: Session, new_student: Student):
    """添加单个学生。

    若该学生已有被软删除的记录，则复用该记录并更新字段。
    """
    existing = (
        db.query(Student)
        .filter(Student.student_no == new_student.student_no)
        .first()
    )

    if existing:
        if existing.isdeleted == 0:
            return None

        existing.isdeleted = 0
        existing.class_no = new_student.class_no
        existing.name = new_student.name
        existing.birth_place = new_student.birth_place
        existing.graduate_school = new_student.graduate_school
        existing.major = new_student.major
        existing.entrance_time = new_student.entrance_time
        existing.graduate_time = new_student.graduate_time
        existing.education = new_student.education
        existing.advisor_name = new_student.advisor_name
        existing.age = new_student.age
        existing.gender = new_student.gender
        existing.phone = new_student.phone
        existing.id_card = new_student.id_card
        db.commit()
        db.refresh(existing)
        return existing

    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


def update_student_db(db: Session, student_no: str, update_student: Student):
    """更新学生的信息。"""
    try:
        # 如果是空的，就不更新
        update_data = {}
        if update_student.class_no is not None:
            update_data["class_no"] = update_student.class_no
        if update_student.name is not None:
            update_data["name"] = update_student.name
        if update_student.birth_place is not None:
            update_data["birth_place"] = update_student.birth_place
        if update_student.graduate_school is not None:
            update_data["graduate_school"] = update_student.graduate_school
        if update_student.major is not None:
            update_data["major"] = update_student.major
        if update_student.entrance_time is not None:
            update_data["entrance_time"] = update_student.entrance_time
        if update_student.graduate_time is not None:
            update_data["graduate_time"] = update_student.graduate_time
        if update_student.education is not None:
            update_data["education"] = update_student.education
        if update_student.advisor_name is not None:
            update_data["advisor_name"] = update_student.advisor_name
        if update_student.age is not None:
            update_data["age"] = update_student.age
        if update_student.gender is not None:
            update_data["gender"] = update_student.gender
        if update_student.phone is not None:
            update_data["phone"] = update_student.phone
        if update_student.id_card is not None:
            update_data["id_card"] = update_student.id_card

        #  如果是个空字典，直接返回
        if not update_data:
            return True

        db.query(Student).filter(Student.student_no == student_no).update(update_data)
        db.commit()
        return True
    except Exception:
        raise HTTPException(status_code=400, detail='更新失败')


def delete_student_db(db: Session, student_no: str, delete_student: int = 1):
    """软删除学生的信息。"""
    try:
        db.query(Student).filter(Student.student_no == student_no).update({
            'isdeleted': delete_student
        })
        db.commit()
        return True
    except Exception:
        raise HTTPException(status_code=400, detail='删除失败')


def delete_back_db(db: Session, student_no: str, delete_student: int = 0):
    """恢复软删除学生信息。"""
    try:
        db.query(Student).filter(Student.student_no == student_no).update({
            'isdeleted': delete_student
        })
        db.commit()
        return True
    except Exception:
        raise HTTPException(status_code=400, detail='恢复失败')


def get_student_by_class_db(db: Session, class_no: str):
    """按班级查询学生。"""
    data = db.query(Student).filter(Student.class_no == class_no).all()
    return data


def search_student_db(db: Session, name: str):
    """根据姓名模糊查询学生。"""
    data = db.query(Student).filter(Student.name.like(f'%{name}%')).all()
    return data
