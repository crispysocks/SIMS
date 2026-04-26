from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class EmploymentCreate(BaseModel):
    """v2 添加就业信息请求模型"""

    student_no: str
    open_time: date
    offer_time: date
    company: str
    salary: int


class EmploymentUpdate(BaseModel):
    """v2 更新就业信息请求模型"""

    open_time: Optional[date] = None
    offer_time: Optional[date] = None
    company: Optional[str] = None
    salary: Optional[int] = None
    status: Optional[str] = None


class EmploymentOut(BaseModel):
    """v2 就业信息基础响应模型"""

    student_no: str
    open_time: date
    offer_time: Optional[date]
    company: str
    salary: int

    model_config = ConfigDict(from_attributes=True)


class EmploymentQuery(BaseModel):
    """v2 就业信息搜索查询模型"""

    student_no: Optional[str] = None
    company: Optional[str] = None
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None


class EmploymentSearchResponse(BaseModel):
    """v2 就业信息搜索响应模型"""

    student_no: str
    student_name: str
    class_no: str
    company: str
    salary: float
    open_time: Optional[date] = None
    offer_time: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)
