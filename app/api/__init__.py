from app.api.auth import router as auth_router
from app.api.classes import router as classes_router
from app.api.employment import router as employment_router
from app.api.employment_v2 import router as employment_v2_router
from app.api.scores import router as scores_router
from app.api.statistics import router as statistics_router
from app.api.students import router as students_router
from app.api.teachers import router as teachers_router

__all__ = [
    'auth_router',
    'classes_router',
    'employment_router',
    'employment_v2_router',
    'scores_router',
    'statistics_router',
    'students_router',
    'teachers_router',
]
