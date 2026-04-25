# from datetime import date
#
# from pydantic import BaseModel, Field
# from sqlalchemy import Enum
#
#
# class Sgender(str,Enum):#枚举验证
#     man = '男'
#     woman = '女'
#
# class Student_add(BaseModel):#学生请求体
#     student_id:int = Field()
#     class_id:int
#     student_name:str
#     hometown:str
#     graduate_school:str
#     major:str
#     enroll_date:date
#     graduate_date:date
#     education:str
#     advisor_id:int
#     age:int
#     gender:Sgender
#     status:int
#
#
#
# class Student_response(BaseModel):#学生响应体
#     student_id: int
#     class_id: int
#     student_name: str
#     hometown: str
#     graduate_school: str
#     major: str
#     enroll_date: date
#     graduate_date: date
#     education: str
#     advisor_id: int
#     age: int
#     gender: str
#
#     class Config:
#         orm_mode = True
#
#
# class Student_update(BaseModel):#修改模型
#     class_id: int
#     student_name: str
#     hometown: str
#     graduate_school: str
#     major: str
#     enroll_date: date
#     graduate_date: date
#     education: str
#     advisor_id: int
#     age: int
#     gender: Sgender | None = None
#


from pydantic import BaseModel, Field
from datetime import date
from enum import Enum

# ====================== 枚举定义 ======================
class Gender(str, Enum):
    男 = "男"
    女 = "女"

class Education(str, Enum):
    专科 = "专科"
    本科 = "本科"
    硕士 = "硕士"

# ====================== 新增学生（请求体）======================
class Student_add(BaseModel):
    student_id: int = Field(..., description="学生编号，唯一")
    class_id: int = Field(..., description="班级编号")
    student_name: str = Field(..., min_length=1, max_length=50, description="学生姓名，非空")
    hometown: str | None = Field(None, max_length=100, description="籍贯")
    graduate_school: str  = Field(..., max_length=100, description="毕业院校")
    major: str = Field(..., max_length=50, description="专业，非空")
    enroll_date: date = Field(..., description="入学日期")
    graduate_date: date  = Field(..., description="毕业日期")
    education: Education = Field(..., description="学历：专科/本科/硕士")
    advisor_id: int = Field(..., description="顾问编号")
    age: int = Field(..., gt=0, lt=100, description="年龄 1-99")
    gender: Gender = Field(..., description="性别：男/女")
    status: int = Field(1, description="状态 1可查询0不可查询")

# ====================== 修改学生（所有字段可选）======================
class Student_update(BaseModel):
    class_id: int | None = None
    student_name: str | None = Field(None, min_length=1, max_length=50)
    hometown: str | None = Field(None, max_length=100)
    graduate_school: str | None = Field(None, max_length=100)
    major: str | None = Field(None, max_length=50)
    enroll_date: date | None = None
    graduate_date: date | None = None
    education: Education | None = None
    advisor_id: int | None = None
    age: int | None = Field(None, gt=0, lt=100)
    gender: Gender | None = None
    status: int | None = None

# ====================== 返回模型 ======================
class Student_response(BaseModel):
    student_id: int
    class_id: int
    student_name: str
    hometown: str | None
    graduate_school: str | None
    major: str
    enroll_date: date
    graduate_date: date | None
    education: str
    advisor_id: int
    age: int
    gender: str

    class Config:
        from_attributes = True