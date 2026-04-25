
from fastapi import FastAPI
import uvicorn

from fastapi1 import student_api

app = FastAPI()

app.include_router(student_api.stu_router)


@app.get("/")
async def root():
    return {"message": "欢迎进入学生信息管理系统"}



if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8025)



