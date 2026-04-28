from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.classes import router as classes_router
from app.core.config import settings
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="学生管理系统", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(classes_router)


@app.get("/")
def root():
    return {"message": "学生管理系统 API"}
