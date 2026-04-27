from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import md5_hash
from app.dependencies import require_role
from app.models.user import User
from app.schemas.response import ApiResponse
from app.schemas.user import UserRead, UserUpdate

router = APIRouter(
    prefix='/users',
    tags=['用户管理'],
    dependencies=[Depends(require_role(['admin']))],
)


@router.get('', summary='获取用户列表')
def get_users(db: Session = Depends(get_db)) -> ApiResponse[list[UserRead]]:
    users = db.query(User).all()
    return ApiResponse(message='查询成功', data=users)


@router.put('/{user_id}', summary='更新用户信息')
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)) -> ApiResponse[UserRead]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='用户不存在')

    if data.roles is not None:
        user.roles = data.roles
    if data.is_active is not None:
        user.is_active = data.is_active
    if data.password is not None:
        user.password_hash = md5_hash(data.password)

    db.commit()
    db.refresh(user)
    return ApiResponse(message='更新成功', data=user)


@router.delete('/{user_id}', summary='删除用户')
def delete_user(user_id: int, db: Session = Depends(get_db)) -> ApiResponse[None]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='用户不存在')
    if user.username == 'admin':
        raise HTTPException(status_code=403, detail='不能删除默认管理员账号')
    db.delete(user)
    db.commit()
    return ApiResponse(message='删除成功', data=None)
