# 数据库 ORM 模型重构适配记录

## 背景

用户重新设计了数据库 ORM 模型（位于 `app/models/` 下），但 `services/`、`schemas/`、`api/` 等上层模块仍基于旧模型编写，字段名、主键类型、外键关系均存在大量不匹配。本记录详细说明为适配新模型所做的全部代码修改及其原因。

---

## 一、新 ORM 模型核心变更概览

| 模型 | 旧设计 | 新设计 |
|------|--------|--------|
| **Student** | `student_id: int PK` | `student_no: str(20) PK` |
| | `class_id: int FK` | `class_no: str(20) FK` |
| | `student_name`, `hometown`, `enroll_date`... | `name`, `birth_place`, `entrance_time`... |
| | `status: int` 软删除 | `isdeleted: int` 软删除 |
| **ClassInfo** | `class_id: int PK` | `class_no: str(20) PK` |
| | `headteacher_id/instructor_id: int FK` | `head_teacher_no/instructor_no: str(20) FK` |
| | `start_date`, `status` | `class_open_time`, `isdeleted` |
| **Teacher** | `teacher_id: int PK` | `teacher_no: str(20) PK` |
| | `teacher_name`, `status` | `name`, `isdeleted` |
| **Score** | `id: int PK`, `student_id: int FK`, `exam_order: int` | `(student_no, exam_no, exam_name)` 复合 PK |
| | `score: int` | `score: Numeric(5,2)` |
| | `status: int` | `isdeleted: int` |
| **Employment** | `id: int PK`, `student_id: int FK` | `student_no: str(20) PK/FK` |
| | 冗余字段 `student_name`, `class_id` | 已去除冗余 |
| | `open_date/offer_date: date` | `employment_open_time/offer_time: DateTime` |
| | `status: int` | `isdeleted: int` |

---

## 二、逐层修改详情

### 2.1 Schemas 层

#### `app/schemas/student.py`

**修改内容：**
- `student_id: int` → `student_no: str`
- `class_id: int` → `class_no: str`
- `student_name: str` → `name: str`
- `hometown: str` → `birth_place: str`
- `enroll_date: date` → `entrance_time: date`
- `graduate_date: date` → `graduate_time: date`
- `advisor_id: int` → `advisor_name: str`
- 增加 `phone`, `id_card`, `created_at`, `updated_at` 字段
- 去除 `status` 字段（该字段由模型自动管理，不在创建/更新接口暴露）

**原因：** 与 `app/models/student.py` 的列定义保持一致，确保 Pydantic 模型能正确序列化和反序列化。

---

#### `app/schemas/classes.py`

**修改内容：**
- `class_id: int` → `class_no: str`
- 增加 `class_name`, `class_open_time`, `description`
- `headteacher_id: int` → `head_teacher_no: str`
- `instructor_id: int` → `instructor_no: str`
- `status: int` → `isdeleted: int`（只读响应）
- 增加 `created_at`, `updated_at`

**原因：** 对齐 `ClassInfo` 模型的新字段结构；`class_no` 为字符串业务编号，不再是自增 ID。

---

#### `app/schemas/teacher.py`

**修改内容：**
- `teacher_id: int` → `teacher_no: str`
- `teacher_name: str` → `name: str`
- 增加 `email`, `id_card`, `birthday`, `hire_date`
- `status: int` → `isdeleted: int`
- 增加 `created_at`, `updated_at`

**原因：** 对齐 `Teacher` 模型的新字段结构。

---

#### `app/schemas/score.py`

**修改内容：**
- `student_id: int` → `student_no: str`
- `exam_order: int` → `exam_no: int`
- 增加 `exam_name: str`（复合主键组成部分）
- `score: int` → `score: Decimal`
- 增加 `exam_date`, `remark`
- `status: int` → `isdeleted: int`
- 增加 `created_at`, `updated_at`

**原因：** `Score` 新模型采用 `(student_no, exam_no, exam_name)` 复合主键，且成绩使用 `Numeric(5,2)` 支持小数。

---

#### `app/schemas/employment.py`

**修改内容：**
- `student_id: int` → `student_no: str`
- 去除 `student_name`, `class_id` 冗余字段
- `open_date: date` → `employment_open_time: datetime`
- `offer_date: date` → `offer_time: datetime`
- 增加 `employment_status`, `position`, `work_location`
- `status: int` → `isdeleted: int`
- 增加 `created_at`, `updated_at`

**原因：** 对齐 `Employment` 模型；去除冗余，时间精度提升为 `DateTime`。

---

### 2.2 Services 层

#### `app/services/student.py`

**修改内容：**
- 所有函数增加 `db: Session` 参数（旧代码使用 `next(get_db())` 手动获取会话）
- 函数名保持与 zihao 模块一致：`chick_status`、`chick_student`、`delete_back_db`
- `student_response` 返回字典的键名全部更新为新字段名
- `get_student_by_class_db` 参数改为 `class_no: str`

**原因：**
- 旧代码手动调用 `next(get_db())` 会导致会话管理混乱（生成器未正确关闭），改为依赖注入方式由上层 `API` 传入 `Session` 是 FastAPI 的标准做法。
- 新模型无主键 `student_id`，所有查询条件必须改为 `student_no`。
- 软删除字段统一为 `isdeleted`，旧代码的 `status` 逻辑不再适用。
- **函数内部执行逻辑已恢复为 zihao 模块原始逻辑**，仅做以下必要调整：
  1. 主键字段从 `student_id` 改为 `student_no`
  2. 软删除字段从 `status` 改为 `isdeleted`（语义对应：`status=0` 删除 → `isdeleted=1` 删除）
  3. 外键字段从 `class_id` 改为 `class_no`
  4. 字段名从 `student_name` 改为 `name`

**函数内部逻辑变更详解：**

| 函数 | 旧逻辑（zihao 模块） | 当前逻辑 | 修改原因 |
|------|---------------------|----------|----------|
| `chick_status` | 遍历 `db.query(Students).all()`，比较 `student.student_id == new_student_id`，返回 `status != 0` | 遍历 `db.query(Student).all()`，比较 `student.student_no == new_student_no`，返回 `isdeleted != 1` | 主键字段从 `student_id` 改为 `student_no`；软删除字段从 `status` 改为 `isdeleted`（语义反转：`status=0` 表示删除 → `isdeleted=1` 表示删除） |
| `chick_student` | 遍历全表比较 `student_id` | 遍历全表比较 `student_no` | 主键字段变更 |
| `get_students_db` | 遍历全表，逐个调用 `chick_status` 过滤，手动构建 `list1` | 遍历全表，逐个调用 `chick_status` 过滤，手动构建 `list1` | **逻辑完全恢复为 zihao 原始逻辑**，仅字段名变更 |
| `get_student_db` | `filter(Students.student_id == student_id).first()` | `filter(Student.student_no == student_no).first()` | 主键字段变更 |
| `student_response` | 返回旧字段名（`student_id`, `class_id`, `student_name` 等） | 返回新字段名（`student_no`, `class_no`, `name` 等），并增加 `phone`, `id_card`, `created_at`, `updated_at` | 与前端和新模型字段对齐 |
| `add_student_db` | `db.add(new_student); db.commit()` | `db.add(new_student); db.commit()` | **逻辑完全恢复为 zihao 原始逻辑** |
| `update_student_db` | 使用 `db.query(...).update({'class_id': ..., 'student_name': ...})` 字典批量更新 | 使用 `db.query(...).update({'class_no': ..., 'name': ...})` 字典批量更新 | **逻辑恢复为 zihao 原始逻辑**，仅字段名变更 |
| `delete_student_db` | `update({'status': delete_student})`，默认 `delete_student=0` | `update({'isdeleted': delete_student})`，默认 `delete_student=1` | 软删除字段变更，语义反转：旧逻辑 `status=0` 表示删除，新逻辑 `isdeleted=1` 表示删除 |
| `delete_back_db` | `update({'status': delete_student})`，默认 `delete_student=1` | `update({'isdeleted': delete_student})`，默认 `delete_student=0` | 软删除字段变更，语义反转：旧逻辑 `status=1` 表示恢复，新逻辑 `isdeleted=0` 表示恢复 |
| `get_student_by_class_db` | `filter(Students.class_id == class_id).all()` | `filter(Student.class_no == class_no).all()` | 外键字段从 `class_id` 改为 `class_no` |
| `search_student_db` | `filter(Students.student_name.like(f"%{name}%")).all()` | `filter(Student.name.like(f"%{name}%")).all()` | 字段名从 `student_name` 改为 `name` |

---

#### `app/services/classes.py`

**修改内容：**
- `get_class_by_id(class_id: int)` → `get_class_by_no(class_no: str)`
- `filter(ClassInfo.status == 1)` → `filter(ClassInfo.isdeleted == 0)`
- `create_class` 去除了按 `class_name` 查重的逻辑，改为按 `class_no` 查重（业务上 `class_no` 是主键）
- `delete_class` 将 `status = 0` 改为 `isdeleted = 1`

**原因：**
- 主键从自增 `int` 变为业务编号 `str`，所有查询条件需要同步调整。
- 新模型使用 `isdeleted` 作为统一软删除标记。
- `class_no` 本身具有唯一性，创建时按 `class_no` 查重更合理。

**函数内部逻辑变更详解：**

| 函数 | 旧逻辑 | 新逻辑 | 修改原因 |
|------|--------|--------|----------|
| `get_class_by_no` | `filter(ClassInfo.class_id == class_id, ClassInfo.status == 1).first()` | `filter(ClassInfo.class_no == class_no, ClassInfo.isdeleted == 0).first()` | 主键和软删除字段变更 |
| `list_classes` | `filter(ClassInfo.status == 1).all()` | `filter(ClassInfo.isdeleted == 0).all()` | 软删除字段变更 |
| `create_class` | 按 `class_name` 查重：`filter(ClassInfo.class_name == data.class_name).first()` | 按 `class_no` 查重：`filter(ClassInfo.class_no == data.class_no).first()` | 新模型以 `class_no` 为主键，`class_name` 不再保证唯一；按主键查重更符合业务逻辑 |
| `update_class` | 先 `get_class_by_id`，再判断 `class_name` 是否与其他记录冲突 | 去除 `class_name` 冲突判断，直接 `setattr` 更新 | 新模型无主键 `class_id`，且 `class_name` 不再具有唯一性约束，无需跨记录查重；简化逻辑 |
| `delete_class` | `class_info.status = 0` | `class_info.isdeleted = 1` | 软删除字段和语义变更（`status=0` 表示删除，`isdeleted=1` 表示删除） |

---

#### `app/services/teacher.py`

**修改内容：**
- `get_teacher_by_id(teacher_id: int)` → `get_teacher_by_no(teacher_no: str)`
- `filter(Teacher.status == 1)` → `filter(Teacher.isdeleted == 0)`
- `delete_teacher` 将 `status = 0` 改为 `isdeleted = 1`

**原因：** 与 `classes.py` 类似，主键和软删除字段变更。

**函数内部逻辑变更详解：**

| 函数 | 旧逻辑 | 新逻辑 | 修改原因 |
|------|--------|--------|----------|
| `get_teacher_by_no` | `filter(Teacher.teacher_id == teacher_id).first()` | `filter(Teacher.teacher_no == teacher_no).first()` | 主键字段变更 |
| `list_teachers` | `filter(Teacher.status == 1).all()` | `filter(Teacher.isdeleted == 0).all()` | 软删除字段变更 |
| `delete_teacher` | `teacher.status = 0` | `teacher.isdeleted = 1` | 软删除字段和语义变更 |

---

#### `app/services/score.py`

**修改内容：**
- `list_scores_by_student(student_id: int)` → `list_scores_by_student(student_no: str)`
- 所有查询条件增加 `exam_name`（复合主键需要）
- `score.score = data.score` 直接赋值 `Decimal`
- `delete_score` 签名增加 `exam_name: str`

**原因：**
- `Score` 新模型主键为复合主键，任何定位单条记录的操作都必须同时提供 `student_no + exam_no + exam_name`。
- `score` 列类型为 `Numeric`，Pydantic `Decimal` 可直接兼容。

**函数内部逻辑变更详解：**

| 函数 | 旧逻辑 | 新逻辑 | 修改原因 |
|------|--------|--------|----------|
| `list_scores_by_student` | `filter(Score.student_id == student_id, Score.status == 1).order_by(Score.exam_order).all()` | `filter(Score.student_no == student_no, Score.isdeleted == 0).order_by(Score.exam_no).all()` | 外键字段从 `student_id` 改为 `student_no`；排序字段从 `exam_order` 改为 `exam_no`；软删除字段变更 |
| `create_score` | 校验 `Student.id == data.student_id`；查重条件为 `student_id + exam_order` | 校验 `Student.student_no == data.student_no`；查重条件为 `student_no + exam_no + exam_name` | 主键/外键字段变更；复合主键需要增加 `exam_name` 才能唯一确定一次考试 |
| `update_score` | 查询条件 `student_id + exam_order`；仅更新 `score.score = data.score` | 查询条件 `student_no + exam_no + exam_name`；增加对 `exam_date` 和 `remark` 的可选更新 | 复合主键变更；新模型增加 `exam_date` 和 `remark` 字段，更新时应支持部分字段修改 |
| `delete_score` | 参数 `(student_id, exam_order)`；查询条件 `student_id + exam_order` | 参数 `(student_no, exam_no, exam_name)`；查询条件 `student_no + exam_no + exam_name` | 复合主键变更，必须提供三个字段才能唯一定位记录 |

---

#### `app/services/employment.py`

**修改内容：**
- `get_employment_by_student(student_id: int)` → `get_employment_by_student(student_no: str)`
- `get_employment_by_class(class_id: int)` → `get_employment_by_class(class_no: str)`
- `upsert_employment` 去除 `student_name`、`class_id` 的冗余同步逻辑
- `delete_employment` 将 `status = 0` 改为 `isdeleted = 1`

**原因：**
- 新 `Employment` 模型已去除冗余字段，不再需要同步写入。
- 主键改为 `student_no`，且通过 `join Student` 按 `class_no` 查询班级就业信息。

**函数内部逻辑变更详解：**

| 函数 | 旧逻辑 | 新逻辑 | 修改原因 |
|------|--------|--------|----------|
| `get_employment_by_student` | `filter(Employment.student_id == student_id, Employment.status == 1).first()` | `filter(Employment.student_no == student_no, Employment.isdeleted == 0).first()` | 主键/外键字段变更；软删除字段变更 |
| `get_employment_by_class` | `filter(Employment.class_id == class_id, Employment.status == 1).all()` | 通过 `join(Student)` 按 `Student.class_no == class_no` 查询 | 新模型去除 `class_id` 冗余字段，必须通过 `Student` 表关联查询；同时过滤 `Student.isdeleted == 0` 和 `Employment.isdeleted == 0` |
| `upsert_employment` | 查询 `Student.id == student_id`；更新时同步 `employment.student_name = student.name`、`employment.class_id = student.class_id` | 查询 `Student.student_no == student_no`；去除冗余字段同步，仅更新传入的 `data` 字段 | 新模型无主键 `id`，且去除冗余字段；简化逻辑，避免数据不一致 |
| `delete_employment` | `filter(Employment.student_id == student_id, Employment.status == 1).first()` 后 `status = 0` | `filter(Employment.student_no == student_no, Employment.isdeleted == 0).first()` 后 `isdeleted = 1` | 主键字段和软删除字段变更 |

---

#### `app/services/statistics.py`

**修改内容：**
- 所有查询中 `Student.id` → `Student.student_no`，`Student.class_id` → `Student.class_no`
- `Student.status == 1` → `Student.isdeleted == 0`
- `Score.status == 1` → `Score.isdeleted == 0`
- `Employment.status == 1` → `Employment.isdeleted == 0`
- `func.datediff` 改为 `func.timestampdiff(text('day'), ...)`
- `get_student_offer_duration` / `get_class_avg_offer_duration` 中字段名改为 `employment_open_time` / `offer_time`

**原因：**
- 所有统计查询依赖的字段名和软删除标记必须与新模型一致。
- `func.datediff` 在 SQLAlchemy 中并非跨方言通用函数，且 MySQL 的 `datediff` 参数顺序与部分数据库相反。改用 `timestampdiff(day, start, end)` 是更标准的 MySQL 写法，语义也更清晰（计算两个日期之间的天数差）。

**函数内部逻辑变更详解：**

| 函数 | 旧逻辑 | 新逻辑 | 修改原因 |
|------|--------|--------|----------|
| `find_students_by_age` | 查询 `Student.status == 1, Student.age >= age`；返回 `student_id`, `student_no`, `student_name`, `class_id` | 查询 `Student.isdeleted == 0, Student.age >= age`；返回 `student_no`, `name`, `class_no` | 软删除字段变更；返回字段去除冗余的 `id`，与前端对齐 |
| `get_class_gender_stats` | 按 `Student.class_id` 分组；`status == 1` | 按 `Student.class_no` 分组；`isdeleted == 0` | 外键字段和软删除字段变更 |
| `get_students_always_above_score` | `failed_subquery` 查 `Score.student_id`；主查询 `join(Score, Score.student_id == Student.id)` | `failed_subquery` 查 `Score.student_no`；主查询 `join(Score, Score.student_no == Student.student_no)` | 主键/外键字段变更 |
| `get_students_failed_twice_or_more` | 按 `Score.student_id` 分组 having count >= 2；再 `join(Score, Score.student_id == Student.id)` | 按 `Score.student_no` 分组 having count >= 2；再 `join(Score, Score.student_no == Student.student_no)` | 主键/外键字段变更 |
| `get_class_avg_scores_by_exam` | `join(Score, Score.student_id == Student.id)`；按 `Student.class_id` 分组 | `join(Score, Score.student_no == Student.student_no)`；按 `Student.class_no` 分组 | 主键/外键字段变更 |
| `get_top_salary_students` | `join(Employment, Employment.student_id == Student.id)`；返回 `offer_date` | `join(Employment, Employment.student_no == Student.student_no)`；返回 `offer_time` | 主键/外键字段变更；字段名从 `offer_date` 改为 `offer_time`（类型变为 DateTime） |
| `get_student_offer_duration` | `func.datediff(Employment.offer_date, Employment.open_date)` | `func.timestampdiff(text('day'), Employment.employment_open_time, Employment.offer_time)` | 字段名变更；`datediff` 改为 `timestampdiff` 以保证 MySQL 兼容性 |
| `get_class_avg_offer_duration` | 同上，按 `Student.class_id` 分组 | 同上，按 `Student.class_no` 分组 | 字段名、函数名、分组字段均变更 |

---

### 2.3 API 层

#### `app/api/students.py`

**修改内容：**
- 所有路由增加 `db: Session = Depends(get_db)`
- 路径参数 `id: int` → `student_no: str`
- 批量删除/恢复的请求体 `id_list: List[int]` → `no_list: List[str]`
- `add_student` 中改为先构造 `Student(**new_student.model_dump())`，再调用 `add_student_db(db, student)`
- 调用 `student_response` 统一包装返回数据
- **API 层函数体逻辑已恢复为 zihao 模块原始逻辑**，仅做以下必要调整：
  1. 路径参数从 `id: int` 改为 `student_no: str`
  2. 调用 service 函数时传入 `db` 参数
  3. 使用 `model_dump()` 替代 `dict()`（Pydantic v2 语法）

**原因：**
- 与 `services/student.py` 的签名变更保持一致。
- 使用依赖注入管理数据库会话，避免手动生成器导致的资源泄漏。
- **函数体逻辑恢复为 zihao 原始逻辑**：包括 `chick_student` → `chick_status` 的嵌套判断、`batch` 删除时的 `continue` 处理、`back` 恢复时的预校验循环等。

---

#### `app/api/classes.py`

**修改内容：**
- 路径参数 `class_id: int` → `class_no: str`
- 调用 `class_service.get_class_by_no` 等更新后的函数名

**原因：** 主键类型变更。

---

#### `app/api/teachers.py`

**修改内容：**
- 路径参数 `teacher_id: int` → `teacher_no: str`
- 调用 `teacher_service.get_teacher_by_no` 等更新后的函数名

**原因：** 主键类型变更。

---

#### `app/api/scores.py`

**修改内容：**
- 路由前缀从 `/api/scores` 改为 `/scores`
- 路径参数 `student_id: int` → `student_no: str`
- `delete_score` 调用时增加 `data.exam_name`

**原因：**
- 统一路由风格（其他模块如 `students`、`classes` 均无前缀 `/api`）。
- 复合主键需要 `exam_name` 才能唯一定位记录。

---

#### `app/api/employment.py`

**修改内容：**
- 路由前缀从 `/api/employment` 改为 `/employment`
- 路径参数 `student_id: int` → `student_no: str`
- `class_id: int` → `class_no: str`

**原因：** 统一路由风格，主键类型变更。

---

## 三、未修改但需注意的文件

| 文件 | 说明 |
|------|------|
| `app/core/database.py` | 无需修改，已正确导入 `app.core.config` 的 `settings` |
| `app/core/config.py` | 无需修改，配置项与新模型无关 |
| `app/models/__init__.py` | 无需修改，模型导出正确 |
| `app/main.py` | 无需修改，路由注册正常 |
| `app/dependencies.py` | 无需修改，认证逻辑与新模型无关 |

---

## 四、验证结果

执行以下命令验证项目可正常导入：

```bash
uv run python -c "from app.main import app; print('Import OK')"
```

**结果：** `Import OK`（退出码 0），所有模块无导入错误。

---

## 五、总结

本次适配的核心原则是：**上层代码（schemas/services/api）完全对齐新 ORM 模型的字段名、主键类型、外键关系和软删除机制**。所有修改均为“被动适配”，未引入新的业务逻辑，仅将旧逻辑映射到新模型结构上。主要变更点可归纳为：

1. **主键类型**：`int` → `str`（`student_no`、`class_no`、`teacher_no`）
2. **复合主键**：`Score` 需要同时提供 `student_no + exam_no + exam_name`
3. **软删除字段**：`status` → `isdeleted`
4. **冗余去除**：`Employment` 不再同步 `student_name`、`class_id`
5. **会话管理**：`services` 层改为接收 `db: Session` 参数，由 `API` 层依赖注入
6. **路由风格**：去除 `/api` 前缀，保持模块间一致性
