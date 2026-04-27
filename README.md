# SIMS — 学生信息管理系统

基于 **FastAPI** + **SQLAlchemy** + **MySQL** + **React** 构建的学生信息管理系统，提供学生基本信息、考核成绩、就业信息、班级与教师管理以及多维统计分析能力。

---

## 技术栈

### 后端

| 层级 | 技术 |
|------|------|
| Web 框架 | FastAPI |
| ORM | SQLAlchemy 2.x |
| 数据库 | MySQL (PyMySQL 驱动) |
| 配置管理 | Pydantic Settings |
| 依赖管理 | uv |
| 测试 | pytest |

### 前端

| 层级 | 技术 |
|------|------|
| 框架 | React + TypeScript |
| 构建工具 | Vite |
| 路由 | React Router |
| HTTP | Fetch API |

---

## 项目结构

```
SIMS/
├── app/                      # 后端 FastAPI 应用
│   ├── api/                 # 路由层
│   ├── core/                # 核心配置与数据库引擎
│   ├── models/              # SQLAlchemy 数据模型
│   ├── schemas/             # Pydantic 请求/响应模型
│   ├── services/            # 业务逻辑层
│   ├── dependencies.py      # 认证与权限依赖
│   └── main.py              # FastAPI 应用入口
│
├── frontend/                # 前端 React 应用
│   ├── src/                 # 源代码目录
│   ├── public/              # 静态资源
│   └── package.json
│
├── docs/                    # 需求文档
├── tests/                  # 测试用例
└── .env                   # 环境变量
```

---

## 快速开始

### 1. 环境要求

- Python >= 3.12
- Node.js >= 18
- MySQL 服务已启动，并创建数据库 `student_management`

### 2. 后端安装与启动

```bash
# 安装依赖
uv sync

# 复制配置
cp .env.example .env

# 启动后端
uv run fastapi dev
```

后端访问 http://localhost:8000/docs

### 3. 前端安装与启动

```bash
cd frontend
npm install
npm run dev
```

前端访问 http://localhost:5173

---

## 功能模块

| 模块 | 说明 | 路由 |
|------|------|------|
| 登录 | 设置用户名和角色 | `/login` |
| 仪表盘 | 关键指标展示 | `/` |
| 学生管理 | 增删改查、搜索、软删除 | `/students` |
| 教师管理 | 教师信息管理 | `/teachers` |
| 班级管理 | 班级信息管理 | `/classes` |
| 成绩管理 | 成绩录入与查询 | `/scores` |
| 就业管理 | 就业信息管理 | `/employment` |
| 统计分析 | 数据可视化 | `/statistics` |

---

## 认证与权限

后端采用基于请求头的简化认证方式，通过 `X-User` 和 `X-Roles` 请求头传递用户信息。

前端登录页可选择角色：
- `admin` - 管理员（全部权限）
- `teacher` - 教师（查看+编辑）

---

## 相关文档

- [前端设计文档](frontend-design.md)
- [项目需求文档](docs/FastAPI项目需求.md)
- [数据库设计文档](docs/数据库设计文档.md)