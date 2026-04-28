# ============================================================
# auth.py —— 用户认证模块（登录、注册）
# ============================================================
# 这个文件处理用户的"身份验证"，也就是确认"你是谁"。
#
# 包含两个核心功能：
#   1. 注册（register）：新用户创建账号
#   2. 登录（login）：已有用户验证身份，获取"通行证"（token）
#
# 什么是 token？
#   就像游乐园的手环，登录成功后后端发给你一个"令牌"，
#   之后你每次请求都带着这个令牌，后端就知道你是谁了。
# ============================================================

# FastAPI 框架的核心工具
from fastapi import APIRouter, Depends, HTTPException, status
# SQLAlchemy 的数据库会话，用来操作数据库
from sqlalchemy.orm import Session

# 我们自己项目的工具
from app.core.database import get_db
# security 里放了密码加密和 token 生成的工具
from app.core.security import create_access_token, md5_hash, verify_password
# User 是数据库里的"用户表"的模型
from app.models.user import User
# 统一的返回格式
from app.schemas.response import ApiResponse
# 用户相关的数据格式定义
from app.schemas.user import TokenResponse, UserCreate, UserLogin

# 创建路由，所有以 /auth 开头的请求都归这里处理
# tags=['认证'] 是在接口文档里显示的分类名称
router = APIRouter(prefix='/auth', tags=['认证'])


# ============================================================
# 注册接口
# ============================================================

@router.post('/register', status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)) -> ApiResponse[TokenResponse]:
    """
    用户注册接口。

    访问地址：POST /auth/register
    功能：创建一个新账号，注册成功后自动登录，返回 token。

    参数：
        data: 注册信息，包含用户名和密码
        db: 数据库连接，自动提供

    返回值：
        包含 token、用户名、角色列表的响应数据
    """
    # 第一步：检查用户名是否已经被占用
    # db.query(User) 表示"我要查 User 这张表"
    # filter(User.username == data.username) 表示"筛选用户名为传入值的数据"
    # .first() 表示"只取第一条"
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        # 如果查到了，说明用户名已存在，返回 400 错误
        raise HTTPException(status_code=400, detail='用户名已存在')

    # 第二步：创建新用户
    # md5_hash 把密码变成一串不可反推的乱码，这样即使数据库泄露，密码也不会暴露
    user = User(
        username=data.username,
        password_hash=md5_hash(data.password),
        roles='teacher',  # 新注册用户默认角色是老师
    )

    # 第三步：保存到数据库
    db.add(user)       # 把新用户加入"待保存"队列
    db.commit()        # 真正执行保存（提交到数据库）
    db.refresh(user)   # 刷新一下，获取数据库生成的自增 ID 等字段

    # 第四步：生成 token（通行证）
    # 'sub' 是 token 的主题，一般放用户唯一标识（这里是用户名）
    # 'roles' 是用户的角色，后面用来判断权限
    token = create_access_token({'sub': user.username, 'roles': user.roles})

    # 第五步：组装返回数据
    # 把 roles 字符串（如 "admin,teacher"）拆分成列表（如 ["admin", "teacher"]）
    result = TokenResponse(
        access_token=token,
        username=user.username,
        roles=[r.strip() for r in user.roles.split(',') if r.strip()],
    )

    return ApiResponse(message='注册成功', data=result)


# ============================================================
# 登录接口
# ============================================================

@router.post('/login')
def login(data: UserLogin, db: Session = Depends(get_db)) -> ApiResponse[TokenResponse]:
    """
    用户登录接口。

    访问地址：POST /auth/login
    功能：验证用户名和密码，验证通过后返回 token。

    参数：
        data: 登录信息，包含用户名和密码
        db: 数据库连接，自动提供

    返回值：
        包含 token、用户名、角色列表的响应数据
    """
    # 第一步：根据用户名查找用户
    user = db.query(User).filter(User.username == data.username).first()

    # 第二步：验证用户是否存在，以及密码是否正确
    # verify_password 会把输入的密码用同样的方式加密，然后和数据库里的比对
    if not user or not verify_password(data.password, user.password_hash):
        # 401 表示"未授权"，也就是身份验证失败
        raise HTTPException(status_code=401, detail='用户名或密码错误')

    # 第三步：检查账号是否被禁用
    if not user.is_active:
        # 403 表示"禁止访问"，账号被禁用
        raise HTTPException(status_code=403, detail='账号已被禁用')

    # 第四步：生成 token
    token = create_access_token({'sub': user.username, 'roles': user.roles})

    # 第五步：组装返回数据
    result = TokenResponse(
        access_token=token,
        username=user.username,
        roles=[r.strip() for r in user.roles.split(',') if r.strip()],
    )

    return ApiResponse(message='登录成功', data=result)
