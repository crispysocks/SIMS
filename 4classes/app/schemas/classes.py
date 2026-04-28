# 导入时间类型
from datetime import date, datetime
# 可选字段工具
from typing import Optional
# 数据校验基类
from pydantic import BaseModel

# 新增班级用，前端传什么就写什么
class ClassCreate(BaseModel):
    class_name: str                # 必须填
    start_time: Optional[date] = None  # 可选
    head_teacher_id: Optional[int] = None  # 可选

# 修改班级用，所有都可以选填
class ClassUpdate(BaseModel):
    class_name: Optional[str] = None
    start_time: Optional[date] = None
    head_teacher_id: Optional[int] = None

# 返回给前端的数据格式
class ClassResponse(BaseModel):
    class_id: int
    class_name: str
    start_time: Optional[date] = None
    head_teacher_id: Optional[int] = None
    is_deleted: int = 0
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    # 允许把数据库对象直接转成JSON
    model_config = {"from_attributes": True}