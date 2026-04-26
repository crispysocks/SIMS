from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class EmploymentUpsert(BaseModel):
    """就业信息新增或更新请求模型。"""

    open_date: date | None = Field(default=None, description='就业开放时间')
    offer_date: date | None = Field(default=None, description='Offer下发时间')
    company_name: str | None = Field(default=None, max_length=100, description='公司名称')
    salary: Decimal | None = Field(default=None, ge=0, description='薪资')


class EmploymentRead(BaseModel):
    """就业信息详情响应模型。"""

    id: int
    student_id: int
    student_name: str | None = None
    class_id: int | None = None
    open_date: date | None = None
    offer_date: date | None = None
    company_name: str | None = None
    salary: Decimal | None = None
    status: int

    model_config = ConfigDict(from_attributes=True)
