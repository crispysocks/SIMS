from fastapi import FastAPI
import uvicorn
from file.api.stu_api import emp_router

app = FastAPI()

app.include_router(emp_router, prefix="/employees", tags=["employees"])

@app.get("/")
def first_menu():
    return {"message": "学生管理系统"}

if __name__ == '__main__':
    uvicorn.run("__init__:app", host='127.0.0.1', port=8000, reload=True)