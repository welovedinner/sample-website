# 聚餐小助手 - 开发文档

## 项目概述

聚餐小助手是一个轻量级的聚餐活动管理工具，帮助群友协调聚餐时间、地点和参与人员。

**线上地址**: https://g6c6bfmqq1dh.space.minimax.io

## 已完成功能

### 1. 活动展示
- 按创建时间倒序显示所有聚餐活动
- 展示活动标题、日期、时间、地点、发起人
- 显示备注信息和已加入成员列表

### 2. 发起聚餐
- 点击「+ 发起聚餐」按钮弹出表单
- 必填：活动名称、发起人
- 选填：日期、时间、地点、备注
- 发起人自动加入参与者列表

### 3. 加入聚餐
- 点击活动卡片上的「我要加入」
- 输入称呼后即可加入
- 防止重复加入（同名检测）

## 技术架构

### 前端
- 纯 HTML + CSS + JavaScript（无框架依赖）
- 响应式设计，适配移动端
- 渐变色 UI 风格

### 后端
- **Supabase** (PostgreSQL + REST API)
- 项目 URL: `https://xciikonoumkqweemukec.supabase.co`
- 使用原生 fetch 调用 REST API（避免 SDK 被浏览器拦截）

### 数据库结构

```sql
CREATE TABLE events (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  title TEXT NOT NULL,           -- 活动名称
  date TEXT,                     -- 日期（如：2/24）
  time TEXT,                     -- 时间（如：晚上7点）
  location TEXT,                 -- 地点
  organizer TEXT,                -- 发起人
  note TEXT,                     -- 备注
  participants TEXT[] DEFAULT '{}',  -- 参与者列表
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### RLS 策略
- 允许公开读取（SELECT）
- 允许公开插入（INSERT）
- 允许公开更新（UPDATE）

## 计划用法

### 场景 1：群友发起聚餐
1. 有人在群里提议聚餐
2. 发起人打开网站，点击「发起聚餐」
3. 填写活动信息并发布
4. 分享网站链接到群里

### 场景 2：群友加入聚餐
1. 点击群里分享的链接
2. 查看活动详情
3. 点击「我要加入」，输入称呼

### 场景 3：AI 辅助录入（进阶）
1. 用户将群聊天记录复制给 AI
2. AI 总结出聚餐信息
3. 确认后 AI 通过 API 创建活动

## 待开发功能

根据 PRD 规划，以下功能暂不开发：

- [ ] 用户登录/注册
- [ ] 复杂的权限管理
- [ ] 活动删除/编辑（需权限）
- [ ] 评论/聊天功能
- [ ] 通知推送

## 文件结构

```
dinner-planner/
├── index.html      # 主页面（包含所有代码）
├── DEVELOPMENT.md  # 开发文档（本文件）
└── PRD.md          # 产品需求文档（在 GitHub）
```

## 部署方式

使用 MiniMax 平台部署静态网站：
```bash
# 部署命令由平台自动处理
deploy(dist_dir="dinner-planner")
```

---

*Created by MiniMax Agent*
