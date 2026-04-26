from app.schemas.classes import ClassCreate, ClassRead, ClassUpdate
from app.schemas.employment import EmploymentRead, EmploymentUpsert
from app.schemas.score import ScoreCreate, ScoreDelete, ScoreRead, ScoreUpdate
from app.schemas.student import StudentCreate, StudentListResponse, StudentRead, StudentUpdate
from app.schemas.teacher import (
    CourseCreate,
    CourseRead,
    CourseUpdate,
    TeacherCreate,
    TeacherRead,
    TeacherUpdate,
)

__all__ = [
    'ClassCreate',
    'ClassRead',
    'ClassUpdate',
    'CourseCreate',
    'CourseRead',
    'CourseUpdate',
    'EmploymentRead',
    'EmploymentUpsert',
    'ScoreCreate',
    'ScoreDelete',
    'ScoreRead',
    'ScoreUpdate',
    'StudentCreate',
    'StudentListResponse',
    'StudentRead',
    'StudentUpdate',
    'TeacherCreate',
    'TeacherRead',
    'TeacherUpdate',
]
