# ============================================================
# main.py —— 应用程序入口
# ============================================================
# 这个文件是整个后端程序的"起点"。
#
# 当你运行 `uvicorn app.main:app` 时，
# Python 会加载这个文件，创建 FastAPI 应用实例。
#
# 这个文件做了什么？
#   1. 创建 FastAPI 应用对象
#   2. 配置跨域（CORS），让前端可以访问后端
#   3. 注册所有路由模块（api/ 下的各个模块）
#   4. 定义根路径接口（访问 / 时返回欢迎信息）
#   5. 启动时初始化数据库表
#
# 什么是 CORS？
#   浏览器的安全机制，默认不允许一个网站访问另一个网站的接口。
#   比如前端在 http://localhost:5173，后端在 http://localhost:8000，
#   如果不配置 CORS，浏览器会阻止前端的请求。
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 从 api/__init__.py 导入所有路由
from app.api import (
    agent_router,
    auth_router,
    classes_router,
    employment_router,
    employment_v2_router,
    scores_router,
    statistics_router,
    students_router,
    teachers_router,
    users_router,
)

# 从 core 导入配置和数据库初始化函数
from app.core.config import settings
from app.core.database import init_db

# ---------- 创建 FastAPI 应用 ----------
# title: 应用名称，会显示在 API 文档页面
# version: 版本号
app = FastAPI(title='SIMS 学生管理系统', version='0.1.0')

# ---------- 配置跨域（CORS） ----------
# CORSMiddleware 是 FastAPI 提供的中间件
# 它会在每个响应头里加上允许跨域的标记
app.add_middleware(
    CORSMiddleware,
    # allow_origins: 允许哪些网站访问
    # settings.cors_origins_list 从 .env 文件读取，默认是 ['http://localhost:5173']
    allow_origins=settings.cors_origins_list,
    # allow_credentials: 是否允许携带 Cookie
    allow_credentials=True,
    # allow_methods: 允许哪些 HTTP 方法，* 表示全部
    allow_methods=['*'],
    # allow_headers: 允许哪些请求头，* 表示全部
    allow_headers=['*'],
)

# ---------- 注册路由 ----------
# include_router 把各个模块的路由添加到主应用上
# 这样访问 /students、/classes 等路径时，就会由对应的模块处理
app.include_router(agent_router)
app.include_router(auth_router)
app.include_router(students_router)
app.include_router(classes_router)
app.include_router(scores_router)
app.include_router(employment_router)

# v2 版就业接口加了前缀 /v2
# 所以访问路径是 /v2/employment/...
app.include_router(employment_v2_router, prefix='/v2')

app.include_router(statistics_router)
app.include_router(teachers_router)
app.include_router(users_router)


# ---------- 根路径接口 ----------
@app.get('/')
def read_root() -> dict:
    """
    访问 http://localhost:8000/ 时返回的信息。

    用来确认后端服务是否正常运行。
    """
    return {'message': 'SIMS backend is running'}


# ---------- 启动事件 ----------
@app.on_event('startup')
def on_startup() -> None:
    """
    应用启动时自动执行的函数。

    这里调用 init_db() 来检查数据库连接，
    并在表不存在时自动创建表。
    """
    init_db()
