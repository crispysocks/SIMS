# SIMS — 学生信息管理系统

基于 **FastAPI** + **SQLAlchemy** + **MySQL** + **React 19** + **TypeScript** 构建的学生信息管理系统，提供学生基本信息、考核成绩、就业信息、班级与教师管理以及多维统计分析能力。

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
| 框架 | React 19 + TypeScript |
| 构建工具 | Vite 8 |
| 样式 | Tailwind CSS 3 |
| UI 组件 | shadcn/ui 风格自研组件 |
| 路由 | React Router v7 |
| 状态管理 | Zustand（持久化） |
| 数据请求 | TanStack Query v5 |
| 图表 | Recharts |
| 图标 | Lucide React |

---

## 项目结构

```
SIMS/
├── app/                      # 后端 FastAPI 应用
│   ├── api/                  # 路由层
│   ├── core/                 # 核心配置与数据库引擎
│   ├── models/               # SQLAlchemy 数据模型
│   ├── schemas/              # Pydantic 请求/响应模型
│   ├── services/             # 业务逻辑层
│   ├── dependencies.py       # 认证与权限依赖
│   └── main.py               # FastAPI 应用入口
│
├── frontend/                 # 前端 React 应用
│   ├── src/
│   │   ├── api/              # API 请求封装（按模块）
│   │   ├── components/       # UI 组件 + 布局组件
│   │   │   ├── ui/           # 基础 UI 组件（Button、Input、Table 等）
│   │   │   └── layout/       # 布局组件（Sidebar、Header、Layout）
│   │   ├── pages/            # 页面组件
│   │   ├── routes/           # 路由配置
│   │   ├── stores/           # Zustand 状态管理
│   │   ├── types/            # TypeScript 类型定义
│   │   └── lib/              # 工具函数和常量
│   ├── public/               # 静态资源
│   └── package.json
│
├── docs/                     # 需求与设计文档
│   ├── FastAPI项目需求.md
│   ├── 数据库设计文档.md
│   └── 数据库设计说明文档（通俗版）.md
│
├── tests/                    # 测试用例
├── frontend-design.md        # 前端设计文档
├── AGENTS.md                 # 项目规范与指南
└── .env                      # 环境变量
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
# 编辑 .env 配置数据库连接信息

# 启动后端
uv run uvicorn app.main:app
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

| 模块 | 说明 | 路由 | 权限 |
|------|------|------|------|
| 登录 | 设置用户名和角色 | `/login` | 公开 |
| 仪表盘 | 关键指标展示、快捷入口 | `/` | 任意用户 |
| 学生管理 | 增删改查、搜索、班级筛选、批量软删除/恢复 | `/students` | 任意用户查看；admin 可操作 |
| 学生详情 | 基本信息、成绩记录、就业信息（Tab 切换） | `/students/:student_no` | 任意用户 |
| 教师管理 | 教师信息增删改查 | `/teachers` | 任意用户 |
| 班级管理 | 班级信息增删改查 | `/classes` | 任意用户 |
| 成绩管理 | 按学生查询、录入/修改/删除成绩 | `/scores` | 任意用户查看；admin/teacher 可录入修改；admin 可删除 |
| 就业管理 v1 | 多维度筛选、增删改查 | `/employment` | 任意用户查看；admin/teacher 可编辑；admin 可删除 |
| 就业管理 v2 | 条件搜索、软删除、批量恢复 | `/employment-v2` | 任意用户查看；admin/teacher 可编辑；admin 可删除 |
| 统计分析 | 8 个统计维度，含图表和表格 | `/statistics` | 任意用户 |

---

## 认证与权限

- **认证方式**：Header-based（`X-User`, `X-Roles`）
- **角色**：`admin`（管理员）、`teacher`（教师）
- **权限控制**：
  - `admin`：拥有全部权限（删除、恢复、批量操作等）
  - `teacher`：可录入/修改成绩、添加/更新就业信息
  - 任意登录用户：可查看学生、成绩、就业、统计等信息

---

## 前端设计规范

- **布局**：侧边栏 + 顶部栏 + 内容区的经典后台管理结构
- **数据展示**：无分页设计，表格内滚动查看所有数据
- **主题**：支持浅色/深色模式切换
- **响应式**：侧边栏可折叠，适配不同屏幕尺寸
