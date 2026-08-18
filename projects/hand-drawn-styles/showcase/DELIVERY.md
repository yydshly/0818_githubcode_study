# Hand-drawn Styles Study Showcase · Delivery Record

## Design contract

```text
Entry mode: Brief-led extension of an existing research repository
Request revision: 1
Target user and context: 主仓库维护者，以及希望把日常内容快速转成稳定视觉风格提示词的研究与内容创作者
Desired first impression: 先看到真实风格效果，再明确它不是生图模型，而是一套可执行的视觉风格合同
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: 延续研究主库的深色档案气质，但用纸张、蜡笔和墨线作为项目识别；不依赖外部字体或 UI 框架；390px–1440px 可读
Information constraints: 必须区分上游事实、我们的解释和我们的扩展；先展示效果能力，再解释五层实现，最后提供贴近日常场景的交互演示
Operation constraints: 纯静态 HTML/CSS/JavaScript；无后端、登录、真实图像 API 或构建依赖；演示只生成可复制 Prompt/调用方案，不伪装成已经出图
State constraints: 风格筛选、场景模板、强度与比例选择、Prompt 预览和复制反馈；禁用 JavaScript 时核心研究内容与静态示例仍可阅读
Environment constraints: GitHub Pages artifact；本地使用 Python HTTP server；上游以 Git submodule 固定版本
Primary journey: 进入展厅 → 浏览上游真实效果 → 理解 Prompt/参考图/多阶段编辑原理 → 选择我们的日常场景 → 生成并复制扩展 Prompt
User-defined phases: 获取上游；展示效果能力并说明原理；结合我们的场景说明意义；演示可日常扩展的能力
Required artifacts: Git submodule、项目 README、研究文档、可运行展厅、主索引与 Pages workflow 更新、浏览器验收记录与最终截图
Autonomy authorization: 用户明确要求将该库作为研究子项目获取、分析、展示并结合我们的场景实现演示
User-decision boundary: 对外调用付费图像模型、修改或提交上游仓库、创建独立仓库需要另行授权
Observable completion criteria: 上游 commit 固定；能力与原理有源码证据；至少 8 个真实样图入口；至少 4 个日常场景可交互生成 Prompt；桌面/平板/390px 无遮挡或横向溢出；键盘焦点可见；reduced-motion 与无 JavaScript 可读；本地发布路径与链接通过
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
