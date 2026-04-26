# SIMS 前端项目设计方案

## 附录：完整项目文件树（前后端合并后）

```
SIMS/                                    # 项目根目录
│
├── app/                                 # ====== 后端 FastAPI 主应用 ======
│   ├── api/                             # API 路由层
│   │   ├── __init__.py                  # 路由聚合导出
│   │   ├── classes.py                   # 班级管理接口
│   │   ├── deps.py                      # 依赖注入
│   │   ├── employment.py                # 就业管理 v1 接口
│   │   ├── employment_v2.py             # 就业管理 v2 接口
│   │   ├── scores.py                    # 成绩管理接口
│   │   ├── statistics.py                # 统计分析接口
│   │   ├── students.py                  # 学生管理接口
│   │   └── teachers.py                  # 教师管理接口
│   │
│   ├── core/                            # 核心配置
│   │   ├── __init__.py
│   │   ├── config.py                    # 环境变量配置（Settings）
│   │   └── database.py                  # 数据库引擎、Session、初始化
│   │
│   ├── models/                          # SQLAlchemy 数据模型
│   │   ├── __init__.py
│   │   ├── classes.py                   # 班级模型 ClassInfo
│   │   ├── employment.py                # 就业模型 Employment
│   │   ├── score.py                     # 成绩模型 Score
│   │   ├── student.py                   # 学生模型 Student
│   │   └── teacher.py                   # 教师模型 Teacher
│   │
│   ├── schemas/                         # Pydantic 数据校验模型
│   │   ├── __init__.py
│   │   ├── classes.py                   # 班级 Schema
│   │   ├── employment.py                # 就业 Schema（v1）
│   │   ├── employment_v2.py             # 就业 Schema（v2）
│   │   ├── score.py                     # 成绩 Schema
│   │   ├── student.py                   # 学生 Schema
│   │   └── teacher.py                   # 教师 Schema
│   │
│   ├── services/                        # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── classes.py                   # 班级业务逻辑
│   │   ├── employment.py                # 就业业务逻辑（v1）
│   │   ├── employment_v2.py             # 就业业务逻辑（v2）
│   │   ├── score.py                     # 成绩业务逻辑
│   │   ├── statistics.py                # 统计分析逻辑
│   │   ├── student.py                   # 学生业务逻辑
│   │   └── teacher.py                   # 教师业务逻辑
│   │
│   ├── __init__.py
│   ├── dependencies.py                  # 认证依赖（Header-based）
│   └── main.py                          # FastAPI 入口（注册路由、CORS、启动事件）
│
├── docs/                                # 项目文档
│   ├── FastAPI项目需求.md
│   ├── MODEL_MIGRATION_LOG.md
│   ├── 数据库设计文档.md
│   └── 数据库设计说明文档（通俗版）.md
│
├── frontend/                            # ====== 前端 Vue 3 应用 ======
│   ├── public/                          # 静态资源（不经过构建）
│   │   └── favicon.ico
│   │
│   ├── src/
│   │   ├── api/                         # API 接口封装
│   │   │   ├── request.ts               # Axios 实例（拦截器、错误处理）
│   │   │   ├── student.ts               # 学生管理接口
│   │   │   ├── teacher.ts               # 教师管理接口
│   │   │   ├── classes.ts               # 班级管理接口
│   │   │   ├── score.ts                 # 成绩管理接口
│   │   │   ├── employment.ts            # 就业管理接口
│   │   │   └── statistics.ts            # 统计分析接口
│   │   │
│   │   ├── assets/                      # 静态资源（图片、样式）
│   │   │   └── styles/
│   │   │       └── variables.scss       # SCSS 变量
│   │   │
│   │   ├── components/                  # 公共组件
│   │   │   ├── AppHeader.vue            # 顶部导航栏
│   │   │   ├── AppSidebar.vue           # 侧边菜单栏
│   │   │   ├── AppLayout.vue            # 布局容器
│   │   │   ├── DataTable.vue            # 通用数据表格
│   │   │   ├── SearchForm.vue           # 通用搜索表单
│   │   │   ├── DetailCard.vue           # 详情卡片
│   │   │   └── StatChart.vue            # 统计图表封装
│   │   │
│   │   ├── composables/                 # 组合式函数
│   │   │   ├── useTable.ts              # 表格分页/加载逻辑
│   │   │   ├── useForm.ts               # 表单提交/校验逻辑
│   │   │   └── useAuth.ts               # 权限判断逻辑
│   │   │
│   │   ├── router/                      # 路由配置
│   │   │   └── index.ts                 # 路由定义 + 导航守卫
│   │   │
│   │   ├── stores/                      # Pinia 状态管理
│   │   │   ├── auth.ts                  # 用户认证状态
│   │   │   ├── app.ts                   # 应用状态（侧边栏、主题）
│   │   │   └── tagsView.ts              # 标签页状态（可选）
│   │   │
│   │   ├── types/                       # TypeScript 类型定义
│   │   │   ├── student.ts               # 学生类型
│   │   │   ├── teacher.ts               # 教师类型
│   │   │   ├── classes.ts               # 班级类型
│   │   │   ├── score.ts                 # 成绩类型
│   │   │   ├── employment.ts            # 就业类型
│   │   │   ├── statistics.ts            # 统计类型
│   │   │   └── api.ts                   # 通用 API 响应类型
│   │   │
│   │   ├── utils/                       # 工具函数
│   │   │   ├── format.ts                # 日期/数字格式化
│   │   │   ├── validate.ts              # 表单校验规则
│   │   │   └── constants.ts             # 常量定义（性别、学历枚举等）
│   │   │
│   │   ├── views/                       # 页面视图（按模块组织）
│   │   │   ├── login/
│   │   │   │   └── Index.vue            # 登录页（模拟 Header 设置）
│   │   │   ├── dashboard/
│   │   │   │   └── Index.vue            # 首页仪表盘
│   │   │   ├── student/
│   │   │   │   ├── Index.vue            # 学生列表页
│   │   │   │   ├── Detail.vue           # 学生详情页
│   │   │   │   └── Form.vue             # 学生表单（新增/编辑）
│   │   │   ├── teacher/
│   │   │   │   ├── Index.vue            # 教师列表页
│   │   │   │   └── Form.vue             # 教师表单
│   │   │   ├── classes/
│   │   │   │   ├── Index.vue            # 班级列表页
│   │   │   │   └── Form.vue             # 班级表单
│   │   │   ├── score/
│   │   │   │   ├── Index.vue            # 成绩列表/查询页
│   │   │   │   └── Form.vue             # 成绩录入/编辑页
│   │   │   ├── employment/
│   │   │   │   ├── Index.vue            # 就业信息列表页
│   │   │   │   ├── Detail.vue           # 就业详情页
│   │   │   │   └── Form.vue             # 就业信息表单
│   │   │   └── statistics/
│   │   │       ├── Index.vue            # 统计概览页
│   │   │       ├── AgeFilter.vue        # 年龄筛选统计
│   │   │       ├── ClassGender.vue      # 班级性别统计
│   │   │       ├── ScoreAnalysis.vue    # 成绩分析
│   │   │       ├── EmploymentAnalysis.vue # 就业分析
│   │   │       └── SalaryRank.vue       # 薪资排行
│   │   │
│   │   ├── App.vue                      # 根组件
│   │   └── main.ts                      # 入口文件
│   │
│   ├── .env                             # 前端环境变量（通用，本地开发用）
  ├── .env.development                 # 前端开发环境配置（如 VITE_API_BASE_URL）
  ├── .env.production                  # 前端生产环境配置
│   ├── index.html                       # HTML 模板
│   ├── package.json                     # 依赖管理
│   ├── tsconfig.json                    # TypeScript 配置
│   ├── vite.config.ts                   # Vite 构建配置
│   └── README.md                        # 前端项目说明
│
├── tests/                               # 后端测试
│   ├── __init__.py
│   ├── conftest.py
│   └── test_database.py
│
├── .env                                 # 后端环境变量（本地，gitignore，不提交）
├── .env.example                         # 后端环境变量模板（示例值，提交仓库）
├── .gitignore                           # Git 忽略规则
├── .python-version                      # Python 版本
├── AGENTS.md                            # 项目规范文档
├── frontend-design.md                   # 前端设计方案（本文档）
├── main.py                              # 后端入口（兼容启动）
├── pyproject.toml                       # Python 依赖配置
├── README.md                            # 项目总说明
└── uv.lock                              # uv 依赖锁定文件
```

---

## 一、后端项目分析总结

### 1.1 技术栈
- 后端：FastAPI + SQLAlchemy + MySQL
- 认证：Header-based（`X-User`, `X-Roles`），角色：`admin`、`teacher`
- CORS：默认 `http://localhost:5173`
- 数据格式：JSON，统一返回结构（部分接口有 `message` + `data`，部分直接返回模型）

### 1.2 数据模型（5个核心实体）
| 实体 | 主键 | 核心字段 | 关联关系 |
|------|------|----------|----------|
| Student（学生） | `student_no` | 姓名、班级、性别、年龄、籍贯、毕业院校、专业、入学/毕业时间、学历、顾问、电话、身份证 | 关联 Class |
| Teacher（教师） | `teacher_no` | 姓名、性别、电话、邮箱、身份证、生日、入职日期、授课科目 | 被 Class 关联 |
| ClassInfo（班级） | `class_no` | 班级名称、开课时间、班主任、授课老师、描述 | 关联 Teacher（班主任/授课老师） |
| Score（成绩） | 联合主键 (`student_no`, `exam_no`, `exam_name`) | 成绩、考核日期、备注 | 关联 Student |
| Employment（就业） | `student_no` | 就业状态、就业开放时间、offer时间、公司、薪资、岗位、工作地点、签约日期 | 关联 Student |

### 1.3 API 接口汇总

#### 学生管理 (`/students`)
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/students/all` | 获取所有学生列表 |
| GET | `/students/search?name=xxx` | 按姓名模糊查询 |
| GET | `/students/{student_no}` | 获取单个学生详情 |
| POST | `/students/add` | 创建学生 |
| PUT | `/students/{student_no}` | 更新学生 |
| DELETE | `/students/batch` | 批量软删除 |
| DELETE | `/students/back` | 批量恢复软删除 |
| GET | `/students/class/{class_no}` | 按班级查询学生 |

#### 班级管理 (`/classes`)
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/classes` | 获取班级列表 |
| POST | `/classes` | 创建班级 |
| GET | `/classes/{class_no}` | 获取班级详情（含教师信息） |
| PUT | `/classes/{class_no}` | 更新班级 |
| DELETE | `/classes/{class_no}` | 删除班级 |

#### 教师管理 (`/teachers`)
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/teachers` | 获取教师列表 |
| POST | `/teachers` | 创建教师 |
| GET | `/teachers/{teacher_no}` | 获取教师详情 |
| PUT | `/teachers/{teacher_no}` | 更新教师 |
| DELETE | `/teachers/{teacher_no}` | 删除教师 |

#### 成绩管理 (`/scores`)
| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/scores/{student_no}` | 查询学生成绩 | 任意用户 |
| POST | `/scores/` | 录入成绩 | admin/teacher |
| PUT | `/scores/update` | 修改成绩 | admin/teacher |
| POST | `/scores/delete` | 删除成绩 | admin |

#### 就业管理 v1 (`/employment`)
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/employment/students/{student_no}` | 查询学生就业信息 |
| GET | `/employment/class/{class_no}` | 查询班级就业信息 |
| POST | `/employment/students/{student_no}` | 新增就业信息 |
| PUT | `/employment/students/{student_no}` | 更新就业信息 |
| DELETE | `/employment/students/{student_no}` | 删除就业信息 |
| GET | `/employment/salary?min_salary=xxx` | 按最低薪资查询 |
| GET | `/employment/avg-salary?group_by=xxx` | 平均工资统计（按班级/性别） |
| GET | `/employment/status/{status}` | 按状态查询 |

#### 就业管理 v2 (`/v2/employment`)
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/v2/employment` | 添加就业信息 |
| PUT | `/v2/employment/{student_no}` | 更新就业信息 |
| GET | `/v2/employment/{student_no}` | 获取学生就业信息 |
| GET | `/v2/employment/class/{class_no}` | 获取班级就业信息 |
| DELETE | `/v2/employment` | 软删除（body: student_nos 数组） |
| PUT | `/v2/employment/restore` | 批量恢复 |
| POST | `/v2/employment/search` | 条件搜索 |

#### 统计分析 (`/api/statistics`)
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/statistics/age-filter?age=30` | 超过指定年龄的学生 |
| GET | `/api/statistics/class-gender` | 班级男女人数统计 |
| GET | `/api/statistics/always-above?score=80` | 每次考试都高于指定分 |
| GET | `/api/statistics/failed-twice` | 两次及以上不及格 |
| GET | `/api/statistics/class-avg-score` | 班级平均分 |
| GET | `/api/statistics/top-salary` | 高薪学生 TOP |
| GET | `/api/statistics/student-offer-duration` | 个人就业时长 |
| GET | `/api/statistics/class-offer-duration` | 班级平均就业时长 |

### 1.4 认证机制
- 请求头传递：`X-User`（用户名）、`X-Roles`（角色，逗号分隔）
- 默认角色：`admin`, `teacher`
- 前端需要在请求头中携带这些信息

---

## 二、前端技术选型

| 层级 | 技术方案 | 说明 |
|------|----------|------|
| 框架 | **Vue 3** + **TypeScript** | 主流前端框架，类型安全 |
| 构建工具 | **Vite** | 快速构建，与 Vue 3 生态完美契合 |
| UI 组件库 | **Element Plus** | 适合中后台管理系统，组件丰富 |
| 状态管理 | **Pinia** | Vue 官方推荐，TypeScript 友好 |
| 路由 | **Vue Router 4** | 官方路由方案 |
| HTTP 请求 | **Axios** | 成熟的 HTTP 客户端，支持拦截器 |
| 图表库 | **ECharts** | 统计分析页面需要数据可视化 |
| 代码规范 | **ESLint** + **Prettier** | 统一代码风格 |

---

## 三、前端项目结构

```
frontend/
├── public/                          # 静态资源
│   └── favicon.ico
├── src/
│   ├── api/                         # API 接口封装
│   │   ├── request.ts               # Axios 实例配置（拦截器、错误处理）
│   │   ├── student.ts               # 学生管理接口
│   │   ├── teacher.ts               # 教师管理接口
│   │   ├── classes.ts               # 班级管理接口
│   │   ├── score.ts                 # 成绩管理接口
│   │   ├── employment.ts            # 就业管理接口（v1 + v2）
│   │   └── statistics.ts            # 统计分析接口
│   ├── assets/                      # 静态资源（图片、样式）
│   │   └── styles/
│   │       └── variables.scss       # SCSS 变量
│   ├── components/                  # 公共组件
│   │   ├── AppHeader.vue            # 顶部导航栏
│   │   ├── AppSidebar.vue           # 侧边菜单栏
│   │   ├── AppLayout.vue            # 布局容器（Header + Sidebar + Main）
│   │   ├── DataTable.vue            # 通用数据表格（分页、排序、筛选）
│   │   ├── SearchForm.vue           # 通用搜索表单
│   │   ├── DetailCard.vue           # 详情卡片
│   │   └── StatChart.vue            # 统计图表封装
│   ├── composables/                 # 组合式函数（可复用逻辑）
│   │   ├── useTable.ts              # 表格分页/加载逻辑
│   │   ├── useForm.ts               # 表单提交/校验逻辑
│   │   └── useAuth.ts               # 权限判断逻辑
│   ├── router/                      # 路由配置
│   │   └── index.ts                 # 路由定义 + 导航守卫
│   ├── stores/                      # Pinia 状态管理
│   │   ├── auth.ts                  # 用户认证状态（角色、用户名）
│   │   ├── app.ts                   # 应用状态（侧边栏折叠、主题）
│   │   └── tagsView.ts              # 标签页状态（可选）
│   ├── types/                       # TypeScript 类型定义
│   │   ├── student.ts               # 学生相关类型
│   │   ├── teacher.ts               # 教师相关类型
│   │   ├── classes.ts               # 班级相关类型
│   │   ├── score.ts                 # 成绩相关类型
│   │   ├── employment.ts            # 就业相关类型
│   │   ├── statistics.ts            # 统计相关类型
│   │   └── api.ts                   # 通用 API 响应类型
│   ├── utils/                       # 工具函数
│   │   ├── format.ts                # 日期/数字格式化
│   │   ├── validate.ts              # 表单校验规则
│   │   └── constants.ts             # 常量定义（性别枚举、学历枚举等）
│   ├── views/                       # 页面视图
│   │   ├── login/                   # 登录页（模拟 Header 设置）
│   │   │   └── Index.vue
│   │   ├── dashboard/               # 首页仪表盘
│   │   │   └── Index.vue
│   │   ├── student/                 # 学生管理模块
│   │   │   ├── Index.vue            # 学生列表页
│   │   │   ├── Detail.vue           # 学生详情页
│   │   │   └── Form.vue             # 学生表单（新增/编辑）
│   │   ├── teacher/                 # 教师管理模块
│   │   │   ├── Index.vue
│   │   │   └── Form.vue
│   │   ├── classes/                 # 班级管理模块
│   │   │   ├── Index.vue
│   │   │   └── Form.vue
│   │   ├── score/                   # 成绩管理模块
│   │   │   ├── Index.vue            # 成绩列表/查询
│   │   │   └── Form.vue             # 成绩录入/编辑
│   │   ├── employment/              # 就业管理模块
│   │   │   ├── Index.vue            # 就业信息列表
│   │   │   ├── Detail.vue           # 就业详情
│   │   │   └── Form.vue             # 就业信息录入/编辑
│   │   └── statistics/              # 统计分析模块
│   │       ├── Index.vue            # 统计概览
│   │       ├── AgeFilter.vue        # 年龄筛选统计
│   │       ├── ClassGender.vue      # 班级性别统计
│   │       ├── ScoreAnalysis.vue    # 成绩分析
│   │       ├── EmploymentAnalysis.vue # 就业分析
│   │       └── SalaryRank.vue       # 薪资排行
│   ├── App.vue                      # 根组件
│   └── main.ts                      # 入口文件
├── .env                             # 环境变量（API 基础地址）
├── .env.development
├── .env.production
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

---

## 四、路由设计

| 路径 | 页面 | 说明 |
|------|------|------|
| `/login` | 登录页 | 设置 X-User 和 X-Roles |
| `/` | 仪表盘 | 系统首页，展示关键指标 |
| `/students` | 学生列表 | 学生信息管理主页 |
| `/students/:student_no` | 学生详情 | 单个学生详细信息 |
| `/students/form` | 新增学生 | |
| `/students/form/:student_no` | 编辑学生 | |
| `/teachers` | 教师列表 | |
| `/teachers/form` | 新增教师 | |
| `/teachers/form/:teacher_no` | 编辑教师 | |
| `/classes` | 班级列表 | |
| `/classes/form` | 新增班级 | |
| `/classes/form/:class_no` | 编辑班级 | |
| `/scores` | 成绩管理 | 可按学生查询成绩 |
| `/scores/form` | 录入成绩 | |
| `/employment` | 就业信息列表 | |
| `/employment/:student_no` | 就业详情 | |
| `/employment/form` | 新增就业信息 | |
| `/employment/form/:student_no` | 编辑就业信息 | |
| `/statistics` | 统计概览 | 各统计图表入口 |
| `/statistics/age` | 年龄统计 | |
| `/statistics/gender` | 性别统计 | |
| `/statistics/score` | 成绩统计 | |
| `/statistics/employment` | 就业统计 | |

---

## 五、状态管理设计（Pinia）

### 5.1 Auth Store
```typescript
interface AuthState {
  username: string;
  roles: string[];
  isLoggedIn: boolean;
}
// Actions: login(username, roles), logout()
// Getters: isAdmin, isTeacher, hasRole(role)
```

### 5.2 App Store
```typescript
interface AppState {
  sidebarCollapsed: boolean;
  theme: 'light' | 'dark';
}
```

---

## 六、API 请求封装设计

### 6.1 Axios 实例配置
- BaseURL: 从环境变量读取（开发环境 `http://localhost:8000`）
- 请求拦截器：自动注入 `X-User` 和 `X-Roles` Header
- 响应拦截器：统一处理错误码、消息提示

### 6.2 统一响应类型
```typescript
interface ApiResponse<T> {
  code?: number;
  message: string;
  data: T;
}
```

---

## 七、页面布局设计

### 7.1 整体布局（AppLayout）
```
+------------------+
|     Header       |  ← 系统名称 + 用户信息 + 退出
+------------------+
| Sidebar |  Main  |  ← 左侧菜单 + 右侧内容区
|         |        |
+------------------+
```

### 7.2 列表页通用结构
```
+----------------------------------+
| 面包屑导航                        |
+----------------------------------+
| 搜索表单（姓名/编号等筛选条件）      |
+----------------------------------+
| 操作按钮（新增、批量删除、导出）      |
+----------------------------------+
| 数据表格（分页、排序、操作列）        |
+----------------------------------+
```

### 7.3 表单页通用结构
```
+----------------------------------+
| 面包屑导航                        |
+----------------------------------+
| 表单区域（Element Plus Form）      |
| - 基础信息                        |
| - 扩展信息                        |
| - 提交/取消按钮                   |
+----------------------------------+
```

---

## 八、权限控制设计

### 8.1 前端权限
- 路由守卫：根据角色控制页面访问
- 按钮级权限：通过 `v-if` 或自定义指令控制（如成绩录入仅 admin/teacher 可见）
- 菜单权限：根据角色过滤侧边栏菜单项

### 8.2 权限映射
| 角色 | 可访问模块 |
|------|-----------|
| admin | 全部模块 |
| teacher | 学生、成绩、就业（查看+编辑）、统计（查看） |

---

## 九、关键交互设计

### 9.1 学生管理
- 列表页支持：按姓名搜索、按班级筛选、分页
- 支持批量软删除和恢复
- 详情页展示学生完整信息 + 成绩列表 + 就业信息（Tab 切换）

### 9.2 成绩管理
- 按学生查询成绩（表格展示）
- 录入成绩时选择学生、输入考试名称/序次/成绩
- 支持修改和逻辑删除

### 9.3 就业管理
- 列表展示学生就业状态（待业/在聘/已离职）
- 支持按薪资范围、公司名、状态筛选
- 统计图表展示平均工资、就业时长等

### 9.4 统计分析
- 使用 ECharts 展示各类统计图表
- 支持参数调整（如年龄阈值、分数阈值）实时刷新图表
- 班级性别统计使用柱状图
- 薪资排行使用条形图
- 就业时长使用柱状图

---

## 十、开发计划建议

### Phase 1：项目搭建（1天）
1. 使用 Vite 创建 Vue 3 + TypeScript 项目
2. 安装 Element Plus、Pinia、Vue Router、Axios、ECharts
3. 配置路由、状态管理、Axios 拦截器
4. 搭建 AppLayout（Header + Sidebar + Main）

### Phase 2：基础模块（2天）
1. 实现登录页（Header 设置模拟）
2. 实现学生管理（列表、新增、编辑、删除、搜索）
3. 实现教师管理
4. 实现班级管理

### Phase 3：业务模块（2天）
1. 实现成绩管理（录入、查询、修改）
2. 实现就业管理（CRUD + 搜索）

### Phase 4：统计模块（1天）
1. 集成 ECharts
2. 实现各统计图表页面
3. 实现仪表盘首页

### Phase 5：优化完善（1天）
1. 权限控制细化
2. 表单校验完善
3. 错误处理优化
4. 代码规范检查

---

## 十一、与后端的协作注意事项

1. **CORS 配置**：前端开发服务器默认端口 `5173`，已在后端 CORS 配置中
2. **认证 Header**：每个请求必须携带 `X-User` 和 `X-Roles`
3. **响应格式不一致**：部分接口返回 `{message, data}`，部分直接返回模型，前端需要做兼容处理
4. **软删除机制**：学生、班级、教师、成绩、就业均有 `isdeleted` 逻辑删除标记
5. **就业管理双版本**：同时存在 `/employment`（v1）和 `/v2/employment`（v2），建议统一使用 v2
6. **上传目录**：后端 `./backend/uploads` 目录可能需要手动创建
