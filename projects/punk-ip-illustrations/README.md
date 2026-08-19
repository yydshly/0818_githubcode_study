# Punk IP Illustrations 项目研究

> 研究如何把一次人物照片生成，变成可确认、可持久化、可跨文章复用的个人 IP 插图工作流。

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 上游项目 | `adrianpunk/punk-ip-illustrations` |
| 上游地址 | https://github.com/adrianpunk/punk-ip-illustrations |
| 研究版本 | `8bcc522192a9f757cbf2b52cefabc9ffbfb1712c` |
| 研究状态 | 已获取 · 自有 ImageGen 实演已完成 |
| 开始日期 | 2026-08-19 |
| 最后更新 | 2026-08-19 |
| 本地实验 | `projects/punk-ip-illustrations/` |
| 在线演示 | `projects/punk-ip-illustrations/showcase/` |

## 研究目标

- 解释仓库真正提供的能力，以及它与底层图像模型的边界。
- 拆解“个人形象一致使用”如何通过角色包、状态机和参考图合同落地。
- 展示文章配图的两种模式、适用场景和实际限制。
- 用自生成虚构人物跑通一次“原始图—角色确认—文章场景”链路，并与上游样张对照。
- 说明用户如何把一句意图、文章大纲或完整文章交给 AI，并由 Skill 规划和生成配图。
- 将现有固定风格与多风格扩展分开，提出可插拔风格包及身份风险分类。
- 给出从可用 Skill 走向可靠内容系统的工程、产品和研究扩展路线。

## 核心结论

它不是新图像模型，而是一套运行在 Agent 与图像生成工具之间的工作流。它先把人物照片编译成角色设定板、干净身份参考和人物规范；用户明确确认后，角色才能成为当前 IP。随后 Agent 读取完整文章，选择认知锚点，以“流程拆解”或“核心动作”模式逐张生成 16:9 编辑插图。

真正可确定复用的是角色包结构、`draft → confirmed` 状态和文件版本管理；身份保真、文章理解与最终画质仍取决于宿主 Agent 和图像模型。

## 研究产物

- [Web 研究展厅](showcase/)
- [能力、原理与限制](docs/analysis.md)
- [使用场景与扩展路线](docs/extension-roadmap.md)
- [自有 ImageGen 生成记录](showcase/assets/generated/PROMPTS.md)
- [小岚角色规范](showcase/assets/generated/xiaolan-character-spec.md)
- [固定上游版本](upstream/)

## 阅读路径

1. `upstream/SKILL.md`：理解阶段路由和角色确认门。
2. `upstream/references/character-package.md`：理解角色状态与本地资产结构。
3. `upstream/scripts/character_registry.py`：确认确定性代码的真实范围。
4. `upstream/references/article-workflow.md`：理解认知锚点、数量与交付规则。
5. `upstream/references/illustration-style.md`：理解两种视觉模式与固定风格合同。

Web 展厅在自有实演之后新增两组实践说明：`如何使用` 将内容输入分为一句意图、文章大纲和完整文章，并解释用户、AI + Skill、图像模型的职责；`多风格` 说明当前上游只有一套复古扁平 3D 合同，多风格属于可扩展方向，需要独立风格包与身份一致性评估。

## 边界

- 本研究不安装该 Skill 到用户全局环境。
- 不上传或使用真人照片；自有实演使用 ImageGen 生成的虚构人物作为模拟原始图。
- 不复制或再分发 `assets/` 中受单独许可约束的 Punk 角色源资产。
- Web 展厅同时展示本研究原创生成资产，以及 `docs/images/` 中许可证允许用于描述仓库的上游示例图；两者明确分区。
- 扩展路线均明确标记为建议，不冒充上游现有能力。
