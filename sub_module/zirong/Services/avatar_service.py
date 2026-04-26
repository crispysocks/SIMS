import os
from sqlalchemy.orm import Session
from app.dao.teacher_dao import TeacherDAO
from app.utils.file_storage import FileStorage
from fastapi import HTTPException, UploadFile

class AvatarService:
    def __init__(self, db: Session):
        self.db = db
        self.teacher_dao = TeacherDAO(db)
        self.file_storage = FileStorage()

    def upload_avatar(self, teacher_id: int, file: UploadFile) -> dict:
        teacher = self.teacher_dao.get_by_id(teacher_id)
        if not teacher:
            raise HTTPException(status_code=404, detail="老师不存在或已离职")

        file_path = self.file_storage.save(file)

        if teacher.avatar_path and os.path.exists(teacher.avatar_path):
            self.file_storage.delete(teacher.avatar_path)

        teacher.avatar_path = file_path
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"更新头像失败: {str(e)}")
        return {"message": "头像上传成功", "data": {"avatar_path": file_path}}

    def get_avatar_path(self, teacher_id: int) -> dict:
        teacher = self.teacher_dao.get_by_id(teacher_id)
        if not teacher:
            raise HTTPException(status_code=404, detail="老师不存在或已离职")
        path = teacher.avatar_path or "default_avatar.png"
        return {"message": "获取成功", "data": {"avatar_path": path}}

    def delete_avatar(self, teacher_id: int) -> dict:
        teacher = self.teacher_dao.get_by_id(teacher_id)
        if not teacher:
            raise HTTPException(status_code=404, detail="老师不存在或已离职")
        if teacher.avatar_path:
            self.file_storage.delete(teacher.avatar_path)
            teacher.avatar_path = None
            try:
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")
            return {"message": "头像删除成功", "data": None}
        return {"message": "没有头像可删除", "data": None}