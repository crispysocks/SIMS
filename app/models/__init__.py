# ============================================================
# models/__init__.py —— 数据模型汇总文件
# ============================================================
# 这个文件就像"花名册"，把所有数据模型类登记在一起。
#
# 为什么要汇总？
#   其他文件需要导入模型时，可以从这里统一导入，
#   不用记住每个模型具体在哪个文件里。
#
# 比如：
#   from app.models import Student, Teacher
#   等价于：
#   from app.models.student import Student
#   from app.models.teacher import Teacher
# ============================================================

from app.models.classes import ClassInfo
from app.models.employment import Employment
from app.models.score import Score
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.user import User

# __all__ 控制 "from app.models import *" 时导出哪些类
__all__ = [
    'ClassInfo',
    'Employment',
    'Score',
    'Student',
    'Teacher',
    'User',
]
