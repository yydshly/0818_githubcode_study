# ChatGPT-generated demonstration assets

这些图片由本研究任务直接使用 ChatGPT 内置 ImageGen 生成，用来演示“风格能力如何转化为有内容意义的项目资产”。它们不是上游仓库样图，也不是技术证据。

| 文件 | 图片职责 | 代表内容 | 页面位置 | 推荐复用 |
| --- | --- | --- | --- | --- |
| `project-cover.png` | 项目封面 | 从零散 Prompt 到可复用视觉风格档案 | 展厅首屏、主研究索引 | README 头图、OG 图、项目卡片 |
| `method-explainer.png` | 原理讲解 | 收集内容 → 选择风格 → 组装约束 → 图像模型出图 | 内容资产演示区 | 教程、工作流说明、分享长图 |
| `milestone-story.png` | 研究故事 | 失败样例不是垃圾，而是需要保存的回归证据 | 内容资产演示区 | 里程碑、复盘、团队故事 |

## 六幕连续案例

`project-cover.png` 同时作为角色/画风锚点和第02幕，配合5张新图形成一条完整因果链：

| 幕 | 文件 | 叙事作用 |
| --- | --- | --- |
| 01 | `story-01-problem.png` | 发现同一项目的图片彼此不一致 |
| 02 | `project-cover.png` | 把散乱提示与样图整理成档案 |
| 03 | `story-03-route.png` | 根据内容任务选择视觉风格 |
| 04 | `story-04-assemble.png` | 把内容、风格和规则组装成受控请求 |
| 05 | `story-05-review.png` | 保留失败结果并把缺陷写回规则 |
| 06 | `story-06-publish.png` | 发布一套用途不同但视觉一致的资产 |

完整背景、角色设定、逐幕因果与最终提示词见 [`STORY.md`](STORY.md)。

## 其他风格应用实验

为同一研究主题补充4种传播任务样例：

- `style-08-ink-archive.png`：文化/策略型水墨封面；
- `style-09-pixel-workflow.png`：游戏化研究流程；
- `style-13-paper-system.png`：纸雕编辑主视觉；
- `style-15-vinyl-researcher.png`：研究项目角色IP。

完整背景、适用/不适用场景与生成提示词见 [`MULTI-STYLE.md`](MULTI-STYLE.md)。

生成日期：2026-08-18。

## 生成原则

- 图片本身不承担精确文字，标题和解释由 HTML 提供。
- 每张图片只有一个明确职责，不作为事实证据。
- 保留对应 Prompt，便于复现、调整和审计。
- 页面必须同时提供 alt、用途、对应内容和生成来源。

完整提示词见 [`PROMPTS.md`](PROMPTS.md)。
