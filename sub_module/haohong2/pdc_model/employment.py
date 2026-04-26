from pydantic import BaseModel
from datetime import date
from typing import Optional

from pydantic import BaseModel
from datetime import date
from typing import Optional

# 创建用
class EmploymentCreate(BaseModel):
    student_id: int
    open_time: date
    offer_time: date
    company: str
    salary: int

# 修改用
class EmploymentUpdate(BaseModel):
    open_time: Optional[date] = None
    offer_time: Optional[date] = None
    company: Optional[str] = None
    salary: Optional[int] = None
    status: Optional[str] = None

# 响应体
class EmploymentOut(BaseModel):
    id: int
    student_id: int
    open_time: date
    offer_time: Optional[date]
    company: str
    salary: int

class EmploymentQuery(BaseModel):
    student_id:Optional[int]=None
    company:Optional[str]=None
    min_salary:Optional[int] = None
    max_salary:Optional[int]=None


class EmploymentSearchResponse(BaseModel):
    student_id: int
    student_name: str
    class_id: int
    company: str
    salary: float
    open_time: Optional[date] = None
    offer_time: Optional[date] = None


