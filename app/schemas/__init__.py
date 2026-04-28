# ============================================================
# schemas/__init__.py —— 数据校验模型汇总文件
# ============================================================
# 这个文件就像"目录"，把所有数据校验类（Schema）集中在一起。
#
# 什么是 Schema？
#   Schema 是 Pydantic 模型，用来：
#   1. 校验前端传来的数据是否符合要求（比如长度、类型）
#   2. 把后端数据转换成 JSON 格式返回给前端
#
# 为什么要汇总？
#   其他模块导入时可以从这里统一导入，
#   不用记住每个 Schema 具体在哪个文件里。
#
# 例如：
#   from app.schemas import StudentCreate, StudentUpdate
#   等价于：
#   from app.schemas.student import StudentCreate, StudentUpdate
# ============================================================

from app.schemas.classes import ClassCreate, ClassRead, ClassUpdate
from app.schemas.employment import (
    AvgSalaryByGroup,
    EmploymentCreate,
    EmploymentRead,
    EmploymentUpdate,
)
from app.schemas.score import ScoreCreate, ScoreRead, ScoreUpdate
from app.schemas.student import StudentCreate, StudentUpdate
from app.schemas.teacher import TeacherCreate, TeacherRead, TeacherUpdate

# __all__ 控制 "from app.schemas import *" 时导出哪些类
__all__ = [
    'AvgSalaryByGroup',
    'ClassCreate',
    'ClassRead',
    'ClassUpdate',
    'EmploymentCreate',
    'EmploymentRead',
    'EmploymentUpdate',
    'ScoreCreate',

    'ScoreRead',
    'ScoreUpdate',
    'StudentCreate',
    'StudentUpdate',
    'TeacherCreate',
    'TeacherRead',
    'TeacherUpdate',
]
