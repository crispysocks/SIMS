from datetime import date

from pydantic import BaseModel, ConfigDict, Field
from enum import Enum

class Gender(str, Enum):
    男 = '男'
    女 = '女'

class TeacherBase(BaseModel):
    teacher_no: str = Field(..., min_length=1, max_length=20, description='老师编号')
    name: str = Field(..., min_length=1, max_length=50, description='老师姓名')
    gender: Gender = Field(..., description='性别：男/女')
    phone: str | None = Field(None, max_length=20, description='联系电话')
    email: str | None = Field(None, max_length=100, description='电子邮箱')
    id_card: str | None = Field(None, max_length=18, description='身份证号')
    birthday: date | None = Field(None, description='出生日期')
    hire_date: date | None = Field(None, description='入职日期')
    subject: str | None = Field(None, max_length=50, description='授课科目')


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=50)
    gender: str | None = Field(None, max_length=10)
    phone: str | None = Field(None, max_length=20)
    email: str | None = Field(None, max_length=100)
    id_card: str | None = Field(None, max_length=18)
    birthday: date | None = None
    hire_date: date | None = None
    subject: str | None = Field(None, max_length=50)


class TeacherRead(TeacherBase):
    model_config = ConfigDict(from_attributes=True)

    isdeleted: int


class TeacherGenderStat(BaseModel):
    gender: str
    count: int
    ratio: float
