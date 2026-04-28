# ============================================================
# dependencies.py —— 依赖注入和权限校验
# ============================================================
# 这个文件负责处理"谁可以访问哪个接口"的问题。
#
# 什么是依赖注入（Dependency Injection）？
#   简单来说，就是"需要用到某个功能时，系统自动提供给你"。
#   比如接口需要知道"当前登录的是谁"，
#   只需要在参数里写 current_user = Depends(get_current_user)，
#   FastAPI 就会自动调用 get_current_user 并把结果传进来。
#
# 这个文件包含：
#   - CurrentUser: 当前登录用户的信息模型
#   - get_current_user: 从请求中解析当前用户
#   - require_role: 检查用户是否有指定角色
#
# 认证方式：
#   1. Header 认证（开发/测试用）：X-User 和 X-Roles 头部
#   2. JWT Token 认证（生产用）：Authorization: Bearer <token>
# ============================================================

from collections.abc import Callable

from fastapi import Depends, Header, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

from app.core.security import decode_access_token

# HTTPBearer 是 FastAPI 提供的工具，用于从请求头中提取 Bearer Token
# auto_error=False 表示如果没有 Token，不会自动报错，而是返回 None
security = HTTPBearer(auto_error=False)


class CurrentUser(BaseModel):
    """
    当前登录用户的信息模型。

    字段：
        - username: 用户名
        - roles: 角色列表，如 ['admin']、['teacher']、['admin', 'teacher']
    """

    username: str
    roles: list[str] = Field(default_factory=list)


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> CurrentUser:
    """
    从请求中解析当前登录用户。

    解析顺序：
        1. 先检查 Header 中的 X-User 和 X-Roles（开发/测试用）
        2. 如果没有，再检查 Authorization: Bearer <token>

    参数：
        request: HTTP 请求对象，可以获取请求头
        credentials: 从 Authorization 头中提取的 Token

    返回值：
        CurrentUser 对象，包含用户名和角色列表

    异常情况：
        - 没有提供任何认证信息 → 401 未授权
        - Token 无效或过期 → 401 未授权
        - Token 中没有用户信息 → 401 未授权
    """
    # 方式一：Header 认证（简单，适合开发和测试）
    x_user = request.headers.get('X-User')
    x_roles = request.headers.get('X-Roles')
    if x_user and x_roles:
        # 把逗号分隔的角色字符串转成列表
        roles = [r.strip() for r in x_roles.split(',') if r.strip()]
        return CurrentUser(username=x_user, roles=roles)

    # 方式二：JWT Token 认证（标准方式）
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='未提供认证令牌',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    # 解码 Token
    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='令牌无效或已过期',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    # 从 Token 中提取用户信息
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
    """
    创建一个角色校验器。

    用法：
        @router.get('/admin-only', dependencies=[Depends(require_role(['admin']))])
        def admin_only():
            return {'message': '只有管理员能看到'}

    参数：
        allowed_roles: 允许访问的角色列表，如 ['admin'] 或 ['admin', 'teacher']

    返回值：
        一个依赖函数，如果当前用户没有指定角色，会抛出 403 错误
    """

    def checker(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        # set.intersection 求两个集合的交集
        # 如果用户的角色和允许的角色没有交集，说明没有权限
        if not set(current_user.roles).intersection(allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='当前用户没有访问该接口的权限',
            )
        return current_user

    return checker
