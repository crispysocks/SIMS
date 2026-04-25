from Myproject.first_project.dao import teacher_dao as dao
from .exceptions import (
    TeacherNotFoundException,
    CourseNotFoundException,
    DatabaseOperationException,
    InvalidDataException)
from sqlalchemy.exc import SQLAlchemyError
from typing import Any, Dict


class TeacherService:
    """老师业务服务层，处理所有与老师相关的业务逻辑和异常"""

    def __init__(self, db: Any):
        self.teacher_dao = dao.Teachers(db)
        self.course_dao = dao.Courses(db)

    def create_teacher(self, teacher_data: Dict) -> Dict:
        """创建新老师并处理可能的异常"""
        try:
            # 业务逻辑验证
            if not teacher_data.get('name') or not teacher_data.get('subject'):
                raise InvalidDataException("老师姓名和科目不能为空")

            # 调用DAO层
            new_teacher = self.teacher_dao.create_teacher(teacher_data)
            return {"message": "老师创建成功", "data": new_teacher}

        except SQLAlchemyError as e:
            raise DatabaseOperationException(f"数据库操作失败: {str(e)}")

    def get_teacher(self, teacher_id: int) -> Dict:
        """获取老师信息并处理异常"""
        try:
            teacher = self.teacher_dao.get_teacher(teacher_id)
            if not teacher:
                raise TeacherNotFoundException(f"ID为{teacher_id}的老师不存在")
            return {"message": "获取成功", "data": teacher}

        except SQLAlchemyError as e:
            raise DatabaseOperationException(f"数据库查询失败: {str(e)}")

    def update_teacher(self, teacher_id: int, teacher_data: Dict) -> Dict:
        """更新老师信息并处理异常"""
        try:
            # 验证老师是否存在
            self.get_teacher(teacher_id)

            # 业务逻辑验证
            if 'status' in teacher_data and teacher_data['status'] not in ['正常', '停用']:
                raise InvalidDataException("老师状态必须是'正常'或'停用'")

            # 调用DAO层
            updated_teacher = self.teacher_dao.update_teacher(teacher_id, teacher_data)
            return {"message": "老师信息更新成功", "data": updated_teacher}

        except SQLAlchemyError as e:
            raise DatabaseOperationException(f"数据库更新失败: {str(e)}")

    def delete_teacher(self, teacher_id: int) -> Dict:
        """删除老师并处理关联异常"""
        try:
            # 验证老师是否存在
            self.get_teacher(teacher_id)

            # 检查关联课程
            courses = self.course_dao.get_courses_by_teacher(teacher_id)
            if courses:
                raise InvalidDataException(f"该老师有{len(courses)}个关联课程，无法删除")

            # 调用DAO层
            result = self.teacher_dao.delete_teacher(teacher_id)
            return {"message": "老师删除成功", "data": result}

        except SQLAlchemyError as e:
            raise DatabaseOperationException(f"数据库删除失败: {str(e)}")

    def get_all_teachers(self):
        pass


class CourseService:
    """课程业务服务层，处理所有与课程相关的业务逻辑和异常"""

    def __init__(self, db: Any):
        self.teacher_dao = dao.Teachers(db)
        self.course_dao = dao.Courses(db)

    def create_course(self, course_data: Dict) -> Dict:
        """创建新课程并处理异常"""
        try:
            # 业务逻辑验证
            if not course_data.get('course_name'):
                raise InvalidDataException("课程名称不能为空")

            # 验证老师是否存在
            teacher_id = course_data.get('teacher_id')
            if not self.teacher_dao.get_teacher(teacher_id):
                raise TeacherNotFoundException(f"ID为{teacher_id}的老师不存在")

            # 调用DAO层
            new_course = self.course_dao.create_course(course_data)
            return {"message": "课程创建成功", "data": new_course}

        except SQLAlchemyError as e:
            raise DatabaseOperationException(f"数据库操作失败: {str(e)}")

    def get_course(self, course_id: int) -> Dict:
        """获取课程信息并处理异常"""
        try:
            course = self.course_dao.get_course(course_id)
            if not course:
                raise CourseNotFoundException(f"ID为{course_id}的课程不存在")

            # 添加老师姓名
            teacher = self.teacher_dao.get_teacher(course.teacher_id)
            teacher_name = teacher.name if teacher else "未知老师"
            return {"message": "获取成功", "data": {**course.__dict__, "teacher_name": teacher_name}}

        except SQLAlchemyError as e:
            raise DatabaseOperationException(f"数据库查询失败: {str(e)}")

    def update_course(self, course_id: int, course_data: Dict) -> Dict:
        """更新课程信息并处理异常"""
        try:
            # 验证课程是否存在
            self.get_course(course_id)

            # 验证老师是否存在（如果更新了teacher_id）
            if 'teacher_id' in course_data:
                teacher_id = course_data['teacher_id']
                if not self.teacher_dao.get_teacher(teacher_id):
                    raise TeacherNotFoundException(f"ID为{teacher_id}的老师不存在")

            # 调用DAO层
            updated_course = self.course_dao.update_course(course_id, course_data)
            return {"message": "课程信息更新成功", "data": updated_course}

        except SQLAlchemyError as e:
            raise DatabaseOperationException(f"数据库更新失败: {str(e)}")

    def delete_course(self, course_id: int) -> Dict:
        """删除课程并处理异常"""
        try:
            # 验证课程是否存在
            self.get_course(course_id)

            # 调用DAO层
            result = self.course_dao.delete_course(course_id)
            return {"message": "课程删除成功", "data": result}

        except SQLAlchemyError as e:
            raise DatabaseOperationException(f"数据库删除失败: {str(e)}")

    def get_courses_by_teacher(self, teacher_id: int) -> Dict:
        """获取指定老师的课程并处理异常"""
        try:
            # 验证老师是否存在
            self.teacher_dao.get_teacher(teacher_id)

            # 调用DAO层
            courses = self.course_dao.get_courses_by_teacher(teacher_id)
            return {"message": "获取成功", "data": courses}

        except SQLAlchemyError as e:
            raise DatabaseOperationException(f"数据库查询失败: {str(e)}")