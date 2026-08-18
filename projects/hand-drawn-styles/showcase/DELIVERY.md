# Hand-drawn Styles Study Showcase · Delivery Record

## Design contract

```text
Entry mode: Brief-led extension of an existing research repository
Request revision: 6
Target user and context: 主仓库维护者，以及希望把日常内容快速转成稳定视觉风格提示词的研究与内容创作者
Desired first impression: 先看到真实风格效果，再明确它不是生图模型，而是一套可执行的视觉风格合同
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: 延续研究主库的深色档案气质，但用纸张、蜡笔和墨线作为项目识别；不依赖外部字体或 UI 框架；390px–1440px 可读
Information constraints: 必须区分上游事实、我们的解释和我们的扩展；先展示效果能力，再解释五层实现，最后提供贴近日常场景的交互演示
Operation constraints: 纯静态 HTML/CSS/JavaScript；无后端、登录、真实图像 API 或构建依赖；演示只生成可复制 Prompt/调用方案，不伪装成已经出图
State constraints: 风格筛选、场景模板、强度与比例选择、Prompt 预览和复制反馈；禁用 JavaScript 时核心研究内容与静态示例仍可阅读
Environment constraints: GitHub Pages artifact；本地使用 Python HTTP server；上游以 Git submodule 固定版本
Primary journey: 进入展厅 → 阅读完整案例背景 → 跟随同一研究者经历问题、归档、路由、组装、复盘、发布六幕连续过程 → 再区分上游能力样图与我们的内容资产 → 理解 Prompt/参考图/多阶段编辑原理 → 选择日常场景
User-defined phases: 获取上游；展示效果能力并说明原理；结合我们的场景说明意义；用 ChatGPT 直接生成对应图片；增加更多展示样例；为样例提供背景和描述；把图片串成完整案例而不是孤立单图；继续以其他风格增加样例说明；其他风格也必须以场景或流程串联；把能力与应用场景整理成笔记并接入网页，指导后期使用
Required artifacts: Git submodule、项目 README、研究文档、6幕主案例、3类独立内容资产、4条三幕风格流程、独立使用手册、网页使用指南、场景矩阵、风格路由、标准资产包、五步流程、可复制请求模板、可运行展厅、主索引与 Pages workflow 更新、浏览器验收记录与最终截图
Autonomy authorization: 用户明确要求将该库作为研究子项目获取、分析、展示并结合我们的场景实现演示
User-decision boundary: 对外调用付费图像模型、修改或提交上游仓库、创建独立仓库需要另行授权
Observable completion criteria: 上游 commit 固定；能力与原理有源码证据；至少 8 个真实样图入口；连续案例包含背景、目标、角色、约束、六幕因果和结果，六幕使用同一主角与统一视觉语言；每幕有标题、场景、发生原因、得到结果和下一幕衔接；3类独立内容资产有明确语义、来源和位置；至少 4 个日常场景可交互生成 Prompt；桌面/平板/390px 无遮挡或横向溢出；键盘焦点可见；reduced-motion 与无 JavaScript 可读；本地发布路径与链接通过
Coverage record: 见下表
```

## Brief-led design direction

| 决策 | 选择 | 可观察约束 | 验收标准 |
| --- | --- | --- | --- |
| 信息层级 | 真实效果 → 能力边界 → 五层原理 → 我们的意义 → Prompt 工作台 | 首屏必须同时出现项目结论与进入效果/工作台的入口 | 30 秒内可回答“它能做什么、不是什​​么” |
| 视觉语言 | 深色研究底板 + 暖白纸张样图卡 + 蜡笔橙/薄荷绿信号色 | 装饰不得压过样图与文字 | 样图和操作控件是主要视觉焦点 |
| 交互 | 原生表单控件驱动 Prompt 预览 | 所有操作可键盘完成，复制状态明确 | 场景、风格、比例变化立即反映在结果中 |
| 响应式 | 宽屏双栏、窄屏单栏 | 390px 不横向滚动，控件不截断 | 1440/768/390 三视口通过 |
| 降级 | HTML 内保留研究正文和静态 Prompt 范例 | JavaScript 关闭不隐藏核心能力与原理 | 无 JS 仍可完成阅读主路径 |

## Coverage manifest

| 用户阶段 | 要求/产物 | 界面/状态 | 所需证据 | 阶段 | 状态 | 下一步 |
| --- | --- | --- | --- | --- | --- | --- |
| 获取上游 | 固定来源与 commit | Git submodule | `.gitmodules`、gitlink、版本号 | 1 | pass | 已固定 `9f150d9` |
| 展示效果 | 上游真实样图与风格分类 | 桌面默认态、筛选态 | 样图资源、浏览器截图与 DOM 观察 | 2/3/5 | pass | 10张代表样图加载，4组筛选可用 |
| 说明原理 | Prompt、协议、渲染器、锚点与三阶段合同 | 原理区 | 源文件链接和研究文档 | 3 | pass | 五层实现、普通/3.1合同与 fail-closed 完整呈现 |
| 场景意义 | 研究封面、教程信息图、项目插画、社媒故事卡 | 意义区 | 页面内容与场景映射 | 3 | pass | 5类场景映射及“不复制配方”边界可见 |
| 日常扩展 | 可交互 Prompt 工作台 | 默认、3.1切换、复制失败反馈 | 浏览器交互证据 | 4/5/6 | pass | 3.1输出含合同ID、锚点、三阶段与JSON参数；剪贴板不可用时明确提示 |
| 响应式 | 桌面、平板、390px 手机 | 1440/768/390px | 三视口截图、无溢出 | 7 | pass | 三视口通过；390px溢出从448修正至375内容宽 |
| 可访问性 | 键盘、焦点、语义、reduced-motion、脚本不可用 | 操作与降级态 | 浏览器/DOM 观察 | 7/8 | pass | 首焦点为跳转链接且3px轮廓；reduced-motion=true；阻断app.js后核心正文完整 |
| 工程质量 | 测试、链接、Pages artifact | 本地 HTTP | 自动检查、HTTP、控制台 | 9 | pass | 项目验收通过；无控制台/页面错误；临时Pages根索引与项目路径通过 |

## Canonical runtime

从主仓库根目录运行：

```powershell
python -m http.server 4174 --bind 127.0.0.1 --directory projects/hand-drawn-styles
```

- URL：`http://127.0.0.1:4174/showcase/`
- 验收时间：`2026-08-18T17:40:53+08:00`
- 发布结构复核：临时 Pages artifact 根索引可见第二项目，点击后进入 `/projects/hand-drawn-styles/showcase/`。
- 支持边界：单一深色主题；纯静态；不调用真实图像 API；脚本不可用时研究正文和样图仍可读，交互路由不可用。

## Browser refinement ledger

### Final visual and interaction pass

```text
Current stage: 9 · Engineering and delivery closure
User phase: 获取上游 + 展示能力/原理 + 场景意义 + 日常扩展
Coverage item: 10张上游样图、五层原理、5类场景、3.1输出、三视口、键盘、reduced-motion、脚本降级与Pages入口
User goal: 把上游作为正式研究子项目，并演示它如何服务我们的日常内容生产
Browser environment: agent-browser 0.27.0 / Chromium / 1440×1000, 768×1024, 390×844
Observed evidence: 页面有内容且无错误覆盖层；错误与控制台为空；3.1路由输出完整合同；三张最终截图；临时Pages根入口和项目目标均200
Problem category: Clipboard fallback + mobile layout overflow
Root cause: 旧式execCommand可能抛错且没有二次容错；移动端代码块的grid item保留min-content宽度
Minimal intervention: 两条复制路径独立容错并始终设置aria-live反馈；contract card设min-width:0且移动网格使用minmax(0,1fr)
Adjacent regression surfaces: 默认路由、3.1路由、桌面、平板、390px、键盘首焦点、reduced-motion、脚本请求阻断、Pages根入口
Observed result: 复制不可用时显示“请手动选择”；390px innerWidth=390、content scrollWidth=375；其余表面通过
Decision: pass
Next executable action: none
New authority required: none
```

最终浏览器证据保存在会话可视化目录：

- `hand-drawn-styles-desktop.png`
- `hand-drawn-styles-tablet.png`
- `hand-drawn-styles-mobile.png`

## Engineering evidence

- `python projects/hand-drawn-styles/tests/verify_project.py`：通过。
- 普通4号配方可完整渲染；3.1输出 `family-crayon-card-v3` 且阶段顺序正确。
- 上游自测在 Windows 为 `18/19`：唯一失败是路径分隔符断言；另发现1号配方标签与占位符语法冲突。两项均记录在项目 README 与完整分析中，固定上游未改动。
- `git diff --check`：通过。

## Revision 2 · ChatGPT-generated use-case assets

### Scope revision

```text
Entry mode: Revision-led
Request revision: 2
User goal: 不只展示上游风格样图，还要直接使用 ChatGPT 生成与本研究内容关联的图片，演示图片的意义与使用场景
Preserved evidence: 上游获取、能力画廊、五层原理、场景路由、普通/3.1合同、既有键盘与脚本降级路径
Reopened surfaces: 首屏主视觉、效果与场景意义之间的信息层级、图片资源性能、桌面/平板/手机布局、Pages artifact
Visual direction: 用三张语义明确的项目内容资产替换“漂亮但无关”的示意方式；每张必须同时说明代表内容、页面职责、推荐复用位置和生成来源
Required artifacts: project-cover.png、method-explainer.png、milestone-story.png、对应提示词与资产清单、修订后浏览器证据
Autonomy authorization: 用户明确确认，并要求直接用 ChatGPT 生成对应图片进行演示
Observable completion: 首屏使用项目相关封面；新增三职责演示区；上游样图继续只作为能力证据；图片有alt、caption、来源与用途；三视口和发布路径通过
```

### Revision 2 coverage manifest

| 用户阶段 | 要求/产物 | 界面/状态 | 所需证据 | 阶段 | 状态 | 下一步 |
| --- | --- | --- | --- | --- | --- | --- |
| ChatGPT直接生图 | 项目封面 | 首屏主视觉 | 工作区PNG、视觉检查、生成提示词 | 2/3 | pass | 1122×1402 PNG 已用于首屏与主索引 |
| ChatGPT直接生图 | 原理讲解插图 | 三职责演示区 | 工作区PNG、语义映射与caption | 3 | pass | 四格无文字流程图完整呈现收集→归档→组合→出图 |
| ChatGPT直接生图 | 里程碑故事插图 | 三职责演示区 | 工作区PNG、情绪焦点与caption | 3 | pass | 失败图回到证据墙、橙色单焦点和记录动作清楚 |
| 图片意义与关联 | 用途、内容、位置、来源 | 三职责演示区 | DOM观察与文档资产清单 | 3/6 | pass | 每张含职责、对应内容、当前位置、复用位置、alt和ImageGen来源 |
| 性能与降级 | 图片加载和无图文本语义 | 默认/慢加载 | naturalWidth、alt、尺寸与fallback | 7/8 | pass | 14/14图片加载，missingAlt=0；非首屏新增图使用lazy loading |
| 响应式与交付 | 1440/768/390及Pages | 全页 | 三视口截图、无溢出、HTTP | 7/9 | pass | 三视口通过；390px scrollWidth=390；临时Pages根封面和项目入口通过 |

### Revision 2 browser refinement ledger

```text
Current stage: 9 · Engineering and delivery closure
User phase: 用 ChatGPT 直接生成对应图片进行演示
Coverage item: 项目封面、原理讲解图、里程碑故事图、语义关联、三视口、主索引与Pages发布路径
User goal: 让图片不只是风格样例，而是能直接说明本研究的意义和使用场景
Browser environment: agent-browser 0.27.0 / Chromium / 1440×1000, 768×1024, 390×844
Observed evidence: 首屏主视觉与项目主题一致；三职责区图片、caption与元数据可读；14张图片全部加载且有alt；控制台与页面错误为空；主索引封面naturalWidth=1122
Problem category: Information hierarchy / semantic association
Root cause: Revision 1 首屏使用上游家庭样图，只能证明风格效果，不能代表“Prompt工程化”研究内容
Minimal intervention: 用项目专属封面替换首屏样图；新增三职责演示区；上游样图继续独立保留为能力证据；主研究索引复用同一封面
Adjacent regression surfaces: 首屏、效果画廊、五层原理、工作台、1440/768/390、图片慢加载、主Pages索引与项目跳转
Observed result: 用户先理解三张图为什么存在，再进入上游效果画廊；390px无横向溢出；临时Pages路径通过
Decision: pass
Next executable action: none
New authority required: none
```

Revision 2 最终浏览器证据保存在会话可视化目录：

- `hand-drawn-styles-generated-assets-desktop.png`
- `hand-drawn-styles-generated-assets-tablet.png`
- `hand-drawn-styles-generated-assets-mobile.png`

## Revision 3 · Six-scene connected case

### Scope revision

```text
Entry mode: Revision-led
Request revision: 3
User goal: 更多展示样例必须有背景、描述和前后因果，能够串成一个完整案例，而不是若干孤立图片
Preserved evidence: 上游仓库、能力画廊、三类图片职责、五层原理、场景路由、既有生成资产和浏览器验收
Reopened surfaces: 应用演示的信息架构、生成资产数量与一致性、长页面阅读节奏、三视口、图片加载和Pages artifact
Story premise: 一个研究团队要发布 Hand-drawn Styles 研究项目，但初始图片彼此无关；同一位研究者将混乱样例变成可追踪、可复用、可发布的视觉系统
Character anchor: project-cover.png 中的深蓝上衣、黑色发髻研究者
Visual contract: 暖白纸底、深藏青/雾蓝/珊瑚橙/金橙、扁平绘本几何形、无图片内文字；HTML承担准确标题与叙事
Narrative: 01发现混乱 → 02建立档案 → 03按任务路由 → 04组装生成 → 05保留失败并修正 → 06形成可发布资产系列
Required artifacts: 5张新增连续场景 + 既有封面组成6幕；STORY.md；逐幕Prompt；六幕时间线；最终浏览器证据
Autonomy authorization: 用户明确要求更多样例、有背景和描述、并且必须串联成完整案例
Observable completion: 六幕同一主角/画风；每幕有因果与下一步；桌面横向阅读关系清楚、移动端纵向顺序清楚；图片加载、alt和发布路径通过
```

### Revision 3 coverage manifest

| 用户要求 | 要求/产物 | 界面/状态 | 所需证据 | 阶段 | 状态 | 下一步 |
| --- | --- | --- | --- | --- | --- | --- |
| 更多展示样例 | 六幕连续图片 | 故事时间线 | 6张工作区PNG、统一主角与画风 | 2/3 | pass | 既有封面作第02幕，5张新图组成完整六幕 |
| 有背景和描述 | 背景、目标、角色、约束、结果 | 案例序言 | DOM、文档与浏览器观察 | 3 | pass | 背景/任务/连续性合同和4项案例统计完整可读 |
| 能串起来 | 每幕原因→行动→结果→下一幕 | 六幕卡片与连接线 | 顺序DOM、视觉连接与移动端阅读 | 3/7 | pass | 桌面左右交替时间线、手机单列连接线；6个标题顺序正确 |
| 一致性 | 同一研究者与统一视觉合同 | 6张图片 | 人物、发型、服装、色板与材质目视检查 | 2 | pass | 黑色发髻、深蓝服装、暖白纸底与蓝橙色板六幕一致 |
| 来源与复现 | STORY.md与逐幕Prompt | 资产档案 | 文件、链接与ImageGen来源 | 9 | pass | 背景、角色、因果、依赖树和5张新增图最终Prompt已归档 |
| 响应式与性能 | 1440/768/390及图片加载 | 全页 | 截图、scrollWidth、naturalWidth、alt | 7/8/9 | pass | 20/20图片加载、missingAlt=0、390px scrollWidth=390、控制台无错误 |

### Revision 3 browser refinement ledger

```text
Current stage: 9 · Engineering and delivery closure
User phase: 更多样例 + 背景描述 + 串联成完整案例
Coverage item: 六幕图片、案例背景、因果时间线、一致角色、逐幕Prompt、三视口和图片加载
User goal: 看到一个能够说明“为什么、怎么做、最后得到什么”的连续案例，而不是孤立图片
Browser environment: agent-browser 0.27.0 / Chromium / 1440×1000, 768×1024, 390×844
Observed evidence: 浏览器语义树按01-06列出六幕标题；桌面左右交替并由中心线连接；手机恢复图片→描述的单列顺序；20张页面图片全部加载且有alt
Problem category: Information architecture / narrative continuity
Root cause: Revision 2只按“封面/讲解/故事”分类，没有共同背景、固定角色和前后因果，用户必须自己猜图片之间的关系
Minimal intervention: 固定一个主角与视觉合同，以既有封面为第02幕新增5张场景；在三职责区之前增加背景、任务、合同、六幕原因/行动/结果/衔接时间线
Adjacent regression surfaces: 首屏CTA、三职责区、上游画廊、五层原理、工作台、1440/768/390、图片懒加载与STORY.md链接
Observed result: 案例从“图片分类”升级为“发现混乱→建立档案→路由→组装→回归→发布”的完整闭环；三视口无横向溢出
Decision: pass
Next executable action: none
New authority required: none
```

Revision 3 最终浏览器证据：

- `hand-drawn-styles-story-desktop.png`
- `hand-drawn-styles-story-tablet.png`
- `hand-drawn-styles-story-mobile.png`

## Revision 4 · Multi-style application lab

### Scope revision

```text
Entry mode: Revision-led
Request revision: 4
User goal: 在六幕主案例之外，继续用其他风格生成与本研究相关的样例，并解释不同风格为什么适合不同场景
Preserved evidence: 六幕主案例、三类图片职责、上游能力画廊、五层原理、工作台与既有响应式验收
Reopened surfaces: 应用演示与上游效果之间的内容层级、多风格图片加载、三视口和Pages artifact
Comparison premise: 核心主题保持“把混乱 Prompt 变成可复用视觉系统”，但传播任务分别改变为文化隐喻、游戏化进度、编辑主视觉和角色IP
Style references: upstream/examples/08-ink-wash.png、09-pixel-art.png、13-paper-folk.png、15-softnose-vinyl.png，仅作风格参考，不复制其人物与情节
Required artifacts: style-08-ink-archive.png、style-09-pixel-workflow.png、style-13-paper-system.png、style-15-vinyl-researcher.png、MULTI-STYLE.md、页面对比区
Autonomy authorization: 用户明确要求继续以其他风格增加样例说明
Observable completion: 4张项目主题新图分别命中参考风格；每张说明背景、表达意义、适合位置和不适合场景；与六幕主案例区分清楚；三视口、alt、加载和发布路径通过
```

### Revision 4 coverage manifest

| 用户要求 | 要求/产物 | 界面/状态 | 所需证据 | 阶段 | 状态 | 下一步 |
| --- | --- | --- | --- | --- | --- | --- |
| 其他风格样例 | 8 水墨写意 | 多风格实验区 | 项目主题PNG、参考来源、用途说明 | 2/3 | pass | 1086×1448水墨策略隐喻图已集成 |
| 其他风格样例 | 9 复古像素 | 多风格实验区 | 项目主题PNG、参考来源、用途说明 | 2/3 | pass | 1448×1086四站游戏化流程图已集成 |
| 其他风格样例 | 13 北欧纸雕 | 多风格实验区 | 项目主题PNG、参考来源、用途说明 | 2/3 | pass | 1254×1254纸雕系统主视觉已集成 |
| 其他风格样例 | 15 大鼻软偶 | 多风格实验区 | 项目主题PNG、参考来源、用途说明 | 2/3 | pass | 1122×1402研究者角色IP已集成 |
| 样例说明 | 背景、意义、适合/不适合 | 多风格卡片 | DOM与MULTI-STYLE.md | 3/6 | pass | 4张均包含背景、适合、不适合、位置和风格参考声明 |
| 响应式与性能 | 1440/768/390及图片加载 | 全页 | 截图、scrollWidth、naturalWidth、alt | 7/8/9 | pass | 24/24页面图片完整滚动后加载，missingAlt=0，390px scrollWidth=375 |

### Revision 4 browser refinement ledger

```text
Current stage: 9 · Engineering and delivery closure
User phase: 继续以其他风格增加样例说明
Coverage item: 水墨、像素、纸雕、软偶项目主题新图、适用边界、三视口与图片加载
User goal: 理解同一研究内容在其他风格下如何改变意义和使用场景，而不是只看风格名称
Browser environment: agent-browser 0.27.0 / Chromium / 1440×1000, 768×1024, 390×844
Observed evidence: 多风格区语义树包含4个风格标题；桌面2×2、平板图片+说明双栏、手机单列；完整滚动后24/24图片加载，4张新图均有alt
Problem category: Use-case coverage / semantic comparison
Root cause: 既有连续案例证明了单一视觉系统的价值，但还没有展示受众与传播任务改变时为什么应该换风格
Minimal intervention: 保持核心内容不变，使用上游08/09/13/15样图作为纯风格参考分别生成文化隐喻、游戏化进度、编辑主视觉和角色IP，并明确适用/不适用场景
Adjacent regression surfaces: 六幕案例、三职责区、上游画廊、1440/768/390、图片懒加载和MULTI-STYLE.md链接
Observed result: 用户可以比较“同一主题、不同传播任务”；页面明确说明换风格是改变理解路径而非换皮
Decision: pass
Next executable action: none
New authority required: none
```

Revision 4 最终浏览器证据：

- `hand-drawn-styles-multi-style-desktop.png`
- `hand-drawn-styles-multi-style-desktop-2.png`
- `hand-drawn-styles-multi-style-tablet.png`
- `hand-drawn-styles-multi-style-mobile.png`

## Revision 5 · Multi-style scenario flows

### Scope revision

```text
Entry mode: Revision-led
Request revision: 5
User goal: 水墨、像素、纸雕、软偶不能再以单张图说明单项能力；每种都要有场景背景和前因→处理→结果的连续理解
Preserved evidence: 六幕主案例、三职责区、4种风格中间场景、上游画廊、五层原理、工作台和既有响应式验收
Reopened surfaces: 多风格实验区的信息架构、8张新增图片、图片性能、长页面阅读、三视口和Pages artifact
Flow model: 每种风格固定3幕——01问题/背景、02该风格如何处理、03适合该传播任务的最终结果
Existing middle frames: style-08-ink-archive.png、style-09-pixel-workflow.png、style-13-paper-system.png、style-15-vinyl-researcher.png
Required artifacts: 每种风格新增before/after各1张，共8张；MULTI-STYLE.md补4条三幕因果；页面改为4条流程而非4张单图卡
Autonomy authorization: 用户明确要求以场景或者流程串起来理解，而不是单个图片的能力展示
Observable completion: 4种风格各有3张一致图片和清楚背景；每幕说明原因、动作、结果；桌面横向三幕、手机纵向三幕；图片加载、alt、无溢出和发布路径通过
```

### Revision 5 coverage manifest

| 用户要求 | 要求/产物 | 界面/状态 | 所需证据 | 阶段 | 状态 | 下一步 |
| --- | --- | --- | --- | --- | --- | --- |
| 水墨流程 | 混乱→墨路归档→知识卷轴 | 08三幕流程 | 3张风格一致PNG与因果文本 | 2/3 | pass | 纸片风暴、墨石阶梯、知识庭院三幕完成 |
| 像素流程 | 初始任务→四站关卡→完成界面 | 09三幕流程 | 3张风格一致PNG与因果文本 | 2/3 | pass | 锁定起点、四站过程、全节点点亮三幕完成 |
| 纸雕流程 | 散乱纸材→中央系统→展览交付 | 13三幕流程 | 3张风格一致PNG与因果文本 | 2/3 | pass | 散乱材料、中央档案、三件展览系列三幕完成 |
| 软偶流程 | 无身份项目→研究助手→持续栏目 | 15三幕流程 | 3张风格一致PNG与因果文本 | 2/3 | pass | 灰色身份卡、研究助手、持续栏目角色三幕完成 |
| 流程化说明 | 每种背景、问题、处理、结果 | 4条流程 | DOM与MULTI-STYLE.md | 3/6 | pass | 单图卡已替换为4条横向/纵向三幕流程，并链接MULTI-STYLE-FLOWS.md |
| 响应式与性能 | 1440/768/390及32张图片 | 全页 | 截图、scrollWidth、naturalWidth、alt | 7/8/9 | pass | 完整滚动后32/32图片加载；4条流程/12幕；390px scrollWidth=375；alt完整 |

### Revision 5 browser refinement ledger

```text
Current stage: 9 · Engineering and delivery closure
User phase: 其他风格也必须以场景或流程串联
Coverage item: 水墨/像素/纸雕/软偶各三幕、8张新增图、因果文档、桌面/平板/手机与32张图片加载
User goal: 不通过单图猜测能力，而是沿场景看到为什么使用、怎样处理、最后得到什么
Browser environment: agent-browser 0.27.0 / Chromium / 1440×1000, 768×1024, 390×844
Observed evidence: 桌面每组3张横排并由箭头连接；平板仍保持三幕横向；手机恢复01→02→03纵向箭头；完整滚动后32张图片全部加载且无缺失alt
Problem category: Narrative continuity / process comprehension
Root cause: Revision 4虽然有背景和适用边界，但每种风格仍只有一张中间结果，不能呈现前因和结果变化
Minimal intervention: 保留4张既有项目图作为处理幕，分别生成before/after共8张；将2×2单图卡重构为4条独占整行的三幕流程；新增MULTI-STYLE-FLOWS.md归档因果与Prompt
Adjacent regression surfaces: 六幕主案例、三职责区、上游画廊、1440/768/390、32张图片懒加载和文档链接
Observed result: 每种风格现在都能按“问题→风格处理→适合的传播结果”阅读，用户不再需要从单图反推流程
Decision: pass
Next executable action: none
New authority required: none
```

Revision 5 最终浏览器证据：

- `hand-drawn-styles-style-flows-desktop.png`
- `hand-drawn-styles-style-flows-tablet.png`
- `hand-drawn-styles-style-flows-mobile.png`
- `hand-drawn-styles-style-flows-mobile-2.png`

## Revision 6 · Long-term usage playbook

### Scope revision

```text
Entry mode: Revision-led
Request revision: 6
User goal: 把“这个库适合哪些场景、怎样选择风格、如何形成资产”整理成长期笔记并接入网页，供后续项目直接照着使用
Preserved evidence: 六幕主案例、4条三幕风格流程、三职责区、上游能力、五层原理、工作台和既有浏览器验收
Reopened surfaces: 意义区之后的阅读路径、导航、工作台衔接、键盘与复制反馈、三视口、主索引入口与Pages artifact
Guide model: 是否应使用 → 选择交付场景 → 选择图片职责 → 路由画风 → 生成/验收/归档
Required artifacts: docs/usage-guide.md；网页Guide区；7类场景矩阵；适用/不适用边界；项目标准资产包；5步SOP；可复制请求模板和反馈
Autonomy authorization: 用户明确要求整理笔记并接入网页指导后期使用
Observable completion: 新用户能在页面回答“什么时候用、用在哪里、选什么风格、交付哪些资产、怎样请求Agent、怎样验收”；复制模板可用/失败有反馈；桌面/平板/390px、无脚本阅读和Pages路径通过
```

### Revision 6 coverage manifest

| 用户要求 | 要求/产物 | 界面/状态 | 所需证据 | 阶段 | 状态 | 下一步 |
| --- | --- | --- | --- | --- | --- | --- |
| 笔记整理 | 独立使用手册 | docs/usage-guide.md | 文件、目录与项目入口 | 3/9 | pass | 完整决策、场景、资产包、SOP、模板、验收和清单已归档 |
| 接入网页 | 使用指南主路径 | #usage-guide | DOM、导航与浏览器截图 | 3/4 | pass | 导航入口、决策门、场景矩阵、资产包、路由、SOP和模板区可达 |
| 后期指导 | 7类场景与风格路由 | 场景矩阵 | 项目/PPT/报告/教程/社媒/产品/品牌 | 3 | pass | 浏览器语义树确认7类交付场景和8条目标→风格路由 |
| 标准化 | 每项目视觉资产包 | 资产包区 | 资产数量、职责和文件建议 | 3 | pass | 默认7张+可选角色、职责和文件名完整呈现 |
| 可执行 | 5步流程和请求模板 | 模板区 | 复制成功/失败、键盘、无JS | 4/5/6 | pass | 5步SOP；复制受限时显示手动选择反馈；按钮3px焦点 |
| 响应式与交付 | 1440/768/390及Pages | 全页 | 截图、scrollWidth、链接、控制台 | 7/8/9 | pass | 三视口通过；390px scrollWidth=375；usage-guide.md HTTP 200；控制台无错误 |

### Revision 6 browser refinement ledger

```text
Current stage: 9 · Engineering and delivery closure
User phase: 把能力与应用场景整理成笔记并接入网页
Coverage item: 使用决策、7类场景、标准资产包、风格路由、5步SOP、请求模板、复制反馈、三视口和文档路径
User goal: 后续研究项目、PPT、报告和内容生产可以直接照指南使用，不依赖本次对话记忆
Browser environment: agent-browser 0.27.0 / Chromium / 1440×1000, 768×1024, 390×844
Observed evidence: #usage-guide语义树包含使用/禁用门、7个场景、资产包、路由、5步和模板；复制受限时aria-live提示手动选择；焦点轮廓3px；文档HTTP 200
Problem category: Operational guidance / knowledge retention
Root cause: 项目已有大量案例和风格实验，但“什么时候用、交付什么、怎样请求和验收”仍散落在对话和页面各处
Minimal intervention: 新增独立usage-guide.md并在意义区与工作台之间插入可执行指南；以决策门、7场景、资产包、路由、SOP和复制模板组成后期主路径
Adjacent regression surfaces: 导航、意义区、工作台、复制逻辑、主索引、1440/768/390、无脚本正文和Pages docs路径
Observed result: 页面从研究展厅升级为研究+应用手册；新用户可从使用判断直接走到标准请求和工作台
Decision: pass
Next executable action: none
New authority required: none
```

Revision 6 最终浏览器证据：

- `hand-drawn-styles-usage-guide-viewport.png`
- `hand-drawn-styles-usage-guide-tablet.png`
- `hand-drawn-styles-usage-guide-mobile.png`
