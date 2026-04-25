# 日期、时间类型
from datetime import date, datetime
# 可选类型（可以传null）
from typing import Optional
# Pydantic基类，用来校验前端数据
from pydantic import BaseModel

# 新增班级时，前端必须传这些字段
class ClassCreate(BaseModel):
    class_name: str                # 班级名称（必填）
    start_time: Optional[date] = None  # 开课时间（可选）
    head_teacher_id: Optional[int] = None  # 班主任ID（可选）
    lecturer_id: Optional[int] = None  # 授课老师ID（可选）

# 修改班级时，所有字段都是可选
class ClassUpdate(BaseModel):
    class_name: Optional[str] = None
    start_time: Optional[date] = None
    head_teacher_id: Optional[int] = None
    lecturer_id: Optional[int] = None

# 返回给前端的班级数据格式
class ClassResponse(BaseModel):
    class_id: int
    class_name: str
    start_time: Optional[date] = None
    head_teacher_id: Optional[int] = None
    lecturer_id: Optional[int] = None
    is_deleted: int = 0
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    # 允许从ORM模型（数据库对象）创建数据
    model_config = {"from_attributes": True}