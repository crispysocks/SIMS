from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, md5_hash, verify_password
from app.models.user import User
from app.schemas.response import ApiResponse
from app.schemas.user import TokenResponse, UserCreate, UserLogin

router = APIRouter(prefix='/auth', tags=['认证'])


@router.post('/register', status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)) -> ApiResponse[TokenResponse]:
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail='用户名已存在')
    user = User(
        username=data.username,
        password_hash=md5_hash(data.password),
        roles='teacher',
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({'sub': user.username, 'roles': user.roles})
    result = TokenResponse(
        access_token=token,
        username=user.username,
        roles=[r.strip() for r in user.roles.split(',') if r.strip()],
    )
    return ApiResponse(message='注册成功', data=result)


@router.post('/login')
def login(data: UserLogin, db: Session = Depends(get_db)) -> ApiResponse[TokenResponse]:
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail='用户名或密码错误')
    if not user.is_active:
        raise HTTPException(status_code=403, detail='账号已被禁用')
    token = create_access_token({'sub': user.username, 'roles': user.roles})
    result = TokenResponse(
        access_token=token,
        username=user.username,
        roles=[r.strip() for r in user.roles.split(',') if r.strip()],
    )
    return ApiResponse(message='登录成功', data=result)
