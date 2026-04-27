from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
from app.core.config import settings
from app.core.database import init_db

app = FastAPI(title='SIMS 学生管理系统', version='0.1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(agent_router)
app.include_router(auth_router)
app.include_router(students_router)
app.include_router(classes_router)
app.include_router(scores_router)
app.include_router(employment_router)
app.include_router(employment_v2_router, prefix='/v2')
app.include_router(statistics_router)
app.include_router(teachers_router)
app.include_router(users_router)


@app.get('/')
def read_root() -> dict:
    """返回应用首页信息。"""
    return {'message': 'SIMS backend is running'}


@app.on_event('startup')
def on_startup() -> None:
    """在应用启动时初始化数据库表。"""
    init_db()
