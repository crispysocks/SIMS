# 报错用
from fastapi import HTTPException
# 数据库会话
from sqlalchemy.orm import Session

# 导入表结构
from models.classes import ClassInfo
# 导入校验类
from schemas.classes import ClassCreate, ClassUpdate

# 班级业务类，所有功能都在这里
class ClassService:

    # 1.分页 + 模糊查询  获取班级列表
    @staticmethod
    def get_class_list(db: Session, skip: int, limit: int, class_name=None):
        # 先查未被逻辑删除的有效班级数据
        query = db.query(ClassInfo).filter(ClassInfo.is_deleted == 0)

        # 判断前端是否传入班级名称，如果传了班级名字，就模糊搜索
        if class_name:
            query = query.filter(ClassInfo.class_name.contains(class_name))

        # 统计数据总条数
        total = query.count()
        # 配合offset和limit实现分页功能
        classes = query.offset(skip).limit(limit).all()

        return classes, total

    # 2.新增班级
    @staticmethod
    def create_class(db: Session, data: ClassCreate):
        # 班级重名校验：先查询数据库中是否存在同名且未删除的班级
        existing = db.query(ClassInfo).filter(
            ClassInfo.class_name == data.class_name,
            ClassInfo.is_deleted == 0
        ).first()

        # 重复就报错，提示班级名称已存在
        if existing:
            raise HTTPException(status_code=400, detail="班级已存在")

        # 创建班级对象 校验通过后，把前端传过来的班级数据，转换成数据库能识别的 ORM 对象，准备保存
        new_class = ClassInfo(**data.model_dump())

        # 保存到数据库
        db.add(new_class)
        db.commit()
        db.refresh(new_class)

        return new_class

    # 3.修改班级
    @staticmethod
    def update_class(db: Session, class_id: int, data: ClassUpdate):
        # 根据班级ID查询数据，判断班级是否存在
        cls = db.query(ClassInfo).filter(
            ClassInfo.class_id == class_id,
            ClassInfo.is_deleted == 0
        ).first()

        # 找不到报错
        if not cls:
            raise HTTPException(status_code=404, detail="班级不存在")

        # 只更新传过来的字段
        update_data = data.model_dump(exclude_unset=True)

        # 同时自动刷新更新时间，记录数据修改时间
        for key, value in update_data.items():
            setattr(cls, key, value)

        db.commit()
        db.refresh(cls)

        return cls

    # 4.删除班级（逻辑删除）
    @staticmethod
    def delete_class(db: Session, class_id: int):
        # 先根据班级ID查找班级
        cls = db.query(ClassInfo).filter(
            ClassInfo.class_id == class_id,
            ClassInfo.is_deleted == 0
        ).first()

        if not cls:
            raise HTTPException(status_code=404, detail="班级不存在")

        # 如果找到，就把它的删除标记改成1，代表已删除。数据还留在数据库里，方便以后恢复和查找记录。
        cls.is_deleted = 1
        db.commit()

    # 5.获取所有班级名称
    @staticmethod
    def get_class_names(db: Session):
        classes = db.query(ClassInfo).filter(ClassInfo.is_deleted == 0).all()
        return [cls.class_name for cls in classes]

    # 6.统计一共有多少班级
    @staticmethod
    def get_class_total_count(db: Session):
        return db.query(ClassInfo).filter(ClassInfo.is_deleted == 0).count()

    # 7.根据ID查单个班级
    @staticmethod
    #根据传入的班级ID，查询没有被删除的班级
    def get_class_by_id(db: Session, class_id: int):
        #查到就返回班级信息
        return db.query(ClassInfo).filter(
            ClassInfo.class_id == class_id,
            ClassInfo.is_deleted == 0
        ).first()



