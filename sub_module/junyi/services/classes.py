# 获取当前时间
from datetime import datetime
# 快速抛出异常
from fastapi import HTTPException
# 数据库会话
from sqlalchemy.orm import Session

# 导入数据库表模型
from app.models.classes import ClassInfo
# 导入数据校验类
from app.schemas.classes import ClassCreate, ClassUpdate

# 班级业务类：所有增删改查都在这里
class ClassService:
    # 静态方法：获取班级列表（分页+搜索）
    @staticmethod
    def get_class_list(db: Session, skip: int, limit: int, class_name: str = None):
        # 1. 先查未删除的班级
        query = db.query(ClassInfo).filter(ClassInfo.is_deleted == 0)
        
        # 2. 如果传了班级名称，模糊搜索
        if class_name:
            query = query.filter(ClassInfo.class_name.contains(class_name))
        
        # 3. 查询总条数
        total = query.count()
        # 4. 分页查询数据
        classes = query.offset(skip).limit(limit).all()
        
        # 5. 返回数据 + 总数
        return classes, total

    # 静态方法：新增班级
    @staticmethod
    def create_class(db: Session, data: ClassCreate):
        # 1. 检查班级名称是否重复
        existing = db.query(ClassInfo).filter(
            ClassInfo.class_name == data.class_name, ClassInfo.is_deleted == 0
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="班级名称已存在")
        
        # 2. 创建班级对象
        cls = ClassInfo(**data.model_dump(), create_time=datetime.now(), update_time=datetime.now())
        
        # 3. 保存到数据库
        db.add(cls)
        db.commit()
        db.refresh(cls)
        
        return cls

    # 静态方法：修改班级
    @staticmethod
    def update_class(db: Session, class_id: int, data: ClassUpdate):
        # 1. 查询要修改的班级
        cls = db.query(ClassInfo).filter(ClassInfo.class_id == class_id, ClassInfo.is_deleted == 0).first()
        
        if not cls:
            raise HTTPException(status_code=404, detail="班级不存在")
        
        # 2. 获取要更新的字段（只更新传了的字段）
        update_data = data.model_dump(exclude_unset=True)
        
        # 3. 赋值更新
        for key, value in update_data.items():
            setattr(cls, key, value)
        
        cls.update_time = datetime.now()
        
        # 4. 提交
        db.commit()
        db.refresh(cls)
        
        return cls

    # 静态方法：删除班级（逻辑删除，不是真删）
    @staticmethod
    def delete_class(db: Session, class_id: int):
        # 1. 查询班级
        cls = db.query(ClassInfo).filter(ClassInfo.class_id == class_id, ClassInfo.is_deleted == 0).first()
        
        if not cls:
            raise HTTPException(status_code=404, detail="班级不存在")
        
        # 2. 标记为已删除
        cls.is_deleted = 1
        cls.update_time = datetime.now()
        
        # 3. 提交
        db.commit()
