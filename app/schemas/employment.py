from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class EmploymentUpsert(BaseModel):
    """就业信息新增或更新请求模型。"""

    employment_status: str | None = Field(default='待业', max_length=20, description='就业状态')
    employment_open_time: datetime | None = Field(default=None, description='就业开放时间')
    offer_time: datetime | None = Field(default=None, description='Offer下发时间')
    company_name: str | None = Field(default=None, max_length=100, description='公司名称')
    salary: Decimal | None = Field(default=None, ge=0, description='薪资')
    position: str | None = Field(default=None, max_length=50, description='工作岗位')
    work_location: str | None = Field(default=None, max_length=100, description='工作地点')
    contract_date: date | None = Field(default=None, description='签约日期')


class EmploymentRead(BaseModel):
    """就业信息详情响应模型。"""

    student_no: str
    employment_status: str
    employment_open_time: datetime | None
    offer_time: datetime | None
    company_name: str | None
    salary: Decimal | None
    position: str | None
    work_location: str | None
    contract_date: date | None
    isdeleted: int

    model_config = ConfigDict(from_attributes=True)
