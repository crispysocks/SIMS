from collections.abc import Callable

from fastapi import Depends, Header, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

from app.core.security import decode_access_token

security = HTTPBearer(auto_error=False)


class CurrentUser(BaseModel):
    """当前登录用户信息模型。"""

    username: str
    roles: list[str] = Field(default_factory=list)


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> CurrentUser:
    """从 JWT Token 或 Header 中解析当前用户。"""
    x_user = request.headers.get('X-User')
    x_roles = request.headers.get('X-Roles')
    if x_user and x_roles:
        roles = [r.strip() for r in x_roles.split(',') if r.strip()]
        return CurrentUser(username=x_user, roles=roles)

    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='未提供认证令牌',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='令牌无效或已过期',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    username = payload.get('sub')
    roles_str = payload.get('roles', '')
    roles = [r.strip() for r in roles_str.split(',') if r.strip()] if roles_str else []
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='令牌中无用户信息',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return CurrentUser(username=username, roles=roles)


def require_role(allowed_roles: list[str]) -> Callable:
    """校验当前用户是否具备指定角色。"""

    def checker(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if not set(current_user.roles).intersection(allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='当前用户没有访问该接口的权限',
            )
        return current_user

    return checker
