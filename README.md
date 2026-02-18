# 聚餐小助手 🍽️

一个帮助朋友群组织聚餐的轻量级 Web 应用。

## 在线访问

🔗 **线上版本**：https://pqvu6zadvjib.space.minimax.io

## 项目背景

源自微信群组织聚餐的真实需求：
- 大家想去的餐厅散落在聊天记录里，难以追溯
- 发起聚餐时不知道谁有空、想去哪
- 需要一个简单的地方收集想法、组织活动

## 已实现功能 (P1 MVP)

### B组 - 想法池
- ✅ 餐厅/地点列表展示
- ✅ 添加新的餐厅想法（名称 + 描述）
- ✅ 查看餐厅详情
- ✅ 评论功能（对餐厅发表看法）
- ✅ 伪用户系统（localStorage 存储昵称）

### 技术实现
- ✅ 纯前端 HTML/CSS/JS，无框架依赖
- ✅ Supabase 后端（PostgreSQL + REST API）
- ✅ 原生 fetch 调用 REST API（避免 SDK 被浏览器拦截）
- ✅ 响应式设计，移动端友好

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | HTML5 + CSS3 + Vanilla JS |
| 后端 | Supabase (PostgreSQL) |
| API | Supabase REST API |
| 部署 | MiniMax Space |

## 数据库结构

```
places          # 餐厅/地点（想法池）
├── id, name, description
├── created_by  # 伪用户昵称
└── created_at

place_comments  # 餐厅评论
├── id, place_id, content
├── created_by
└── created_at

events          # 聚餐事件（待实现）
event_participants  # 参与者（待实现）
```

## 文档索引

| 文档 | 说明 |
|------|------|
| [📋 P1 TODO](docs/TODO.md) | MVP 功能清单（已基本完成） |
| [🚀 P2 TODO](docs/P2TODO.md) | 二期功能：排序、点赞等 |
| [📖 Glossary](docs/glossary.md) | 核心概念：A组/B组、Place、Event |
| [📄 PRD](PRD.md) | 产品需求文档 |

## 未来规划

详见 [P2TODO.md](docs/P2TODO.md)：
- 排序功能（时间、评论数、点赞数）
- 点赞系统
- A组功能（发起聚餐、报名参与）

## 本地开发

```bash
# 直接打开 index.html 即可
open index.html

# 或使用任意 HTTP 服务器
python -m http.server 8080
```

## License

MIT

---

*由 MiniMax Agent 协助开发* 🤖
