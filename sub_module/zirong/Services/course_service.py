from sqlalchemy.orm import Session
from app.dao.teacher_dao import TeacherDAO, CourseDAO
from fastapi import HTTPException

class CourseService:
    def __init__(self, db: Session):
        self.db = db
        self.teacher_dao = TeacherDAO(db)
        self.course_dao = CourseDAO(db)

    def create_course(self, course_data: dict) -> dict:
        if not course_data.get("course_name"):
            raise HTTPException(status_code=400, detail="课程名称不能为空")
        try:
            new_course = self.course_dao.create(course_data)
            self.db.commit()
            return {"message": "课程创建成功", "data": {
                "id": new_course.id,
                "course_name": new_course.course_name
            }}
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"创建课程失败: {str(e)}")

    def get_course(self, course_id: int) -> dict:
        course = self.course_dao.get_by_id(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="课程不存在")
        return {
            "message": "获取成功",
            "data": {"id": course.id, "course_name": course.course_name}
        }

    def get_all_courses(self) -> dict:
        courses = self.course_dao.get_all()
        return {"message": "获取成功", "data": courses}

    def update_course(self, course_id: int, update_data: dict) -> dict:
        course = self.course_dao.get_by_id(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="课程不存在")
        filtered = {k: v for k, v in update_data.items() if v is not None}
        if not filtered:
            raise HTTPException(status_code=400, detail="没有提供要更新的字段")
        try:
            updated_course = self.course_dao.update(course, filtered)
            self.db.commit()
            return {"message": "课程更新成功", "data": updated_course}
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"更新失败: {str(e)}")

    def delete_course(self, course_id: int) -> dict:
        course = self.course_dao.get_by_id(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="课程不存在")

        # 检查是否还有老师关联此课程
        teacher_count = self.teacher_dao.count_by_course(course_id)
        if teacher_count > 0:
            raise HTTPException(
                status_code=400,
                detail=f"该课程下还有 {teacher_count} 位在职老师，无法删除。请先将相关老师调离或更改课程。"
            )

        try:
            self.course_dao.delete(course)
            self.db.commit()
            return {"message": "课程删除成功", "data": None}
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")

    def get_courses_by_teacher(self, teacher_id: int) -> dict:
        """根据老师 ID 获取其唯一课程（一对一关系）"""
        teacher = self.teacher_dao.get_by_id(teacher_id)
        if not teacher:
            raise HTTPException(status_code=404, detail="老师不存在或已离职")
        course = self.course_dao.get_by_id(teacher.course_id)
        if course:
            return {"message": "获取成功", "data": [course]}  # 返回列表保持一致
        return {"message": "获取成功", "data": []}