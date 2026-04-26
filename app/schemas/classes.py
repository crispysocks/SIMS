from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class ClassCreate(BaseModel):
    """班级新增请求模型。"""

    class_name: str = Field(min_length=1, max_length=50, description='班级名称')
    start_time: date | None = Field(default=None, description='开课时间')
    head_teacher_id: int | None = Field(default=None, description='班主任ID')
    lecturer_id: int | None = Field(default=None, description='授课老师ID')


class ClassUpdate(BaseModel):
    """班级更新请求模型。"""

    class_name: str | None = Field(default=None, min_length=1, max_length=50)
    start_time: date | None = None
    head_teacher_id: int | None = None
    lecturer_id: int | None = None
    is_deleted: int | None = Field(default=None, ge=0, le=1)


class ClassRead(BaseModel):
    """班级详情响应模型。"""

    class_id: int
    class_name: str
    start_time: date | None = None
    head_teacher_id: int | None = None
    lecturer_id: int | None = None
    is_deleted: int
    create_time: datetime | None = None
    update_time: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
