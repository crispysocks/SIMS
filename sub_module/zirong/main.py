import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.teacher_api import router as teacher_router
from app.database import engine, Base
# 导入所有模型，以便 create_all 能发现它们
from app.models import teacher, course  # noqa: F401

app = FastAPI(
    title="教学管理系统",
    description="老师与课程管理 API",
    version="1.0.0"
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(teacher_router)

# 启动时创建数据库表（仅开发环境）
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)