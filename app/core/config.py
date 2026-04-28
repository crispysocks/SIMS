# ============================================================
# config.py —— 系统配置文件
# ============================================================
# 这个文件负责管理系统的所有配置项，比如数据库连接信息、文件上传路径等。
#
# 它是怎么工作的？
#   1. 定义一个 Settings 类，里面列出所有配置项
#   2. 启动时自动读取 .env 文件（如果存在），用文件里的值覆盖默认值
#   3. 其他文件通过 "from app.core.config import settings" 来使用配置
#
# 为什么要用 .env 文件？
#   密码、密钥等敏感信息不应该写在代码里，
#   而是放在 .env 文件中，这个文件不会被提交到代码仓库。
# ============================================================

# json 用来把字符串转成列表（比如 CORS_ORIGINS）
import json

# pydantic_settings 是 Pydantic 的配置管理工具
# BaseSettings 可以自动从环境变量和 .env 文件读取配置
# SettingsConfigDict 用来设置配置的行为
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    系统配置类。

    每个字段都是一个配置项：
    - 字段名必须是大写（如 DB_HOST）
    - 等号后面是默认值，如果 .env 文件里有同名配置，会覆盖默认值
    """

    # ---------- 数据库配置 ----------
    DB_HOST: str = "localhost"          # 数据库服务器地址，默认本机
    DB_PORT: int = 3306                 # MySQL 默认端口
    DB_NAME: str = "student_management" # 数据库名称

    DB_USER: str = "root"               # 数据库用户名
    DB_PASSWORD: str = "123456"         # 数据库密码（生产环境务必修改）

    # 连接池配置（控制数据库连接的复用）
    DB_POOL_SIZE: int = 5               # 连接池大小，同时保持多少个连接
    DB_POOL_RECYCLE: int = 3600         # 连接多久后自动回收（秒），防止连接超时

    # ---------- 跨域配置 ----------
    # CORS_ORIGINS 表示哪些前端网址可以访问后端接口
    # 默认只允许 localhost:5173（前端开发服务器）
    CORS_ORIGINS: str = '["http://localhost:5173"]'

    # ---------- 文件上传配置 ----------
    UPLOAD_DIR: str = "./uploads"       # 上传文件保存的文件夹路径
    MAX_FILE_SIZE: int = 5242880        # 最大文件大小（字节），默认 5MB

    # ---------- 安全密钥 ----------
    # 用于生成用户登录 token，生产环境必须改成复杂随机字符串
    SECRET_KEY: str = "sims-secret-key-change-in-production"

    # ---------- 示例数据开关 ----------
    # 设为 True 时，系统启动会自动导入 sample_data.json 中的测试数据
    # 导入完成后会自动变回 False，防止重复导入
    LOAD_SAMPLE_DATA: bool = False

    # ---------- Pydantic 配置 ----------
    # env_file=".env" 表示从 .env 文件读取配置
    # case_sensitive=True 表示配置名区分大小写（DB_HOST 和 db_host 是不同的）
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    # ---------- 计算属性 ----------
    # @property 表示这个"方法"可以像属性一样访问（不用加括号）

    @property
    def database_url(self) -> str:
        """
        组装数据库连接地址。

        格式：mysql+pymysql://用户名:密码@地址:端口/数据库名
        这是 SQLAlchemy 认识的标准格式。
        """
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def cors_origins_list(self) -> list[str]:
        """
        把 CORS_ORIGINS 字符串转成 Python 列表。

        因为 .env 里只能存字符串，但程序需要列表，所以用 json.loads 转换。
        """
        return json.loads(self.CORS_ORIGINS)


# 创建全局配置实例，其他文件通过导入 settings 来使用
settings = Settings()
