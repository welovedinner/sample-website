# 聚餐小助手 · MVP 实施事项列表

> 目标：  
> 用最小实现跑通 **B 组（想法池）展示 + 创建 + 补充**，  
> 并为 A 组（聚餐事件）和未来扩展留好结构。

---

## Phase 0 · 项目初始化

- [x] 创建 GitHub 仓库
- [ ] 初始化前端项目（React / Next / Vite 均可）
- [x] 创建 Supabase 项目
- [x] 获取 anon public key + project url
- [x] 在前端配置 Supabase client

---

## Phase 1 · 数据模型（Supabase）

### 1. places（B 组核心）

- [x] 创建表 `places`
  - [x] id (uuid, pk)
  - [x] title (text, not null)
  - [x] description (text, nullable)
  - [x] created_at (timestamptz, default now())
  - [x] created_by (text)
  - [x] status (text, default 'active')

---

### 2. place_comments（B 组补充）

- [x] 创建表 `place_comments`
  - [x] id (uuid, pk)
  - [x] place_id (uuid, fk → places.id)
  - [x] content (text)
  - [x] created_at (timestamptz, default now())
  - [x] created_by (text)
  - [x] image_urls (text[])

---

### 3. events（A 组，占位即可）

- [x] 创建表 `events`
  - [x] id (uuid, pk)
  - [x] title (text)
  - [x] place_id (uuid, nullable)
  - [x] time_start (timestamptz)
  - [x] time_end (timestamptz, nullable)
  - [x] location_text (text)
  - [x] created_at (timestamptz, default now())
  - [x] created_by (text)
  - [x] status (text, default 'open')

> ⚠️ 本阶段不需要 UI，仅建表

---

### 4. event_participants（A 组，占位）

- [x] 创建表 `event_participants`
  - [x] id (uuid, pk)
  - [x] event_id (uuid, fk → events.id)
  - [x] display_name (text)
  - [x] intent (text)
  - [x] created_at (timestamptz, default now())

---

## Phase 2 · Storage（图片）

- [ ] 创建 Supabase Storage bucket：`images`
- [ ] 设置为 public read
- [ ] 允许 anon key 上传
- [ ] 确认可以返回 public URL

---

## Phase 3 · 伪用户机制（不鉴权）

- [ ] 页面首次访问要求输入昵称
- [ ] 昵称存入 localStorage
- [ ] 所有写操作都附带 display_name
- [ ] 不做登录 / 注册 / 校验

---

## Phase 4 · B 组前端功能（核心）

### 1. B 组列表页

- [ ] 拉取 `places` 列表（按 created_at desc）
- [ ] 展示：
  - [ ] title
  - [ ] description
  - [ ] 创建人
  - [ ] 评论数
- [ ] 点击进入详情页

---

### 2. 新建 B 组记录（低负担）

- [ ] 「+ 新建想法 / 店」
- [ ] 表单只包含：
  - [ ] title（必填）
  - [ ] description（可选，一句话）
- [ ] 提交后进入详情页

---

### 3. B 组详情页

- [ ] 展示 place 基本信息
- [ ] 拉取并展示 `place_comments`
- [ ] 评论按 created_at asc
- [ ] 每条评论展示：
  - [ ] content
  - [ ] created_by
  - [ ] created_at
  - [ ] 图片（如有）

---

### 4. 评论 + 图片上传

- [ ] 输入评论文本
- [ ] 可选上传 0~N 张图片
- [ ] 图片上传到 Supabase Storage
- [ ] 拿到 public URL
- [ ] 写入 `place_comments.image_urls`

---

## Phase 5 · 首页结构（信息看板）

- [ ] 首页分为两块：
  - [ ] A 组：聚餐事件（占位）
  - [ ] B 组：想法池（真实数据）
- [ ] 明确区分「发生中的事」vs「可以引用的想法」

---

## Phase 6 · A 组最小闭环（可选）

> 若时间允许再做

- [ ] 新建 Event：
  - [ ] title
  - [ ] time_start（必填）
  - [ ] 可选引用 place
- [ ] 展示 Event 列表
- [ ] 简单参与按钮：
  - [ ] join / interested

---

## 非目标（刻意不做）

- [x] 不做用户鉴权
- [x] 不做权限管理
- [x] 不做通知 / 提醒
- [x] 不做复杂时间投票
- [x] 不做餐厅推荐 / 地图
- [x] 不做编辑历史 / 回滚

---

## 完成标准（Definition of Done）

- [ ] 新人打开链接 30 秒内能看懂在干嘛
- [ ] 1 分钟内能创建一个 B 组想法
- [ ] 不翻群聊也能知道「最近有哪些可能的聚餐」
- [ ] 没人需要"负责组织"，但事情能自然发生
