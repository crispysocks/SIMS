from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ScoreCreate(BaseModel):
    """成绩录入请求模型。"""

    student_no: str = Field(..., max_length=20, description='学生编号')
    exam_no: int = Field(..., ge=1, description='考核序次')
    exam_name: str = Field(..., max_length=50, description='考试名称')
    score: Decimal = Field(..., ge=0, le=100, description='成绩')
    exam_date: date | None = Field(None, description='考核日期')
    remark: str | None = Field(None, max_length=200, description='备注')


class ScoreUpdate(BaseModel):
    """成绩修改请求模型。"""

    student_no: str = Field(..., max_length=20, description='学生编号')
    exam_no: int = Field(..., ge=1, description='考核序次')
    exam_name: str = Field(..., max_length=50, description='考试名称')
    score: Decimal = Field(..., ge=0, le=100, description='成绩')
    exam_date: date | None = Field(None, description='考核日期')
    remark: str | None = Field(None, max_length=200, description='备注')


class ScoreDelete(BaseModel):
    """成绩删除请求模型。"""

    student_no: str = Field(..., max_length=20, description='学生编号')
    exam_no: int = Field(..., ge=1, description='考核序次')
    exam_name: str = Field(..., max_length=50, description='考试名称')


class ScoreRead(BaseModel):
    """成绩详情响应模型。"""

    student_no: str
    exam_no: int
    exam_name: str
    score: Decimal
    exam_date: date | None
    remark: str | None
    isdeleted: int

    model_config = ConfigDict(from_attributes=True)
