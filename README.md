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
| [Stamp Edge Skill 项目研究](projects/stamp-edge-skill/README.md) | [xianxie6/stamp-edge-skill](https://github.com/xianxie6/stamp-edge-skill) | 邮票齿孔、透明蒙版、投影、瀑布流合集，以及预设驱动图片风格引擎扩展 | [能力分析](projects/stamp-edge-skill/docs/analysis.md) | [在线演示](https://yydshly.github.io/0818_githubcode_study/projects/stamp-edge-skill/showcase/) | 已复现 · 已收口 |
| [Promise Wall 项目研究](projects/promise-wall/README.md) | [thebuggeddev/promise-wall](https://github.com/thebuggeddev/promise-wall) | Three.js 空间卡片、十二场景第一版效果、后期行动地图与归档边界 | [能力分析](projects/promise-wall/docs/analysis.md) | [在线演示](https://yydshly.github.io/0818_githubcode_study/projects/promise-wall/showcase/) | 已完成 · 已归档 |
| [Photo to Organic Knit 项目研究](projects/photo-to-organic-knit/README.md) | [NalaZhang27/photo-to-organic-knit](https://github.com/NalaZhang27/photo-to-organic-knit) | 照片语义取舍、概念重构、针织材料参考、ImageGen 独立实演与产品化路线 | [能力分析](projects/photo-to-organic-knit/docs/analysis.md) | [在线演示](https://yydshly.github.io/0818_githubcode_study/projects/photo-to-organic-knit/showcase/) | 已复现 · 持续扩展 |

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

## 第三个研究项目：Stamp Edge Skill

[Stamp Edge Skill](https://github.com/xianxie6/stamp-edge-skill) 是一个轻量 Agent Skill：`SKILL.md` 负责把“做成邮票边”等自然语言请求路由到 Pillow 脚本，`stamp_effect.py` 生成齿孔、透明画布和投影，`stamp_sheet.py` 将多张结果排成列高均衡的合集。

本仓库固定上游 v1.2.0 对应 commit，用四张原创生成摄影与两张本地确定性内容卡，复现旅行、建筑、餐饮、植物、社交长帖和编辑海报六类场景；同时完整展示默认 4 列深色与自定义 3 列纸色合集。Alpha 往返实验进一步确认“输入图片内部透明区域不会被保留”的实现边界。在此基础上，文档提出从单一邮票效果演进为形状、边框、材质、色彩、景深和布局模块组成的预设驱动引擎。

第一批扩展已经落地：统一的 Pillow CLI 提供拍立得、撕纸、胶片、票券、Riso 印刷和已有 Alpha 的轮廓贴纸六个 preset，并配套 Agent Skill、行为测试与混合效果合集。

当前研究已正式收口，不继续开发 `stamp-v2` 或更多相似效果；页面仅保留核心画质、批量工作流、邮票语义与可选 AI 四类未来探索索引。

- [真实效果与扩展路线展厅](projects/stamp-edge-skill/showcase/)
- [项目研究说明](projects/stamp-edge-skill/README.md)
- [能力、原理与限制](projects/stamp-edge-skill/docs/analysis.md)
- [通用图片风格系统扩展路线](projects/stamp-edge-skill/docs/extension-roadmap.md)
- [已实现的图片风格扩展 Skill](projects/stamp-edge-skill/extension/image-style-skill/SKILL.md)
- [可复现 Demo](projects/stamp-edge-skill/demo/README.md)

## 第四个研究项目：Promise Wall

[Promise Wall](https://github.com/thebuggeddev/promise-wall) 是一个把短内容、纸张身份和空间位置组合起来的 Three.js 单页原型。上游通过 Canvas 在运行时生成撕边、纤维、横线、方格、手写字、照片、石墙和木纹，再把纸张映射为弯曲的 3D 卡片；Raycaster、摄像机与 DOM 面板共同完成拖动、缩放、聚焦、搜索、创建和墙面放置。

本研究直接嵌入未修改的固定上游页面作为运行证据，同时明确区分三层边界：渲染和空间交互是真实实现；支持、反思、收藏、举报是当前会话内的界面模拟；账号、持久化、实时协作、上传和审核完全未包含。在此基础上，第三版展厅为新年、毕业、婚礼、企业、员工感谢、公益、匿名心声、家庭、旅行、品牌、城市与游戏十二类使用场景分别建立第一版效果舞台，并使用 ImageGen 气氛总览辅助建立整体产品体感。

当前研究已完成并归档。展厅最后保留独立互动、时间变化、集体反馈、成果输出、现场模式、个人空间和跨场景生命周期七类未来行动，以及明确的重新启动条件；它们不是当前实现承诺。

- [原版 Demo 与能力研究展厅](projects/promise-wall/showcase/)
- [项目研究说明](projects/promise-wall/README.md)
- [能力、架构与限制](projects/promise-wall/docs/analysis.md)
- [使用场景与扩展路线](projects/promise-wall/docs/extension-scenarios.md)
- [固定上游版本](projects/promise-wall/upstream)

## 第五个研究项目：Photo to Organic Knit

[Photo to Organic Knit](https://github.com/NalaZhang27/photo-to-organic-knit) 是一套运行在 Codex 与 ImageGen 之间的艺术指导 Skill。它不训练图像模型，而是先将照片元素分成保留、转化和舍弃三组，再以一个视觉隐喻、至少三项结构变化、真实纤维材料和编辑式留白形成生产 Prompt，最后检查结果是否真正重构而不是仅有毛线滤镜。

本研究固定上游 commit，并累计完成六材料、场景、成品、目标驱动 Skill、前向测试与 Pilot。追加式台账锁定旧样例；中文调用进入双渠道设计层，新增验证区则为针织、彩玻璃和陶瓷浮雕逐组并列完整原图和结果，显示保留、转化与舍弃。

- [独立实演与研究展厅](projects/photo-to-organic-knit/showcase/)
- [能力、原理、意义与边界](projects/photo-to-organic-knit/docs/analysis.md)
- [使用场景、扩展方向与实际价值](projects/photo-to-organic-knit/docs/use-cases-and-roadmap.md)
- [完整 ImageGen 生成记录](projects/photo-to-organic-knit/showcase/assets/generated/PROMPTS.md)
- [五种扩展效果 Prompt](projects/photo-to-organic-knit/showcase/assets/generated/MULTI_EFFECT_PROMPTS.md)
- [三组新增场景 Prompt](projects/photo-to-organic-knit/showcase/assets/generated/SCENARIO_PROMPTS.md)
- [目标驱动扩展 Skill](projects/photo-to-organic-knit/extension/photo-to-conceptual-art/SKILL.md)
- [Prompt 编译器](projects/photo-to-organic-knit/extension/photo-to-conceptual-art/scripts/build_prompt.py)
- [未见照片前向测试](projects/photo-to-organic-knit/extension/photo-to-conceptual-art/forward-tests/lighthouse-travel/RESULT.md)
- [跨题材 n=3 Pilot](projects/photo-to-organic-knit/extension/photo-to-conceptual-art/forward-tests/pilot-n3/RESULT.md)
- [Review 记录器](projects/photo-to-organic-knit/extension/photo-to-conceptual-art/scripts/score_review.py)
- [固定上游版本](projects/photo-to-organic-knit/upstream)

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
