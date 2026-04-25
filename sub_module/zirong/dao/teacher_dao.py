from models.teacherBase import Teacher, Course
from sqlalchemy.orm import Session


class Teachers:
    """老师数据访问对象"""

    def __init__(self, db: Session):
        self.db = db

    def create_teacher(self, teacher_data):
        """创建新老师"""
        new_teacher = Teacher(**teacher_data)
        self.db.add(new_teacher)
        self.db.commit()
        self.db.refresh(new_teacher)
        return new_teacher

    def get_teacher(self, teacher_id):
        """获取单个老师"""
        return self.db.query(Teacher).filter(Teacher.id == teacher_id).first()

    def get_all_teachers(self):
        """获取所有老师"""
        return self.db.query(Teacher).all()

    def update_teacher(self, teacher_id, teacher_data):
        """更新老师信息"""
        db_teacher = self.get_teacher(teacher_id)
        if not db_teacher:
            return None

        for key, value in teacher_data.items():
            setattr(db_teacher, key, value)

        self.db.commit()
        self.db.refresh(db_teacher)
        return db_teacher

    def delete_teacher(self, teacher_id):
        """删除老师"""
        teacher = self.get_teacher(teacher_id)
        if not teacher:
            return None

        # 检查是否有课程关联
        courses = self.db.query(Course).filter(Course.teacher_id == teacher_id).all()
        if courses:
            return "关联课程"

        self.db.delete(teacher)
        self.db.commit()
        return teacher


class Courses:
    """课程数据访问对象"""

    def __init__(self, db: Session):
        self.db = db

    def create_course(self, course_data):
        """创建新课程"""
        new_course = Course(**course_data)
        self.db.add(new_course)
        self.db.commit()
        self.db.refresh(new_course)
        return new_course

    def get_course(self, course_id):
        """获取单个课程"""
        return self.db.query(Course).filter(Course.id == course_id).first()

    def get_all_courses(self):
        """获取所有课程"""
        courses = self.db.query(Course).all()
        result = []
        for course in courses:
            teacher = self.db.query(Teacher).filter(Teacher.id == course.teacher_id).first()
            teacher_name = teacher.name if teacher else "未知老师"
            result.append({**course.__dict__, "teacher_name": teacher_name})
        return result

    def update_course(self, course_id, course_data):
        """更新课程信息"""
        db_course = self.get_course(course_id)
        if not db_course:
            return None

        for key, value in course_data.items():
            setattr(db_course, key, value)

        self.db.commit()
        self.db.refresh(db_course)
        return db_course

    def delete_course(self, course_id):
        """删除课程"""
        course = self.get_course(course_id)
        if not course:
            return None

        self.db.delete(course)
        self.db.commit()
        return course

    def get_courses_by_teacher(self, teacher_id):
        """获取指定老师的课程"""
        return self.db.query(Course).filter(Course.teacher_id == teacher_id).all()



