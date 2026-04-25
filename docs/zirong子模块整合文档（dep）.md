# 子模块 zirong 整合方案

## 一、整合方向

将 `sub_module/zirong` 中的以下功能整合到当前项目 `app/` 中：

| 子模块目录 | 整合后目标位置 | 说明 |
|-----------|--------------|------|
| `models/teacherBase.py` | `app/models/teacher.py` | Teacher 和 Course 模型 |
| `dao/teacher_dao.py` | `app/dao/teacher_dao.py` | Teacher 和 Course DAO |
| `Services/teacher_services.py` | `app/services/teacher_service.py` | Teacher 和 Course 服务 |
| `Services/exceptions.py` | `app/utils/exceptions.py` | 自定义异常类 |
| `schemas/teacher_info.py` | `app/schemas/teacher.py` | Pydantic schemas |
| `api/teacher_api.py` | `app/api/teacher.py` | API 路由 |

---

## 二、必须修改的代码逻辑

### 2.1 Teacher 模型表名冲突

**问题**：子模块中 `Teacher` 类的 `__tablename__` 设为 `"teacher"`，而 `Course` 外键引用 `ForeignKey("teachers.id")`，表名不一致会导致外键约束失败。

**解决方案**：将 `Teacher.__tablename__` 改为 `"teachers"`，与外键引用保持一致。

```python
# 修改前
class Teacher(Base):
    __tablename__ = "teacher"  # 错误

# 修改后
class Teacher(Base):
    __tablename__ = "teachers"
```

### 2.2 DAO 层查询字段名错误

**问题**：子模块 `teacher_dao.py:21` 使用 `Teacher.id` 查询，但模型定义的字段名是 `teacher_id`。

**解决方案**：将查询条件从 `Teacher.id == teacher_id` 改为 `Teacher.teacher_id == teacher_id`。

### 2.3 Service 层字段名映射错误

**问题**：
- `teacher_services.py:22` 使用 `teacher_data.get('name')`，但模型字段是 `teacher_name`
- `teacher_services.py:117` 访问 `teacher.name`，应该是 `teacher.teacher_name`

**解决方案**：修正字段名映射。

### 2.4 Schema 与模型字段对齐

**问题**：子模块 schemas 使用 `name` 和 `status`，但模型定义 `teacher_name` 和 `status`(整型默认值0)。

**解决方案**：
- `TeacherCreate.name` → `teacher_name`
- `TeacherCreate.status` 类型改为 `int`，默认值 `0`

---

## 三、命名对齐

### 3.1 导入路径命名

| 子模块 (错误) | 整合后 (正确) |
|--------------|--------------|
| `Myproject.first_project.core.database` | `app.core.database` |
| `Myproject.first_project.schemas.teacher_info` | `app.schemas.teacher` |
| `Myproject.first_project.Services` | `app.services` |
| `Myproject.first_project.dao` | `app.dao` |
| `models.teacherBase` | `app.models.teacher` |

### 3.2 类和函数命名

| 子模块 | 推荐命名 | 说明 |
|--------|----------|------|
| `Teachers` (DAO) | `TeacherDAO` | 符合类名大写风格 |
| `Courses` (DAO) | `CourseDAO` | 符合类名大写风格 |
| `TeacherService` | `TeacherService` | 保持不变 |
| `CourseService` | `CourseService` | 保持不变 |
| `TeacherCreate` | `TeacherCreate` | 保持 Pydantic 风格 |
| `CourseCreate` | `CourseCreate` | 保持 Pydantic 风格 |

### 3.3 模型字段命名

| 子模块 Schema | 模型字段 | 整合后 Schema |
|--------------|----------|--------------|
| `name` | `teacher_name` | `teacher_name` |
| `subject` | `subject` | `subject` |
| `gender` | `gender` | `gender` |
| `phone_number` | `phone_number` | `phone_number` |
| `status` (str) | `status` (int) | `status` (int) |

---

## 四、代码冲突及解决方案

### 4.1 config.py 密码差异

| 项目 | DB_PASSWORD |
|------|-------------|
| 当前项目 | `123456` |
| 子模块 | `your_password` |

**解决**：保留当前项目配置 (`123456`)，子模块配置不覆盖。

### 4.2 database.py 连接池参数

当前项目 `database.py` 包含连接池配置，子模块没有。

**解决**：保留当前项目的完整配置：
```python
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE,
    pool_recycle=settings.DB_POOL_RECYCLE,
)
```

### 4.3 FastAPI 应用实例

子模块 `teacher_api.py` 创建了独立的 FastAPI 实例：
```python
app = FastAPI(description='老师信息及任课信息的管理')
```

**解决**：在 `app/main.py` 中使用项目的 `FastAPI` 实例，通过 `app.include_router()` 合并路由，而不是创建新实例。

---

## 五、整合后的目录结构

```
app/
├── main.py                    # 主入口，include_router
├── core/
│   ├── config.py            # 保留当前配置
│   └── database.py          # 保留当前配置
├── models/
│   ├── __init__.py
│   └── teacher.py           # Teacher, Course 模型
├── schemas/
│   ├── __init__.py
│   └── teacher.py          # TeacherCreate, TeacherUpdate, CourseCreate, CourseUpdate
├── dao/
│   ├── __init__.py
│   └── teacher_dao.py      # TeacherDAO, CourseDAO
├── services/
│   ├── __init__.py
│   └── teacher_service.py # TeacherService, CourseService
├── utils/
│   └── exceptions.py       # 自定义异常类
└── api/
    ├── __init__.py
    └── teacher.py          # Teacher API 路由
```

---

## 六、整合步骤摘要

1. **创建模型** `app/models/teacher.py` → 定义 `Teacher`, `Course`，表名改为 `"teachers"`
2. **创建 Schemas** `app/schemas/teacher.py` → 字段名与模型对齐
3. **创建 DAO** `app/dao/teacher_dao.py` → 修正 `Teacher.teacher_id` 查询
4. **创建 Service** `app/services/teacher_service.py` → 修正字段名映射
5. **创建异常** `app/utils/exceptions.py` → 复制异常类
6. **创建 API** `app/api/teacher.py` → 修正导入路径，使用 `app.include_router()`
7. **修改 main.py** → 添加路由

---

## 七、需要注意的风险点

1. **数据库表名**：`Teacher` 表名必须与 `Course` 外键一致，否则外键约束失败
2. **字段类型**：`status` 在模型中是 `Integer`，Schema 中需对应
3. **导入前缀**：所有 `Myproject.first_project` 替换为 `app`
4. **独立实例**：不要创建新的 FastAPI 实例，合并到主应用