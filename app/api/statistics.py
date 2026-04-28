# ============================================================
# statistics.py —— 统计分析接口模块
# ============================================================
# 这个文件提供各种统计查询接口，用于数据分析和报表展示，包括：
#   1. 按年龄筛选学生
#   2. 统计每个班级的男女生人数
#   3. 查询每次考试都高于指定分数的学生
#   4. 查询两次及以上不及格的学生
#   5. 统计班级平均分
#   6. 统计高薪学生
#   7. 统计个人就业时长
#   8. 统计班级平均就业时长
#
# 这些接口都是查询类的，不涉及数据修改，所以不需要权限控制。
# ============================================================

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.response import ApiResponse
from app.services import statistics as statistics_service

# 创建路由，所有以 /api/statistics 开头的请求都归这里处理
router = APIRouter(
    prefix='/api/statistics',
    tags=['统计分析'],
)


# ============================================================
# 1. 按年龄筛选学生
# ============================================================

@router.get('/age-filter')
def age_filter(
    age: int = Query(30, ge=0),
    db: Session = Depends(get_db),
) -> ApiResponse[list[dict]]:
    """
    查询年龄达到指定值的学生。

    访问地址：GET /api/statistics/age-filter?age=25

    参数：
        age: 年龄门槛，默认 30，必须大于等于 0
        db: 数据库连接

    返回值：
        年龄大于等于指定值的学生列表
    """
    data = statistics_service.find_students_by_age(db, age)
    return ApiResponse(message='查询成功', data=data)


# ============================================================
# 2. 班级男女生人数统计
# ============================================================

@router.get('/class-gender')
def class_gender(
    db: Session = Depends(get_db),
) -> ApiResponse[list[dict]]:
    """
    统计每个班级的男女生人数。

    访问地址：GET /api/statistics/class-gender

    参数：
        db: 数据库连接

    返回值：
        每个班的男女人数，比如：
        [{ 'class_no': 'C001', 'class_name': '一班', 'male_count': 20, 'female_count': 15 }]
    """
    data = statistics_service.get_class_gender_stats(db)
    return ApiResponse(message='查询成功', data=data)


# ============================================================
# 3. 查询每次考试都高于指定分数的学生
# ============================================================

@router.get('/always-above')
def always_above(
    score: int = Query(80, ge=0, le=100),
    db: Session = Depends(get_db),
) -> ApiResponse[list[dict]]:
    """
    查询每次考试都高于指定分数的学生（学霸筛选器）。

    访问地址：GET /api/statistics/always-above?score=80

    参数：
        score: 分数门槛，默认 80，范围 0~100
        db: 数据库连接

    返回值：
        所有考试都达到该分数的学生列表
    """
    data = statistics_service.get_students_always_above_score(db, score)
    return ApiResponse(message='查询成功', data=data)


# ============================================================
# 4. 查询两次及以上不及格的学生
# ============================================================

@router.get('/failed-twice')
def failed_twice(
    db: Session = Depends(get_db),
) -> ApiResponse[list[dict]]:
    """
    查询两次及以上考试不及格的学生。

    访问地址：GET /api/statistics/failed-twice

    参数：
        db: 数据库连接

    返回值：
        挂科两次及以上的学生列表，方便老师重点关注
    """
    data = statistics_service.get_students_failed_twice_or_more(db)
    return ApiResponse(message='查询成功', data=data)


# ============================================================
# 5. 统计班级平均分
# ============================================================

@router.get('/class-avg-score')
def class_avg_score(
    db: Session = Depends(get_db),
) -> ApiResponse[list[dict]]:
    """
    统计各班级每次考试的平均分。

    访问地址：GET /api/statistics/class-avg-score

    参数：
        db: 数据库连接

    返回值：
        每个班每次考试的平均分对比数据
    """
    data = statistics_service.get_class_avg_scores_by_exam(db)
    return ApiResponse(message='查询成功', data=data)


# ============================================================
# 6. 统计高薪学生
# ============================================================

@router.get('/top-salary')
def top_salary(
    db: Session = Depends(get_db),
) -> ApiResponse[list[dict]]:
    """
    统计薪资排名靠前的学生（高薪榜）。

    访问地址：GET /api/statistics/top-salary

    参数：
        db: 数据库连接

    返回值：
        薪资较高的学生列表，通常用于展示就业成果
    """
    data = statistics_service.get_top_salary_students(db)
    return ApiResponse(message='查询成功', data=data)


# ============================================================
# 7. 统计个人就业时长
# ============================================================

@router.get('/student-offer-duration')
def student_offer_duration(
    db: Session = Depends(get_db),
) -> ApiResponse[list[dict]]:
    """
    统计每个学生从入学到拿到 offer 的时长。

    访问地址：GET /api/statistics/student-offer-duration

    参数：
        db: 数据库连接

    返回值：
        每个学生的就业时长（天数），用于分析就业速度
    """
    data = statistics_service.get_student_offer_duration(db)
    return ApiResponse(message='查询成功', data=data)


# ============================================================
# 8. 统计班级平均就业时长
# ============================================================

@router.get('/class-offer-duration')
def class_offer_duration(
    db: Session = Depends(get_db),
) -> ApiResponse[list[dict]]:
    """
    统计每个班级的平均就业时长。

    访问地址：GET /api/statistics/class-offer-duration

    参数：
        db: 数据库连接

    返回值：
        每个班的平均就业天数，用于对比各班的就业效率
    """
    data = statistics_service.get_class_avg_offer_duration(db)
    return ApiResponse(message='查询成功', data=data)
