# GitHub Code Study

[![Deploy research showcase to Pages](https://github.com/yydshly/0818_githubcode_study/actions/workflows/pages.yml/badge.svg)](https://github.com/yydshly/0818_githubcode_study/actions/workflows/pages.yml)
[![Online showcase](https://img.shields.io/badge/GitHub%20Pages-online-147b78)](https://yydshly.github.io/0818_githubcode_study/)

这是一个面向长期积累的代码研究主仓库，用于整理、索引和展示值得深入阅读的开源项目与实践成果。

本仓库主要承担三项职责：

- 作为所有研究子项目的统一入口；
- 记录每个项目的研究目标、关键发现与复现进度；
- 关联独立部署的演示、源码仓库和完整研究笔记。

## 项目索引

新增项目时，请复制[研究记录模板](docs/research-template.md)，并在下表登记。

| 项目 | 来源 | 研究主题 | 研究记录 | 在线演示 | 状态 |
| --- | --- | --- | --- | --- | --- |
| [Luopan 项目研究](projects/luopan/README.md) | [zhangxiaoqiang1991/luopan](https://github.com/zhangxiaoqiang1991/luopan) | 原版能力实演、数据与决策原理、AI 编程 Agent 实战及 GitHub 项目研究扩展 | [项目说明](projects/luopan/README.md) | [在线演示](https://yydshly.github.io/0818_githubcode_study/projects/luopan/showcase/) | 已复现 |
| [Hand-drawn Styles 项目研究](projects/hand-drawn-styles/README.md) | [threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles) | 视觉 Prompt 配方、单一真源、锚点校验、多阶段生成合同及日常场景路由 | [当前状态](projects/hand-drawn-styles/STATUS.md) | [在线演示](https://yydshly.github.io/0818_githubcode_study/projects/hand-drawn-styles/showcase/) | 已复现 · 持续扩展 |

状态建议使用：`待开始`、`研究中`、`已复现`、`持续跟踪`、`已归档`。

## 首个研究项目：Luopan

[Luopan](https://github.com/zhangxiaoqiang1991/luopan) 是一套运行在 Codex、Claude Code 等 AI 宿主中的商业研究 Skill。它先识别用户研究的是行业、公司、股票还是岗位，再根据投资、求职或行业进入目标，获取必要证据并运行对应判断框架。

本仓库围绕 Luopan 完成了四层归档：

1. **原版能力实演**：直接关联上游已有的 3 份行业报告，以及 NVIDIA 投资、字节跳动求职、腾讯双线公司报告。
2. **数据来源整理**：归档 westock-data、A/H/美股、SEC、非上市公司、行业六视角、行情估值和证据冲突处理方式。
3. **原理与判断拆解**：解释对象路由、A/B/C 证据等级、行业九阶段、投资七道门和求职五层漏斗。
4. **关联扩展**：使用 Luopan 方法研究 AI 编程 Agent 行业，并扩展出标准化的 GitHub 项目研究 Skill。

### 数据来源概览

| 类型 | 主要来源 | 作用 |
| --- | --- | --- |
| 原始披露（A 级） | SEC、巨潮资讯、上交所、深交所、北交所、HKEXnews、公司正式报告 | 公司身份、财务和重大事项的事实基准 |
| 结构化金融数据（B 级） | 外部 `westock-data` / 腾讯自选股接口 | 财务三表、行情、一致预期和行业板块快扫 |
| 行业研究（B 级） | 政策、资本、产业链、技术、需求和人才六类来源 | 建立行业边界、权力格局、利润池和趋势 |
| 调查线索（C 级） | 员工评价、论坛、社交内容和未说明口径的数字 | 发现需要继续核实的问题，不独立支撑结论 |

> 重要边界：`westock-data` 是 Luopan 方法依赖的外部 CLI，并不包含在上游仓库内；仓库自带的数据自动化主要是 SEC 标准财务事实的最小抓取器。

- [在线研究展厅](https://yydshly.github.io/0818_githubcode_study/projects/luopan/showcase/)
- [数据来源与信息获取档案](projects/luopan/docs/data-sources-and-acquisition.md)
- [AI 编程 Agent 行业实战](projects/luopan/applied/ai-coding-agents-2026.md)
- [GitHub 项目研究扩展 Skill](projects/luopan/extension/study-github-projects/SKILL.md)
- [项目技术审计](projects/luopan/showcase/audit/analysis.md)

## 第二个研究项目：Hand-drawn Styles

[Hand-drawn Styles](https://github.com/threerocks/hand-drawn-styles) 不是图像模型，而是一套运行在 Agent 与外部图像模型之间的视觉 Prompt 编排层。它将 19 套风格保存为配方，以协议约束风格选择和变量填充，并对 3.1 稳定变体加入固定视觉锚点、像素身份校验和三阶段编辑合同。

本仓库在不复制上游风格规则的前提下，增加了研究方法拆解、结论摘要卡、项目封面、里程碑故事和团队日常故事卡五类场景路由，用于演示如何把“风格怎么画”进一步转化为“我们的日常任务什么时候使用哪种风格”。

- [在线效果与场景路由工作台](https://yydshly.github.io/0818_githubcode_study/projects/hand-drawn-styles/showcase/)
- [项目研究说明](projects/hand-drawn-styles/README.md)
- [能力、原理与使用意义分析](projects/hand-drawn-styles/docs/analysis.md)
- [后期使用指南：项目、PPT、报告、教程、社媒与品牌场景](projects/hand-drawn-styles/docs/usage-guide.md)
- [固定上游版本](projects/hand-drawn-styles/upstream)

## 仓库结构

```text
.
├── README.md                  # 全部子项目的索引入口
├── docs/
│   └── research-template.md  # 单个项目的研究记录模板
└── projects/
    └── README.md             # 子项目收录与目录约定
```

## 收录方式

根据项目规模选择一种方式：

1. **仓库内研究**：轻量实验、阅读笔记和最小复现放在 `projects/<project-slug>/`。
2. **独立仓库研究**：需要单独构建、部署或长期维护的项目放在独立 GitHub 仓库，本仓库只保留索引、摘要与链接。

不直接复制来源项目的完整代码历史。需要保留上游提交关系时，应在独立仓库中 fork；仅作版本引用时，可记录上游仓库地址与研究时使用的 commit/tag。

## 新增研究项目

1. 确定项目名称、来源仓库和研究问题。
2. 复制 `docs/research-template.md` 创建研究记录。
3. 按实际情况在 `projects/` 内建立实验目录，或创建独立仓库。
4. 在本页“项目索引”中补充源码、记录与演示链接。
5. 在研究记录中固定上游版本，并持续维护结论和复现步骤。

## 基本约定

- 目录名和独立仓库名使用小写 `kebab-case`。
- 每项结论尽量关联源码位置、commit、issue 或官方文档。
- 明确区分“上游原始实现”“个人修改”和“实验性推断”。
- 引入第三方代码前检查并保留其许可证与署名要求。
- 演示链接失效或项目停止维护时，及时更新状态。

## 后续规划

- 持续补充项目索引与研究笔记；
- 为适合展示的子项目建立独立部署；
- 在项目数量增加后，再按主题增加标签、筛选和自动化索引。
