# 聚餐小助手 · P2 功能清单

> 排序、点赞/收藏功能

---

## 一、数据模型扩展

### 1. 新建 `place_likes` 表

- [ ] 创建表 `place_likes`
  - [ ] id (uuid, pk)
  - [ ] place_id (uuid, fk → places.id, ON DELETE CASCADE)
  - [ ] user_name (text, not null) — 伪用户昵称
  - [ ] created_at (timestamptz, default now())
  - [ ] UNIQUE 约束 (place_id, user_name) — 防止重复点赞

- [ ] 设置 RLS 策略
  - [ ] 允许公开读取
  - [ ] 允许公开插入
  - [ ] 允许公开删除（取消点赞）

---

## 二、点赞功能

### 1. 后端接口

- [ ] 点赞：INSERT place_likes (place_id, user_name)
- [ ] 取消点赞：DELETE place_likes WHERE place_id = ? AND user_name = ?
- [ ] 查询我是否点赞：SELECT * FROM place_likes WHERE place_id = ? AND user_name = ?
- [ ] 统计点赞数：SELECT COUNT(*) FROM place_likes WHERE place_id = ?

### 2. 前端 UI

- [ ] 想法卡片显示点赞数（❤️ 12）
- [ ] 点赞按钮交互
  - [ ] 未赞：空心 ♡ → 点击后变实心 ❤️
  - [ ] 已赞：实心 ❤️ → 点击后取消变 ♡
- [ ] 详情页显示点赞数和点赞按钮

---

## 三、排序功能

### 1. 支持的排序方式

| 排序方式 | 实现难度 | 说明 |
|---------|---------|------|
| 按时间（最新） | ✅ 简单 | `ORDER BY created_at DESC` |
| 按时间（最早） | ✅ 简单 | `ORDER BY created_at ASC` |
| 按评论数 | ⚠️ 中等 | 需要 LEFT JOIN + COUNT 或子查询 |
| 按点赞数 | ⚠️ 中等 | 需要 LEFT JOIN + COUNT（依赖 place_likes 表） |

### 2. 前端 UI

- [ ] 列表页顶部添加排序选择器
- [ ] 排序选项：
  - [ ] 最新发布（默认）
  - [ ] 最早发布
  - [ ] 最多评论
  - [ ] 最多点赞
- [ ] 切换排序后刷新列表

### 3. 后端实现

```sql
-- 按评论数排序
SELECT p.*, COUNT(c.id) as comment_count
FROM places p
LEFT JOIN place_comments c ON p.id = c.place_id
WHERE p.status = 'active'
GROUP BY p.id
ORDER BY comment_count DESC;

-- 按点赞数排序
SELECT p.*, COUNT(l.id) as like_count
FROM places p
LEFT JOIN place_likes l ON p.id = l.place_id
WHERE p.status = 'active'
GROUP BY p.id
ORDER BY like_count DESC;
```

> ⚠️ 注意：Supabase REST API 对复杂 JOIN 查询支持有限，可能需要创建 View 或 RPC 函数

---

## 四、「我赞过的」筛选

### 1. 功能描述

- 用户可以筛选出自己点赞过的想法
- 相当于简易收藏功能

### 2. 实现方式

- [ ] 前端添加「我赞过的」筛选开关
- [ ] 查询：
  ```sql
  SELECT p.* FROM places p
  INNER JOIN place_likes l ON p.id = l.place_id
  WHERE l.user_name = '当前用户昵称'
  ORDER BY l.created_at DESC;
  ```

---

## 五、优先级建议

| 优先级 | 功能 | 理由 |
|-------|------|------|
| P2.1 | 点赞功能 | 排序和筛选的基础 |
| P2.2 | 按时间排序 | 最简单，立即可做 |
| P2.3 | 按点赞数排序 | 依赖点赞功能 |
| P2.4 | 按评论数排序 | 需要聚合查询 |
| P2.5 | 我赞过的筛选 | 依赖点赞功能 |

---

## 六、建表 SQL（参考）

```sql
-- 创建 place_likes 表
CREATE TABLE IF NOT EXISTS place_likes (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  place_id UUID REFERENCES places(id) ON DELETE CASCADE,
  user_name TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(place_id, user_name)
);

-- RLS 策略
ALTER TABLE place_likes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "允许公开读取 place_likes" ON place_likes FOR SELECT USING (true);
CREATE POLICY "允许公开插入 place_likes" ON place_likes FOR INSERT WITH CHECK (true);
CREATE POLICY "允许公开删除 place_likes" ON place_likes FOR DELETE USING (true);
```
