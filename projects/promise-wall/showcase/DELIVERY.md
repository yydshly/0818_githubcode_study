# Promise Wall 研究展厅交付记录

## Design contract

```text
Entry mode: brief-led implementation
Request revision: 1
Target user and context: 在 GitHub Code Study 中评估 Three.js 项目、寻找可复用交互模式的中文读者
Desired first impression: 先看到可操作的真实 3D 承诺墙，再快速理解它的技术层、能力边界与迁移方向
Visual ambition: Immersive
Experience architecture: Hybrid Workspace
Visual constraints: 延续上游暖纸张与石墙质感；研究说明保持高对比、可扫描；不用装饰性 3D 替代真实上游运行证据
Information constraints: 明确区分“上游已实现”“界面模拟”“本研究建议扩展”；所有核心结论关联固定源码行或文件
Operation constraints: 原版体验可在页面内运行并可单独打开；研究导航、能力切换和场景卡键盘可达
State constraints: 覆盖上游加载、可运行、网络/CDN 不可用提示；研究页无脚本时仍能阅读全部结论
Environment constraints: 纯静态 GitHub Pages；不引入后端、账号、数据库或真实社区数据；上游保持未修改子模块
Primary journey: 浏览研究结论 -> 操作真实上游 Demo -> 查看内部能力层 -> 理解使用与扩展场景 -> 进入源码/文档
User-defined phases: 获取项目；展示内部样例/原始样例；说明能力；说明使用场景；说明可扩展场景；接入研究主页
Required artifacts: 固定上游子模块、项目 README、能力分析、扩展场景文档、可运行展厅、自动验证、主页与 Pages 接线
Autonomy authorization: 用户已明确要求作为下一个研究子项目直接实施
User-decision boundary: 推送、合并、发布及改变上游代码需要新授权
Observable completion criteria: 固定 commit 可验证；原版 iframe/独立入口可运行；三类能力边界可见；至少 6 类使用场景和 6 类扩展方向可读；桌面/平板/390px 无横向溢出；键盘与 reduced-motion 可用；Pages 产物包含所需文件
Coverage record: 下表
```

### Hybrid Workspace architecture

```text
Scene base: 同源 iframe 中运行的上游 Three.js/WebGL 页面
Scene persistence: 在首个“真实样例”工作台内持续可见；进入深度文档后允许让位给正常阅读流
Foreground control model: 顶部研究导航、Demo 独立打开/重载、能力层切换、场景矩阵
State-to-scene mapping: 加载提示 -> 原版运行；CDN 失败时由上游提示网络依赖，父页面仍保留完整文字证据
Mobile transformation: Demo 舞台缩为定高全宽窗口，研究控制与说明转为单列，不隐藏核心入口
Fallback: 所有能力、边界、场景和源码证据均为语义 HTML；WebGL 失败不影响研究结论阅读
```

## Coverage manifest

| 用户要求 | 页面／状态 | 证据 | 阶段 | 状态 | 下一步 |
| --- | --- | --- | --- | --- | --- |
| 固定并获取上游 | `upstream` 子模块 | commit 与未修改状态 | 0–1 | pass | 无 |
| 展示内部与原始样例 | 真实 Demo 工作台 | iframe 运行、独立入口、加载状态 | 1–5 | pass | 无 |
| 说明真实能力 | 能力地图与源码证据 | 渲染、材质、交互、产品层、边界 | 2–6 | pass | 无 |
| 说明使用场景 | 场景路由 | 至少 6 个具体场景及适配理由 | 3 | pass | 无 |
| 说明可扩展场景 | 扩展路线 | 至少 6 条路线并标注工程代价 | 3 | pass | 无 |
| 研究主页入口 | 根 README、站点首页、Pages | 路径和文案自动检查 | 3、9 | pass | 无 |
| 桌面视觉与主旅程 | 1440px / 默认状态 | 截图、交互、无溢出、无错误 | 2–6 | pass | 无 |
| 平板与手机 | 768px、390px | 截图、无横向溢出、控制可达 | 7 | pass | 无 |
| 键盘与前景层 | Tab、Enter、Escape、iframe 入口 | 焦点可见、状态可操作 | 7 | pass | 无 |
| 动效与能力降级 | reduced-motion、WebGL/CDN 边界 | CSS/运行观察及文本 fallback | 8 | pass | 无 |
| 工程交付 | 静态资源、链接、脚本、上游 pin | 自动测试与 `git diff --check` | 9 | pass | 无 |

## Selected WebGL research route

```text
Selected pattern: Research + production-hardened static showcase
Evidence branch: upstream source -> unchanged live runtime -> bounded capability map -> extension scenarios
Required inputs: pinned upstream commit, root index.html, runtime browser, existing Pages conventions
Expected output: an evidence-led Chinese research workspace with the original demo embedded as proof
What should update the skill: no reusable skill update unless runtime evidence yields a new general conclusion
```

## Refinement ledger

```text
Current stage: 9 / Engineering and delivery closure
User phase: 获取、展示样例、解释能力、使用场景与可扩展场景
Coverage item: 固定上游、真实 WebGL 舞台、五层能力、八类使用场景、八条扩展路线、主页与 Pages
User goal: 将 Promise Wall 作为下一个可运行、可解释、可扩展的研究子项目
Browser environment: agent-browser 0.27.0；Python http.server；2026-08-19
Canonical command: python -m http.server 8895 --bind 127.0.0.1
Canonical URL: http://127.0.0.1:8895/projects/promise-wall/showcase/
Observed evidence: 页面正文 3169 字符；无错误覆盖层；console/errors 为空；横向溢出 0；五个能力标签、八个使用场景和八个扩展场景存在
WebGL evidence: iframe 同源；THREE 与 gsap 均已加载；canvas 为 1238×720；上游 loader.done；固定原版正文可读
Interaction evidence: 键盘聚焦 interaction 标签后按 Enter，aria-selected=true，标题切换为“指针先进入射线，再回到墙面。”，focus outline=solid
Responsive evidence: 1440×1000、768×1024、390×844 均无横向溢出；手机为单列，Demo 高 560px，iframe 内 THREE 仍存在
Motion evidence: parent 与 iframe 的 reduced-motion 均为 true；scroll-behavior=auto；CSS transition=0.001ms
Fallback evidence: 在隔离会话移除 WebGL iframe 后，父页面仍保留 3169 字符、五个能力控制、八个使用场景和八个扩展场景
Pages evidence: 按工作流目录组装的临时站点有四张项目卡；旧项目图片均加载；Promise Wall 路由、原版 iframe 和 Three.js 均通过
Problem category: 首版桌面标题因 7.4rem 字号在中文行内产生非预期换行
Root cause: 英文式超大标题尺寸没有匹配左栏的中文字符宽度
Minimal intervention: 将标题上限降至 5.5rem，并保留两行明确断点
Adjacent regression surfaces: 平板、390px、右侧结构示意、事实栏、Live Demo、总入口卡片
Observed result: 桌面标题稳定为两行；其余视口和交互证据全部通过
Decision: pass
Next executable action: 无
New authority required: 推送、合并或发布需要用户另行授权
```

## Final evidence

- `promise-wall-desktop.png`：1440px 首屏；
- `promise-wall-live-demo.png`：原版 Three.js 工作台运行状态；
- `promise-wall-tablet.png`：768px 平板布局；
- `promise-wall-mobile.png`：390px 手机首屏；
- `promise-wall-mobile-live.png`：390px 原版 Demo 与底部详情层。

截图保存在当前任务的外部可视化目录，没有加入产品仓库。

## Terminal audit

- 上游固定在 `0cb1b20c3952e4c4184b7e0e33fe5acfac2b4447` 且没有修改；
- 上游 `npm run build` 通过，产物为 116.13 kB，gzip 25.25 kB；
- `tests/verify_project.py` 与 `git diff --check` 通过；
- 研究页、原版运行页、主页和 Pages 结构均有真实浏览器证据；
- coverage manifest 没有 `continue`、`defer` 或 `blocked`；
- 当前范围完成，未执行推送、合并或发布。

## Revision 2 · 场景体验扩展

### Revised design contract

```text
Entry mode: revision-led implementation
Request revision: 2
Target user and context: 不关心底层技术、希望快速感知产品效果和适用场景的活动策划者、内容负责人和普通体验者
Desired first impression: 这不只是一面便签墙，而是一组可直接体验的情绪空间产品方向
Visual ambition: Immersive
Experience architecture: Hybrid Workspace
Visual constraints: 保留暖纸张语言；六个场景必须有明显不同的环境、材料、光线和反馈隐喻；ImageGen 只做气氛资产，不能代替真实交互
Information constraints: 使用场景先于工程路线；每个场景回答“谁来、写什么、墙发生什么、记住什么”；不把初步效果写成完整产品
Operation constraints: 六场景可按顺序点击、键盘激活、上一幕/下一幕和自动播放；12 个使用场景可一键路由到对应效果
State constraints: 覆盖六个稳定场景、自动播放/暂停、循环结束、reduced-motion、无脚本阅读和图片不可用
Environment constraints: 继续保持纯静态 Pages；不增加后端、账号、上传或真实社区数据
Primary journey: 浏览 12 类使用场景 -> 选择一个场景 -> 在同一舞台观看初步效果 -> 顺序体验六种方向 -> 理解对应用户体感
User-defined phases: 第一，把可扩展使用场景落地到 Web；第二，按场景依次做初步效果展示；补充，使用 ImageGen 提升产品感和用户体感
Required artifacts: ImageGen 气氛总览资产、12 场景路由、六场景舞台、顺序播放控制、文档和验证更新
Autonomy authorization: 用户已明确要求直接加入 Web 并按场景扩展
User-decision boundary: 真实品牌、真实用户内容、公开活动运营和后端能力需要新授权
Observable completion criteria: 页面存在 12 个场景入口和六个可辨识状态；场景卡可改变舞台；上一幕/下一幕/自动播放可用；ImageGen 资产加载；1440/768/390 无溢出；键盘和 reduced-motion 可用；原版 Demo 与既有研究内容不回归
```

### Revision 2 coverage manifest

| 用户要求 | 页面／状态 | 所需证据 | 阶段 | 状态 | 下一步 |
| --- | --- | --- | --- | --- | --- |
| 可扩展使用场景进入 Web | 12 个场景路由卡 | DOM 数量、内容、路由目标 | 3–5 | pass | 无 |
| 场景依次展示 | 六幕体验舞台 | 六状态、上一幕/下一幕、进度 | 4–6 | pass | 无 |
| 提升产品感 | ImageGen 气氛总览 | 项目内资产、来源说明、加载结果 | 2–3 | pass | 无 |
| 用户体感可理解 | 每幕体验说明 | 谁来、写什么、变化、记忆点 | 3–6 | pass | 无 |
| 自动播放 | 播放/暂停/结束 | 浏览器状态转换与控制文本 | 5–6 | pass | 无 |
| 桌面、平板、手机 | 1440/768/390 | 截图、无溢出、控制可达 | 7 | pass | 无 |
| 键盘与降动效 | Enter、焦点、reduced-motion | 真实键盘和媒体偏好观察 | 7–8 | pass | 无 |
| 无图／无脚本阅读 | fallback | 语义内容仍存在、舞台说明可读 | 8 | pass | 无 |
| 工程与回归 | 原版 iframe、测试、Pages | 自动验证、原版运行、diff check | 9 | pass | 无 |

### Revision 2 WebGL route

```text
Selected pattern: product-case scene anthology inside the existing hybrid research workspace
Evidence branch: scenario definition -> generated atmosphere asset -> interactive scene prototype -> bounded user-experience conclusion
Required inputs: existing warm paper system, six effect directions, twelve concrete use cases, static browser runtime
Expected output: one coherent six-scene experience lab rather than six disconnected decorative cards
What should update the skill: no skill update; conclusions remain project-specific until user testing exists
```

### Revision 2 refinement ledger

```text
Current stage: 9 / Engineering and delivery closure
User phase: 可扩展使用场景落地、六场景依次展示、ImageGen 产品体感增强
Coverage item: 12 个使用入口、6 幕舞台、顺序播放、语义效果语言、ImageGen 总览与根入口封面
User goal: 先不关注技术，把效果和真实使用场景做成可以感知的网页产品草案
Browser environment: agent-browser 0.27.0；Python http.server；2026-08-19
Canonical command: python -m http.server 8897 --bind 127.0.0.1
Canonical URL: http://127.0.0.1:8897/projects/promise-wall/showcase/
Baseline evidence: 正文 3169 字符；8 个文字使用场景；无 scene-lab；扩展区以工程量为中心；原版 iframe 正常
Implementation evidence: 正文 4052 字符；12 个 data-route-scene；6 个 canonical scene tab；ImageGen 图片 naturalWidth=1672；默认 capsule；原版 iframe 继续完成加载
Sequence evidence: 下一幕依次得到 capsule、garden、starlight、memory、anonymous、gratitude；标题、01–06 计数和 aria-selected 均同步
Routing evidence: 第 7 张“匿名心声墙”卡路由后，scene=anonymous、背景 rgb(63,69,111)、第 5 个标签选中、scene-lab top=80
Playback evidence: 从 anonymous 播放完整其余五幕后停在 memory；aria-pressed=false；按钮恢复“播放六幕”
Keyboard evidence: memory 标签聚焦后按 ArrowRight，切换到 anonymous，焦点跟随、aria-selected=true、outline=solid
Responsive evidence: 1440、768、390 横向溢出均为 0；平板舞台单列、说明双栏、标签三列；手机舞台 470px、说明可见、标签两列、使用场景单列
Motion evidence: reduced-motion 下按钮 disabled，文案“降动效：手动切换”，手动 gratitude 仍可用，transition=0.001ms
Fallback evidence: 精确拦截 app.js 后 js class=false，但 4052 字符、12 个场景入口、6 个标签、时间胶囊初始舞台和 ImageGen 图片仍可阅读，溢出 0
Pages evidence: 真实 Pages 目录结构下三张项目封面全部加载；新封面 naturalWidth=1672；展厅链接正确；桌面和 390px 无溢出
Problem category: Root index asset ratio / reduced-motion state feedback
Root cause: 横向 ImageGen 资产继承旧竖版封面 height 属性；手动切换场景时 stopScenePlayback 覆盖了降动效文案
Minimal intervention: 为 promise-scene-cover 设置更高特异性的 16:9 + height:auto；播放复位文案按 media query 状态选择
Adjacent regression surfaces: 原版 Demo、既有能力切换、根入口旧项目封面、桌面/平板/手机、无脚本阅读
Observed result: 根封面从 400×985 修正为 393×256，卡片高度从 1147 降至 675；降动效按钮和手动切换状态一致；全部验收通过
Decision: pass
Next executable action: 无
New authority required: 提交、推送或合并本轮改动需要用户授权
```

### Revision 2 final evidence

- `promise-scenes-desktop-atlas.png`：ImageGen 六场景气氛总览与舞台入口；
- `promise-scenes-capsule.png`：时间胶囊第一幕；
- `promise-scenes-anonymous.png`：匿名心声第五幕；
- `promise-scenes-tablet.png`：768px 场景舞台与说明；
- `promise-scenes-mobile.png`：390px 控制、舞台和说明；
- `promise-scenes-root-card.png`：Pages 研究主页的新横向场景封面。

截图保存在当前任务外部可视化目录，没有加入产品仓库。ImageGen 最终项目资产和完整提示词保存在 `assets/generated/`。

### Revision 2 terminal audit

- coverage manifest 没有 `continue`、`defer` 或 `blocked`；
- 六个效果状态、十二个使用入口、自动播放、键盘与 reduced-motion 均有真实浏览器证据；
- ImageGen 资产、提示词、使用边界和本地交互均已落地；
- 原版 iframe、既有研究内容、根入口和 Pages 路由未回归；
- 本轮没有实现后端、上传、账号或真实活动运营，也未修改上游源码。

## Revision 3 · 十二场景独立效果

### Revised design contract

```text
Entry mode: revision-led implementation
Request revision: 3
Target user and context: 希望逐一判断十二类实际活动是否有明确产品效果的策划者、内容负责人和体验设计者
Desired first impression: 每个场景都不是换一句文案，而是拥有自己的空间身份、材料、反馈和记忆时刻
Visual ambition: Immersive
Experience architecture: Hybrid Workspace
Visual constraints: 延续同一纸张世界，但新年、毕业、婚礼、企业、感谢、公益、匿名、家庭、旅行、品牌、城市、游戏必须一眼可辨；避免十二个完全割裂的风格 Demo
Information constraints: 严格覆盖用户给出的“用户写什么”和“最适合的效果”；每幕继续说明谁来、写什么、墙的变化和记忆点
Operation constraints: 12 个使用场景一对一路由；12 个标签按给定顺序；上一幕/下一幕/自动播放/方向键覆盖完整十二幕
State constraints: 覆盖 12 个稳定状态、12 步计数、播放结束复位、reduced-motion 和无脚本初始状态
Environment constraints: 纯静态 Pages；复用现有 ImageGen 六区气氛图作为总览，不新增真实照片、上传、品牌或后端
Primary journey: 从具体使用场景进入 -> 看到该场景独立第一版效果 -> 查看用户体感说明 -> 继续下一幕 -> 完整浏览十二幕
User-defined phases: 为表格中的 12 个场景分别展示第一版效果
Required artifacts: 12 场景导演数据、12 个视觉状态、12 标签与计数、文档和自动验证更新
Autonomy authorization: 用户明确要求继续落地全部十二个场景
User-decision boundary: 真实客户品牌、人物照片、活动内容和上线运营需要新授权
Observable completion criteria: 12 个入口一对一映射 12 个 canonical scene；每幕标题/计数/内容/颜色/视觉元素不同；12 幕自动播放结束复位；1440/768/390 无溢出；键盘和 reduced-motion 可用；原版 Demo 与无脚本阅读不回归
```

### Revision 3 coverage manifest

| 用户场景 | 独立效果 | 所需证据 | 阶段 | 状态 | 下一步 |
| --- | --- | --- | --- | --- | --- |
| 新年愿望墙 | 时间胶囊、倒计时、跨年开启 | newyear 状态与视觉 | 3–6 | pass | 无 |
| 毕业留言墙 | 校园墙、照片卡、班级分区 | graduation 状态与视觉 | 3–6 | pass | 无 |
| 婚礼祝福墙 | 信封、花瓣、暖光、周年开启 | wedding 状态与视觉 | 3–6 | pass | 无 |
| 企业目标墙 | 部门分区、完成印章、成长植物 | goals 状态与视觉 | 3–6 | pass | 无 |
| 员工感谢墙 | 金线、人物聚合、月度回顾 | recognition 状态与视觉 | 3–6 | pass | 无 |
| 公益承诺墙 | 成长花园、行动计数、群体图案 | publicgood 状态与视觉 | 3–6 | pass | 无 |
| 匿名心声墙 | 安静展开、温和回应、隐私模式 | anonymous 状态与视觉 | 3–6 | pass | 无 |
| 家庭记忆墙 | 旧纸、相框、年代分区、语音 | family 状态与视觉 | 3–6 | pass | 无 |
| 旅行记忆墙 | 明信片、地图区域、路线连接 | travel 状态与视觉 | 3–6 | pass | 无 |
| 品牌故事墙 | 品牌空间、自动导览、活动大屏 | brand 状态与视觉 | 3–6 | pass | 无 |
| 城市故事墙 | 街区分区、年代层、公共展览 | city 状态与视觉 | 3–6 | pass | 无 |
| 游戏线索墙 | 连线、隐藏信息、阶段解锁 | game 状态与视觉 | 3–6 | pass | 无 |
| 完整体验 | 12 路由、12 标签、自动播放、键盘 | 状态序列与浏览器证据 | 5–8 | pass | 无 |
| 工程回归 | 文档、测试、Pages、原版 iframe | 自动检查与无脚本证据 | 9 | pass | 无 |

### Revision 3 route

```text
Selected pattern: twelve-scene product-case anthology with one persistent stage
Evidence branch: user scenario contract -> distinct scene state -> browser-observed visual identity -> bounded first-version conclusion
Required inputs: the user's twelve-row table, existing six-scene director, shared paper-wall visual system
Expected output: twelve recognizable but coherent first-version scenes, not twelve full products
What should update the skill: no reusable skill update; user testing is still absent
```

### Revision 3 refinement ledger

```text
Current stage: 9 / Engineering and delivery closure
User phase: 为十二个具体场景分别提供第一版效果
Coverage item: 12 个一对一路由、12 个独立舞台状态、12 步导演、自动播放、键盘与跨端
User goal: 每个表格场景都能直接看到匹配“写什么”和“最适合效果”的第一版体验
Browser environment: agent-browser 0.27.0；Python http.server；2026-08-19
Canonical command: python -m http.server 8899 --bind 127.0.0.1
Canonical URL: http://127.0.0.1:8899/projects/promise-wall/showcase/
Baseline evidence: Revision 2 已有 12 个使用入口，但只映射到 6 个 canonical scene；六幕舞台、播放和跨端均通过
Implementation evidence: routes=12、tabs=12、默认 newyear、title=新年愿望墙、counter=01/12；原版 iframe 继续完成加载
Sequence evidence: 真实“下一幕”依次得到 newyear、graduation、wedding、goals、recognition、publicgood、anonymous、family、travel、brand、city、game；标题、01–12 计数、唯一颜色和 aria-selected 0–11 同步
Scene evidence: 毕业场景显示 CLASS OF 2026、照片卡与班级区域；婚礼显示花瓣、信封胶带与周年开启；旅行显示明信片、虚线路线和地图节点；游戏显示红线、模糊隐藏卡与阶段锁
Playback evidence: 从 game 播放完整其余十一幕后停在 city；aria-pressed=false；按钮恢复“播放十二幕”
Keyboard evidence: city 聚焦后按 ArrowRight，切到 game，焦点跟随、aria-selected=true、outline=solid
Responsive evidence: 1440 无溢出且标签 4 列×3 行；768 无溢出、舞台单列、说明双栏、标签 3 列×4 行；390 无溢出、舞台 470px、标签 2 列×6 行、使用场景单列
Motion evidence: reduced-motion 下自动播放 disabled、文案“降动效：手动切换”，手动 recognition 仍可用，transition=0.001ms
Fallback evidence: 精确拦截 app.js 后 js class=false，但 4153 字符、12 个路由、12 个标签、newyear 初始舞台仍可阅读，溢出 0
Regression evidence: ImageGen 气氛图延迟加载后可见；原版 iframe、五层能力、使用场景、效果语言和 Pages 资源路径未回归；console/errors 为空
Problem category: State specificity / navigation density
Root cause: 六个通用状态不能满足十二个场景的一对一效果；六列标签扩展到十二项后会过密
Minimal intervention: 将导演数据和 data-scene 扩为十二个 canonical key；共享纸张舞台但为每幕增加独立材料和效果；标签改为桌面 4×3、平板 3×4、手机 2×6
Adjacent regression surfaces: 自动播放、键盘焦点、reduced-motion、无脚本阅读、原版 iframe、桌面/平板/手机
Observed result: 十二个场景均可一对一直达并依次播放，重点场景视觉明显可辨，所有验收通过
Decision: pass
Next executable action: 无
New authority required: 提交、推送或更新 Draft PR 需要用户授权
```

### Revision 3 final evidence

- `promise-12-newyear.png`：新年倒计时和统一开启；
- `promise-12-graduation.png`：校园墙、照片卡和班级分区；
- `promise-12-wedding.png`：花瓣、祝福信封和周年开启；
- `promise-12-travel.png`：明信片、地图节点和路线连接；
- `promise-12-game.png`：红线证据、隐藏信息和阶段锁；
- `promise-12-mobile-game.png`：390px 手机游戏线索舞台。

截图保存在当前任务外部可视化目录，没有加入产品仓库。

### Revision 3 terminal audit

- 十二个用户场景全部有独立 canonical scene、内容、颜色、材料、状态反馈和记忆点；
- 自动播放、上一幕/下一幕、12 标签、方向键、reduced-motion 和无脚本层均通过；
- 桌面、平板、手机无横向溢出；
- 自动检查、JavaScript 语法、资源、原版上游和 Pages 接线通过；
- 当前交付仍是第一版效果，不声明真实照片、语音播放、隐私系统、活动大屏或阶段解锁业务已经实现。

## Revision 4 · 后期动作与研究归档

### Revised design contract

```text
Entry mode: revision-led implementation and publication
Request revision: 4
Target user and context: 未来重新打开研究时需要快速理解“还可以做什么、为什么做、什么时候做”的维护者与产品负责人
Desired first impression: 当前研究已经完整收口，同时保留一张清晰、可执行但不冒充承诺的未来动作地图
Visual ambition: Editorial
Experience architecture: Editorial Flow appended to the existing Hybrid Workspace
Visual constraints: 归档章节保持现有暖纸张语言，以行动卡和明确状态区分已完成、未实现和重新启动条件；不再增加新的场景特效
Information constraints: 描述用户动作、场景范围、体感、可带走结果与重新启动条件；避免技术路线和实现承诺
Operation constraints: 后期动作可从顶部导航直达；桌面、平板、手机可扫描；无脚本仍完整可读
State constraints: 项目状态统一为“已完成 · 已归档”；明确当前停止项和恢复研究的触发条件
Environment constraints: 不新增后端、第三方服务、真实运营或新资产；保留现有十二场景及原版 Demo
Primary journey: 完成十二场景浏览 -> 查看后期动作 -> 理解当前收口边界 -> 未来按触发条件恢复研究
User-defined phases: 把后期可扩展动作加入网页；提交到远端；归档该子项目
Required artifacts: Web 后期动作章节、归档说明、README/主页状态、测试更新、提交、推送和 PR 更新
Autonomy authorization: 用户明确授权修改、提交和推送到远端
User-decision boundary: 合并 PR、部署 main 和恢复后续研究需要新授权
Observable completion criteria: Web 至少呈现 7 类后期动作及用户体感/结果/触发条件；归档状态在项目 README、根 README、研究主页和展厅一致；1440/768/390 无溢出；测试通过；远端分支和 Draft PR 更新
```

### Revision 4 coverage manifest

| 用户要求 | 产物／状态 | 所需证据 | 阶段 | 状态 | 下一步 |
| --- | --- | --- | --- | --- | --- |
| 后期动作加入 Web | 七类行动地图 | 内容、DOM、导航、视觉 | 3–6 | pass | 无 |
| 描述使用价值 | 动作/场景/体感/结果 | 每张行动卡四字段 | 3 | pass | 无 |
| 明确重新启动条件 | 归档决策区 | 已完成/停止/触发条件 | 6 | pass | 无 |
| 项目归档 | README、根索引、主页、展厅 | “已完成 · 已归档”一致 | 3、9 | pass | 无 |
| 桌面/平板/手机 | 1440/768/390 | 截图、DOM、无溢出 | 7 | pass | 无 |
| 无脚本与既有体验 | fallback、12 scenes、原版 iframe | 内容和回归证据 | 8 | pass | 无 |
| 自动验证 | 文档、页面、状态、资源 | 测试与 diff check | 9 | pass | 无 |
| 远端提交 | commit、push、PR #5 | SHA、远端分支、PR 状态 | 9 | pass | 无 |

### Revision 4 route

```text
Selected pattern: archived product-case research with explicit reopen triggers
Evidence branch: completed prototype evidence -> bounded future actions -> visible archive decision -> remote publication
Required inputs: current twelve-scene showcase, prior expansion recommendations, existing Draft PR #5
Expected output: a closed research artifact that remains useful without implying ongoing development
What should update the skill: nothing; this is project-specific archival guidance
```

### Revision 4 refinement ledger

```text
Current stage: 9 / Engineering and delivery closure
User phase: 后期动作入 Web、远端提交、子项目归档
Coverage item: 七类后期行动、三段归档边界、全局状态、跨端与无脚本、远端 PR
User goal: 当前研究正式收口，同时让未来恢复时有清晰可执行的动作入口
Browser environment: agent-browser 0.27.0；Python http.server；2026-08-19
Canonical command: python -m http.server 8901 --bind 127.0.0.1
Canonical URL: http://127.0.0.1:8901/projects/promise-wall/showcase/
Observed evidence: 正文 5570 字符；7 个 data-future-action；archive pill“已完成 · 已归档”；归档状态“当前决定：完成研究，停止继续扩展。”；3 个边界卡；12 scenes；原版 iframe 完成加载；无错误覆盖层
Content evidence: 每张行动卡均包含适用场景、用户体感、结果和重启条件；行动覆盖互动闭环、时间、集体反馈、成果、现场、个人空间和生命周期
Desktop evidence: 1440 无溢出；行动卡双栏；状态栏三段；标题、归档决定和首两张行动卡在同一阅读视图内
Tablet evidence: 768 无溢出；行动卡双栏 346.5px；状态栏 150px + 467px；宽卡跨两列；归档边界转为单列
Mobile evidence: 390 无溢出；行动卡、状态栏、归档边界均为单列；归档决定和 Action 01 在首个归档阅读视图中可见
Fallback evidence: 拦截 app.js 后 js class=false，但 5570 字符、7 个行动、归档状态、3 个边界卡和 12 scenes 仍可读，溢出 0
Regression evidence: console/errors 为空；十二场景、原版 iframe、ImageGen 资产、效果语言和既有导航未回归
Problem category: Archive information architecture
Root cause: 先前未来方向散落在文档和对话中，网页没有说明当前停止范围与恢复研究的具体条件
Minimal intervention: 在体验曲线与总结之间增加正式行动地图、归档状态和 completed/stopped/reopen 三段边界；同步四个公开状态入口
Adjacent regression surfaces: 顶部导航、十二场景、原版 iframe、README、根索引、研究主页、桌面/平板/手机
Observed result: 未来方向可扫描、归档边界一致、既有体验保持正常，全部验收通过
Decision: pass
Next executable action: 无；项目按用户决定归档
New authority required: 未来恢复研究或合并 PR 需要新的用户指令
```

### Revision 4 final evidence

- `promise-archive-actions-desktop.png`：桌面后期行动地图与归档决定；
- `promise-archive-actions-mobile.png`：390px 单列归档阅读流。

截图保存在当前任务外部可视化目录，没有加入产品仓库。

### Revision 4 terminal audit

- 七类后期行动和重启条件已经进入 Web；
- 项目 README、根 README、研究主页和展厅统一标记“已完成 · 已归档”；
- 1440、768、390 与无脚本阅读通过；
- 十二场景、原版 Demo、ImageGen 资产和测试合同未回归；
- 当前研究正式收口，未来仅按页面列出的真实触发条件重新启动；
- 本轮归档提交已推送至 `codex/promise-wall-research`，Draft PR #5 已更新。
