---
name: use-sims
description: >
  SIMS 学生管理系统的 Agent 专用接口使用指南。
  当用户（Agent）需要通过 SQL 查询系统数据库、或将数据保存到 xlsx/数据库时，必须使用此技能。
  适用于：查询学生、班级、成绩、就业、教师等数据；批量导出数据到 Excel；将外部数据写入数据库。
  触发关键词：SIMS、学生管理系统、sql查询、数据库查询、导出xlsx、保存到数据库、agent接口。
license: MIT
---

# SIMS Agent 接口使用指南

> 本文档用于指导 Agent 正确调用 SIMS 系统提供的两个专用 HTTP 接口。
> 测试数据来源：`resources/agent-import-sample.json`

## 概述

SIMS（学生管理系统）为 Agent 提供了两个专用 HTTP 接口：

1. **SQL 查询接口** (`POST /agent/sql/query`) — 直接执行 SELECT 查询
2. **数据保存接口** (`POST /agent/save`) — 将数据保存到 xlsx 文件或数据库表

Agent 接口的权限要求为 `admin` 或 `teacher`，调用接口时需要在请求头中携带 JWT Token。

---

## 前置准备

### 1. 获取 JWT Token

所有 Agent 接口使用 JWT Token 认证（与系统现有认证一致）：

- 先调用 `/auth/login` 获取 token
- 在请求头中携带 `Authorization: Bearer <token>`

**PowerShell 示例：**

```powershell
$loginBody = @{username="admin"; password="123456"} | ConvertTo-Json
$loginResponse = Invoke-WebRequest -Uri http://localhost:8000/auth/login `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body $loginBody `
  -UseBasicParsing
$token = ($loginResponse.Content | ConvertFrom-Json).data.access_token
Write-Host "Token: $token"
```

> 注意：PowerShell 终端可能显示中文乱码，这是终端编码问题，接口实际返回的是正确的 UTF-8 编码数据。

---

## 一、SQL 查询接口

### 接口信息

| 项目 | 内容 |
|------|------|
| 端点 | `POST /agent/sql/query` |
| 认证 | `Authorization: Bearer <token>` |
| Content-Type | `application/json` |

### 请求体模板

```json
{
  "sql": "SELECT student_no, name, gender FROM students WHERE isdeleted = 0 LIMIT 10",
  "params": null
}
```

> `params` 为可选字段，用于参数化查询。不传时设为 `null` 或省略即可。

### 安全限制

- 仅允许 `SELECT` 语句
- 禁止包含以下关键字：`insert`, `update`, `delete`, `drop`, `truncate`, `alter`, `create`, `grant`, `revoke`
- 安全过滤使用单词边界匹配，字段名如 `isdeleted` 不会被误判

### 响应示例

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

### 常用查询模板

#### 查询学生列表（含班级名称）

```powershell
$queryBody = @{
  sql = "SELECT s.student_no, s.name, s.gender, s.age, c.class_name FROM students s LEFT JOIN classes c ON s.class_no = c.class_no WHERE s.isdeleted = 0 AND c.isdeleted = 0 LIMIT 20"
  params = $null
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:8000/agent/sql/query `
  -Method POST `
  -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} `
  -Body $queryBody `
  -UseBasicParsing
```

#### 查询班级就业统计

```powershell
$queryBody = @{
  sql = "SELECT c.class_name, COUNT(e.student_no) AS employment_count, AVG(e.salary) AS avg_salary FROM classes c LEFT JOIN students s ON c.class_no = s.class_no AND s.isdeleted = 0 LEFT JOIN employment e ON s.student_no = e.student_no AND e.isdeleted = 0 WHERE c.isdeleted = 0 GROUP BY c.class_no, c.class_name"
  params = $null
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:8000/agent/sql/query `
  -Method POST `
  -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} `
  -Body $queryBody `
  -UseBasicParsing
```

#### 查询学生成绩

```powershell
$queryBody = @{
  sql = "SELECT s.student_no, s.name, sc.exam_no, sc.score, sc.exam_date FROM students s JOIN scores sc ON s.student_no = sc.student_no WHERE s.isdeleted = 0 AND sc.isdeleted = 0 ORDER BY s.student_no, sc.exam_date"
  params = $null
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:8000/agent/sql/query `
  -Method POST `
  -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} `
  -Body $queryBody `
  -UseBasicParsing
```

#### 参数化查询（按班级查学生）

```powershell
$queryBody = @{
  sql = "SELECT student_no, name, gender, age FROM students WHERE class_no = :class_no AND isdeleted = 0"
  params = @{class_no = "C001"}
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:8000/agent/sql/query `
  -Method POST `
  -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} `
  -Body $queryBody `
  -UseBasicParsing
```

---

## 二、数据保存接口

### 接口信息

| 项目 | 内容 |
|------|------|
| 端点 | `POST /agent/save` |
| 认证 | `Authorization: Bearer <token>` |
| Content-Type | `application/json` |

### 支持的数据来源与保存目标组合

| source_type | target_type | 说明 |
|-------------|-------------|------|
| `sql` | `xlsx` | SQL 查询结果导出为 Excel 文件 |
| `data` | `db` | JSON 数据写入数据库表 |

### 示例 A：SQL → xlsx（导出学生数据到 Excel）

```powershell
$saveBody = @{
  source_type = "sql"
  sql = "SELECT student_no, name, gender, class_no, age, phone, education, entrance_time, graduate_time FROM students WHERE isdeleted = 0"
  target_type = "xlsx"
  file_path = "./exports/students.xlsx"
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:8000/agent/save `
  -Method POST `
  -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} `
  -Body $saveBody `
  -UseBasicParsing
```

> 注意：确保 `./exports/` 目录存在，否则提前创建目录。

### 示例 B：data → db（JSON 数据写入数据库表）

使用 `resources/agent-import-sample.json` 中的数据导入数据库：

```powershell
$jsonData = Get-Content -Raw -Path "resources/agent-import-sample.json" | ConvertFrom-Json

$saveBody = @{
  source_type = "data"
  data = $jsonData.students
  target_type = "db"
  table_name = "temp_students"
} | ConvertTo-Json -Depth 10

Invoke-WebRequest -Uri http://localhost:8000/agent/save `
  -Method POST `
  -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} `
  -Body $saveBody `
  -UseBasicParsing
```

> 注意：`data` 字段的值必须是数组（列表），即使只有一条记录也要用 `[{...}]` 格式。保存到数据库时使用 `if_exists='append'` 模式，目标表需已存在且字段类型匹配。

---

## 三、数据库设计说明

### 核心设计规则

1. **所有业务表都有 `isdeleted` 字段**（0=正常，1=已删除）。查询时必须加 `WHERE isdeleted = 0`，否则可能查到已删除的数据。
2. **逻辑删除而非物理删除**。数据不会真正从数据库删除，只是标记为已删除。
3. **外键约束**：
   - `students.class_no` -> `classes.class_no`（ondelete=RESTRICT，有学生的班级不能删）
   - `scores.student_no` -> `students.student_no`（ondelete=CASCADE，学生删除则成绩删除）
   - `employment.student_no` -> `students.student_no`（ondelete=CASCADE，学生删除则就业记录删除）
   - `classes.head_teacher_no` -> `teachers.teacher_no`（ondelete=SET NULL）
   - `classes.instructor_no` -> `teachers.teacher_no`（ondelete=SET NULL）
4. **联合主键**：`scores` 表使用 `(student_no, exam_no)` 作为联合主键，不是一个独立的 id 字段。
5. **枚举字段**：部分字段只能取固定值，写入非法值会导致错误。

### 表结构详情

#### `students` — 学生信息表

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| student_no | VARCHAR(20) | PRIMARY KEY | 学生编号，主键 |
| class_no | VARCHAR(20) | NOT NULL, FOREIGN KEY -> classes.class_no | 班级编号 |
| name | VARCHAR(50) | NOT NULL | 学生姓名 |
| birth_place | VARCHAR(100) | 可空 | 籍贯 |
| graduate_school | VARCHAR(100) | 可空 | 毕业院校 |
| major | VARCHAR(50) | 可空 | 专业 |
| entrance_time | DATE | NOT NULL | 入学时间 |
| graduate_time | DATE | 可空 | 毕业时间 |
| education | ENUM('专科','本科','硕士') | 可空 | 学历 |
| advisor_name | VARCHAR(50) | 可空 | 顾问姓名 |
| age | INT | 可空 | 年龄 |
| gender | ENUM('男','女') | NOT NULL | 性别 |
| phone | VARCHAR(20) | 可空 | 联系电话 |
| id_card | VARCHAR(18) | 可空 | 身份证号 |
| isdeleted | INT | DEFAULT 0 | 逻辑删除标记 |

#### `classes` — 班级信息表

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| class_no | VARCHAR(20) | PRIMARY KEY | 班级编号，主键 |
| class_name | VARCHAR(50) | NOT NULL | 班级名称 |
| class_open_time | DATE | NOT NULL | 开课时间 |
| head_teacher_no | VARCHAR(20) | FOREIGN KEY -> teachers.teacher_no, 可空 | 班主任编号 |
| instructor_no | VARCHAR(20) | FOREIGN KEY -> teachers.teacher_no, 可空 | 授课老师编号 |
| description | VARCHAR(500) | 可空 | 班级描述 |
| isdeleted | INT | DEFAULT 0 | 逻辑删除标记 |

#### `teachers` — 教师信息表

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| teacher_no | VARCHAR(20) | PRIMARY KEY | 教师编号，主键 |
| name | VARCHAR(50) | NOT NULL | 教师姓名 |
| gender | ENUM('男','女') | NOT NULL | 性别 |
| phone | VARCHAR(20) | 可空 | 联系电话 |
| email | VARCHAR(100) | 可空 | 电子邮箱 |
| id_card | VARCHAR(18) | 可空 | 身份证号 |
| birthday | DATE | 可空 | 出生日期 |
| hire_date | DATE | 可空 | 入职日期 |
| subject | VARCHAR(50) | 可空 | 授课科目 |
| isdeleted | INT | DEFAULT 0 | 逻辑删除标记 |

#### `scores` — 成绩信息表

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| student_no | VARCHAR(20) | NOT NULL, FOREIGN KEY -> students.student_no, 联合主键之一 | 学生编号 |
| exam_no | INT | NOT NULL, 联合主键之一 | 考核序次（第几次考试） |
| score | INT | NOT NULL | 成绩分数 |
| exam_date | DATE | 可空 | 考核日期 |
| isdeleted | INT | DEFAULT 0 | 逻辑删除标记 |

> **重要**：`scores` 没有 `exam_name` 字段！只有 `exam_no`（数字序次）和 `exam_date`。
> 主键是 `(student_no, exam_no)` 联合主键，不是自增 id。

#### `employment` — 就业信息表

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| student_no | VARCHAR(20) | PRIMARY KEY, FOREIGN KEY -> students.student_no | 学生编号，既是主键也是外键 |
| employment_status | ENUM('待业','在聘','已离职') | DEFAULT '在聘' | 就业状态 |
| employment_open_time | DATETIME | 可空 | 就业开放时间 |
| offer_time | DATETIME | 可空 | offer 下发时间 |
| company_name | VARCHAR(100) | 可空 | 公司名称 |
| salary | DECIMAL(10,2) | 可空 | 薪资 |
| position | VARCHAR(50) | 可空 | 工作岗位 |
| work_location | VARCHAR(100) | 可空 | 工作地点 |
| isdeleted | INT | DEFAULT 0 | 逻辑删除标记 |

> **重要**：一个学生只能有一条就业记录（`student_no` 是主键）。如果要更新学生就业信息，应该用 UPDATE 而不是 INSERT。

#### `users` — 系统用户表

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 用户ID，自增主键 |
| username | VARCHAR(50) | NOT NULL, UNIQUE | 登录账号 |
| password_hash | VARCHAR(128) | NOT NULL | 密码MD5哈希值 |
| roles | VARCHAR(100) | NOT NULL, DEFAULT 'teacher' | 角色列表，逗号分隔 |
| is_active | INT | DEFAULT 1, NOT NULL | 账号是否启用（1=启用，0=禁用） |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

> **注意**：`users` 表与学生表/教师表是分开的，没有外键关系。用户是系统登录账号，学生/教师是业务数据。

---

## 四、agent-import-sample.json 数据结构说明

文件路径：`resources/agent-import-sample.json`

### 根对象字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `description` | string | 文件描述 |
| `students` | array | 学生数据数组 |
| `scores` | array | 成绩数据数组 |
| `employment` | array | 就业数据数组 |

### students 数组字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `student_no` | string | 学生编号（主键） |
| `name` | string | 学生姓名 |
| `gender` | string | 性别（男/女） |
| `class_no` | string | 班级编号（外键 → classes.class_no） |
| `age` | int | 年龄 |
| `phone` | string | 联系电话 |
| `education` | string | 学历（专科/本科/硕士） |
| `entrance_time` | string | 入学时间（YYYY-MM-DD） |
| `graduate_time` | string | 毕业时间（YYYY-MM-DD） |

### scores 数组字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `student_no` | string | 学生编号（外键 → students.student_no） |
| `exam_no` | int | 考核序次（联合主键之一） |
| `exam_name` | string | 考核名称（注意：数据库 scores 表无此字段，仅作标识） |
| `score` | int | 成绩分数 |
| `exam_date` | string | 考核日期（YYYY-MM-DD） |

### employment 数组字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `student_no` | string | 学生编号（主键/外键 → students.student_no） |
| `employment_status` | string | 就业状态（待业/在聘/已离职） |
| `company_name` | string | 公司名称 |
| `salary` | int | 薪资 |
| `position` | string | 工作岗位 |
| `work_location` | string | 工作地点 |
| `offer_time` | string | Offer 下发时间（YYYY-MM-DD） |
| `employment_open_time` | string | 就业开放时间（YYYY-MM-DD） |

---

## 五、错误处理

接口返回标准 `ApiResponse` 格式，错误时 `data` 为 `null`，`message` 包含错误详情。常见错误：

- `仅允许执行SELECT查询语句` — SQL 中包含非 SELECT 语句
- `SQL中包含禁止的关键字: xxx` — 触发了安全限制（使用单词边界匹配，不会误判字段名）
- `SQL执行错误: ...` — 语法错误或表不存在
- `保存xlsx失败: ...` — 文件路径无效或磁盘空间不足
- `写入数据库失败: ...` — 表结构不匹配或数据库错误

---

## 六、最佳实践

1. **始终过滤 isdeleted = 0**，避免查询到已删除的数据。
2. **使用 LIMIT** 进行大数据量查询，防止返回过多数据。
3. **保存到数据库时**，确保目标表已存在且字段类型匹配；`to_sql` 使用 `if_exists='append'` 模式。
4. **保存 xlsx 时**，确保目录存在（如 `./exports/`），否则提前创建目录。
5. **参数化查询**：使用 `params` 传递参数，避免 SQL 注入风险。
