# 项目研究报告模型

先创建 JSON 真源，再由 `scripts/render_report.py` 同时生成 Markdown 和 HTML。

## 必需结构

```json
{
  "project": {
    "name": "project-name",
    "upstream_url": "https://github.com/owner/repo",
    "upstream_commit": "40-character SHA",
    "license": "MIT",
    "study_date": "YYYY-MM-DD"
  },
  "verdict": {
    "what": "一句话能力",
    "purpose": "解决的问题",
    "mechanism": "一句话原理",
    "fit": "采用/改造/参考/放弃及原因"
  },
  "capabilities": [
    {
      "name": "能力名",
      "status": "verified",
      "description": "能力边界",
      "evidence": ["证据说明"],
      "source_ids": ["src_1"]
    }
  ],
  "mechanism": [
    {"stage": "触发与输入", "description": "...", "source_ids": ["src_1"]}
  ],
  "verification": {
    "environment": "...",
    "commands": ["..."],
    "passed": 0,
    "failed": 0,
    "notes": ["..."]
  },
  "limitations": ["..."],
  "extensions": [
    {"name": "...", "description": "...", "acceptance": "..."}
  ],
  "sources": [
    {"id": "src_1", "title": "...", "url": "https://...", "level": "A"}
  ]
}
```

## 校验规则

- `capabilities.status` 只允许 `verified`、`declared`、`external`、`gap`。
- 所有 `source_ids` 必须存在于 `sources`。
- `upstream_commit` 必须是 40 位十六进制 SHA。
- `verification.passed` 和 `failed` 必须为非负整数。
- `mechanism` 应覆盖五层原理模型；缺失层也要写明未提供。
- HTML 与 Markdown 不在渲染后手工改写；修改必须回到 JSON。
