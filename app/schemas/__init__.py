from app.schemas.classes import ClassCreate, ClassRead, ClassUpdate
from app.schemas.employment import (
    AvgSalaryByGroup,
    EmploymentCreate,
    EmploymentRead,
    EmploymentUpdate,
)
from app.schemas.score import ScoreCreate, ScoreDelete, ScoreRead, ScoreUpdate
from app.schemas.student import StudentCreate, StudentUpdate
from app.schemas.teacher import TeacherCreate, TeacherRead, TeacherUpdate

__all__ = [
    'AvgSalaryByGroup',
    'ClassCreate',
    'ClassRead',
    'ClassUpdate',
    'EmploymentCreate',
    'EmploymentRead',
    'EmploymentUpdate',
    'ScoreCreate',
    'ScoreDelete',
    'ScoreRead',
    'ScoreUpdate',
    'StudentCreate',
    'StudentUpdate',
    'TeacherCreate',
    'TeacherRead',
    'TeacherUpdate',
]
