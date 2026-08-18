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
