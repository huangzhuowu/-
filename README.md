# 史料众包档案

本项目用于**众包提交史料**并经审核后**自动展示**（GitHub Pages）。
- 📜 **真实史料区（History）**
- 🎭 **娱乐信息区（Entertainment）**
- 🔮 **玄学信息区（Metaphysics）**

## 提交规范（Markdown + Front-matter）

每个条目是一个 `.md` 文件，文件头采用 YAML 前置信息：

```yaml
---
title: "条目标题"
area: "history|entertainment|metaphysics"   # 可不写，放在哪个文件夹就会自动标注
type: "primary|secondary|commentary|rumor"
date_event: "YYYY-MM-DD"                    # 事件发生时间，用于排序
date_source: "YYYY-MM-DD"                   # （可选）资料出版/录制时间
source_title: "出处题名"
source_author: "作者"
source_publisher: "出版社/版本"
source_url: "https://..."
location: "地点"
language: "zh"
submitter: "你的 GitHub 用户名"
license: "CC BY-SA 4.0"
tags: ["标签1","标签2"]
verification_status: "pending|approved|rejected"
summary: "一句话摘要"
---
（正文：可放摘录、影印链接、你的考据说明等）
```

- 仅当 `verification_status: approved` 时，条目会出现在前台列表。
- 排序依据 `date_event`。

## 目录结构

- `_history/`：真实史料
- `_entertainment/`：娱乐信息
- `_metaphysics/`：玄学信息
- `pages/`：三个专区的入口页面
- `_layouts/`：页面模板
- `schema/`：字段 JSON Schema（供 CI 校验）
- `.github/workflows/validate.yml`：PR 校验工作流

## 本地预览

安装 Ruby 与 Bundler 后：

```bash
bundle install
bundle exec jekyll serve
```

## 许可证

- 代码：MIT
- 内容：CC BY-SA 4.0（提交内容默认同意此许可，除非条目另有声明）
