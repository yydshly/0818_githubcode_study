# Punk IP Illustrations 研究展厅交付记录

## Design Contract

```text
Entry mode: Revision-led refinement
Request revision: 4
Target user and context: 希望快速判断视觉 Agent Skill 能力、使用价值和后续研究方向的中文研究者与内容创作者
Desired first impression: 从首屏“自有实演”入口进入第一个实证区，先看见本研究用自己的虚构角色和 ImageGen 完整跑通角色设定、确认与文章配图，再理解它不是新模型而是一套一致性工作流
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: 暖白研究纸面、墨黑正文、钴蓝与珊瑚红语义强调；大字号编辑层级；不使用外部字体、渐变、连续动画或受限角色源资产；新增自有实演只使用本研究 ImageGen 资产，现有上游公开样张保留为独立对照证据
Information constraints: 必须区分上游规则、本研究实际执行、底层图像模型能力和后续扩展；自有演示要展示输入设定、角色草稿、确认参考、文章锚点、最终插图与观察结论；不把模拟角色冒充真人照片流程
Operation constraints: 纯静态 HTML/CSS/JS；能力层切换、场景筛选和扩展路线切换均可由键盘完成；核心内容在 JavaScript 失效时仍可阅读
State constraints: 默认展示完整能力链和全部场景；交互只切换解释层与筛选可见卡片；无远程数据、登录、上传、弹窗或真实图像生成状态
Environment constraints: GitHub Pages；无构建依赖、后端、账号、外部 API 或外部字体；上游以 Git submodule 固定
Primary journey: 首屏点击“看自有实演” → 理解模拟原始图到最终插图 → 在“如何使用”中区分意图/大纲/全文三类输入并看清 AI、Skill、图像模型分工 → 在“风格扩展”中理解身份、语义与风格三层解耦及风险分类 → 对照上游证据与研究路线 → 阅读复核材料
User-defined phases: 保留自有实演与上游样张；新增详细“如何使用”说明；按意图、大纲、全文分类输入；新增详细“风格扩展”说明；按风格类型与身份风险分类；提交远端 GitHub 并触发 Pages 部署
Required artifacts: 固定上游 submodule、自有 ImageGen 资产、使用说明模块、风格扩展模块、更新后的研究文档与主索引、三视口浏览器验收记录、Git 提交、远端推送与 Pages 部署证据
Autonomy authorization: 用户明确要求将两项总结接入 Web、详细分类描述，并提交远端 GitHub 和部署；授权修改当前研究项目、主索引和 Pages 配置，提交并推送本次研究范围内的变更
User-decision boundary: 不安装 Skill 到全局环境，不上传或使用真人照片，不发布或再分发受限 Punk 角色源资产，不新增后端、真实上传/生成表单或业务账号；不修改 GitHub 凭据，仅使用已有认证通道
Observable completion criteria: 页面明确说明“文章/目标 + 已确认角色 + Skill/AI/图像模型”的使用关系；分别描述意图、大纲、全文输入的适用性和输出差异；明确当前上游只有一套固定风格，多风格是扩展建议；给出风格包结构、类型与身份风险；原有实演和上游证据保留；1440/768/390px 无横向溢出；图片、键盘和 reduced-motion 可用；变更进入远端并由 GitHub Pages 返回成功部署
Coverage record: 见下表
```

## Brief-led Design Direction

| 决策 | 选择 | 可观察约束 | 验收标准 |
| --- | --- | --- | --- |
| 信息层级 | “不是模型，是一致性工作流”作为唯一首屏主结论 | 首屏只保留一个主标题、一个边界判断和两个阅读入口 | 首次扫描无需阅读长段落即可复述定位 |
| 阅读路径 | 结论 → 工作流 → 证据 → 场景 → 扩展 → 研究判断 | 每段有编号与明确问题，不用卡片堆满首屏 | 桌面与手机保持相同语义顺序 |
| 视觉语言 | 编辑研究档案，而非 AI 产品营销页 | 暖白底、细规则线、克制蓝红语义色，无渐变 | 能力、外部依赖和扩展设想有不同视觉标记 |
| 交互 | 只为比较层级和筛选信息服务 | 使用原生 button/tab 语义与可见焦点 | 鼠标与键盘均能切换，禁用 JS 时正文仍存在 |
| 图片使用 | 自有 ImageGen 资产用于实际流程，上游 `docs/images` 用于对照 | 不直接展示或复制上游 `assets/` 下的角色源文件 | 自有资产和上游证据明确分区并标注来源 |
| 响应式 | 编辑双栏在窄屏重排为单列 | 1440、768、390 三档无遮挡和横向滚动 | 主旅程与操作在三档均可完成 |

## Coverage Manifest

| 用户阶段 | 要求或资产 | 表面 / 状态 | 证据 | 阶段 | 状态 | 下一步 |
| --- | --- | --- | --- | --- | --- | --- |
| 获取上游 | submodule 与固定 commit | 文件系统 | Git 与文件检查 | 0 / 1 / 9 | pass | — |
| 研究归档 | README、能力分析、扩展路线 | 文档 | 文件与源码链接 | 3 / 9 | pass | — |
| 能力说明 | 三层能力边界与六步工作流 | 展厅默认状态 | 浏览器阅读流 | 2 / 3 | pass | — |
| 上游证据 | 四张公开示例与两种配图模式 | 桌面 / 手机 | 图片加载与说明 | 3 / 7 | pass | — |
| 使用场景 | 至少六类场景和不适用边界 | 全部 / 筛选状态 | 点击、键盘与 DOM 状态 | 4 / 5 / 6 / 7 | pass | — |
| 可扩展方向 | 工程层、产品层、研究层 | tab 状态 | 点击、方向键、Home/End | 4 / 5 / 6 / 7 | pass | — |
| 响应式 | 桌面、平板、390px | 1440 / 768 / 390 | 截图与溢出检查 | 7 | pass | — |
| 可访问性 | 语义、焦点、reduced motion | 键盘 / CSS | 焦点路径与媒体条件 | 7 / 8 | pass | — |
| 工程闭环 | 资源、链接、本地 HTTP、主索引 | 文件 / 页面 | 引用检查、HTTP、git diff | 9 | pass | — |
| 修订 3 · 自有角色 | 模拟原始图、角色设定板与干净身份参考 | ImageGen / 本地资产 | 图片检查、保存路径、人物规范与生成记录 | 2 / 3 / 9 | pass | — |
| 修订 3 · 自有场景 | 开源项目研究流程插图 | ImageGen / 16:9 | 身份、动作、物件与画面检查 | 2 / 3 / 9 | pass | — |
| 修订 3 · 自有实演 | 在上游证据之前新增完整自有流程，保留原样张 | 首页 / 自有实演 / 上游证据 / 主索引 | DOM、资源引用与浏览器截图 | 2 / 3 / 7 | pass | — |
| 修订 3 · 流程说明 | 显示模拟输入、确认门、认知锚点与观察 | 展厅 / 文档 | 阅读流与事实边界检查 | 3 / 9 | pass | — |
| 修订 3 · 回归 | 三视口、图片、tabs、筛选、键盘与 reduced-motion | 1440 / 768 / 390 | Chrome 浏览器与工程检查 | 5 / 7 / 8 / 9 | pass | — |
| 修订 4 · 使用说明 | 文章/目标如何与确认角色和 Skill 结合 | 使用模块 / 三类输入 / 分工 / 示例 | DOM、阅读流与事实边界检查 | 2 / 3 / 7 / 9 | pass | — |
| 修订 4 · 风格扩展 | 从当前固定风格扩展为可插拔风格包 | 扩展模块 / 类型 / 风险 / 合同 | DOM、响应式与研究边界检查 | 2 / 3 / 7 / 9 | pass | — |
| 修订 4 · GitHub 发布 | 提交、推送并触发 Pages | 当前研究文件 / 远端 / Pages | Git、远端 commit、Actions 与在线 URL | 9 | pass | — |

## Canonical Runtime

```text
Start command: python -m http.server 8879 --directory E:\0818_codex_project
Canonical URL: http://127.0.0.1:8879/projects/punk-ip-illustrations/showcase/
Theme: light only
Required viewports: 1440×1000, 768×1024, 390×844
Verified: 2026-08-19 Asia/Shanghai
```

## Browser Evidence

- `agent-browser` CLI 未安装到 PATH；按技能降级规则改用工作区内置 Playwright 1.x + 本机 Chrome 做真实浏览器验收，没有把源码检查替代为视觉证据。
- canonical URL 返回标题 `Punk IP Illustrations · 角色一致性工作流研究`，正文 4451 字符，无错误覆盖层、控制台错误、页面错误或失败请求。
- 页面 9 个图片元素全部成功加载且都有替代文字：4 张自有 ImageGen 资产、5 个上游样张元素（其中 hero 与证据区复用同一流程图）；上游受限角色源资产没有被直接展示或复制。
- 自有实演区明确披露模拟原始图为虚构人物而非真人照片；`source → sheet → confirmed clean reference → final scene` 四步资产链与研究场景均可见。
- 能力层点击后“文章层”可见且“角色层”隐藏；扩展路线在工程 tab 上按 `End` 后正确选中“研究验证”并显示对应面板。
- 场景筛选点击“不适合”后只显示 3 张边界卡，状态文字同步为“当前显示 3 个场景”。
- 1440×1000、768×1024、390×844 的 `scrollWidth - clientWidth` 均为 `0`；三档均保留 6 个 tab 与 9 张场景卡。
- 键盘聚焦控件具有 3px 可见焦点；`prefers-reduced-motion: reduce` 命中时根元素 `scroll-behavior` 为 `auto`。
- Pages 主索引第 08 项已改用自有最终场景图；按部署根路径解析后封面成功加载。先前 Pages 临时组装的 8 个项目、入口与路径回归仍通过。
- 工程检查：展厅 14 个本地引用无缺失；注册脚本 `--help` 正常；`git diff --check` 通过。
- 修订 3 证据截图保存在工作区外的 Codex visualization 目录：自有实演桌面全区、390px 全区与 390px 最终场景视口；实际像素与文案经视觉检查。
- 修订 4 新增使用与风格模块：浏览器确认 3 类内容输入、6 类风格家族、无生图工具降级边界和“多风格不是上游现成功能”声明均存在；1440、768、390px 的 `scrollWidth` 均等于视口宽度。
- 修订 4 保持 9 个图片元素全部加载，既有能力 tab、场景筛选、路线键盘 `End` 和 reduced-motion 回归通过；控制台错误、页面错误和失败请求均为 0。
- 修订 4 桌面两模块全区截图与 390px 顶部视口截图保存在工作区外的 Codex visualization 目录，并完成实际像素检查。
- 发布提交 `27ff9df` 已推送至 `codex/punk-ip-illustrations-research` 与 `main`；GitHub Actions 运行 [`32267950806`](https://github.com/yydshly/0818_githubcode_study/actions/runs/32267950806) 完成且结论为 `success`。
- 线上地址 `https://yydshly.github.io/0818_githubcode_study/projects/punk-ip-illustrations/showcase/` 返回 HTTP 200，并包含 `GUIDE A / HOW TO USE IT`、`GUIDE B / STYLE EXPANSION`、三类输入和六类风格；自有原始图、最终场景图与 `styles.css?v=3` 均返回 HTTP 200。

## Session Handoff

1. **项目与阶段：** Punk IP Illustrations 研究子项目；Stage 9 已完成本地交付闭环。
2. **已完成：** 固定上游 submodule、能力分析、场景与扩展文档、四张自有 ImageGen 资产、完整角色实演、响应式研究展厅、主索引与 Pages 组装规则均已完成；原上游样张完整保留。
3. **剩余或延期：** 当前授权范围内无未完成项；研究内容已提交、推送并部署到 GitHub Pages。
4. **证据：** 真实 Chrome 浏览器、三视口、9 个图片元素、三类内容输入、六类风格、键盘、筛选、tabs、reduced-motion、主入口与主索引封面均通过；Actions 与线上页面/资源均验证成功。
5. **下一步：** 若后续进入实证研究，优先实现“结构化图片计划 + 角色一致性评分 + 无字底图确定性排版”三项 P0/P1 实验。
