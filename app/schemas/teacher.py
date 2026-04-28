# ============================================================
# schemas/teacher.py —— 教师数据校验模型（Schema）
# ============================================================
# 这个文件定义了"教师"相关的数据校验规则。
#
# 包含的 Schema：
#   - Gender: 性别枚举（男/女）
#   - TeacherBase: 教师基础信息（Create 和 Read 都继承它）
#   - TeacherCreate: 新增教师时的校验规则
#   - TeacherUpdate: 更新教师时的校验规则
#   - TeacherRead: 返回教师信息时的数据格式
#   - TeacherGenderStat: 教师性别统计项
# ============================================================

from datetime import date

from pydantic import BaseModel, ConfigDict, Field
from enum import Enum


class Gender(str, Enum):
    """
    性别枚举。

    只能从 '男' 或 '女' 中选择。
    """
    男 = '男'
    女 = '女'


class TeacherBase(BaseModel):
    """
    教师基础信息模型。

    定义了教师共有的字段，Create 和 Read 都继承它。
    """

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
    """
    新增教师时的请求模型。

    直接继承 TeacherBase，因为新增时需要所有字段。
    """
    pass


class TeacherUpdate(BaseModel):
    """
    更新教师时的请求模型。

    所有字段都是可选的，前端可以只传要修改的字段。
    """

    name: str | None = Field(None, min_length=1, max_length=50)
    gender: str | None = Field(None, max_length=10)
    phone: str | None = Field(None, max_length=20)
    email: str | None = Field(None, max_length=100)
    id_card: str | None = Field(None, max_length=18)
    birthday: date | None = None
    hire_date: date | None = None
    subject: str | None = Field(None, max_length=50)


class TeacherRead(TeacherBase):
    """
    教师信息响应模型。

    返回教师的所有字段，包括逻辑删除标记。
    """

    model_config = ConfigDict(from_attributes=True)

    isdeleted: int


class TeacherGenderStat(BaseModel):
    """
    教师性别统计项。

    用于统计接口，返回某种性别的教师数量和占比。
    """

    gender: str
    count: int
    ratio: float
