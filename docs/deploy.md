# 部署指南 · Deployment Guide

## 前置条件

| 组件 | 说明 |
|------|------|
| Nanobot | 已部署在云服务器（本项目基于 Nanobot skill 机制） |
| DeepSeek API Key | 用于 AI 路由和内容生成 |
| Tavily API Key | 用于联网搜索 |
| QQ 邮箱 | SMTP 发送（需开启授权码） |
| 微信通道 | Nanobot 微信 adapter（可选，作为保底通道） |

## 快速部署

### 1. 克隆仓库

```bash
git clone https://github.com/your-username/morning-news-briefing.git
cd morning-news-briefing
```

### 2. 配置邮箱

创建 `_email_config.json`：

```json
{
    "smtp_host": "smtp.qq.com",
    "smtp_port": 465,
    "sender": "your_email@qq.com",
    "password": "your_smtp_auth_code",
    "receiver": "receiver@qq.com"
}
```

### 3. 安装 Nanobot Skill

将 `skill.md` 放入 Nanobot 的 `skills/morning-news-briefing/` 目录。

### 4. 配置 Cron

在 Nanobot 中创建 cron 任务：

```
cron add "7:30 daily" "generate morning news briefing" --cron-expr "30 7 * * *"
```

### 5. 初始化日记

创建你的日记文件（路径在 skill 中配置），写入初始状态。系统的核心能力是从日记中动态提取你的关注点。

## 工作原理

1. **7:30 触发** → cron 启动 skill
2. **读取日记** → 从前一日日记提取关键词和当前状态
3. **动态选题** → 根据日记内容决定今天搜什么（不是固定赛道）
4. **搜索 + 筛选** → Tavily API 搜索，按"本地+即时 × 用户方向挂钩 × 行动入口"过滤
5. **格式化** → 固定 Markdown 模板写入 `/tmp/morning_news.md`
6. **双通道发送** → SMTP 邮件 + 微信保底
7. **清理** → 删除临时文件

## 成本估算

| 项目 | 月费用（¥） |
|------|------------|
| DeepSeek API tokens | ~15 |
| Tavily API | ~5 |
| QQ 邮箱 SMTP | 0 |
| 腾讯云 4GB 服务器 | ~70 |
| **合计** | **~90/月** |

---

→ 返回 [README](../README.md)
