from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services import statistics as statistics_service

router = APIRouter(
    prefix='/api/statistics',
    tags=['统计分析'],
)


@router.get('/age-filter')
def age_filter(
    age: int = Query(30, ge=0),
    db: Session = Depends(get_db),
):
    """查询达到指定年龄的学生。"""
    return statistics_service.find_students_by_age(db, age)


@router.get('/class-gender')
def class_gender(
    db: Session = Depends(get_db),
):
    """统计每个班级的男女生人数。"""
    return statistics_service.get_class_gender_stats(db)


@router.get('/always-above')
def always_above(
    score: int = Query(80, ge=0, le=100),
    db: Session = Depends(get_db),
):
    """查询每次考试都高于指定分数的学生。"""
    return statistics_service.get_students_always_above_score(db, score)


@router.get('/failed-twice')
def failed_twice(
    db: Session = Depends(get_db),
):
    """查询两次及以上不及格的学生。"""
    return statistics_service.get_students_failed_twice_or_more(db)


@router.get('/class-avg-score')
def class_avg_score(
    db: Session = Depends(get_db),
):
    """统计班级平均分。"""
    return statistics_service.get_class_avg_scores_by_exam(db)


@router.get('/top-salary')
def top_salary(
    db: Session = Depends(get_db),
):
    """统计高薪学生。"""
    return statistics_service.get_top_salary_students(db)


@router.get('/student-offer-duration')
def student_offer_duration(
    db: Session = Depends(get_db),
):
    """统计个人就业时长。"""
    return statistics_service.get_student_offer_duration(db)


@router.get('/class-offer-duration')
def class_offer_duration(
    db: Session = Depends(get_db),
):
    """统计班级平均就业时长。"""
    return statistics_service.get_class_avg_offer_duration(db)
