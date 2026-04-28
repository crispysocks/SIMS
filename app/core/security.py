# ============================================================
# security.py —— 安全工具模块
# ============================================================
# 这个文件负责处理所有跟"安全"相关的事情，包括：
#   1. 密码加密（MD5）
#   2. 密码验证
#   3. 生成用户登录 token（JWT）
#   4. 验证/解析 token
#
# 什么是 JWT Token？
#   JWT（JSON Web Token）是一种安全的"通行证"格式。
#   用户登录成功后，后端生成一个 token 给前端，
#   前端之后每次请求都带着这个 token，后端就能识别用户身份。
#
#   Token 里可以存放：用户ID、角色、过期时间等信息。
#   Token 是用密钥签名的，别人无法伪造。
# ============================================================

# hashlib 是 Python 自带的加密库，提供 MD5、SHA 等算法
import hashlib
# datetime 用来处理 token 的过期时间
from datetime import datetime, timedelta, timezone

# PyJWT 是用来生成和验证 JWT token 的第三方库
import jwt

# 导入系统配置，获取密钥
from app.core.config import settings


# ---------- 全局常量 ----------

# 从配置里读取密钥，用于签名 token
# 生产环境务必改成复杂随机字符串，不能泄露
SECRET_KEY = settings.SECRET_KEY

# JWT 使用的签名算法，HS256 是 HMAC + SHA256 的缩写
ALGORITHM = 'HS256'

# Token 有效期，默认 24 小时（60 分钟 × 24）
# 用户登录后 24 小时内不需要重新登录
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


# ============================================================
# 密码加密
# ============================================================

def md5_hash(password: str) -> str:
    """
    把密码用 MD5 算法加密成一串固定长度的乱码。

    为什么要加密？
        数据库里不能存明文密码！如果数据库泄露，所有人的密码都会暴露。
        加密后，即使泄露，黑客也只能看到乱码，无法知道真实密码。

    参数：
        password: 用户输入的原始密码

    返回值：
        32 位的十六进制字符串，如 "e10adc3949ba59abbe56e057f20f883e"
    """
    # 把密码转成字节，用 MD5 加密，再转成十六进制字符串
    return hashlib.md5(password.encode('utf-8')).hexdigest()


# ============================================================
# 密码验证
# ============================================================

def verify_password(plain_password: str, password_hash: str) -> bool:
    """
    验证用户输入的密码是否正确。

    原理：
        把用户输入的密码同样用 MD5 加密，然后和数据库里存的密文比对，
        如果一样，说明密码正确。

    参数：
        plain_password: 用户输入的原始密码
        password_hash: 数据库里存储的加密后的密码

    返回值：
        True 表示密码正确，False 表示密码错误
    """
    return md5_hash(plain_password) == password_hash


# ============================================================
# 生成登录 Token
# ============================================================

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    生成 JWT 登录令牌（token）。

    参数：
        data: 要放到 token 里的数据，通常包含：
            - 'sub': 用户唯一标识（如用户名）
            - 'roles': 用户角色
        expires_delta: 自定义过期时间，不传就默认 24 小时

    返回值：
        一串加密后的字符串，就是 token
    """
    # 复制一份数据，避免修改原始字典
    to_encode = data.copy()

    # 计算过期时间：当前时间 + 有效期
    # timezone.utc 表示使用 UTC 时间（世界标准时间），避免时区问题
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    # 把过期时间加入数据
    to_encode.update({'exp': expire})

    # 用密钥和算法对数据签名，生成 token
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ============================================================
# 解析/验证 Token
# ============================================================

def decode_access_token(token: str) -> dict | None:
    """
    解析并验证 JWT token。

    参数：
        token: 前端传来的 token 字符串

    返回值：
        - 如果 token 有效且未过期，返回 token 里存放的数据（字典）
        - 如果 token 无效或已过期，返回 None

    注意：
        这个函数不会抛出异常，解析失败就返回 None，
        调用方需要自己判断返回值。
    """
    try:
        # 用同样的密钥和算法验证签名，并解析数据
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        # PyJWTError 是所有 JWT 相关错误的基类
        # 包括：签名错误、过期错误、格式错误等
        return None
