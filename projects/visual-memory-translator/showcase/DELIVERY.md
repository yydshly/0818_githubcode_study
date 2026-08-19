# Visual Memory Translator 展厅交付记录

## Design Contract

```text
Entry mode: Revision-led refinement
Request revision: 3
Target user and context: 希望快速理解开源视觉 Skill 能力、效果、扩展与场景的中文研究者
Desired first impression: 在一个视口内直接看见原图与场景成品的明显差异，再理解“六格只是候选、场景决定成品”
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: 暖米白纸面、锈红强调、编辑层级、大留白；不使用外部字体和连续动画
Information constraints: 明确区分上游样张、本研究生成、Skill 规则和外部模型能力；明确六格并非固定滤镜；用“输入—场景—适配—成品—用途”解释能力
Operation constraints: 保留键盘可达的原图/成品 range 比较器；新增键盘可达的旅行/人物/节日场景切换台；其他内容在正常文档流中
State constraints: 比较器从 50% 开始，可显示 0–100%；场景切换台默认旅行成品，按钮与面板同步 aria-selected / hidden；无加载、空态或远程数据状态
Environment constraints: 纯静态 HTML/CSS/JS；GitHub Pages；无构建依赖、后端、账号或外部 API
Primary journey: 首页理解定位 → 看懂六格与最终成品的关系 → 在大幅左右对照中切换旅行/人物/节日成品 → 阅读七类场景能力 → 明确不适用边界 → 从公开 Web URL 访问
User-defined phases: 强化效果差异；增加大幅场景切换；响应式与键盘验收；提交并部署到 Web
Required artifacts: 更新后的静态展厅与交付记录、Git 提交、GitHub PR、成功的 Pages 部署、公开 URL
Autonomy authorization: 用户指出“效果没有那么明显”并要求部署到 Web，授权本次前端修订与发布流程
User-decision boundary: 不引入后端、登录或批量生产系统；发布仅限现有 GitHub 仓库和 Pages 工作流
Observable completion criteria: 一个桌面视口内同时出现原图与大幅场景成品；三种成品可通过鼠标和键盘切换且状态明确；桌面/平板/390px 无横向溢出；原比较器无回归；提交合并后 Pages 工作流成功，公开 URL 返回页面
Coverage record: 见下表
```

## Coverage Manifest

| 用户阶段 | 要求或资产 | 表面 / 状态 | 证据 | 阶段 | 状态 | 下一步 |
| --- | --- | --- | --- | --- | --- | --- |
| 获取上游 | submodule 固定 commit | 文件系统 | Git 与文件检查 | 1 / 9 | pass | — |
| 理解能力 | README + analysis | 文档 | 文件与链接检查 | 3 / 9 | pass | — |
| 演示效果 | 照片、预览、成品、文本卡 | 桌面页面 | 浏览器截图、全部图片滚动加载 | 2 / 3 / 7 | pass | — |
| 演示效果 | before/after 比较器 | 鼠标与键盘 | range 50 → End 100 → Home 0 → ArrowRight 1 | 4 / 5 / 7 | pass | — |
| 描述扩展 | 扩展章节与文档 | 桌面 / 手机 | 浏览器阅读流与链接 | 3 / 7 | pass | — |
| 描述场景 | 场景章节与文档 | 桌面 / 手机 | 浏览器阅读流与响应式卡片 | 3 / 7 | pass | — |
| 响应式 | 桌面、平板、390px | 1440 / 768 / 390 | 三视口截图；scrollWidth 与 clientWidth 相等 | 7 | pass | — |
| 可访问性 | 焦点、语义与 reduced motion | 键盘 / CSS | range 有语义名称；父级 3px focus ring；reduced motion 下 `scroll-behavior:auto` | 7 / 8 | pass | — |
| 工程闭环 | 资源、链接、Pages 复制 | 文件与本地 HTTP | 相对引用无缺失、HTTP 200、`git diff --check` 通过 | 9 | pass | — |
| 核心解释 | 六格候选与最终成品关系 | 桌面 / 手机 | 浏览器阅读流与可访问性快照 | 3 / 7 | pass | — |
| 场景适配 | 同一原图的旅行、人物、节日三种处理 | 桌面 / 手机 | 生成资产、图片加载与场景说明 | 2 / 3 / 7 | pass | — |
| 场景映射 | 七类典型场景的输入、适配、成品与用途 | 桌面 / 手机 | 浏览器阅读流与响应式卡片 | 3 / 7 | pass | — |
| 不适用边界 | 五类明确限制及原因 | 桌面 / 手机 | 浏览器阅读流 | 3 / 7 | pass | — |
| 修订闭环 | 新资源、链接、响应式与键盘回归 | 1440 / 768 / 390 / keyboard | 浏览器与工程检查 | 5 / 7 / 9 | pass | — |
| 效果强化 | 原图与大幅场景成品同时可见 | 桌面 / 平板 / 手机 | 浏览器截图与 DOM 尺寸 | 2 / 3 / 7 | pass | — |
| 场景交互 | 旅行、人物、节日三个成品状态 | 鼠标 / 键盘 | click、ArrowLeft/Right、Home/End 与 aria 状态 | 4 / 5 / 6 / 7 | pass | — |
| Web 发布 | 提交、PR、合并、Pages 部署与公开 URL | GitHub / Web | commit、PR、Actions、HTTP 页面 | 9 | continue | 浏览器验收后执行发布流程 |

## Canonical Runtime

```text
Start command: python -m http.server 8878 --directory E:\0818_codex_project
Canonical URL: http://127.0.0.1:8878/projects/visual-memory-translator/showcase/
Theme: light only
Required viewports: 1440×1000, 768×1024, 390×844
Verified: 2026-08-19 Asia/Shanghai
```

## Browser Evidence

- 页面标题、主导航、六格解释、照片实演、同图三用、比较器、文本路径、能力、上游样张、扩展、七类场景、五类不适用边界与页脚均出现在可访问性快照中。
- 页面无错误覆盖层，浏览器错误列表为空，正文长度 4462 个字符。
- 20 个页面图片引用均能成功加载，失败数为 0；两张新资产在页面中的四处实例均报告 `1086×1448`。
- 1440、768 与 390 三个视口的横向溢出均为 `0`。
- 比较器键盘值通过 `100 / 0 / 1`，焦点时父级 `outline: solid 3px`。
- reduced-motion 媒体条件下根元素 `scroll-behavior` 为 `auto`。
- 桌面全页截图验证整体阅读流；390px 对“核心解释”“同图三用”“场景目录”“不适用边界”分别做真实视口截图，避免超长全页截图的拼接失真。
- Revision 3 将三张小卡替换为大幅切换台；1440px 同一视口同时显示原始照片、场景成品和变化说明，390px 以原图 → 成品的纵向顺序呈现。
- 场景 tabs 默认“旅行纪念”，真实点击切换到“人物纪念”；ArrowRight、Home、End 均能切换选中项与对应面板，任一时刻只有一个 `tabpanel` 可见，焦点环为 `solid 3px`。
- Revision 3 页面共 21 个图片引用；滚动加载后失败数为 0。原比较器回归通过，End 后值为 `100`；1440、768 与 390 三个视口横向溢出均为 `0`。
- 按 Pages 根目录结构组装主站后，第 07 项目卡存在、封面加载成功，桌面与 390px 均无横向溢出。
- 仅支持 light theme；页面没有弹窗、菜单、加载、空态、错误态或远程数据，因此这些矩阵项不适用。

## Session Handoff

1. **项目与阶段：** Visual Memory Translator 研究子项目；Revision 3 / Stage 9 发布中。
2. **已完成：** 用大幅原图/成品切换台强化效果差异；三种场景状态、三视口、键盘与原比较器回归均通过。
3. **剩余或延期：** `Web 发布`仍为 `continue`；没有 `defer` 或 `blocked`。
4. **证据：** 桌面前后截图、手机切换台截图、21 张图片加载、tabs 状态、键盘路径、原比较器、三视口溢出和浏览器错误检查均通过。
5. **下一步：** 审查提交范围，推送分支、创建并合并 PR，等待 Pages 成功后验证公开 URL，再关闭发布记录。
