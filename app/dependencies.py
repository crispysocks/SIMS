from collections.abc import Callable

from fastapi import Depends, Header, HTTPException, status
from pydantic import BaseModel, Field


class CurrentUser(BaseModel):
    """当前登录用户信息模型。"""

    username: str = Field(default='demo_admin')
    roles: list[str] = Field(default_factory=lambda: ['admin', 'teacher'])


def get_current_user(
    x_user: str | None = Header(default=None),
    x_roles: str | None = Header(default=None),
) -> CurrentUser:
    """从请求头解析当前用户，作为开发阶段的简化认证实现。"""
    roles = ['admin', 'teacher']
    if x_roles:
        roles = [item.strip() for item in x_roles.split(',') if item.strip()]
    return CurrentUser(username=x_user or 'demo_admin', roles=roles)


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
