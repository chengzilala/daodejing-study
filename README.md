# 道德经学习网站（daodejing-study）

> 面向零基础读者的《道德经》学习网站：原文 + 白话 + 逐章导读。
> **当前状态**：v1.0.0 已完成——八十一章全量内容，本地可构建、可预览（见 [usage/Running.md](./usage/Running.md)）。

---

## 这是什么

一个纯静态网站，把《道德经》八十一章整理成「读得进去、看得懂」的形式：

- **原文**：据通行本（王弼本）
- **白话**：每章一句句讲成大白话
- **导读**：每章要点与背景解读（均标注「编者解读」，非定论）

内容用 Markdown 维护，Python 脚本构建成静态 HTML，零外部依赖，可直接部署（如 Vercel）。

## 能做什么

- 首页 81 章卡片，支持「道篇（1–37）/ 德篇（38–81）」分组切换
- 每章「原文 / 白话 / 导读」分块阅读，上下章导航
- 古卷黄 + 墨色双主题切换（古绢质感，纯 CSS 生成纹理，无图片请求）

## 怎么跑起来

```bash
# 1. 构建：把 web/content/ 的 Markdown 编译成 web/dist/ 静态站点
python3 web/build.py

# 2. 本地预览
python3 web/serve.py
# 浏览器打开 http://localhost:5173
```

详细步骤见 [usage/Running.md](./usage/Running.md)。

## 目录结构

```
daodejing-study/
├── .trae/                # AI 协作配置（规则 + 技能，项目级；不入库）
├── web/                  # 🖥 网站本体
│   ├── content/          #   内容源：81 章 Markdown（part-01 ~ part-09）
│   ├── templates/        #   页面骨架（首页 / 章节页）
│   ├── assets/           #   样式 / 脚本 / 图片
│   ├── dist/             #   构建产物（不入库）
│   ├── build.py          #   构建脚本
│   ├── serve.py          #   本地预览服务
│   └── site.config.json  #   站点配置
├── plan/                 # 📋 RPD 需求文档
├── dev/                  # 🔧 可复制项目指南 / 会话记录
├── test/                 # 🧪 验收测试清单
├── usage/                # 📖 Running.md（安装启动全流程）
└── screenshots/          # 截图素材
```

## 相关文档

- 需求：[plan/RPD_需求文档.md](./plan/RPD_需求文档.md)
- 运行：[usage/Running.md](./usage/Running.md)
- 工作法：[dev/可复制项目指南.md](./dev/可复制项目指南.md)
- 会话记录：[dev/session_log.md](./dev/session_log.md)
