# ============================================================
# api/__init__.py —— API 路由汇总文件
# ============================================================
# 这个文件的作用就像"通讯录"，把所有模块的接口都登记在一起。
# 当系统启动时，main.py 会从这里导入所有路由，注册到 FastAPI 应用中。
#
# 为什么要汇总？
#   每个业务模块（学生、老师、成绩等）都有自己的路由文件，
#   如果分散导入会很乱，所以统一从这里导出，方便管理。
# ============================================================

# 从各个模块导入路由，并给它们起个别名
# "router as xxx_router" 是为了避免名字冲突，因为每个模块里的路由对象都叫 router
from app.api.agent import router as agent_router
from app.api.auth import router as auth_router
from app.api.classes import router as classes_router
from app.api.employment import router as employment_router
from app.api.employment_v2 import router as employment_v2_router
from app.api.scores import router as scores_router
from app.api.statistics import router as statistics_router
from app.api.students import router as students_router
from app.api.teachers import router as teachers_router
from app.api.users import router as users_router

# __all__ 表示当其他文件用 "from app.api import *" 时，只导出下面这些名字
# 这是一种良好的封装习惯，控制哪些东西可以被外部使用
__all__ = [
    'agent_router',
    'auth_router',
    'classes_router',
    'employment_router',
    'employment_v2_router',
    'scores_router',
    'statistics_router',
    'students_router',
    'teachers_router',
    'users_router',
]
