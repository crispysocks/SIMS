from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.response import ApiResponse
from app.services import statistics as statistics_service

router = APIRouter(
    prefix='/api/statistics',
    tags=['统计分析'],
)


@router.get('/age-filter')
def age_filter(
    age: int = Query(30, ge=0),
    db: Session = Depends(get_db),
) -> ApiResponse[list[dict]]:
    """查询达到指定年龄的学生。"""
    data = statistics_service.find_students_by_age(db, age)
    return ApiResponse(message='查询成功', data=data)


@router.get('/class-gender')
def class_gender(
    db: Session = Depends(get_db),
) -> ApiResponse[list[dict]]:
    """统计每个班级的男女生人数。"""
    data = statistics_service.get_class_gender_stats(db)
    return ApiResponse(message='查询成功', data=data)


@router.get('/always-above')
def always_above(
    score: int = Query(80, ge=0, le=100),
    db: Session = Depends(get_db),
) -> ApiResponse[list[dict]]:
    """查询每次考试都高于指定分数的学生。"""
    data = statistics_service.get_students_always_above_score(db, score)
    return ApiResponse(message='查询成功', data=data)


@router.get('/failed-twice')
def failed_twice(
    db: Session = Depends(get_db),
) -> ApiResponse[list[dict]]:
    """查询两次及以上不及格的学生。"""
    data = statistics_service.get_students_failed_twice_or_more(db)
    return ApiResponse(message='查询成功', data=data)


@router.get('/class-avg-score')
def class_avg_score(
    db: Session = Depends(get_db),
) -> ApiResponse[list[dict]]:
    """统计班级平均分。"""
    data = statistics_service.get_class_avg_scores_by_exam(db)
    return ApiResponse(message='查询成功', data=data)


@router.get('/top-salary')
def top_salary(
    db: Session = Depends(get_db),
) -> ApiResponse[list[dict]]:
    """统计高薪学生。"""
    data = statistics_service.get_top_salary_students(db)
    return ApiResponse(message='查询成功', data=data)


@router.get('/student-offer-duration')
def student_offer_duration(
    db: Session = Depends(get_db),
) -> ApiResponse[list[dict]]:
    """统计个人就业时长。"""
    data = statistics_service.get_student_offer_duration(db)
    return ApiResponse(message='查询成功', data=data)


@router.get('/class-offer-duration')
def class_offer_duration(
    db: Session = Depends(get_db),
) -> ApiResponse[list[dict]]:
    """统计班级平均就业时长。"""
    data = statistics_service.get_class_avg_offer_duration(db)
    return ApiResponse(message='查询成功', data=data)
