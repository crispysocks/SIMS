# Agent 接口测试模板

> 本文档用于测试 SIMS 系统为 Agent 提供的两个专用 HTTP 接口：
>
> 1. `POST /agent/sql/query` — SQL 查询接口
> 2. `POST /agent/save` — 数据保存接口（支持 sql/data → xlsx/db 四种组合）
>
> 测试数据来源：`resources/agent-import-sample.json`

***

## 前置准备

### 1. 启动后端服务

```bash
cd c:\Users\Windows\Desktop\SIMS
uv run fastapi dev
```

> 默认服务地址：`http://localhost:8000`

### 2. 获取 JWT Token

所有 Agent 接口需要携带 `Authorization: Bearer <token>` 请求头。

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

***

## 一、SQL 查询接口测试

### 接口信息

| 项目           | 内容                              |
| ------------ | ------------------------------- |
| 端点           | `POST /agent/sql/query`         |
| 认证           | `Authorization: Bearer <token>` |
| Content-Type | `application/json`              |

### 请求体模板

```json
{
  "sql": "SELECT student_no, name, gender, class_no, age FROM students WHERE isdeleted = 0 LIMIT 10",
  "params": null
}
```

### 测试用例 1：查询学生列表（含班级名称）

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

### 测试用例 2：查询班级就业统计

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

### 测试用例 3：查询学生成绩

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

### 测试用例 4：参数化查询（按班级查学生）

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

### 测试用例 5：安全限制测试（应返回错误）

```powershell
$queryBody = @{
  sql = "DELETE FROM students WHERE student_no = 'AGENT001'"
  params = $null
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:8000/agent/sql/query `
  -Method POST `
  -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} `
  -Body $queryBody `
  -UseBasicParsing
```

> 预期结果：`仅允许执行SELECT查询语句`

***

## 二、数据保存接口测试

### 接口信息

| 项目           | 内容                              |
| ------------ | ------------------------------- |
| 端点           | `POST /agent/save`              |
| 认证           | `Authorization: Bearer <token>` |
| Content-Type | `application/json`              |

### 支持的数据来源与保存目标组合

| source\_type | target\_type | 说明                |
| ------------ | ------------ | ----------------- |
| `sql`        | `xlsx`       | SQL 查询结果导出为 Excel |
| `data`       | `db`         | JSON 数据写入数据库表     |

### 测试用例 A：SQL → xlsx（导出学生数据到 Excel）

```powershell
$saveBody = @{
  source_type = "sql"
  sql = "SELECT student_no, name, gender, class_no, age, phone, education, entrance_time, graduate_time FROM students WHERE isdeleted = 0"
  target_type = "xlsx"
  file_path = "./exports/agent_test_students.xlsx"
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:8000/agent/save `
  -Method POST `
  -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} `
  -Body $saveBody `
  -UseBasicParsing
```

> 注意：确保 `./exports/` 目录存在，否则提前创建 `mkdir -p ./exports`

### 测试用例 B：data → db（JSON 数据写入数据库表）

#### B1. 导入学生数据到临时表

```powershell
$jsonData = Get-Content -Raw -Path "resources/agent-import-sample.json" | ConvertFrom-Json

$saveBody = @{
  source_type = "data"
  data = $jsonData.students
  target_type = "db"
  table_name = "temp_import_students"
} | ConvertTo-Json -Depth 10

Invoke-WebRequest -Uri http://localhost:8000/agent/save `
  -Method POST `
  -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} `
  -Body $saveBody `
  -UseBasicParsing
```

#### B2. 导入成绩数据到临时表

```powershell
$jsonData = Get-Content -Raw -Path "resources/agent-import-sample.json" | ConvertFrom-Json

$saveBody = @{
  source_type = "data"
  data = $jsonData.scores
  target_type = "db"
  table_name = "temp_import_scores"
} | ConvertTo-Json -Depth 10

Invoke-WebRequest -Uri http://localhost:8000/agent/save `
  -Method POST `
  -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} `
  -Body $saveBody `
  -UseBasicParsing
```

#### B3. 导入就业数据到临时表

```powershell
$jsonData = Get-Content -Raw -Path "resources/agent-import-sample.json" | ConvertFrom-Json

$saveBody = @{
  source_type = "data"
  data = $jsonData.employment
  target_type = "db"
  table_name = "temp_import_employment"
} | ConvertTo-Json -Depth 10

Invoke-WebRequest -Uri http://localhost:8000/agent/save `
  -Method POST `
  -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} `
  -Body $saveBody `
  -UseBasicParsing
```

***

## 三、agent-import-sample.json 数据结构说明

文件路径：`resources/agent-import-sample.json`

### 根对象字段

| 字段名           | 类型     | 说明     |
| ------------- | ------ | ------ |
| `description` | string | 文件描述   |
| `students`    | array  | 学生数据数组 |
| `scores`      | array  | 成绩数据数组 |
| `employment`  | array  | 就业数据数组 |

### students 数组字段

| 字段名             | 类型     | 说明                           |
| --------------- | ------ | ---------------------------- |
| `student_no`    | string | 学生编号（主键）                     |
| `name`          | string | 学生姓名                         |
| `gender`        | string | 性别（男/女）                      |
| `class_no`      | string | 班级编号（外键 → classes.class\_no） |
| `age`           | int    | 年龄                           |
| `phone`         | string | 联系电话                         |
| `education`     | string | 学历（专科/本科/硕士）                 |
| `entrance_time` | string | 入学时间（YYYY-MM-DD）             |
| `graduate_time` | string | 毕业时间（YYYY-MM-DD）             |

### scores 数组字段

| 字段名          | 类型     | 说明                              |
| ------------ | ------ | ------------------------------- |
| `student_no` | string | 学生编号（外键 → students.student\_no） |
| `exam_no`    | int    | 考核序次（联合主键之一）                    |
| `exam_name`  | string | 考核名称（注意：数据库 scores 表无此字段，仅作标识）  |
| `score`      | int    | 成绩分数                            |
| `exam_date`  | string | 考核日期（YYYY-MM-DD）                |

### employment 数组字段

| 字段名                    | 类型     | 说明                                 |
| ---------------------- | ------ | ---------------------------------- |
| `student_no`           | string | 学生编号（主键/外键 → students.student\_no） |
| `employment_status`    | string | 就业状态（待业/在聘/已离职）                    |
| `company_name`         | string | 公司名称                               |
| `salary`               | int    | 薪资                                 |
| `position`             | string | 工作岗位                               |
| `work_location`        | string | 工作地点                               |
| `offer_time`           | string | Offer 下发时间（YYYY-MM-DD）             |
| `employment_open_time` | string | 就业开放时间（YYYY-MM-DD）                 |

***

## 四、常见问题与注意事项

1. **isdeleted 过滤**：所有业务表都有 `isdeleted` 字段（0=正常，1=已删除），查询时务必加上 `WHERE isdeleted = 0`。
2. **scores 表结构**：数据库中 `scores` 表没有 `exam_name` 字段，只有 `exam_no`（数字序次）和 `exam_date`。
3. **employment 主键**：`employment` 表以 `student_no` 为主键，一个学生只能有一条就业记录。
4. **xlsx 目录**：保存到 xlsx 前确保目录存在，否则可能报错。
5. **db 写入模式**：保存到数据库时使用 `if_exists='append'` 模式，目标表需已存在且字段匹配。
6. **安全限制**：SQL 查询接口仅允许 `SELECT` 语句，禁止 `insert/update/delete/drop` 等关键字。

