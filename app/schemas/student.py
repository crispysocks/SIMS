# ============================================================
# schemas/student.py —— 学生数据校验模型（Schema）
# ============================================================
# 这个文件定义了"学生"相关的数据校验规则。
#
# 包含的 Schema：
#   - Gender: 性别枚举（男/女）
#   - Education: 学历枚举（专科/本科/硕士）
#   - StudentCreate: 新增学生时的校验规则
#   - StudentUpdate: 更新学生时的校验规则
#   - StudentRead: 返回学生信息时的数据格式
#
# 枚举的作用：
#   限制字段只能从固定的几个值中选择，防止出现"男"/"male"等不一致的值。
# ============================================================

from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Gender(str, Enum):
    """
    性别枚举。

    只能从 '男' 或 '女' 中选择，
    这样数据库里不会出现 'Male'、'male' 等不一致的值。
    """
    男 = '男'
    女 = '女'


class Education(str, Enum):
    """
    学历枚举。

    只能从 '专科'、'本科'、'硕士' 中选择。
    """
    专科 = '专科'
    本科 = '本科'
    硕士 = '硕士'


class StudentCreate(BaseModel):
    """
    新增学生时的请求模型。

    校验规则：
        - student_no: 必填，1-20 个字符
        - class_no: 必填，1-20 个字符
        - name: 必填，1-50 个字符
        - age: 可选，1-99 之间的整数
        - gender: 必填，必须是 Gender 枚举中的值
        - education: 必填，必须是 Education 枚举中的值
    """

    student_no: str = Field(..., min_length=1, max_length=20, description='学生编号，唯一')
    class_no: str = Field(..., min_length=1, max_length=20, description='班级编号')
    name: str = Field(..., min_length=1, max_length=50, description='学生姓名，非空')
    birth_place: str | None = Field(None, max_length=100, description='籍贯')
    graduate_school: str | None = Field(None, max_length=100, description='毕业院校')
    major: str | None = Field(None, max_length=50, description='专业')
    entrance_time: date = Field(..., description='入学时间')
    graduate_time: date | None = Field(None, description='毕业时间')
    education: Education = Field(..., max_length=20, description='学历')
    advisor_name: str | None = Field(None, max_length=50, description='顾问姓名')
    age: int | None = Field(None, gt=0, lt=100, description='年龄 1-99')
    gender: Gender = Field(..., description='性别：男/女')
    phone: str | None = Field(None, max_length=20, description='联系电话')
    id_card: str | None = Field(None, max_length=18, description='身份证号')


class StudentUpdate(BaseModel):
    """
    更新学生时的请求模型。

    所有字段都是可选的，前端可以只传要修改的字段。
    """

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
    """
    学生信息响应模型。

    返回学生的所有字段给前端展示。
    """

    student_no: str
    class_no: str
    name: str
    birth_place: str | None
    graduate_school: str | None
    major: str | None
    entrance_time: date
    graduate_time: date | None
    education: str
    advisor_name: str | None
    age: int | None
    gender: str
    phone: str | None
    id_card: str | None

    model_config = ConfigDict(from_attributes=True)
