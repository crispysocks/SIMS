from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.dao.teacher_dao import TeacherDAO, CourseDAO
from app.services.exceptions import (
    TeacherNotFoundException,
    InvalidDataException,
    DatabaseOperationException
)
from fastapi import HTTPException

class TeacherService:
    def __init__(self, db: Session):
        self.db = db
        self.teacher_dao = TeacherDAO(db)
        self.course_dao = CourseDAO(db)

    def create_teacher(self, teacher_data: dict) -> dict:
        """创建老师，必须指定 course_id"""
        try:
            if not teacher_data.get("name"):
                raise InvalidDataException("老师姓名不能为空")
            if not teacher_data.get("course_id"):
                raise InvalidDataException("课程ID不能为空")

            # 校验课程是否存在
            course = self.course_dao.get_by_id(teacher_data["course_id"])
            if not course:
                raise HTTPException(status_code=404, detail="指定的课程不存在")

            new_teacher = self.teacher_dao.create(teacher_data)
            self.db.commit()
            return {"message": "老师创建成功", "data": {
                "id": new_teacher.id,
                "name": new_teacher.name,
                "course_id": new_teacher.course_id
            }}
        except InvalidDataException as e:
            raise HTTPException(status_code=400, detail=str(e))
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=409, detail="数据冲突，可能已存在同名教师")
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"创建老师失败: {str(e)}")

    def get_teacher(self, teacher_id: int) -> dict:
        """获取单个老师，附带课程信息"""
        teacher = self.teacher_dao.get_by_id(teacher_id)
        if not teacher:
            raise HTTPException(status_code=404, detail="老师不存在或已离职")

        # 手动获取课程名称
        course = self.course_dao.get_by_id(teacher.course_id)
        course_name = course.course_name if course else "未知课程"

        return {
            "message": "获取成功",
            "data": {
                "id": teacher.id,
                "name": teacher.name,
                "course_id": teacher.course_id,
                "course_name": course_name,
                "gender": teacher.gender,
                "phone_number": teacher.phone_number,
                "status": teacher.status,
                "avatar_path": teacher.avatar_path
            }
        }

    def get_all_teachers(self) -> dict:
        """获取所有在职老师，已包含课程名称"""
        teachers = self.teacher_dao.get_all_with_course()
        return {"message": "获取成功", "data": teachers}

    def update_teacher(self, teacher_id: int, update_data: dict) -> dict:
        teacher = self.teacher_dao.get_by_id(teacher_id)
        if not teacher:
            raise HTTPException(status_code=404, detail="老师不存在或已离职")

        # 如果要修改课程，先校验新课程存在
        new_course_id = update_data.get("course_id")
        if new_course_id:
            course = self.course_dao.get_by_id(new_course_id)
            if not course:
                raise HTTPException(status_code=404, detail="新指定的课程不存在")

        # 过滤掉值为 None 的字段
        filtered = {k: v for k, v in update_data.items() if v is not None}
        if not filtered:
            raise HTTPException(status_code=400, detail="没有提供要更新的字段")

        try:
            updated_teacher = self.teacher_dao.update(teacher, filtered)
            self.db.commit()
            # 重新查询带课程名称
            return self.get_teacher(teacher_id)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"更新失败: {str(e)}")

    def delete_teacher(self, teacher_id: int) -> dict:
        """逻辑删除老师（标记为离职），不再检查关联课程，因为课程不在老师名下"""
        teacher = self.teacher_dao.get_by_id(teacher_id)
        if not teacher:
            raise HTTPException(status_code=404, detail="老师不存在或已离职")

        try:
            self.teacher_dao.soft_delete(teacher)
            self.db.commit()
            return {"message": "老师已标记为离职", "data": None}
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")