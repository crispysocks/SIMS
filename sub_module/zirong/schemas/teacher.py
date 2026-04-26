from pydantic import BaseModel, Field
from typing import Optional

# =============== 老师 ===============
class TeacherCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=20, description="老师姓名")
    course_id: int = Field(..., gt=0, description="所属课程ID")
    gender: Optional[str] = Field(None, max_length=5, description="性别")
    phone_number: Optional[str] = Field(None, max_length=20, description="联系电话")
    status: int = Field(0, ge=0, le=1, description="状态：0正常，1离职")

    class Config:
        from_attributes = True

class TeacherUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=20, description="老师姓名")
    course_id: Optional[int] = Field(None, gt=0, description="所属课程ID")
    gender: Optional[str] = Field(None, max_length=5, description="性别")
    phone_number: Optional[str] = Field(None, max_length=20, description="联系电话")
    status: Optional[int] = Field(None, ge=0, le=1, description="状态：0正常，1离职")

    class Config:
        from_attributes = True

# =============== 课程 ===============
class CourseCreate(BaseModel):
    course_name: str = Field(..., min_length=1, max_length=100, description="课程名称")

    class Config:
        from_attributes = True

class CourseUpdate(BaseModel):
    course_name: Optional[str] = Field(None, min_length=1, max_length=100, description="课程名称")

    class Config:
        from_attributes = True