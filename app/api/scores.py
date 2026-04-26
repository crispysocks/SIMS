from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import CurrentUser, get_current_user, require_role
from app.schemas.score import ScoreCreate, ScoreDelete, ScoreRead, ScoreUpdate
from app.services import score as score_service

router = APIRouter(prefix='/scores', tags=['成绩管理'])


@router.get('/{student_no}', response_model=list[ScoreRead])
def get_scores(
    student_no: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """查询指定学生的成绩列表。"""
    return score_service.list_scores_by_student(db, student_no)


@router.post('/', response_model=ScoreRead, status_code=status.HTTP_201_CREATED)
def create_score(
    data: ScoreCreate,
    current_user: CurrentUser = Depends(require_role(['admin', 'teacher'])),
    db: Session = Depends(get_db),
):
    """录入学生成绩。"""
    return score_service.create_score(db, data)


@router.put('/update', response_model=ScoreRead)
def update_score(
    data: ScoreUpdate,
    current_user: CurrentUser = Depends(require_role(['admin', 'teacher'])),
    db: Session = Depends(get_db),
):
    """修改指定学生某次成绩。"""
    return score_service.update_score(db, data)


@router.post('/delete', status_code=status.HTTP_204_NO_CONTENT)
def delete_score(
    data: ScoreDelete,
    current_user: CurrentUser = Depends(require_role(['admin'])),
    db: Session = Depends(get_db),
):
    """逻辑删除指定学生某次成绩。"""
    score_service.delete_score(db, data.student_no, data.exam_no, data.exam_name)
    return None
