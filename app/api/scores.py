from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import require_role
from app.schemas.response import ApiResponse
from app.schemas.score import (
    ClassScoreReportItem,
    ExamRankingItem,
    ScoreCreate,
    ScoreDelete,
    ScoreRead,
    ScoreUpdate,
)
from app.services import score as score_service

router = APIRouter(
    prefix='/scores',
    tags=['成绩管理'],
)


@router.post('/', status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role(['admin', 'teacher']))])
def create_score(
    data: ScoreCreate,
    db: Session = Depends(get_db),
) -> ApiResponse[ScoreRead]:
    """录入学生成绩。"""
    result = score_service.create_score(db, data)
    return ApiResponse(message='录入成功', data=result)


@router.put('/update', dependencies=[Depends(require_role(['admin', 'teacher']))])
def update_score(
    data: ScoreUpdate,
    db: Session = Depends(get_db),
) -> ApiResponse[ScoreRead]:
    """修改指定学生某次成绩。"""
    result = score_service.update_score(db, data)
    return ApiResponse(message='更新成功', data=result)


@router.post('/delete', dependencies=[Depends(require_role(['admin']))])
def delete_score(
    data: ScoreDelete,
    db: Session = Depends(get_db),
) -> ApiResponse[None]:
    """逻辑删除指定学生某次成绩。"""
    score_service.delete_score(db, data.student_no, data.exam_no)
    return ApiResponse(message='删除成功', data=None)


@router.get('/')
def list_scores(
    db: Session = Depends(get_db),
) -> ApiResponse[list[ScoreRead]]:
    """查询所有学生成绩记录。"""
    data = score_service.list_all_scores(db)
    return ApiResponse(message='查询成功', data=data)


@router.get('/{student_no}')
def get_scores(
    student_no: str,
    db: Session = Depends(get_db),
) -> ApiResponse[list[ScoreRead]]:
    """查询指定学生的成绩列表。"""
    data = score_service.list_scores_by_student(db, student_no)
    return ApiResponse(message='查询成功', data=data)


@router.get('/ranking/exam')
def exam_ranking(
    exam_no: int = Query(..., ge=1, description='考核序次'),
    db: Session = Depends(get_db),
) -> ApiResponse[list[ExamRankingItem]]:
    """每次考试的学生成绩排名。"""
    data = score_service.get_exam_ranking(db, exam_no)
    return ApiResponse(message='查询成功', data=data)


@router.get('/report/class')
def class_score_report(
    exam_no: int = Query(..., ge=1, description='考核序次'),
    db: Session = Depends(get_db),
) -> ApiResponse[list[ClassScoreReportItem]]:
    """班级成绩报表（平均分、优秀率、及格率）。"""
    data = score_service.get_class_score_report(db, exam_no)
    return ApiResponse(message='查询成功', data=data)
