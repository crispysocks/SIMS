# SIMS 前端项目设计方案

> **注意**：当前前端是基于 Vite + React 的初始模板，尚未实现任何业务逻辑。以下文档保留后端 API 设计相关内容，前端实现部分待开发。

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

## 二、前端技术选型（待实现）

当前前端使用 Vite + React 初始模板，具体技术栈待定。

---

## 三、前端项目结构（待实现）

当前前端项目结构待开发确定。

---

## 四、路由设计（待实现）

路由设计待前端实现后确定。

---

## 五、状态管理设计（待实现）

状态管理方案待前端实现后确定。

---

## 六、API 请求封装设计（待实现）

API 请求封装方案待前端实现后确定。

---

## 七、页面布局设计（待实现）

页面布局方案待前端实现后确定。

---

## 八、权限控制设计（待实现）

权限控制方案待前端实现后确定。

---

## 九、关键交互设计（待实现）

关键交互设计待前端实现后确定。

---

## 十、开发计划建议（待实现）

开发计划待前端实现后确定。

---

## 十一、与后端的协作注意事项

1. **CORS 配置**：前端开发服务器默认端口 `5173`，已在后端 CORS 配置中
2. **认证 Header**：每个请求必须携带 `X-User` 和 `X-Roles`
3. **响应格式不一致**：部分接口返回 `{message, data}`，部分直接返回模型，前端需要做兼容处理
4. **软删除机制**：学生、班级、教师、成绩、就业均有 `isdeleted` 逻辑删除标记
5. **就业管理双版本**：同时存在 `/employment`（v1）和 `/v2/employment`（v2），两个版本视为独立接口，前端均需要实现对应功能
