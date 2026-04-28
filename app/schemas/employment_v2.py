# ============================================================
# schemas/employment_v2.py —— 就业信息 v2 版数据校验模型
# ============================================================
# 这个文件是 employment.py 的升级版，用于就业管理 v2 接口。
#
# v2 和 v1 的区别：
#   - v2 的 student_no 在 Create 模型里（v1 是从 URL 参数传入）
#   - v2 支持批量操作
#   - v2 的查询条件更灵活
#
# 包含的 Schema：
#   - EmploymentCreate: 新增就业信息
#   - EmploymentUpdate: 更新就业信息
#   - EmploymentOut: 就业信息基础响应
#   - EmploymentQuery: 搜索查询条件
#   - EmploymentSearchResponse: 搜索结果响应（包含学生姓名、班级）
# ============================================================

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class EmploymentCreate(BaseModel):
    """
    v2 添加就业信息请求模型。

    和 v1 的区别：
        - student_no 在这里作为必填字段传入
        - company_name 和 salary 也是必填的
    """

    student_no: str = Field(..., max_length=20, description='学号')
    employment_open_time: Optional[datetime] = Field(default=None, description='就业开放时间')
    offer_time: Optional[datetime] = Field(default=None, description='Offer下发时间')
    company_name: str = Field(..., max_length=100, description='公司名称')
    salary: Decimal = Field(..., ge=0, description='薪资')
    position: Optional[str] = Field(default=None, max_length=50, description='工作岗位')
    work_location: Optional[str] = Field(default=None, max_length=100, description='工作地点')
    employment_status: Optional[str] = Field(default='在聘', max_length=20, description='就业状态')


class EmploymentUpdate(BaseModel):
    """
    v2 更新就业信息请求模型。

    所有字段都是可选的，前端可以只传要修改的字段。
    """

    employment_open_time: Optional[datetime] = None
    offer_time: Optional[datetime] = None
    company_name: Optional[str] = Field(default=None, max_length=100, description='公司名称')
    salary: Optional[Decimal] = Field(default=None, ge=0, description='薪资')
    position: Optional[str] = Field(default=None, max_length=50, description='工作岗位')
    work_location: Optional[str] = Field(default=None, max_length=100, description='工作地点')
    employment_status: Optional[str] = Field(default=None, max_length=20, description='就业状态')


class EmploymentOut(BaseModel):
    """
    v2 就业信息基础响应模型。

    返回就业表里的原始字段，不包含学生姓名等关联信息。
    """

    student_no: str
    employment_open_time: Optional[datetime]
    offer_time: Optional[datetime]
    company_name: str
    salary: Decimal
    position: Optional[str]
    work_location: Optional[str]
    employment_status: str
    isdeleted: int

    model_config = ConfigDict(from_attributes=True)


class EmploymentQuery(BaseModel):
    """
    v2 就业信息搜索查询模型。

    所有字段都是可选的，用于组合查询。
    比如：只传 company_name='腾讯'，就查所有在腾讯就业的学生。
    """

    student_no: Optional[str] = None
    company_name: Optional[str] = None
    min_salary: Optional[Decimal] = None
    max_salary: Optional[Decimal] = None
    employment_status: Optional[str] = None
    position: Optional[str] = None
    work_location: Optional[str] = None


class EmploymentSearchResponse(BaseModel):
    """
    v2 就业信息搜索响应模型。

    在 EmploymentOut 的基础上，额外返回：
        - student_name: 学生姓名（从学生表关联查询）
        - class_no: 班级编号（从学生表关联查询）

    这样前端搜索后可以直接显示学生姓名，不用再去查学生表。
    """

    student_no: Optional[str] = None
    student_name: Optional[str] = None
    class_no: Optional[str] = None
    company_name: Optional[str] = None
    salary: Optional[Decimal] = None
    employment_open_time: Optional[datetime] = None
    offer_time: Optional[datetime] = None
    position: Optional[str] = None
    work_location: Optional[str] = None
    employment_status: Optional[str] = None
    isdeleted: int = 0

    model_config = ConfigDict(from_attributes=True)
