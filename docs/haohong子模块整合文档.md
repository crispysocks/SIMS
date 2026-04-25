# 子模块整合文档

## 一、概述

本文档说明如何将 `sub_module/haohong/` 中的统计功能整合到当前主项目中。整合方向是将子模块的统计查询功能（DAO层 + API层）迁移到主项目的 `app/` 架构中。

---

## 二、项目结构对比

### 2.1 当前主项目结构

```
app/
├── core/
│   ├── config.py      # Settings 配置类
│   └── database.py  # SQLAlchemy engine + get_db
├── services/
│   └── student.py  # 学生CRUD服务
├── models/          # 空目录，待实现
├── schemas/        # 空目录，待实现
├── api/            # 空目录，待实现
├── dependencies.py # 空文件，待实现
└── main.py         # 空文件，待添加路由
```

### 2.2 子模块结构（作者：浩宏）

```
sub_module/haohong/
```

---

## 三、命名对齐

### 3.1 模块命名

| 子模块命名 | 推荐命名 | 说明 |
|-----------|----------|------|
| `Student_BASE` | `Student` | 模型命名统一为单数形式 |
| `Score_BASE` | `Score` | 成绩模型 |
| `Employment_BASE` | `Employment` | 就业模型 |
| `stu_api.py` | `statistics.py` | API路由文件重命名，更清晰表达功能 |
| `stu_dao.py` | `statistics_dao.py` | DAO层重命名 |
| `student_project.py` | `statistics_models.py` | 模型文件重命名 |

### 3.2 API端点命名

| 子模块端点 | 现有端点 | 推荐命名 |
|-----------|----------|----------|
| `/statistics/list1` | 无 | `/statistics/age-filter` |
| `/statistics/list2` | 无 | `/statistics/class-gender` |
| `/statistics/list3` | 无 | `/statistics/always-above` |
| `/statistics/list4` | 无 | `/statistics/failed-twice` |
| `/statistics/list5` | 无 | `/statistics/class-avg-score` |
| `/statistics/list6` | 无 | `/statistics/top-salary` |
| `/statistics/list7` | 无 | `/statistics/student-offer-duration` |
| `/statistics/list8` | 无 | `/statistics/class-offer-duration` |

### 3.3 字段映射

| 子模块字段 | 主项目当前字段 | 推荐字段 |
|-----------|---------------|----------|
| `student_id` | 未定义 | `student_id` |
| `student_name` | `name` | `name` |
| `class_id` | 未定义 | `class_id` |
| `gender` | `gender` (0/1) | `gender` (0=女,1=男 或 枚举) |
| `age` | `age` | `age` |
| `salary` | 无 | `salary` |
| `offer_date` | 无 | `offer_date` |
| `open_date` | 无 | `open_date` |
| `company_name` | 无 | `company_name` |

---

## 四、冲突与解决方案

### 4.1 数据库连接冲突

**问题：** 子模块使用硬编码数据库连接 (`mysql+pymysql://root:123456@localhost/test1`)，而主项目通过 `app/core/config.py` 配置管理。

**原因：** 子模块独立开发时未遵循项目配置规范。

**解决方案：**
- 不修改子模块的数据库工具代码
- 在整合时使用 `app/core/database.py` 的 `get_db` 替代 `sub_module/haohong/untils/database_util.py`
- 或者重构子模块 DAO 层，使用主项目的数据库连接方式

### 4.2 ORM模型冲突

**问题：** 子模块定义了 `Student_BASE`、`Score_BASE`、`Employment_BASE` 三个模型，与主项目当前的空模型目录冲突。

**原因：** 主项目的 Student 模型尚未定义，子模块的模型与 `app/services/student.py` 中引用的 `app.models.student.Student` 不存在。

**解决方案：**
1. 直接采用子模块的模型定义，移动到 `app/models/student.py`
2. ��根据需求重新设计模型，添加缺失的 Score 和 Employment 模型

### 4.3 性别字段定义冲突

**问题：** 子模块使用字符串 (`"男"` / `"女"`)，主项目使用整型 (`0` / `1`)。

**原因：** 两套系统独立设计，字段类型不统一。

**解决方案：**
- 推荐使用整型 + 枚举约束，与主项目现有逻辑保持一致
- 如使用子模块的字符串逻辑，需要修改所有查询的过滤条件

### 4.4 导入路径冲突

**问题：** 子模块 API 中导入路径错误：
```python
from fast_api_project.utils.database_util import get_db  # 模块名不存在
from file.dao.stu_dao import find_stu  # 包名不一致
```

**原因：** 子模块开发者使用错误的模块路径（可能是测试或本地配置不同）。

**解决方案：** 整合时修正导入路径为正确的项目结构：
```python
from app.core.database import get_db
from app.dao.statistics_dao import find_stu
```

---

## 五、必须修改主项目代码的原因

### 5.1 添加缺失的模型定义

**原因：** `app/services/student.py` 中引用了 `app.models.student.Student`，但该模型文件不存在。子模块提供了完整的模型定义，可以直接使用或参考。

### 5.2 添加Score和Employment模型

**原因：** 子模块的统计功能依赖 `Score_BASE` 和 `Employment_BASE` 两张表，主项目当前未定义这些模型。整合统计功能前，必须先添加这些模型。

### 5.3 修改get_db实现方式

**原因：** 子模块的 `database_util.py` 使用全局 session 对象，不符合 FastAPI 依赖注入的典型模式。主项目使用 yield 依赖方式，需要确保兼容。

---

## 六、整合实施步骤

### 步骤1：迁移模型定义
- 将 `sub_module/haohong/db_model/student_project.py` 中的模型定义复制到 `app/models/student.py`
- 添加 `Score` 和 `Employment` 模型
- 调整字段类型一致化（性别用枚举或整型）

### 步骤2：创建DAO层
- 创建 `app/dao/statistics_dao.py`
- 将 `sub_module/haohong/dao/stu_dao.py` 中的查询逻辑迁移
- 修改导入路径为实际的模型位置

### 步骤3：创建API路由
- 创建 `app/api/statistics.py`
- 迁移 `sub_module/haohong/api/stu_api.py` 中的8个端点
- 修正导入路径和依赖注入

### 步骤4：注册路由到main.py
- 在 `app/main.py` 中引入统计路由并注册

### 步骤5：更新配置
- 确认数据库配置正确（在 `.env` 或 `config.py` 中）

---

## 七、推荐整合后的目录结构

```
app/
├── core/
│   ├── config.py
│   └── database.py
├── models/
│   ├── __init__.py
│   └── student.py     # Student, Score, Employment 三个模型
├── schemas/
│   └── __init__.py
├── api/
│   ├── __init__.py
│   └── statistics.py  # 统计API路由
├── dao/               # 新增DAO层
│   ├── __init__.py
│   └── statistics_dao.py
├── services/
│   └── student.py    # 现有的学生CRUD服务
├── dependencies.py
└── main.py
```

---

## 八、总结

整合的核心要点：
1. **命名统一** - 将子模块的命名标准化，与主项目保持一致的代码风格
2. **使用配置** - 不使用硬编码数据库连接，统一使用 `app/core/config.py`
3. **迁移模型** - 将3个ORM模型添加到 `app/models/student.py`
4. **修复导入** - 修正子模块中错误的导入路径
5. **保持兼容** - 确保性别字段类型一致，避免运行时错误

整合后主项目将具备完整的统计查询功能，包括成绩统计、就业统计等高级功能。