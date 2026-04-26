from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Gender = Literal['男', '女']


class StudentBase(BaseModel):
    """学生基础信息请求模型。"""

    class_id: int = Field(description='班级编号')
    name: str = Field(min_length=1, max_length=50, description='学生姓名')
    hometown: str | None = Field(default=None, max_length=100, description='籍贯')
    graduate_school: str | None = Field(default=None, max_length=100, description='毕业院校')
    major: str | None = Field(default=None, max_length=50, description='专业')
    enroll_date: date | None = Field(default=None, description='入学时间')
    graduate_date: date | None = Field(default=None, description='毕业时间')
    education: str | None = Field(default=None, description='学历')
    advisor_id: int | None = Field(default=None, description='顾问编号')
    age: int | None = Field(default=None, ge=1, le=120, description='年龄')
    gender: Gender | None = Field(default=None, description='性别')


class StudentCreate(StudentBase):
    """学生新增请求模型。"""

    student_no: str = Field(min_length=1, max_length=32, description='学生编号')


class StudentUpdate(BaseModel):
    """学生更新请求模型。"""

    class_id: int | None = None
    name: str | None = Field(default=None, min_length=1, max_length=50)
    hometown: str | None = Field(default=None, max_length=100)
    graduate_school: str | None = Field(default=None, max_length=100)
    major: str | None = Field(default=None, max_length=50)
    enroll_date: date | None = None
    graduate_date: date | None = None
    education: str | None = None
    advisor_id: int | None = None
    age: int | None = Field(default=None, ge=1, le=120)
    gender: Gender | None = None
    status: int | None = Field(default=None, ge=0, le=1)


class StudentRead(StudentBase):
    """学生详情响应模型。"""

    id: int
    student_no: str
    status: int

    model_config = ConfigDict(from_attributes=True)


class StudentListResponse(BaseModel):
    """学生分页列表响应模型。"""

    total: int
    items: list[StudentRead]
    page: int
    page_size: int
