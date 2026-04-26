from fastapi import HTTPException
from app.core.database import get_db  # noqa: E402

from app.models.student import Student


def chick_status(new_student_id):  # noqa: D103
    db = next(get_db())
    result = db.query(Student).all()
    for student in result:
        if student.student_id == new_student_id:
            if student.status == 0:
                return False
            else:
                return True


def chick_student(new_student_id):  # noqa: D103
    db = next(get_db())
    result = db.query(Student).all()
    for student in result:
        if student.student_id == new_student_id:
            return True
    return False


def get_students_db():  # noqa: D103
    list1 = []
    db = next(get_db())
    result = db.query(Student).all()
    for student in result:
        bool1 = chick_status(student.student_id)
        if bool1 is True:
            list1.append(student)

    return list1


def get_student_db(student_id):  # noqa: D103
    db = next(get_db())
    result = db.query(Student).filter(Student.student_id == student_id).first()
    return result


def student_response(new_student):  # noqa: D103
    return {
        'student_id': new_student.student_id,
        'class_id': new_student.class_id,
        'student_name': new_student.student_name,
        'hometown': new_student.hometown,
        'graduate_school': new_student.graduate_school,
        'major': new_student.major,
        'enroll_date': new_student.enroll_date,
        'graduate_date': new_student.graduate_date,
        'education': new_student.education,
        'advisor_id': new_student.advisor_id,
        'age': new_student.age,
        'gender': new_student.gender,
    }


def add_student_db(new_student):  # noqa: D103
    db = next(get_db())
    db.add(new_student)
    db.commit()


def update_student_db(student_id, update_student):  # noqa: D103
    db = next(get_db())
    try:
        db.query(Student).filter(Student.student_id == student_id).update({
            'class_id': update_student.class_id,
            'student_name': update_student.student_name,
            'hometown': update_student.hometown,
            'graduate_school': update_student.graduate_school,
            'major': update_student.major,
            'enroll_date': update_student.enroll_date,
            'graduate_date': update_student.graduate_date,
            'education': update_student.education,
            'advisor_id': update_student.advisor_id,
            'age': update_student.age,
            'gender': update_student.gender,
        })
        db.commit()
        return True
    except Exception:
        raise HTTPException(status_code=400, detail='更新失败')


def delete_student_db(student_id, delete_student=0):  # noqa: D103
    db = next(get_db())
    try:
        db.query(Student).filter(Student.student_id == student_id).update({
            'status': delete_student
        })
        db.commit()
        return True
    except Exception:
        raise HTTPException(status_code=400, detail='删除失败')


def delete_back_db(student_id, delete_student=1):  # noqa: D103
    db = next(get_db())
    try:
        db.query(Student).filter(Student.student_id == student_id).update({
            'status': delete_student
        })
        db.commit()
        return True
    except Exception:
        raise HTTPException(status_code=400, detail='恢复失败')


def get_student_by_class_db(class_id):  # noqa: D103
    db = next(get_db())
    data = db.query(Student).filter(Student.class_id == class_id).all()
    return data


def search_student_db(name):  # noqa: D103
    db = next(get_db())
    data = db.query(Student).filter(Student.student_name.like(f'%{name}%')).all()
    return data
