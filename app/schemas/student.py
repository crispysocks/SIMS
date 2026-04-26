from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class Gender(str, Enum):
    男 = '男'
    女 = '女'


class Education(str, Enum):
    专科 = '专科'
    本科 = '本科'
    硕士 = '硕士'


class StudentCreate(BaseModel):
    student_no: str = Field(..., min_length=1, max_length=20, description='学生编号，唯一')
    class_no: str = Field(..., min_length=1, max_length=20, description='班级编号')
    name: str = Field(..., min_length=1, max_length=50, description='学生姓名，非空')
    birth_place: str | None = Field(None, max_length=100, description='籍贯')
    graduate_school: str | None = Field(None, max_length=100, description='毕业院校')
    major: str | None = Field(None, max_length=50, description='专业')
    entrance_time: date = Field(..., description='入学时间')
    graduate_time: date | None = Field(None, description='毕业时间')
    education: str | None = Field(None, max_length=20, description='学历')
    advisor_name: str | None = Field(None, max_length=50, description='顾问姓名')
    age: int | None = Field(None, gt=0, lt=100, description='年龄 1-99')
    gender: Gender = Field(..., description='性别：男/女')
    phone: str | None = Field(None, max_length=20, description='联系电话')
    id_card: str | None = Field(None, max_length=18, description='身份证号')


class StudentUpdate(BaseModel):
    class_no: str | None = Field(None, max_length=20)
    name: str | None = Field(None, min_length=1, max_length=50)
    birth_place: str | None = Field(None, max_length=100)
    graduate_school: str | None = Field(None, max_length=100)
    major: str | None = Field(None, max_length=50)
    entrance_time: date | None = None
    graduate_time: date | None = None
    education: str | None = Field(None, max_length=20)
    advisor_name: str | None = Field(None, max_length=50)
    age: int | None = Field(None, gt=0, lt=100)
    gender: Gender | None = None
    phone: str | None = Field(None, max_length=20)
    id_card: str | None = Field(None, max_length=18)


class StudentRead(BaseModel):
    student_no: str
    class_no: str
    name: str
    birth_place: str | None
    graduate_school: str | None
    major: str | None
    entrance_time: date
    graduate_time: date | None
    education: str | None
    advisor_name: str | None
    age: int | None
    gender: str
    phone: str | None
    id_card: str | None

    class Config:
        from_attributes = True


class StudentListResponse(BaseModel):
    total: int
    items: list[StudentRead]
