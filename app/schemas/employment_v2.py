from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class EmploymentCreate(BaseModel):
    """v2 添加就业信息请求模型"""

    student_no: str = Field(..., max_length=20, description='学号')
    employment_open_time: Optional[datetime] = Field(default=None, description='就业开放时间')
    offer_time: Optional[datetime] = Field(default=None, description='Offer下发时间')
    company_name: str = Field(..., max_length=100, description='公司名称')
    salary: Decimal = Field(..., ge=0, description='薪资')
    position: Optional[str] = Field(default=None, max_length=50, description='工作岗位')
    work_location: Optional[str] = Field(default=None, max_length=100, description='工作地点')
    employment_status: Optional[str] = Field(default='在聘', max_length=20, description='就业状态')


class EmploymentUpdate(BaseModel):
    """v2 更新就业信息请求模型"""

    employment_open_time: Optional[datetime] = None
    offer_time: Optional[datetime] = None
    company_name: Optional[str] = Field(default=None, max_length=100, description='公司名称')
    salary: Optional[Decimal] = Field(default=None, ge=0, description='薪资')
    position: Optional[str] = Field(default=None, max_length=50, description='工作岗位')
    work_location: Optional[str] = Field(default=None, max_length=100, description='工作地点')
    employment_status: Optional[str] = Field(default=None, max_length=20, description='就业状态')


class EmploymentOut(BaseModel):
    """v2 就业信息基础响应模型"""

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
    """v2 就业信息搜索查询模型"""

    student_no: Optional[str] = None
    company_name: Optional[str] = None
    min_salary: Optional[Decimal] = None
    max_salary: Optional[Decimal] = None
    employment_status: Optional[str] = None
    position: Optional[str] = None
    work_location: Optional[str] = None


class EmploymentSearchResponse(BaseModel):
    """v2 就业信息搜索响应模型"""

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
