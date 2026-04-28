# ============================================================
# users.py —— 用户管理接口模块
# ============================================================
# 这个文件提供系统用户的管理接口，包括：
#   1. 获取所有用户列表
#   2. 更新用户信息（角色、状态、密码）
#   3. 删除用户
#
# 用户模块的权限控制：
#   - 所有操作：仅 admin
#
# 注意：默认管理员账号（admin）不能被删除，防止系统锁死。
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import md5_hash
from app.dependencies import require_role
from app.models.user import User
from app.schemas.response import ApiResponse
from app.schemas.user import UserRead, UserUpdate

# 创建路由，所有以 /users 开头的请求都归这里处理
# dependencies 表示这个路由下的所有接口都需要 admin 权限
router = APIRouter(
    prefix='/users',
    tags=['用户管理'],
    dependencies=[Depends(require_role(['admin']))],
)


# ============================================================
# 1. 获取所有用户列表
# ============================================================

@router.get('', summary='获取用户列表')
def get_users(db: Session = Depends(get_db)) -> ApiResponse[list[UserRead]]:
    """
    获取系统中所有用户的列表。

    访问地址：GET /users
    权限：仅管理员可操作

    参数：
        db: 数据库连接

    返回值：
        所有用户的信息列表，包含用户名、角色、是否启用等
    """
    users = db.query(User).all()
    return ApiResponse(message='查询成功', data=users)


# ============================================================
# 2. 更新用户信息
# ============================================================

@router.put('/{user_id}', summary='更新用户信息')
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)) -> ApiResponse[UserRead]:
    """
    更新指定用户的信息。

    访问地址：PUT /users/{user_id}
    例子：PUT /users/1
    权限：仅管理员可操作

    可以更新的字段：
        - roles: 用户角色（如 'admin'、'teacher'）
        - is_active: 账号是否启用（True/False）
        - password: 密码（会自动加密存储）

    参数：
        user_id: 用户的数字 ID
        data: 要更新的字段，不需要全部传
        db: 数据库连接

    返回值：
        更新后的用户信息

    可能的错误：
        - 404：用户不存在
    """
    # 先根据 ID 查找用户
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='用户不存在')

    # 只更新传入的字段，没传的不动
    if data.roles is not None:
        user.roles = data.roles
    if data.is_active is not None:
        user.is_active = data.is_active
    if data.password is not None:
        # 密码要用 md5 加密后再存，不能存明文
        user.password_hash = md5_hash(data.password)

    # 保存到数据库
    db.commit()
    db.refresh(user)
    return ApiResponse(message='更新成功', data=user)


# ============================================================
# 3. 删除用户
# ============================================================

@router.delete('/{user_id}', summary='删除用户')
def delete_user(user_id: int, db: Session = Depends(get_db)) -> ApiResponse[None]:
    """
    删除指定用户。

    访问地址：DELETE /users/{user_id}
    例子：DELETE /users/2
    权限：仅管理员可操作

    参数：
        user_id: 用户的数字 ID
        db: 数据库连接

    返回值：
        删除成功的提示

    注意：
        默认管理员账号（username='admin'）不能被删除，
        这是为了防止误操作导致系统无法管理。

    可能的错误：
        - 404：用户不存在
        - 403：不能删除默认管理员账号
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='用户不存在')
    if user.username == 'admin':
        # 403 表示"禁止操作"
        raise HTTPException(status_code=403, detail='不能删除默认管理员账号')

    db.delete(user)
    db.commit()
    return ApiResponse(message='删除成功', data=None)
