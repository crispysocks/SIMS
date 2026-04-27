# SIMS 前端项目设计方案

> **版本**：v2.0
> **日期**：2026-04-27
> **说明**：本文档基于后端 FastAPI 实际接口进行重构，明确前后端交互逻辑，作为前端开发的核心依据。

---

## 一、后端项目分析总结

### 1.1 技术栈
- **后端**：FastAPI + SQLAlchemy + MySQL
- **认证**：Header-based（`X-User`, `X-Roles`），角色：`admin`、`teacher`
- **CORS**：默认 `http://localhost:5173`
- **数据格式**：JSON，响应格式不统一（部分接口返回 `{message, data}`，部分直接返回模型）

### 1.2 数据模型（5 个核心实体）

| 实体 | 主键 | 核心字段 | 关联关系 |
|------|------|----------|----------|
| **Student**（学生） | `student_no` | 姓名、班级编号、性别、年龄、籍贯、毕业院校、专业、入学/毕业时间、学历、顾问、电话、身份证 | 关联 ClassInfo |
| **Teacher**（教师） | `teacher_no` | 姓名、性别、电话、邮箱、身份证、生日、入职日期、授课科目 | 被 ClassInfo 关联 |
| **ClassInfo**（班级） | `class_no` | 班级名称、开课时间、班主任编号、授课老师编号、描述 | 关联 Teacher（班主任/授课老师） |
| **Score**（成绩） | 联合主键 (`student_no`, `exam_no`, `exam_name`) | 成绩、考核日期、备注 | 关联 Student |
| **Employment**（就业） | `student_no` | 就业状态、就业开放时间、offer 时间、公司、薪资、岗位、工作地点 | 关联 Student |

### 1.3 认证机制
- 请求头传递：`X-User`（用户名）、`X-Roles`（角色，逗号分隔，如 `admin,teacher`）
- 默认角色：`admin`, `teacher`
- 权限控制：
  - `admin`：拥有全部权限（删除、恢复等）
  - `teacher`：可录入/修改成绩、添加/更新就业信息
  - 任意登录用户：可查看学生、成绩、就业、统计等信息

---

## 二、前端技术选型

基于当前项目模板及后端特性，前端技术栈确定如下：

| 层级 | 技术/库 | 说明 |
|------|---------|------|
| 框架 | **React 19** + **TypeScript** | 项目已初始化，保持使用 |
| 构建工具 | **Vite 8** | 项目已配置，热更新速度快 |
| UI 组件库 | **shadcn/ui** + **Tailwind CSS** | 与 React + TS 生态契合，支持主题定制 |
| 路由 | **React Router v7** | 声明式路由，支持嵌套路由、路由守卫 |
| 状态管理 | **Zustand** | 轻量、TypeScript 友好，适合中小型项目 |
| 数据请求 | **TanStack Query (React Query) v5** | 缓存、重试、乐观更新、权限控制集成 |
| 表单处理 | **React Hook Form** + **Zod** | 类型安全、性能优、与 shadcn 表单组件配合良好 |
| 图表 | **Recharts** | 基于 React，满足统计图表需求 |
| 图标 | **Lucide React** | 与 shadcn/ui 默认配套 |

---

## 三、前端项目结构

```
frontend/
├── public/                  # 静态资源
├── src/
│   ├── api/                 # API 请求封装
│   │   ├── client.ts        # Axios 实例（拦截器、Header 注入）
│   │   ├── students.ts      # 学生管理接口
│   │   ├── teachers.ts      # 教师管理接口
│   │   ├── classes.ts       # 班级管理接口
│   │   ├── scores.ts        # 成绩管理接口
│   │   ├── employment.ts    # 就业管理 v1 接口
│   │   ├── employmentV2.ts  # 就业管理 v2 接口
│   │   └── statistics.ts    # 统计分析接口
│   ├── components/          # 公共组件
│   │   ├── ui/              # shadcn/ui 基础组件
│   │   ├── layout/          # 布局组件（Sidebar, Header, Content）
│   │   ├── common/          # 业务公共组件（DataTable, FormModal, ConfirmDialog）
│   │   └── charts/          # 图表封装组件
│   ├── hooks/               # 自定义 Hooks
│   │   ├── useAuth.ts       # 认证与权限
│   │   └── useApi.ts        # API 请求 Hook 封装
│   ├── pages/               # 页面组件（按路由模块划分）
│   │   ├── Dashboard/       # 首页仪表盘
│   │   ├── Students/        # 学生管理
│   │   ├── Teachers/        # 教师管理
│   │   ├── Classes/         # 班级管理
│   │   ├── Scores/          # 成绩管理
│   │   ├── Employment/      # 就业管理（v1 + v2）
│   │   └── Statistics/      # 统计分析
│   ├── stores/              # Zustand 状态管理
│   │   ├── authStore.ts     # 用户信息、角色
│   │   └── appStore.ts      # 全局 UI 状态（侧边栏折叠、主题等）
│   ├── types/               # 全局 TypeScript 类型
│   │   ├── api.ts           # API 通用响应类型
│   │   ├── auth.ts          # 认证相关类型
│   │   └── index.ts         # 实体类型导出
│   ├── lib/                 # 工具函数
│   │   ├── utils.ts         # 通用工具（cn 函数等）
│   │   └── constants.ts     # 常量（角色、枚举值映射等）
│   ├── routes/              # 路由配置
│   │   └── index.tsx        # 路由表 + 权限守卫
│   ├── App.tsx              # 根组件（Providers 包裹）
│   └── main.tsx             # 入口文件
├── index.html
├── package.json
├── tailwind.config.js
├── tsconfig.json
└── vite.config.ts
```

---

## 四、路由设计

采用 React Router v7，布局为 **侧边栏 + 顶部栏 + 内容区** 的经典后台管理结构。

| 路径 | 页面 | 权限 | 说明 |
|------|------|------|------|
| `/login` | 登录页 | 公开 | 输入用户名和角色（开发阶段简化登录） |
| `/` | 仪表盘 | 任意用户 | 系统概览、快捷入口、核心统计卡片 |
| `/students` | 学生列表 | 任意用户 | 增删改查、模糊搜索、按班级筛选、批量软删除/恢复 |
| `/students/:student_no` | 学生详情 | 任意用户 | 基本信息、成绩列表、就业信息（Tab 切换） |
| `/teachers` | 教师列表 | 任意用户 | 增删改查 |
| `/classes` | 班级列表 | 任意用户 | 增删改查、查看班级学生 |
| `/scores` | 成绩管理 | 任意用户 | 查询成绩；`admin/teacher` 可录入、修改、删除 |
| `/employment` | 就业管理 v1 | 任意用户 | 查询、新增、更新、删除、按薪资/状态筛选、平均工资统计 |
| `/employment-v2` | 就业管理 v2 | 任意用户 | v2 版本独立页面：条件搜索、软删除、批量恢复 |
| `/statistics` | 统计分析 | 任意用户 | 年龄筛选、班级性别统计、成绩分析、高薪排名、就业时长等 |
| `*` | 404 页面 | 公开 | 未匹配路由 |

### 路由守卫逻辑
- 所有非 `/login` 路由需校验 `authStore` 中是否存在用户信息
- 若未登录，重定向至 `/login`
- 页面级按钮权限（如"删除"按钮）根据 `X-Roles` 中的角色进行条件渲染

---

## 五、状态管理设计（Zustand）

### 5.1 `authStore` — 用户认证状态

```typescript
interface AuthState {
  user: { username: string; roles: string[] } | null;
  isLoggedIn: boolean;
  login: (username: string, roles: string[]) => void;
  logout: () => void;
  hasRole: (role: string) => boolean;
}
```

- **持久化**：使用 `zustand/middleware` 的 `persist` 将用户信息存入 `localStorage`
- **初始化**：应用启动时从 `localStorage` 恢复登录态

### 5.2 `appStore` — 全局 UI 状态

```typescript
interface AppState {
  sidebarCollapsed: boolean;
  theme: 'light' | 'dark';
  toggleSidebar: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
}
```

---

## 六、API 请求封装设计

### 6.1 Axios 实例 (`api/client.ts`)

```typescript
import axios from 'axios';
import { useAuthStore } from '@/stores/authStore';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
});

// 请求拦截器：注入认证 Header
apiClient.interceptors.request.use((config) => {
  const { user } = useAuthStore.getState();
  if (user) {
    config.headers['X-User'] = user.username;
    config.headers['X-Roles'] = user.roles.join(',');
  }
  return config;
});

// 响应拦截器：统一错误处理、格式兼容
apiClient.interceptors.response.use(
  (response) => {
    // 兼容两种响应格式：{ message, data } 或直接返回数据
    const data = response.data;
    if (data && typeof data === 'object' && 'data' in data) {
      response.data = data.data;
    }
    return response;
  },
  (error) => {
    const msg = error.response?.data?.detail || error.message || '请求失败';
    // 可接入全局 Toast 通知
    console.error('[API Error]', msg);
    return Promise.reject(error);
  }
);
```

### 6.2 TanStack Query 封装策略

- 每个模块对应一个 `queryOptions` / `mutation` 工厂函数
- 查询 Key 按模块分级：`['students', 'list']`, `['students', 'detail', student_no]`
- 乐观更新：列表页修改后自动触发 `queryClient.invalidateQueries`

---

## 七、页面布局设计

### 7.1 整体布局（`Layout` 组件）

```
+------------------------------------------+
|  Header (顶部栏：面包屑 + 用户信息 + 主题切换)  |
+------------------------------------------+
|  Sidebar   |                             |
|  (侧边导航) |      Main Content           |
|            |      (路由页面内容)           |
|            |                             |
+------------+-----------------------------+
```

- **Sidebar**：左侧固定，宽度 `240px`（可折叠为 `64px`），包含导航菜单
- **Header**：固定顶部，高度 `64px`，显示当前页面标题、用户角色标签、退出登录按钮
- **Main Content**：自适应剩余区域，内部滚动

### 7.2 导航菜单结构

| 菜单项 | 图标 | 路径 | 权限 |
|--------|------|------|------|
| 仪表盘 | LayoutDashboard | `/` | 任意 |
| 学生管理 | Users | `/students` | 任意 |
| 教师管理 | GraduationCap | `/teachers` | 任意 |
| 班级管理 | School | `/classes` | 任意 |
| 成绩管理 | FileText | `/scores` | 任意 |
| 就业管理 v1 | Briefcase | `/employment` | 任意 |
| 就业管理 v2 | BriefcaseBusiness | `/employment-v2` | 任意 |
| 统计分析 | BarChart3 | `/statistics` | 任意 |

---

## 八、权限控制设计

### 8.1 前端权限层级

1. **路由级**：所有业务路由需登录（除 `/login`）
2. **菜单级**：所有菜单均可见（后端接口已做权限拦截，前端可全部展示）
3. **按钮级**：根据 `roles` 控制操作按钮显隐

### 8.2 权限工具函数

```typescript
// lib/permissions.ts
export const Permissions = {
  canEditScore: (roles: string[]) => roles.includes('admin') || roles.includes('teacher'),
  canDeleteScore: (roles: string[]) => roles.includes('admin'),
  canEditEmployment: (roles: string[]) => roles.includes('admin') || roles.includes('teacher'),
  canDeleteEmployment: (roles: string[]) => roles.includes('admin'),
  canManageStudent: (roles: string[]) => roles.includes('admin'),
} as const;
```

### 8.3 按钮权限映射

| 操作 | 所需角色 | 应用场景 |
|------|----------|----------|
| 录入成绩 | `admin` / `teacher` | 成绩管理页 |
| 修改成绩 | `admin` / `teacher` | 成绩管理页 |
| 删除成绩 | `admin` | 成绩管理页 |
| 新增就业信息 | `admin` / `teacher` | 就业管理页 |
| 更新就业信息 | `admin` / `teacher` | 就业管理页 |
| 删除就业信息 | `admin` | 就业管理页 |
| 学生批量删除/恢复 | `admin` | 学生管理页 |

---

## 九、关键交互设计

### 9.1 登录页（开发阶段简化版）

- **交互流程**：
  1. 用户输入用户名（如 `admin`）
  2. 选择角色（多选：`admin`、`teacher`）
  3. 点击登录 → 写入 `authStore` → 跳转 `/`
- **说明**：当前后端为 Header 简化认证，无真实登录接口，前端模拟登录态

### 9.2 学生管理页

- **列表展示**：表格展示 `student_no`, `name`, `gender`, `class_no`, `phone`, `age`
- **搜索**：顶部搜索框，输入姓名调用 `GET /students/search?name=xxx`
- **筛选**：班级下拉框，选择后调用 `GET /students/class/{class_no}`
- **新增**：弹窗表单，提交 `POST /students/add`
- **编辑**：行内编辑或弹窗，提交 `PUT /students/{student_no}`
- **批量软删除**：表格多选 → 点击删除 → 确认弹窗 → 调用 `DELETE /students/batch`
- **批量恢复**：类似删除，调用 `DELETE /students/back`
- **详情入口**：点击行 → 跳转 `/students/:student_no`

### 9.3 学生详情页

- **Tab 切换**：基本信息 | 成绩记录 | 就业信息
- **基本信息**：展示学生全部字段，支持编辑
- **成绩记录**：调用 `GET /scores/{student_no}`，表格展示，支持新增/编辑/删除（权限控制）
- **就业信息**：调用 `GET /employment/students/{student_no}` 或 v2 接口，展示就业详情

### 9.4 班级管理页

- **列表**：展示 `class_no`, `class_name`, `class_open_time`, `head_teacher_no`, `instructor_no`
- **详情弹窗/抽屉**：点击班级 → 调用 `GET /classes/{class_no}`，展示教师详情
- **查看班级学生**：点击操作按钮 → 跳转 `/students` 并带上 `class_no` 筛选参数

### 9.5 成绩管理页

- **查询方式**：
  - 按学生查询：输入 `student_no` → `GET /scores/{student_no}`
- **录入成绩**：弹窗表单（字段：`student_no`, `exam_no`, `exam_name`, `score`, `exam_date`, `remark`）→ `POST /scores/`
- **修改成绩**：弹窗预填充 → `PUT /scores/update`
- **删除成绩**：确认弹窗 → `POST /scores/delete`（body: `student_no`, `exam_no`, `exam_name`）
- **权限提示**：无权限用户隐藏操作按钮，或点击后提示"无权限"

### 9.6 就业管理 v1 页

- **功能入口**：
  - 查询学生就业：`GET /employment/students/{student_no}`
  - 查询班级就业：`GET /employment/class/{class_no}`
  - 按薪资筛选：`GET /employment/salary?min_salary=xxx`
  - 按状态筛选：`GET /employment/status/{status}`（1=正常，0=已删除）
  - 平均工资统计：`GET /employment/avg-salary?group_by=class/gender`
- **新增/更新**：弹窗表单 → `POST /employment/students/{student_no}` / `PUT /employment/students/{student_no}`
- **删除**：确认弹窗 → `DELETE /employment/students/{student_no}`

### 9.7 就业管理 v2 页

- **独立页面**：与 v1 分开，展示 v2 接口功能
- **条件搜索**：表单输入条件 → `POST /v2/employment/search`（body: `EmploymentQuery`）
- **添加就业**：`POST /v2/employment`
- **更新就业**：`PUT /v2/employment/{student_no}`
- **软删除**：多选 → `DELETE /v2/employment`（body: `student_nos` 数组）
- **批量恢复**：`PUT /v2/employment/restore`（body: `student_nos` 数组）
- **查询**：`GET /v2/employment/{student_no}` / `GET /v2/employment/class/{class_no}`

### 9.8 统计分析页

- **图表 + 表格** 混合展示
- **统计项**：
  - 年龄筛选：`GET /api/statistics/age-filter?age=30` → 表格展示超龄学生
  - 班级性别统计：`GET /api/statistics/class-gender` → 柱状图/饼图
  - 每次考试高于指定分：`GET /api/statistics/always-above?score=80`
  - 两次及以上不及格：`GET /api/statistics/failed-twice`
  - 班级平均分：`GET /api/statistics/class-avg-score` → 柱状图
  - 高薪学生 TOP：`GET /api/statistics/top-salary` → 表格
  - 个人就业时长：`GET /api/statistics/student-offer-duration`
  - 班级平均就业时长：`GET /api/statistics/class-offer-duration`

---

## 十、前后端交互逻辑详表

### 10.1 学生管理模块

| 前端操作 | 请求方法 | 后端接口 | 请求参数 | 响应处理 |
|----------|----------|----------|----------|----------|
| 获取学生列表 | GET | `/students/all` | - | 提取 `data` 渲染表格 |
| 模糊搜索 | GET | `/students/search` | `name` (query) | 提取 `data` 更新表格 |
| 获取学生详情 | GET | `/students/{student_no}` | - | 提取 `student` 展示详情 |
| 创建学生 | POST | `/students/add` | `StudentCreate` (body) | 直接返回学生信息，刷新列表 |
| 更新学生 | PUT | `/students/{student_no}` | `StudentUpdate` (body) | 提取 `student`，刷新详情/列表 |
| 批量软删除 | DELETE | `/students/batch` | `no_list: string[]` (body) | 提示 `message`，刷新列表 |
| 批量恢复 | DELETE | `/students/back` | `no_list: string[]` (body) | 提示 `message`，刷新列表 |
| 按班级查询 | GET | `/students/class/{class_no}` | - | 提取 `data` 更新表格 |

### 10.2 班级管理模块

| 前端操作 | 请求方法 | 后端接口 | 请求参数 | 响应处理 |
|----------|----------|----------|----------|----------|
| 获取班级列表 | GET | `/classes` | - | 直接返回 `ClassRead[]` |
| 创建班级 | POST | `/classes` | `ClassCreate` (body) | 返回 `ClassRead`，刷新列表 |
| 获取班级详情 | GET | `/classes/{class_no}` | - | 返回 `ClassReadDetail`，含教师信息 |
| 更新班级 | PUT | `/classes/{class_no}` | `ClassUpdate` (body) | 返回 `ClassRead`，刷新列表 |
| 删除班级 | DELETE | `/classes/{class_no}` | - | 返回 `ClassRead`，从列表移除 |

### 10.3 教师管理模块

| 前端操作 | 请求方法 | 后端接口 | 请求参数 | 响应处理 |
|----------|----------|----------|----------|----------|
| 获取教师列表 | GET | `/teachers` | - | 直接返回 `TeacherRead[]` |
| 创建教师 | POST | `/teachers` | `TeacherCreate` (body) | 返回 `TeacherRead`，刷新列表 |
| 获取教师详情 | GET | `/teachers/{teacher_no}` | - | 返回 `TeacherRead` |
| 更新教师 | PUT | `/teachers/{teacher_no}` | `TeacherUpdate` (body) | 返回 `TeacherRead`，刷新列表 |
| 删除教师 | DELETE | `/teachers/{teacher_no}` | - | 返回 `TeacherRead`，从列表移除 |

### 10.4 成绩管理模块

| 前端操作 | 请求方法 | 后端接口 | 请求参数 | 响应处理 | 权限 |
|----------|----------|----------|----------|----------|------|
| 查询学生成绩 | GET | `/scores/{student_no}` | - | 返回 `ScoreRead[]` | 任意 |
| 录入成绩 | POST | `/scores/` | `ScoreCreate` (body) | 返回 `ScoreRead`，追加到列表 | admin/teacher |
| 修改成绩 | PUT | `/scores/update` | `ScoreUpdate` (body) | 返回 `ScoreRead`，更新列表 | admin/teacher |
| 删除成绩 | POST | `/scores/delete` | `ScoreDelete` (body) | 204 No Content，移除列表项 | admin |

### 10.5 就业管理 v1 模块

| 前端操作 | 请求方法 | 后端接口 | 请求参数 | 响应处理 | 权限 |
|----------|----------|----------|----------|----------|------|
| 查询学生就业 | GET | `/employment/students/{student_no}` | - | 返回 `EmploymentRead` | 任意 |
| 查询班级就业 | GET | `/employment/class/{class_no}` | - | 返回 `EmploymentRead[]` | 任意 |
| 新增就业信息 | POST | `/employment/students/{student_no}` | `EmploymentCreate` (body) | 返回 `EmploymentRead` | admin/teacher |
| 更新就业信息 | PUT | `/employment/students/{student_no}` | `EmploymentUpdate` (body) | 返回 `EmploymentRead` | admin/teacher |
| 删除就业信息 | DELETE | `/employment/students/{student_no}` | - | 204 No Content | admin |
| 按最低薪资查询 | GET | `/employment/salary` | `min_salary` (query) | 返回 `EmploymentRead[]` | 任意 |
| 平均工资统计 | GET | `/employment/avg-salary` | `group_by` (query, class/gender) | 返回 `AvgSalaryByGroup[]` | 任意 |
| 按状态查询 | GET | `/employment/status/{status}` | `status` (path, 1/0) | 返回 `EmploymentRead[]` | 任意 |

### 10.6 就业管理 v2 模块

| 前端操作 | 请求方法 | 后端接口 | 请求参数 | 响应处理 | 权限 |
|----------|----------|----------|----------|----------|------|
| 添加就业信息 | POST | `/v2/employment` | `EmploymentCreate` (body) | 提取 `data`，提示 `message` | admin/teacher |
| 更新就业信息 | PUT | `/v2/employment/{student_no}` | `EmploymentUpdate` (body) | 提取 `data`，提示 `message` | admin/teacher |
| 获取学生就业 | GET | `/v2/employment/{student_no}` | - | 提取 `data` | 任意 |
| 获取班级就业 | GET | `/v2/employment/class/{class_no}` | - | 直接返回结果 | 任意 |
| 软删除 | DELETE | `/v2/employment` | `student_nos: string[]` (body) | 直接返回结果 | admin |
| 批量恢复 | PUT | `/v2/employment/restore` | `student_nos: string[]` (body) | 直接返回结果 | admin |
| 条件搜索 | POST | `/v2/employment/search` | `EmploymentQuery` (body) | 返回 `EmploymentSearchResponse[]` | 任意 |

### 10.7 统计分析模块

| 前端操作 | 请求方法 | 后端接口 | 请求参数 | 响应处理 |
|----------|----------|----------|----------|----------|
| 年龄筛选 | GET | `/api/statistics/age-filter` | `age` (query, default 30) | 表格展示 |
| 班级性别统计 | GET | `/api/statistics/class-gender` | - | 图表 + 表格 |
| 每次考试高于指定分 | GET | `/api/statistics/always-above` | `score` (query, default 80) | 表格展示 |
| 两次及以上不及格 | GET | `/api/statistics/failed-twice` | - | 表格展示 |
| 班级平均分 | GET | `/api/statistics/class-avg-score` | - | 柱状图 + 表格 |
| 高薪学生 TOP | GET | `/api/statistics/top-salary` | - | 表格展示 |
| 个人就业时长 | GET | `/api/statistics/student-offer-duration` | - | 表格展示 |
| 班级平均就业时长 | GET | `/api/statistics/class-offer-duration` | - | 表格展示 |

---

## 十一、数据类型定义（前端 TypeScript）

```typescript
// types/index.ts

export interface Student {
  student_no: string;
  class_no: string;
  name: string;
  birth_place?: string;
  graduate_school?: string;
  major?: string;
  entrance_time: string; // ISO date
  graduate_time?: string;
  education?: string;
  advisor_name?: string;
  age?: number;
  gender: '男' | '女';
  phone?: string;
  id_card?: string;
}

export interface Teacher {
  teacher_no: string;
  name: string;
  gender: '男' | '女';
  phone?: string;
  email?: string;
  id_card?: string;
  birthday?: string;
  hire_date?: string;
  subject?: string;
}

export interface ClassInfo {
  class_no: string;
  class_name: string;
  class_open_time: string;
  head_teacher_no?: string;
  instructor_no?: string;
  description?: string;
  headteacher?: Teacher;
  instructor?: Teacher;
}

export interface Score {
  student_no: string;
  exam_no: number;
  exam_name: string;
  score: number;
  exam_date?: string;
  remark?: string;
}

export interface Employment {
  student_no: string;
  employment_status: string;
  employment_open_time?: string;
  offer_time?: string;
  company_name?: string;
  salary?: number;
  position?: string;
  work_location?: string;
}

export interface EmploymentSearchResult {
  student_no: string;
  student_name: string;
  class_no: string;
  company_name: string;
  salary: number;
  employment_open_time?: string;
  offer_time?: string;
  position?: string;
  work_location?: string;
  employment_status: string;
}
```

---

## 十二、异常与边界处理

| 场景 | 前端处理策略 |
|------|--------------|
| 后端返回 400 | 提取 `detail` 字段，表单下方或 Toast 提示具体错误 |
| 后端返回 403 | Toast 提示"当前用户没有访问该接口的权限"，按钮置灰 |
| 后端返回 404 | 页面级展示 Empty State 或"数据不存在" |
| 网络超时 | Toast 提示"请求超时，请稍后重试"，提供重试按钮 |
| 响应格式不一致 | Axios 拦截器统一转换，前端始终按标准格式消费 |
| 批量操作部分失败 | 后端目前未返回具体失败项，前端统一提示"操作完成"，后续可优化 |

---

## 十三、开发计划建议

| 阶段 | 任务 | 预计时间 |
|------|------|----------|
| **Phase 1** | 项目初始化：安装依赖（React Router、TanStack Query、Zustand、shadcn/ui、Tailwind、Axios、Recharts） | 0.5 天 |
| **Phase 2** | 基础搭建：路由配置、Layout 布局、登录页、authStore、apiClient | 1 天 |
| **Phase 3** | 学生管理 + 班级管理 + 教师管理（列表、搜索、增删改查） | 2 天 |
| **Phase 4** | 成绩管理 + 就业管理 v1/v2（含权限控制） | 2 天 |
| **Phase 5** | 统计分析页（图表 + 表格） | 1 天 |
| **Phase 6** | 联调测试、响应格式兼容处理、边界 case 处理 | 1 天 |

---

## 十四、与后端的协作注意事项

1. **CORS 配置**：前端开发服务器默认端口 `5173`，已在后端 CORS 配置中，无需修改。
2. **认证 Header**：每个请求必须携带 `X-User` 和 `X-Roles`，由 Axios 拦截器自动注入。
3. **响应格式不一致**：
   - 学生模块：`{ message, data }` 或 `{ message, student }`
   - 班级/教师模块：直接返回模型
   - 就业 v2：`{ code, message, data }`
   - **前端统一在 Axios 拦截器中做兼容转换**。
4. **软删除机制**：学生、成绩、就业均有 `isdeleted` 逻辑删除标记，但前端列表接口通常返回未删除数据，无需额外过滤。
5. **就业管理双版本**：`/employment`（v1）和 `/v2/employment`（v2）为独立接口，前端分别实现独立页面，互不干扰。
6. **成绩删除接口**：使用 `POST /scores/delete` 而非 `DELETE`，注意请求方法。
7. **日期格式**：前后端统一使用 ISO 8601 字符串（如 `2024-01-01` / `2024-01-01T10:00:00`）。
