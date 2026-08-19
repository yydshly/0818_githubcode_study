# Muyang Illustration Skills · 展示交付记录

## Design contract

```text
Entry mode: Brief-led addition to an established research repository
Request revision: 3（恢复上游样例直接可见；增加文字产品化与图生图一致性说明；验证后提交 GitHub）
Target user and context: 想快速理解这个 Skill 是否值得继续研究的中文技术/内容用户
Desired first impression: 同时看见上游原始能力与本研究实测，并清楚理解从艺术底图走向可控产品的两条扩展路径
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: 延续深色编辑感；8 张自有样例与 25 张上游图都直接可见并明确标源；扩展说明使用流程卡而非新生成图片
Information constraints: 明确区分自有生成、上游示意、当前能力、图生图一致性、确定性文字排版和未来设想；不公开复述完整内部 Prompt
Operation constraints: 分类筛选；输入主体与风格后只输出可复制的 Skill 调用文本和路由说明，不执行图片生成
State constraints: 全部/八类筛选；表单默认、修改、校验、复制反馈；无后端和加载态
Environment constraints: 纯静态 HTML/CSS/JS；可由 Python 静态服务器运行；支持桌面与移动端；单一深色主题
Primary journey: 理解结论 → 比较 8 类自有样例 → 直接浏览 25 种上游原样例 → 试填文字入参 → 理解文字产品化与图生图一致性 → 阅读限制和路线
User-defined phases: 安装 Skill；创建研究分支与子项目；基础能力演示；原理描述；后期扩展描述
Required artifacts: 固定上游子模块、项目 README、分析、扩展路线、静态展厅、验证脚本、主仓索引更新、安装记录
Autonomy authorization: 用户明确要求安装、新建分支并作为子项目实施研究
User-decision boundary: 用户已授权恢复展示、增加两条扩展说明并提交推送当前研究分支；修改上游 Prompt、实际实现图生图与排版引擎、合并默认分支不在本阶段授权范围内
Observable completion criteria: 8 张自有样例与 25 张上游原样例均直接可见且标源；网页说明“参考图 + 保留合同 + 图像编辑”及“无字底图 + 确定性排版”；三档视口与交互通过；相关文件提交并推送当前分支，或准确记录认证阻塞
Coverage record: 下表
```

## Coverage manifest

| 用户阶段 | 要求或产物 | 表面 / 状态 | 证据 | 阶段 | 状态 | 下一动作 |
| --- | --- | --- | --- | --- | --- | --- |
| 安装 Skill | 9 个 Skill 位于用户技能目录 | 文件系统 | 安装器输出与目录检查 | 0 | pass | 无 |
| 新建分支 | `codex/muyang-illustration-skills-research` | Git | `git branch --show-current` | 0 | pass | 无 |
| 固定上游 | Git submodule 固定 `8c35300` | 文件系统 / Git | 子模块状态 | 1 | pass | 无 |
| 自有样例 | 同一主体覆盖 8 分类各 1 张 | 图片资产 / 页面主展示 | 本地逐张视觉检查、浏览器截图与 DOM 计数 | 2–5 | pass | 无 |
| 恢复原样例 | 25 风格、8 分类、上游原图直接可见 | 默认页面与筛选 | 浏览器截图、DOM 与筛选计数 | 2–5 | pass | 无 |
| 图生图说明 | 参考图、保留项、可改变项、编辑工具、一致性质检 | 页面 / Markdown | 浏览器阅读顺序与文件检查 | 3 | pass | 无 |
| 文字产品化 | 无字底图、确定性排版、文字质检、成品导出 | 页面 / Markdown | 浏览器阅读顺序与文件检查 | 3 | pass | 无 |
| 基础调用演示 | 主体 + 风格 + 可选限制 → 调用文本 | 桌面 / 默认、修改、复制 | 浏览器交互记录 | 4–6 | pass | 无 |
| 原理描述 | 五层流程、真实边界、限制 | 页面与 Markdown | 文件检查、浏览器阅读顺序 | 3 | pass | 无 |
| 后期扩展描述 | 评测、兼容性、图生图等路线；均标为未来 | 页面与 Markdown | 文件检查、浏览器观察 | 3 | pass | 无 |
| 响应式 | 自有样例、上游图库、扩展流程、工作台无关键遮挡 | 1440 / 768 / 390 px | 浏览器截图 | 7 | pass | 无 |
| 键盘与可访问性 | 样例按钮、筛选、表单和链接可达、焦点可见 | 键盘路径 | 浏览器观察 | 7 | pass | 无 |
| 工程闭环 | 链接、33 张图片、风格计数、脚本语法、Git 提交 | 静态文件 / Git | 自动验证与提交记录 | 9 | pass | 无 |
| 主仓入口 | README 与 Pages 首页新增第 6 项 | 文档 / 首页 | 文件与浏览器检查 | 9 | pass | 无 |

## Design direction

| 决策 | 方向 | 可观察约束 | 验收标准 |
| --- | --- | --- | --- |
| 信息层级 | 先给“不是模型”的结论，再给证据 | 首屏只保留一个主结论和四个规模数字 | 首屏无需滚动即可识别本质与范围 |
| 样例 | 自有生成图片为第一视觉证据 | 同一主体、8 类各 1 张；每张标明“本研究生成” | 8 张优先出现、来源清楚、偏差不隐藏 |
| 原样例 | 上游图片与本研究样例同时保留 | 默认直接可见；每张标明“上游示意” | 25 张完整出现，筛选数量一致，来源不混淆 |
| 产品扩展 | 一致性与文字分成两条流程 | 图生图必须传参考图；文字必须确定性排版 | 当前能力与后期架构边界一眼可辨 |
| 工作台 | 演示真实文字入参，不泄漏配方 | 输出只含 `$muyang-illustration` 调用文本和路由说明 | 修改输入后立即得到合法文本，不执行生图 |
| 视觉语言 | 深墨绿色、纸色、朱橙强调的编辑档案 | 不依赖渐变和连续动画；一套深色主题 | 正文、标签、控件在三档视口清晰可读 |
| 响应式 | 宽屏多列、窄屏单列，工作台上下堆叠 | 不出现水平滚动或不可达控件 | 1440、768、390 px 主流程可完成 |
| 动效 | 只用短暂状态过渡 | `prefers-reduced-motion` 下关闭 | 信息不依赖动效出现 |

## Runtime evidence

- 时间：2026-08-19（Asia/Shanghai）
- 启动命令：`python -m http.server 4178 --bind 127.0.0.1 --directory .`
- 规范 URL：`http://127.0.0.1:4178/projects/muyang-illustration-skills/showcase/`
- 浏览器：工作区内置 Playwright + Chromium（agent-browser CLI 未在 PATH 且沙箱禁止联网安装，因此使用同等的本地浏览器验证路线）
- 页面加载：标题正确、正文非空、无框架错误覆盖层；`errors` 无输出。
- DOM：三档视口均直接渲染 25 个上游原样例卡；逐卡滚动后 25 张图片全部 `complete=true` 且 `naturalWidth>0`。
- 产品扩展：三档视口均存在 2 条扩展轨道与 2 个流程图；“参考图驱动的图生图 / 保留合同”及“确定性文字产品化 / 模板排版”内容均可见。
- 筛选：触发“柔焦梦幻”后，可见上游卡片数为 5。
- 样例联动：点击“暗调黑红插画”自有卡后，工作台选择值为 `7`，路由为 `$muyang-dark-fashion`。
- 表单：主体改为“一位研究者在窗边整理风格卡片”、风格改为“黄黑撞色插画”、限制改为“画幅：4:5”后，输出文本与 `$muyang-fashion-colorblock` 路由同步更新。
- 响应式：1440×1000、768×900、390×844 均完成截图；三档 `scrollWidth` 均等于 `clientWidth`，无横向溢出。
- 键盘：首次 `Tab` 聚焦“跳到主要内容”，计算样式 `outline: solid`；表单和筛选在交互快照中均具有正确的 button、textbox、combobox 语义。
- 自动化：`verify_project.py` 98/98 通过；`node --check showcase/app.js` 通过；`git diff --check` 通过。
- 最终视觉证据保存在 Codex 临时可视化目录，未写入产品仓库；截图确认两条扩展轨道在桌面并排、平板与移动端纵向排列，均无横向溢出。
- Git：归档提交 `1425a42` 已推送到 `origin/codex/muyang-illustration-skills-research`。Draft PR 创建尝试被 GitHub App 以 403 拒绝，本机 `gh` 令牌也已失效；这是非阻塞的审阅入口权限问题，分支与提交本身已在 GitHub 可访问。

## Session handoff

1. **项目与阶段**：Muyang Illustration Skills 基础研究子项目，修订 3 的 Stage 9 已完成并发布研究分支。
2. **已完成**：9 Skill 安装、研究分支、固定上游、8 类自有样例、直接可见的 25 张上游原样例、文字工作台、图生图一致性说明、确定性文字产品化说明、文档、主仓索引、提交与推送。
3. **剩余或延后**：实际图生图引擎、排版引擎、25 风格全覆盖与重复采样仍是后期能力；Draft PR 因连接器和 CLI 认证权限未创建，不影响已发布分支。
4. **证据**：浏览器三视口、25 图逐卡加载、筛选、扩展流程、键盘焦点和错误检查通过；静态验证 98/98 通过；远端分支跟踪建立成功。
5. **下次优先事项**：若启动产品化实施，先定义参考图保留合同与一种成品模板（例如小说封面）；若需要合并审阅，先恢复 `gh auth login` 后从已推送分支创建 PR。
