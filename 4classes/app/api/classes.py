from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.classes import ClassCreate, ClassResponse, ClassUpdate
from app.schemas.common import Response
from app.services.classes import ClassService

# 路由前缀
router = APIRouter(prefix="/api/classes", tags=["班级管理"])

# 1 分页+模糊查询 班级信息
@router.get("", summary="分页查询班级")

def get_class_list(
    skip: int = Query(0),
    limit: int = Query(10),
    class_name: Optional[str] = None,
    db: Session = Depends(get_db),
):
    #调用service层get_class_list方法，接收返回值，接收的是classes orm格式的对象
    classes, total = ClassService.get_class_list(db, skip, limit, class_name)
    #遍历里面的每一个对象然后转换成响应体格式
    data = [ClassResponse.model_validate(c) for c in classes]
    #通过统一响应体去返回结果
    return Response(code=200, message="成功", data={"classes": data, "total": total})

# 2 新增班级
@router.post("", summary="新增班级", status_code=201)
#用请求体模型去校验接收数据
def create_class(
    data: ClassCreate,
    db: Session = Depends(get_db),
):
    #调用service层的创建班级方法，通过data传入，拿到方法返回值
    cls = ClassService.create_class(db, data)
    #将cls转化成响应体对象，然后统一返回
    return Response(code=201, message="新增成功", data=ClassResponse.model_validate(cls))

# 3 修改班级
@router.put("/{class_id}", summary="修改班级")
def update_class(
    class_id: int,
    data: ClassUpdate,
    db: Session = Depends(get_db),
):
    cls = ClassService.update_class(db, class_id, data)
    return Response(code=200, message="修改成功", data=ClassResponse.model_validate(cls))

# 4 删除班级
@router.delete("/{class_id}", summary="删除班级")
def delete_class(
    class_id: int,
    db: Session = Depends(get_db),
):
    ClassService.delete_class(db, class_id)
    return Response(code=200, message="删除成功")

# 5 获取所有班级名称（固定路径，必须放在 /{class_id} 前面）
@router.get("/names", summary="只获取所有班级名称")
def get_class_names(
    db: Session = Depends(get_db),
):
    name_list = ClassService.get_class_names(db)
    return Response(code=200, message="获取班级名称成功", data={"names": name_list})

# 6 统计班级总数（固定路径，必须放在 /{class_id} 前面）
@router.get("/count", summary="统计班级总数")
def get_class_count(
    db: Session = Depends(get_db),
):
    total = ClassService.get_class_total_count(db)
    return Response(code=200, message="成功", data={"total": total})

# 7 根据班级ID查询单个班级详情（动态路径，放最后）
@router.get("/{class_id}", summary="根据ID查询单个班级")
def get_class_by_id(
    class_id: int,
    db: Session = Depends(get_db),
):
    cls = ClassService.get_class_by_id(db, class_id)
    if not cls:
        return Response(code=404, message="班级不存在", data=None)
    return Response(code=200, message="查询成功", data=ClassResponse.model_validate(cls))
