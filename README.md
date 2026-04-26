# SIMS — 学生信息管理系统

基于 **FastAPI** + **SQLAlchemy** + **MySQL** 构建的学生信息管理系统后端，提供学生基本信息、考核成绩、就业信息、班级与教师管理以及多维统计分析能力。

---

## 技术栈

| 层级 | 技术 |
|------|------|
| Web 框架 | FastAPI |
| ORM | SQLAlchemy 2.x |
| 数据库 | MySQL (PyMySQL 驱动) |
| 配置管理 | Pydantic Settings |
| 依赖管理 | uv |
| 测试 | pytest |

---

## 项目结构

```
app/
├── api/              # 路由层（学生、成绩、就业、班级、教师、统计）
├── core/             # 核心配置与数据库引擎
├── models/           # SQLAlchemy 数据模型
├── schemas/          # Pydantic 请求/响应模型
├── services/         # 业务逻辑层
├── dependencies.py   # 认证与权限依赖
└── main.py           # FastAPI 应用入口

docs/                 # 需求文档与子模块整合说明
sub_module/           # 各子模块原始实现（haohong / junyi / zihao / zirong）
tests/                # 测试用例
```

---

## 快速开始

### 1. 环境要求

- Python >= 3.12
- MySQL 服务已启动，并创建数据库 `student_management`

### 2. 安装依赖

```bash
uv sync
```

### 3. 配置环境变量

复制示例配置文件：

```bash
cp .env.example .env
```

按需修改 `.env` 中的数据库连接信息：

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=student_management
DB_USER=root
DB_PASSWORD=your_password
```

### 4. 启动服务

```bash
# 开发模式（热重载）
uv run fastapi dev

# 或使用 uvicorn
uv run uvicorn app.main:app --reload
```

服务启动后访问：

- API 文档（Swagger UI）：http://localhost:8000/docs
- 首页：http://localhost:8000/

---

## 功能模块

| 模块 | 说明 | 路由前缀 |
|------|------|----------|
| 学生基本信息管理 | 学生增删改查、模糊搜索、按班级查询、软删除/恢复 | `/students` |
| 成绩管理 | 成绩录入、修改、删除、按学生查询 | `/api/scores` |
| 就业管理 | 就业信息记录、按学生/班级查询、更新与删除 | `/api/employment` |
| 班级管理 | 班级信息的增删改查 | `/api/classes` |
| 教师管理 | 教师与课程信息的增删改查 | `/api/teachers` |
| 统计分析 | 年龄筛选、班级性别统计、成绩分析、就业时长与薪资统计 | `/api/statistics` |

---

## 认证与权限

当前采用基于请求头的简化认证方式，通过 `X-User` 和 `X-Roles` 请求头传递用户信息。

- 默认角色：`admin`, `teacher`
- 部分接口（如删除操作）仅限 `admin` 角色访问

---

## 开发说明

- 应用启动时会自动调用 `init_db()` 初始化数据库表结构
- CORS 默认允许 `http://localhost:5173`，可在 `.env` 中通过 `CORS_ORIGINS` 调整
- 文件上传目录默认为 `./backend/uploads`

---

## 测试

```bash
uv run pytest
```

---

## 相关文档

- [项目需求文档](docs/FastAPI项目需求.md)
- [子模块整合说明](docs/)
