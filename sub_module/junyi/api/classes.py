from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.classes import ClassCreate, ClassResponse, ClassUpdate
from app.schemas.common import Response
from app.services.classes import ClassService

# 创建路由，前缀 /api/classes
router = APIRouter(prefix="/api/classes", tags=["班级管理"])

# 获取班级列表接口
@router.get("", summary="获取班级信息列表")
def get_class_list(
    skip: int = Query(0, description="跳过多少条"),
    limit: int = Query(10, description="每页条数"),
    class_name: Optional[str] = Query(None, description="班级名称模糊匹配"),
    db: Session = Depends(get_db),
):
    # 调用service获取数据
    classes, total = ClassService.get_class_list(db, skip, limit, class_name)
    # 转成前端格式
    class_responses = [ClassResponse.model_validate(cls) for cls in classes]
    # 返回统一格式
    return Response(code=200, message="获取班级列表成功", data={"classes": class_responses, "total": total})

# 新增班级接口
@router.post("", summary="新增班级")
def create_class(
    data: ClassCreate,
    db: Session = Depends(get_db),
):
    cls = ClassService.create_class(db, data)
    class_response = ClassResponse.model_validate(cls)
    return Response(code=201, message="班级新增成功", data=class_response)

# 修改班级接口
@router.put("/{class_id}", summary="根据班级id修改班级信息")
def update_class(
    class_id: int,
    data: ClassUpdate,
    db: Session = Depends(get_db),
):
    cls = ClassService.update_class(db, class_id, data)
    class_response = ClassResponse.model_validate(cls)
    return Response(code=200, message="修改班级成功", data=class_response)

# 删除班级接口
@router.delete("/{class_id}", summary="根据班级id删除班级(逻辑删除)")
def delete_class(
    class_id: int,
    db: Session = Depends(get_db),
):
    ClassService.delete_class(db, class_id)
    return Response(code=200, message="删除成功")
