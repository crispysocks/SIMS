# ============================================================
# schemas/employment.py —— 就业信息数据校验模型（Schema）
# ============================================================
# 这个文件定义了"就业信息"相关的数据校验规则。
#
# 包含的 Schema：
#   - EmploymentCreate: 新增就业信息时的校验规则
#   - EmploymentUpdate: 更新就业信息时的校验规则
#   - EmploymentRead: 返回就业信息时的数据格式
#   - AvgSalaryByGroup: 分组平均工资的响应格式
# ============================================================

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class EmploymentCreate(BaseModel):
    """
    新增就业信息时的请求模型。

    注意：
        - student_no 不在 Create 模型里，因为它是 URL 参数传入的
        - 默认值用 Field(default=...) 设置
    """

    # default='待业' 表示如果没有传这个字段，默认是"待业"
    employment_status: str | None = Field(default='待业', max_length=20, description='就业状态')

    employment_open_time: datetime | None = Field(default=None, description='就业开放时间')
    offer_time: datetime | None = Field(default=None, description='Offer下发时间')
    company_name: str | None = Field(default=None, max_length=100, description='公司名称')

    # Decimal 是精确小数类型，适合金额
    # ge=0 表示必须大于等于 0（不能是负数）
    salary: Decimal | None = Field(default=None, ge=0, description='薪资')

    position: str | None = Field(default=None, max_length=50, description='工作岗位')
    work_location: str | None = Field(default=None, max_length=100, description='工作地点')


class EmploymentUpdate(BaseModel):
    """
    更新就业信息时的请求模型。

    所有字段都是可选的，前端可以只传要修改的字段。
    """

    employment_status: str | None = Field(default=None, max_length=20, description='就业状态')
    employment_open_time: datetime | None = Field(default=None, description='就业开放时间')
    offer_time: datetime | None = Field(default=None, description='Offer下发时间')
    company_name: str | None = Field(default=None, max_length=100, description='公司名称')
    salary: Decimal | None = Field(default=None, ge=0, description='薪资')
    position: str | None = Field(default=None, max_length=50, description='工作岗位')
    work_location: str | None = Field(default=None, max_length=100, description='工作地点')


class EmploymentRead(BaseModel):
    """
    就业信息详情响应模型。

    包含所有字段，用于返回完整的就业信息给前端。
    """

    student_no: str
    employment_status: str
    employment_open_time: datetime | None
    offer_time: datetime | None
    company_name: str | None
    salary: Decimal | None
    position: str | None
    work_location: str | None
    isdeleted: int

    # 允许从 ORM 对象直接创建
    model_config = ConfigDict(from_attributes=True)


class AvgSalaryByGroup(BaseModel):
    """
    分组平均工资响应模型。

    用于统计接口，返回某个分组（如班级、性别）的平均薪资。
    """

    group_key: str = Field(description='分组标识，如班级编号或性别')
    avg_salary: Decimal | None = Field(description='该组的平均薪资')

    model_config = ConfigDict(from_attributes=True)
