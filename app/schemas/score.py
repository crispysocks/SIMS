from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ScoreCreate(BaseModel):
    """成绩录入请求模型。"""

    student_no: str = Field(..., max_length=20, description='学生编号')
    exam_no: int = Field(..., ge=1, description='考核序次')
    score: int = Field(..., ge=0, le=100, description='成绩')
    exam_date: date | None = Field(None, description='考核日期')


class ScoreUpdate(BaseModel):
    """成绩修改请求模型。"""

    student_no: str = Field(..., max_length=20, description='学生编号')
    exam_no: int = Field(..., ge=1, description='考核序次')
    score: int = Field(..., ge=0, le=100, description='成绩')
    exam_date: date | None = Field(None, description='考核日期')


class ScoreDelete(BaseModel):
    """成绩删除请求模型。"""

    student_no: str = Field(..., max_length=20, description='学生编号')
    exam_no: int = Field(..., ge=1, description='考核序次')


class ScoreRead(BaseModel):
    """成绩详情响应模型。"""

    student_no: str
    exam_no: int
    score: int
    exam_date: date | None
    isdeleted: int

    model_config = ConfigDict(from_attributes=True)


class ExamRankingItem(BaseModel):
    """单次考试学生排名项。"""

    student_no: str
    student_name: str
    class_no: str
    class_name: str
    score: int
    rank: int


class ClassScoreReportItem(BaseModel):
    """班级成绩报表项。"""

    class_no: str
    class_name: str
    exam_no: int
    student_count: int
    avg_score: float
    excellent_rate: float
    pass_rate: float
    excellent_count: int
    pass_count: int
