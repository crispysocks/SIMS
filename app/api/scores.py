# ============================================================
# scores.py —— 成绩管理接口模块
# ============================================================
# 这个文件提供学生成绩相关的所有接口，包括：
#   1. 录入学生成绩
#   2. 修改成绩
#   3. 删除成绩（逻辑删除）
#   4. 查询所有成绩
#   5. 查询指定学生的成绩
#   6. 每次考试的成绩排名
#   7. 班级成绩报表（平均分、优秀率、及格率）
#
# 成绩模块的权限控制：
#   - 查询：任何人都可以
#   - 录入、修改：需要 admin 或 teacher
#   - 删除：仅 admin
# ============================================================

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import require_role
from app.schemas.response import ApiResponse
from app.schemas.score import (
    ClassScoreReportItem,
    ExamRankingItem,
    ScoreCreate,
    ScoreRead,
    ScoreUpdate,
)
from app.services import score as score_service

# 创建路由，所有以 /scores 开头的请求都归这里处理
router = APIRouter(
    prefix='/scores',
    tags=['成绩管理'],
)


# ============================================================
# 1. 录入学生成绩
# ============================================================

@router.post('/', dependencies=[Depends(require_role(['admin', 'teacher']))])
def create_score(
    data: ScoreCreate,
    db: Session = Depends(get_db),
) -> ApiResponse[ScoreRead]:
    """
    录入一条学生成绩。

    访问地址：POST /scores/
    状态码 201 表示"创建成功"
    权限：仅管理员或老师可操作

    参数：
        data: 成绩信息，包含学生编号、考试序次、各科分数等
        db: 数据库连接，通过依赖注入获取数据库会话

    返回值：
        录入成功的成绩信息
    """
    result = score_service.create_score(db, data)
    return ApiResponse(message='录入成功', data=result)


# ============================================================
# 2. 修改成绩
# ============================================================

@router.put('/update', dependencies=[Depends(require_role(['admin', 'teacher']))])
def update_score(
    data: ScoreUpdate,
    db: Session = Depends(get_db),
) -> ApiResponse[ScoreRead]:
    """
    修改指定学生某次考试的成绩。

    访问地址：PUT /scores/update
    权限：仅管理员或老师可操作

    参数：
        data: 要更新的成绩信息，必须包含学生编号和考试序次来定位
        db: 数据库连接

    返回值：
        更新后的成绩信息
    """
    result = score_service.update_score(db, data)
    return ApiResponse(message='更新成功', data=result)


# ============================================================
# 3. 删除成绩（逻辑删除）
# ============================================================

@router.delete('/{student_no}/{exam_no}', dependencies=[Depends(require_role(['admin']))])
def delete_score(
    student_no: str,
    exam_no: int,
    db: Session = Depends(get_db),
) -> ApiResponse[None]:
    """
    逻辑删除指定学生某次考试的成绩。

    访问地址：DELETE /scores/{student_no}/{exam_no}
    权限：仅管理员可操作

    什么是逻辑删除？
        不是真的删掉，而是标记为"已删除"，以后还能恢复。

    参数：
        student_no: 学生编号
        exam_no: 考试序次
        db: 数据库连接

    返回值：
        删除成功的提示
    """
    score_service.delete_score(db, student_no, exam_no)
    return ApiResponse(message='删除成功', data=None)


# ============================================================
# 4. 查询所有成绩
# ============================================================

@router.get('/')
def list_scores(
    db: Session = Depends(get_db),
) -> ApiResponse[list[ScoreRead]]:
    """
    查询系统中所有学生的成绩记录。

    访问地址：GET /scores/

    参数：
        db: 数据库连接

    返回值：
        所有成绩记录的列表
    """
    data = score_service.list_all_scores(db)
    return ApiResponse(message='查询成功', data=data)


# ============================================================
# 5. 查询指定学生的成绩
# ============================================================

@router.get('/{student_no}')
def get_scores(
    student_no: str,
    db: Session = Depends(get_db),
) -> ApiResponse[list[ScoreRead]]:
    """
    查询某个学生的所有成绩。

    访问地址：GET /scores/{student_no}
    例子：GET /scores/S001

    参数：
        student_no: 学生编号
        db: 数据库连接

    返回值：
        该学生所有考试的成绩列表
    """
    data = score_service.list_scores_by_student(db, student_no)
    return ApiResponse(message='查询成功', data=data)


# ============================================================
# 6. 考试排名
# ============================================================

@router.get('/ranking/exam')
def exam_ranking(
    exam_no: int = Query(..., ge=1, description='考核序次'),
    db: Session = Depends(get_db),
) -> ApiResponse[list[ExamRankingItem]]:
    """
    获取某次考试的学生成绩排名。

    访问地址：GET /scores/ranking/exam?exam_no=1

    参数：
        exam_no: 考试序次，必须大于等于 1（第几次考试）
        db: 数据库连接

    返回值：
        按总成绩从高到低排序的排名列表
    """
    data = score_service.get_exam_ranking(db, exam_no)
    return ApiResponse(message='查询成功', data=data)


# ============================================================
# 7. 班级成绩报表
# ============================================================

@router.get('/report/class')
def class_score_report(
    exam_no: int = Query(..., ge=1, description='考核序次'),
    db: Session = Depends(get_db),
) -> ApiResponse[list[ClassScoreReportItem]]:
    """
    获取某次考试的班级成绩统计报表。

    访问地址：GET /scores/report/class?exam_no=1

    参数：
        exam_no: 考试序次，必须大于等于 1
        db: 数据库连接

    返回值：
        每个班的统计数据，包括：
        - 平均分
        - 优秀率（比如 90 分以上的人数占比）
        - 及格率（比如 60 分以上的人数占比）
    """
    data = score_service.get_class_score_report(db, exam_no)
    return ApiResponse(message='查询成功', data=data)
