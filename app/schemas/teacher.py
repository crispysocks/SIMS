from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TeacherCreate(BaseModel):
    """老师新增请求模型。"""

    name: str = Field(min_length=1, max_length=50, description='老师姓名')
    subject: str = Field(min_length=1, max_length=50, description='任教科目')
    gender: str | None = Field(default=None, max_length=10, description='性别')
    phone: str | None = Field(default=None, max_length=20, description='联系电话')


class TeacherUpdate(BaseModel):
    """老师更新请求模型。"""

    name: str | None = Field(default=None, min_length=1, max_length=50)
    subject: str | None = Field(default=None, min_length=1, max_length=50)
    gender: str | None = Field(default=None, max_length=10)
    phone: str | None = Field(default=None, max_length=20)
    status: int | None = Field(default=None, ge=0, le=1)


class TeacherRead(BaseModel):
    """老师详情响应模型。"""

    id: int
    name: str
    subject: str
    gender: str | None = None
    phone: str | None = None
    status: int
    create_time: datetime | None = None
    update_time: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class CourseCreate(BaseModel):
    """课程新增请求模型。"""

    course_name: str = Field(min_length=1, max_length=100, description='课程名称')
    teacher_id: int = Field(description='老师ID')


class CourseUpdate(BaseModel):
    """课程更新请求模型。"""

    course_name: str | None = Field(default=None, min_length=1, max_length=100)
    teacher_id: int | None = None


class CourseRead(BaseModel):
    """课程详情响应模型。"""

    id: int
    course_name: str
    teacher_id: int
    teacher_name: str | None = None

    model_config = ConfigDict(from_attributes=True)
