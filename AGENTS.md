# AGENTS.md

## Project Overview

FastAPI Student Management System (SIMS). Python 3.12 + SQLAlchemy + MySQL + React 19 + TypeScript.

## Commands

### 后端
- **Dev server**: `uv run fastapi dev` or `uv run uvicorn app.main:app --reload`
- **Tests**: `uv run pytest`
- **Sync deps**: `uv sync`

### 前端
- **Dev server**: `cd frontend && npm run dev`
- **Build**: `cd frontend && npm run build` (includes `tsc -b` typecheck)
- **Lint**: `cd frontend && npm run lint`

## Database

- MySQL, database `student_management`. Auto-creates on startup via `app/core/database.py`.
- Config in `.env` (see `.env.example`). Copy it before running: `cp .env.example .env`. Key vars: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `CORS_ORIGINS` (JSON string), `UPLOAD_DIR`.
- Default CORS: `http://localhost:5173` only.

## Architecture

### 后端
- `app/` is root package. Use `from app.core.config import settings` (not `from app.config`).
- Entry point: `app/main.py` (includes all routers on startup, calls `init_db()`).
- Auth: Header-based (`X-User`, `X-Roles`). Default roles: `admin`, `teacher`. See `app/dependencies.py`.

### 前端
- Entry point: `frontend/src/main.tsx`
- Routes: `frontend/src/routes/index.tsx`
- API client: `frontend/src/api/client.ts` (Axios with interceptors for auth headers)
- State management: Zustand with persist middleware (`authStore`, `appStore`)
- Data fetching: TanStack Query v5
- UI components: Custom shadcn/ui-style components in `frontend/src/components/ui/`

## Key Files

### 后端
- `app/core/config.py` — Settings class with `case_sensitive=True` (env vars must be UPPER_SNAKE_CASE).
- `app/core/database.py` — Engine, SessionLocal, get_db, init_db.
- `app/api/` — All route modules.
- `app/models/` — SQLAlchemy models.
- `app/schemas/` — Pydantic schemas.

### 前端
- `frontend/src/api/` — API modules per domain (students, teachers, classes, scores, employment, statistics).
- `frontend/src/types/` — TypeScript interfaces for all entities.
- `frontend/src/stores/` — Zustand stores (auth, app UI state).
- `frontend/src/lib/constants.ts` — Role permissions, enum mappings.

## Quirks

- Upload path `./uploads` hardcoded in some services — directory doesn't exist by default, create it if needed.
- Excel import expects columns matching `Student` model fields (`student_no`, `name`, `gender`, `grade`, etc.).
- Frontend uses no pagination — all data is fetched and scrollable in tables.
- API response format varies: some return `{message, data}`, others return model directly. Client interceptor normalizes this.

---

# SIMS Agent 接口使用指南

## 概述

SIMS（学生管理系统）为 Agent 提供了两个专用 HTTP 接口：

1. **SQL 查询接口** (`POST /agent/sql/query`) — 直接执行 SELECT 查询
2. **数据保存接口** (`POST /agent/save`) — 将数据保存到 xlsx 文件或数据库表

Agent 的权限与 `teacher` 一致，调用接口时需要在请求头中携带模拟的教师身份认证信息（见下方认证说明）。

## 认证方式

所有 Agent 接口需要 Header 认证（与系统现有认证一致）：

- `X-User`: `agent`
- `X-Roles`: `teacher`

示例 curl（Windows PowerShell）：
```powershell
Invoke-WebRequest -Uri http://localhost:8000/agent/sql/query `
  -Method POST `
  -Headers @{"Content-Type"="application/json"; "X-User"="agent"; "X-Roles"="teacher"} `
  -Body '{"sql": "SELECT * FROM students WHERE isdeleted = 0 LIMIT 5"}' `
  -UseBasicParsing
```

> 注意：PowerShell 终端可能显示中文乱码，这是终端编码问题，接口实际返回的是正确的 UTF-8 编码数据。如需确认中文正常，可用 `uv run python` 调用 `urllib.request` 测试。

## 数据库表结构

主要表及字段：

| 表名 | 主要字段 | 说明 |
|------|---------|------|
| `students` | student_no, name, gender, class_no, age, phone, education, entrance_time, graduate_time, isdeleted | 学生信息 |
| `classes` | class_no, class_name, class_open_time, head_teacher_no, instructor_no, isdeleted | 班级信息 |
| `teachers` | teacher_no, name, gender, phone, email, subject, isdeleted | 教师信息 |
| `scores` | student_no, exam_no, exam_name, score, exam_date, isdeleted | 成绩信息 |
| `employment` | student_no, employment_status, company_name, salary, position, work_location, offer_time, isdeleted | 就业信息 |
| `users` | username, password_hash, roles, is_active | 系统用户 |

> 注意：所有业务表都有 `isdeleted` 字段（0=正常，1=已删除），查询时建议加上 `WHERE isdeleted = 0`。

## 接口 1：SQL 查询

**Endpoint**: `POST /agent/sql/query`

**请求体**：
```json
{
  "sql": "SELECT student_no, name, gender FROM students WHERE isdeleted = 0 LIMIT 10",
  "params": {}
}
```

**安全限制**：
- 仅允许 `SELECT` 语句
- 禁止包含以下关键字：`insert`, `update`, `delete`, `drop`, `truncate`, `alter`, `create`, `grant`, `revoke`
- 安全过滤使用单词边界匹配，字段名如 `isdeleted` 不会被误判（已修复）

**响应示例**：
```json
{
  "message": "查询成功",
  "data": {
    "columns": ["student_no", "name", "gender"],
    "rows": [
      {"student_no": "2021001", "name": "张三", "gender": "男"}
    ],
    "row_count": 1
  }
}
```

## 接口 2：保存数据

**Endpoint**: `POST /agent/save`

支持两种数据来源和两种保存目标，共 4 种组合：

| source_type | target_type | 说明 |
|-------------|-------------|------|
| `sql` | `xlsx` | 将 SQL 查询结果导出为 Excel 文件 |
| `sql` | `db` | 将 SQL 查询结果写入数据库表 |
| `data` | `xlsx` | 将 JSON 数据导出为 Excel 文件 |
| `data` | `db` | 将 JSON 数据写入数据库表 |

### 示例 A：SQL 结果导出为 xlsx

```json
{
  "source_type": "sql",
  "sql": "SELECT * FROM students WHERE isdeleted = 0",
  "target_type": "xlsx",
  "file_path": "./exports/students.xlsx"
}
```

### 示例 B：SQL 结果写入数据库表

```json
{
  "source_type": "sql",
  "sql": "SELECT student_no, name FROM students WHERE class_no = 'C001'",
  "target_type": "db",
  "table_name": "temp_students"
}
```

### 示例 C：JSON 数据导出为 xlsx

```json
{
  "source_type": "data",
  "data": [
    {"student_no": "2021001", "name": "张三"},
    {"student_no": "2021002", "name": "李四"}
  ],
  "target_type": "xlsx",
  "file_path": "./exports/new_students.xlsx"
}
```

### 示例 D：JSON 数据写入数据库表

```json
{
  "source_type": "data",
  "data": [
    {"student_no": "2021001", "name": "张三"}
  ],
  "target_type": "db",
  "table_name": "temp_import"
}
```

## 常用查询模板

### 查询学生列表（含班级名称）
```sql
SELECT s.student_no, s.name, s.gender, s.age, c.class_name
FROM students s
LEFT JOIN classes c ON s.class_no = c.class_no
WHERE s.isdeleted = 0
LIMIT 20;
```

### 查询班级就业统计
```sql
SELECT
  c.class_name,
  COUNT(e.student_no) AS employment_count,
  AVG(e.salary) AS avg_salary
FROM classes c
LEFT JOIN students s ON c.class_no = s.class_no AND s.isdeleted = 0
LEFT JOIN employment e ON s.student_no = e.student_no AND e.isdeleted = 0
WHERE c.isdeleted = 0
GROUP BY c.class_no, c.class_name;
```

### 查询学生成绩
```sql
SELECT s.student_no, s.name, sc.exam_name, sc.score
FROM students s
JOIN scores sc ON s.student_no = sc.student_no
WHERE s.isdeleted = 0 AND sc.isdeleted = 0
ORDER BY s.student_no, sc.exam_date;
```

## 错误处理

接口返回标准 `ApiResponse` 格式，错误时 `data` 为 `null`，`message` 包含错误详情。常见错误：

- `仅允许执行SELECT查询语句` — SQL 中包含非 SELECT 语句
- `SQL中包含禁止的关键字: xxx` — 触发了安全限制（使用单词边界匹配，不会误判字段名）
- `SQL执行错误: ...` — 语法错误或表不存在
- `保存xlsx失败: ...` — 文件路径无效或磁盘空间不足
- `写入数据库失败: ...` — 表结构不匹配或数据库错误

## 最佳实践

1. **始终过滤 isdeleted = 0**，避免查询到已删除的数据。
2. **使用 LIMIT** 进行大数据量查询，防止返回过多数据。
3. **保存到数据库时**，确保目标表已存在且字段类型匹配；`to_sql` 使用 `if_exists='append'` 模式。
4. **保存 xlsx 时**，确保目录存在（如 `./exports/`），否则提前创建目录。
5. **参数化查询**：使用 `params` 传递参数，避免 SQL 注入风险。
