from pydantic import BaseModel
class TeacherCreate(BaseModel):
    name: str
    subject: str
    status: str = "正常"

class TeacherUpdate(BaseModel):
    name: str = None
    subject: str = None
    status: str = None

class CourseCreate(BaseModel):
    course_name: str
    teacher_id: int

class CourseUpdate(BaseModel):
    course_name: str = None
    teacher_id: int = None