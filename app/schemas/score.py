# ============================================================
# schemas/score.py —— 成绩数据校验模型（Schema）
# ============================================================
# 这个文件定义了"成绩"相关的数据校验规则。
#
# 包含的 Schema：
#   - ScoreCreate: 录入成绩时的校验规则
#   - ScoreUpdate: 修改成绩时的校验规则
#   - ScoreRead: 返回成绩时的数据格式
#   - ExamRankingItem: 单次考试排名项
#   - ClassScoreReportItem: 班级成绩报表项
# ============================================================

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ScoreCreate(BaseModel):
    """
    成绩录入请求模型。

    校验规则：
        - student_no: 必填，最多 20 个字符
        - exam_no: 必填，必须 >= 1（第几次考试）
        - score: 必填，0-100 分之间
        - exam_date: 可选，考核日期
    """

    student_no: str = Field(..., max_length=20, description='学生编号')
    exam_no: int = Field(..., ge=1, description='考核序次')
    score: int = Field(..., ge=0, le=100, description='成绩')
    exam_date: date | None = Field(None, description='考核日期')


class ScoreUpdate(BaseModel):
    """
    成绩修改请求模型。

    和 ScoreCreate 类似，但用于更新已有成绩。
    """

    student_no: str = Field(..., max_length=20, description='学生编号')
    exam_no: int = Field(..., ge=1, description='考核序次')
    score: int = Field(..., ge=0, le=100, description='成绩')
    exam_date: date | None = Field(None, description='考核日期')


class ScoreRead(BaseModel):
    """
    成绩详情响应模型。

    返回成绩的所有字段，包括逻辑删除标记。
    """

    student_no: str
    exam_no: int
    score: int
    exam_date: date | None
    isdeleted: int

    model_config = ConfigDict(from_attributes=True)


class ExamRankingItem(BaseModel):
    """
    单次考试学生排名项。

    用于返回某次考试的学生排名列表，包含：
        - 学生基本信息（编号、姓名、班级）
        - 分数和排名
    """

    student_no: str
    student_name: str
    class_no: str
    class_name: str
    score: int
    rank: int


class ClassScoreReportItem(BaseModel):
    """
    班级成绩报表项。

    用于返回某个班级的成绩统计信息，包含：
        - 班级基本信息
        - 参考人数
        - 平均分
        - 优秀率和及格率
        - 优秀人数和及格人数
    """

    class_no: str
    class_name: str
    exam_no: int
    student_count: int
    avg_score: float
    excellent_rate: float
    pass_rate: float
    excellent_count: int
    pass_count: int
