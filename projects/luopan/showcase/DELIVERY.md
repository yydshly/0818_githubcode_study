# Luopan Study Showcase · Delivery Record

## Design contract

```text
Entry mode: Brief-led
Request revision: 2
Target user and context: 主仓库维护者，以及从 GitHub README 进入、希望快速理解 luopan 的访客
Desired first impression: 先看到 Luopan 真实生成过的行业、投资和求职报告，再清楚理解它的数据、原理和决策逻辑；仓库审计只是附录
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: 中文优先；强信息层级；纸张/墨色/信号色语义；不依赖外部字体、图片或 UI 框架；390px–1440px 可读
Information constraints: 原版产物、路由原理、数据血缘、三套判断引擎、关联场景实战、本地扩展和仓库审计必须明确分层；保留来源、版本和 MIT 署名
Operation constraints: 纯静态 HTML/CSS/JavaScript；无后端、登录、金融 API 或构建依赖；允许本地 HTTP 与未来静态托管
State constraints: 主导航与判断引擎标签切换；报告链接可达；键盘可达；禁用 JavaScript 时核心内容仍可阅读
Environment constraints: Python 3 本地静态服务器；单一浅色主题；支持 prefers-reduced-motion
Primary journey: 进入页面 → 打开原版报告 → 理解路由与数据来源 → 切换行业/投资/求职判断引擎 → 查看 AI 编程 Agent 实战 → 理解 GitHub 项目研究扩展 → 按需进入技术审计附录
User-defined phases: 展示原版能力；解释原理/数据来源/判断决策；运行关联场景；扩展并关联主项目背景
Required artifacts: 上游源码引用、研究文档、扩展 Skill、可运行展厅、浏览器验收记录、最终截图
Autonomy authorization: 用户要求获取、分析、展示并扩展；范围内可逆实现直接执行
User-decision boundary: 对外部署、创建独立仓库、投资建议或修改上游仓库需要另行授权
Observable completion criteria: 页面可运行且无控制台错误；桌面/平板/390px 无遮挡；六份上游报告入口有效；三套判断引擎可切换；数据等级和外部依赖清晰；AI 编程 Agent 实战与扩展可进入；键盘焦点可见；reduced-motion 有降级；技术审计作为附录可达
Coverage record: 见下表
```

## Coverage manifest

| 用户阶段 | 要求/产物 | 界面/状态 | 所需证据 | 阶段 | 状态 | 下一步 |
| --- | --- | --- | --- | --- | --- | --- |
| 获取上游 | 固定来源与 commit | Git submodule | `.gitmodules`、gitlink、版本号 | 1 | pass | 已固定 `499eb43` |
| 分析 | 能力、原理、作用与边界 | 研究文档 | 文件、源码和测试证据 | 0/9 | pass | JSON、Markdown、HTML 一致 |
| 展示已有能力 | 30 秒结论与原生能力 | 桌面默认态 | 1440px 浏览器截图 | 2/3 | pass | 目视层级通过 |
| 展示已有能力 | 原生能力筛选与报告示例 | 默认态、筛选态 | 点击与 DOM 观察 | 4/5/6 | pass | 外部依赖筛选显示 1 项 |
| 扩展 | GitHub 项目研究模式 | 扩展视角 | 切换前后浏览器观察 | 4/5 | pass | 扩展视角显示且上游专属段落隐藏 |
| 关联主项目 | 从研究到主索引的闭环 | 扩展视角 | 页面内容与根 README 链接 | 3/9 | pass | 两级 README 已更新 |
| 响应式 | 保持完整阅读与操作路径 | 1440/768/390px | 三种视口截图 | 7 | pass | 三个视口无横向溢出 |
| 可访问性 | 键盘、焦点、语义与 reduced-motion | 键盘/媒体偏好 | 浏览器操作与样式检查 | 7/8 | pass | 3px 焦点；动效与无 JS 降级通过 |
| 工程质量 | 静态资源、链接与脚本有效 | 本地 HTTP | HTTP、控制台、自动检查 | 9 | pass | 页面与本地证据均 200；无浏览器错误 |
| 交付 | 保留最小最终证据 | 最终状态 | 截图、验收记录 | 9 | pass | 最终截图与 JSON 证据已保留 |

## Canonical runtime

从主仓库根目录运行：

```shell
python -m http.server 4173 --bind 127.0.0.1 --directory projects/luopan
```

- URL：`http://127.0.0.1:4173/showcase/`
- 验收时间：`2026-08-18T08:20:56.573Z`（Revision 2）
- 支持边界：单一浅色主题；纯静态、无后端；JavaScript 关闭时内容可读但筛选不可用。

## Browser refinement ledger

### Final visual and interaction pass

```text
Current stage: 9 · Engineering and delivery closure
User phase: 展示已有能力 + 扩展
Coverage item: 桌面/平板/手机、筛选、视角、键盘、reduced-motion、无 JavaScript
Browser environment: Headless Chromium / 1440×1000, 768×1024, 390×844
Observed evidence: 三个视口 HTTP 200；9 项能力、5 层原理、4 个扩展；无溢出、错误层或控制台错误；本地扫描链接 200
Problem category: Canonical runtime（首轮服务根目录过窄）
Root cause: 首轮只服务 showcase/，导致 ../research 证据链接无法访问
Minimal intervention: 服务 projects/luopan，并将规范入口设为 /showcase/
Adjacent regression surfaces: 三个视口、筛选、视角切换、键盘焦点、reduced-motion、无 JS、本地证据链接
Observed result: 全部通过；首个焦点 3px；reduced-motion 生效；无 JS 保留 9 项能力与 4 项扩展
Decision: pass
Next executable action: none
New authority required: none
```

最终证据保存在工作区外的会话可视化目录：

- `luopan-showcase-desktop-v2.png`
- `luopan-showcase-tablet-v2.png`
- `luopan-showcase-mobile-v2.png`
- `luopan-showcase-browser-evidence-v2.json`

## Revision 2 coverage manifest

| 用户阶段 | 要求/产物 | 界面/状态 | 所需证据 | 阶段 | 状态 | 下一步 |
| --- | --- | --- | --- | --- | --- | --- |
| 展示原版能力 | 3 份行业 + 3 份公司报告 | 原版能力区 | 六个报告链接与浏览器打开 | 3/5 | pass | 六个链接 200；AI 行业报告新标签打开 |
| 解释原理 | 对象识别、用途路由、研究流水线 | 原理区 | 页面文字与源文件链接 | 3 | pass | 路由与结论契约完整呈现 |
| 解释数据 | A/B/C、westock、监管披露、行业多视角 | 数据区 | 数据血缘卡与边界提示 | 3/6 | pass | 四层数据图与外部依赖边界可见 |
| 解释判断 | 行业、投资、求职三套引擎 | 标签状态 | 点击、键盘与 DOM 观察 | 4/5/6 | pass | 点击与左右方向键切换通过 |
| 关联场景 | AI 编程 Agent 行业实战 | 实战区 | 核心判断与完整简报入口 | 3/5 | pass | 实战卡和 Markdown 简报均 200 |
| 扩展 | GitHub 项目研究闭环 | 扩展区 | Skill、JSON、扫描和审计入口 | 3/5 | pass | 六步闭环和四个本地产物入口有效 |
| 响应式与可访问性 | 1440/768/390、键盘、reduced-motion、无 JS | 全页 | 浏览器截图与交互证据 | 7/8 | pass | 无溢出；3px 焦点；无 JS 三面板可读 |
| 交付 | 主索引、项目 README、契约一致 | 文档 | 文件与 git diff | 9 | pass | 两级 README 已更新，终审通过 |

## Revision 2 refinement ledger

```text
Current stage: 9 · Engineering and delivery closure
User phase: 展示原版能力 + 解释原理/数据/判断 + 关联实战 + 扩展
Coverage item: 六份报告、三套判断引擎、三个视口、键盘、reduced-motion、无 JavaScript、全部本地入口
User goal: 先展示 Luopan 真正能研究什么，再解释它如何用数据形成判断
Browser environment: Headless Chromium / 1440×1000, 768×1024, 390×844
Observed evidence: 页面 200；6 个报告链接均 200；AI 行业报告在新标签打开且正文 16,194 字符；3 个标签点击/键盘状态正确；12 个本地入口全部 200
Problem category: Information hierarchy（Revision 1 主路径错误）
Root cause: 旧页把 Luopan 当研究对象，原版业务输出与判断引擎没有成为主阅读路径
Minimal intervention: 重构为原版报告 → 原理 → 数据 → 三套引擎 → AI 编程 Agent 实战 → GitHub 项目扩展，并将技术审计下沉到附录
Adjacent regression surfaces: 桌面、平板、390px 手机、原版报告新标签、标签状态、键盘焦点、reduced-motion、无 JS、附录链接
Observed result: 三视口无横向溢出和控制台错误；首个焦点 3px；无 JS 时 6 份报告和 3 套引擎全部可读
Decision: pass
Next executable action: none
New authority required: none
```
