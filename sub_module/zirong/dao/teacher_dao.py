from sqlalchemy.orm import Session
from app.models.teacher import Teacher
from app.models.course import Course

class TeacherDAO:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> Teacher:
        teacher = Teacher(**data)
        self.db.add(teacher)
        self.db.flush()
        return teacher

    def get_by_id(self, teacher_id: int) -> Teacher | None:
        """获取在职老师（status=0）"""
        return (
            self.db.query(Teacher)
            .filter(Teacher.id == teacher_id, Teacher.status == 0)
            .first()
        )

    def get_all(self) -> list[Teacher]:
        """获取所有在职老师列表（不含课程名称）"""
        return self.db.query(Teacher).filter(Teacher.status == 0).all()


    def get_all_with_course(self) -> list[dict]:
        """获取所有在职老师，并附带课程名称"""
        results = (
            self.db.query(Teacher, Course.course_name)
            .join(Course, Teacher.course_id == Course.id)
            .filter(Teacher.status == 0)
            .all()
        )
        teacher_list = []
        for t, cname in results:
            teacher_list.append({
                "id": t.id,
                "name": t.name,
                "course_id": t.course_id,
                "course_name": cname,
                "gender": t.gender,
                "phone_number": t.phone_number,
                "status": t.status,
                "avatar_path": t.avatar_path
            })
        return teacher_list

    def update(self, teacher: Teacher, update_data: dict) -> Teacher:
        for key, value in update_data.items():
            setattr(teacher, key, value)
        self.db.flush()
        return teacher

    def soft_delete(self, teacher: Teacher) -> Teacher:
        teacher.status = 1
        self.db.flush()
        return teacher

    def count_by_course(self, course_id: int) -> int:
        """统计某课程下在职老师数量"""
        return (
            self.db.query(Teacher)
            .filter(Teacher.course_id == course_id, Teacher.status == 0)
            .count()
        )


class CourseDAO:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> Course:
        course = Course(**data)
        self.db.add(course)
        self.db.flush()
        return course

    def get_by_id(self, course_id: int) -> Course | None:
        return self.db.query(Course).filter(Course.id == course_id).first()

    def get_all(self) -> list[Course]:
        return self.db.query(Course).all()

    def update(self, course: Course, update_data: dict) -> Course:
        for key, value in update_data.items():
            setattr(course, key, value)
        self.db.flush()
        return course

    def delete(self, course: Course) -> None:
        self.db.delete(course)
        self.db.flush()