from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.teacher import TeacherRead


class ClassBase(BaseModel):
    class_no: str = Field(..., min_length=1, max_length=20, description='班级编号')
    class_name: str = Field(..., min_length=1, max_length=50, description='班级名称')
    class_open_time: date = Field(..., description='开课时间')
    head_teacher_no: str | None = Field(None, max_length=20, description='班主任编号')
    instructor_no: str | None = Field(None, max_length=20, description='授课老师编号')
    description: str | None = Field(None, max_length=500, description='班级描述')


class ClassCreate(ClassBase):
    pass


class ClassUpdate(BaseModel):
    class_name: str | None = Field(None, min_length=1, max_length=50)
    class_open_time: date | None = None
    head_teacher_no: str | None = Field(None, max_length=20)
    instructor_no: str | None = Field(None, max_length=20)
    description: str | None = Field(None, max_length=500)


class ClassRead(ClassBase):
    model_config = ConfigDict(from_attributes=True)

    isdeleted: int


class ClassReadDetail(ClassRead):
    headteacher: TeacherRead | None = None
    instructor: TeacherRead | None = None
