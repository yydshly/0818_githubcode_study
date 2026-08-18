# Stamp Edge 研究展厅交付记录

## Design contract

```text
Entry mode: Revision-led implementation
Request revision: 4
Target user and context: 需要快速理解开源 Skill 能力、真实效果与扩展空间的研究者
Desired first impression: 第一眼先被真实、丰富的邮票成品吸引，随后自然理解“效果由确定性脚本完成”
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: 参考上游社交截图与邮票合集的高信息密度；以照片、旅行、海报、截图等真实场景为视觉主角；不伪造上游能力
Information constraints: 明确区分上游事实、本地复现结果、本地扩展设想与已验证限制
Operation constraints: 静态页面可直接部署；唯一交互用于切换透明 PNG 的承载背景
State constraints: 棋盘格、深色、纸色三种预览状态都必须保持图片可见
Environment constraints: GitHub Pages 静态托管；不依赖构建工具或外部运行时
Primary journey: 先看高质量成品墙 -> 选择场景查看前后对比 -> 查看原始库合集能力 -> 理解参数与边界 -> 浏览可扩展效果地图
User-defined phases: 视觉质量优化；增加效果；增加场景；完整展示上游合集；实现扩展 Skill；研究收口说明；更新文档与验证
Required artifacts: 新场景源图、逐张邮票输出、深浅两种完整合集、六个扩展 preset、统一 CLI、Agent Skill、混合扩展合集、重构展厅、素材说明、更新后的验证脚本
Autonomy authorization: 用户已明确授权新建分支并完成安装、演示和文档沉淀
User-decision boundary: 发布、推送、合并与全局安装不在本次授权范围
Observable completion criteria: 至少 6 个差异明显的真实场景；完整展示上游 `stamp_sheet.py` 深浅合集；新增 6 个可通过统一 CLI 调用的确定性 preset；扩展 Skill 校验通过；本地一条命令可重建基础与扩展 Demo；自动验证通过；桌面与移动端浏览器无溢出；场景和背景切换可用
Coverage record: 见下表
```

## Coverage manifest

| 用户阶段 | 要求或产物 | 界面／状态 | 所需证据 | 阶段 | 状态 | 下一步 |
| --- | --- | --- | --- | --- | --- | --- |
| 引入上游 | 固定仓库与 commit | Git submodule | `.gitmodules`、本地 gitlink 来源、commit | 9 | pass | 无 |
| 安装复现 | 依赖可安装 | Python 3.10 / Pillow 11.3.0 | 项目 `.venv` 安装成功 | 1 | pass | 无 |
| Demo 演示 | 生成三种单图效果 | 原图、透明、白边、底色 | 生成日志与 Alpha 检查 | 1 | pass | 无 |
| Demo 演示 | 生成合集效果 | 深色／纸色合集 | 输出文件与尺寸检查 | 1 | pass | 无 |
| Demo 演示 | 展厅首屏和阅读流 | 1243px 桌面宽屏 | 全页截图、正文 1774 字符、溢出 0 | 2–5 | pass | 无 |
| Demo 演示 | 透明背景切换 | 棋盘格／深色／纸色 | DOM 点击与键盘 Enter；`paper:true` | 5–6 | pass | 无 |
| Demo 演示 | 响应式阅读 | 390×844 移动端 | 全页截图、横向溢出 0 | 7 | pass | 无 |
| 扩展总结 | 模块化扩展路线 | 文档 | `docs/extension-roadmap.md` | 9 | pass | 无 |
| 文档沉淀 | 能力、原理、限制 | 文档 | `README.md`、`docs/analysis.md` | 9 | pass | 无 |
| 交付验证 | 自动化检查 | 文件与图片合同 | `verify_project.py` PASS | 9 | pass | 无 |

## Revision 2 coverage

| 用户要求 | 界面／状态 | 所需证据 | 阶段 | 状态 | 下一步 |
| --- | --- | --- | --- | --- | --- |
| 效果质量明显优于旧版抽象卡片 | 首屏、成品墙、详情场景 | 新旧截图对照、真实浏览器观察 | 2–3 | pass | 无 |
| 补充更多效果 | 默认、白边、浅底、深底叠加、纸色叠加 | 5 种可辨识处理状态 | 3–6 | pass | 无 |
| 补充更多场景 | 旅行、建筑、美食、自然、社交截图、编辑海报 | 6 个原创输入及上游输出 | 1–3 | pass | 无 |
| 展示上游合集效果 | 深色与纸色完整合集 | 两张真实 `stamp_sheet.py` 输出和代码说明 | 3 | pass | 无 |
| 更新文档沉淀 | README、Demo 说明、分析、提示词与扩展路线 | 文件与素材清单 | 9 | pass | 无 |
| 桌面与移动端复验 | 1440px、390px、键盘 | 截图、DOM、交互、无溢出 | 5–7 | pass | 无 |
| 自动化交付检查 | 图片合同、资源、场景数、合集 | 验证脚本 PASS | 9 | pass | 无 |

## Visual direction

| 决策 | 选择 | 可观察约束 | 验收标准 |
| --- | --- | --- | --- |
| 信息层级 | 结论先行，Demo 次之，原理与路线随后 | 首屏只保留一个主结论和关键元数据 | 1280px 首屏能看见结论与首个真实样例 |
| 字体 | 系统无衬线正文 + 衬线展示标题 | 不加载远程字体 | 中英文在离线环境正常回退 |
| 色彩 | 暖纸色、邮政红、墨蓝 | 色彩不替代文字状态 | 三种背景下透明边缘可辨识 |
| 材质 | 轻纸纹、细边框、克制投影 | 不使用高成本 Canvas/WebGL | 静态 CSS 即可完整阅读 |
| 响应式 | 桌面双栏、移动端单栏 | 无固定宽度正文和横向滚动 | 390px 页面宽度内完整操作 |
| 动效 | 仅按钮与卡片轻过渡 | 尊重 reduced-motion | 关闭动效不损失信息 |

## Evidence ledger

```text
Current stage: 9 / Engineering and delivery closure
User phase: Demo 演示
Coverage item: 桌面、移动端、透明背景交互和研究主页入口
User goal: 能力展示及 Demo 演示可以运行、阅读和验证
Browser environment: agent-browser 0.27.0；Python http.server；2026-08-18
Canonical command: python -m http.server 8891 --bind 127.0.0.1
Canonical URL: http://127.0.0.1:8891/projects/stamp-edge-skill/showcase/
Observed evidence: 页面标题正确；正文长度 1774；无错误覆盖层；所有图片 naturalWidth > 0；桌面与 390px 横向溢出均为 0
Problem category: 无阻断问题
Root cause: 不适用
Minimal intervention: 不适用
Adjacent regression surfaces: 研究主页 /site/ 已显示 Stamp Edge；移动端单栏；三种背景；键盘激活
Observed result: 纸色按钮聚焦后按 Enter，预览状态为 paper，按钮 aria-pressed=true
Decision: pass
Next executable action: 无
New authority required: 推送、发布或合并需要用户另行授权
```

临时验收截图保存在系统临时目录，没有加入产品仓库；自动化合同由
`tests/verify_project.py` 长期保留。

## Terminal audit

- 所有用户要求的产物均存在；
- coverage manifest 没有 `continue`、`defer` 或 `blocked`；
- Demo 使用未修改的固定上游脚本生成；
- 自动验证与真实浏览器验证均通过；
- 当前交付范围完成，未执行推送、合并、发布或全局 Skill 安装。

## Revision 2 refinement ledger

```text
Current stage: 9 / Engineering and delivery closure
User phase: 视觉质量优化、增加效果与场景、展示上游合集
Coverage item: 旧版抽象素材替换、六场景工作台、成品墙、三种单图模式、两种合集
User goal: Demo 的真实效果不低于上游示例，并完整呈现合集能力
Browser environment: agent-browser 0.27.0；Python http.server；2026-08-19
Canonical command: python -m http.server 8892 --bind 127.0.0.1
Canonical URL: http://127.0.0.1:8892/projects/stamp-edge-skill/showcase/
Baseline evidence: 旧版首屏和展示主体为三张抽象几何卡，合集仅有三张卡且处于次要位置
Problem category: Composition / focal hierarchy / content quality
Root cause: 输入素材信息密度不足，页面把算法说明置于真实使用效果之前，合集不是首要视觉证据
Minimal intervention: 用 4 张原创摄影与 2 张本地内容卡替换旧素材；首屏改为完整合集；增加六场景选择器、成品墙和双合集大图
Adjacent regression surfaces: 默认/白边/bg 三种模式、深/纸/透明格状态、桌面 1440px、移动端 390px、键盘 Enter、研究主页封面
Observed result: 1938 字符正文；全部图片 naturalWidth > 0；无错误覆盖层；桌面与移动端横向溢出均为 0；场景切换 architecture:true；键盘切换 paper:true
Decision: pass
Next executable action: 无
New authority required: 推送、发布或合并仍需用户另行授权
```

Revision 2 删除了由本项目第一版脚本生成的旧抽象输入和旧输出目录；这些文件属于可替换的本地 Demo 产物，不包含用户原始数据。新版最终素材保存在 `assets/demo/sources/`、`inputs-v2/` 和 `outputs-v2/`。

## Revision 3 coverage

| 用户要求 | 产物／状态 | 所需证据 | 阶段 | 状态 | 下一步 |
| --- | --- | --- | --- | --- | --- |
| 基于已有能力扩展 | 统一 Pillow 扩展引擎 | 六个 preset 都能由同一 CLI 生成 | 1–3 | pass | 无 |
| Agent 可自然语言调用 | 扩展 `SKILL.md` | skill validator 与触发/路由说明 | 1–4 | pass | 无 |
| 拍立得效果 | `polaroid` | 真实图片输出与尺寸/Alpha 合同 | 3 | pass | 无 |
| 撕纸效果 | `torn-paper` | 不规则 Alpha 边缘与投影 | 3 | pass | 无 |
| 胶片效果 | `film-frame` | 黑色片框、透明齿孔、画面保留 | 3 | pass | 无 |
| 票券效果 | `ticket` | 侧边缺口、票根布局与透明外部 | 3 | pass | 无 |
| Riso 印刷效果 | `riso-print` | 双色映射、错版边缘与纸色背景 | 3 | pass | 无 |
| 轮廓贴纸效果 | `sticker-outline` | 从已有 Alpha 扩展白色轮廓 | 3 | pass | 无 |
| 扩展能力展示 | 页面与混合合集 | 桌面/移动端截图、资源、无溢出 | 5–7 | pass | 无 |
| 工程交付 | 文档与自动化测试 | CLI、Skill、图片合同全部 PASS | 9 | pass | 无 |

## Revision 3 refinement ledger

```text
Current stage: 9 / Engineering and delivery closure
User phase: 基于已有能力进行扩展
Coverage item: 六个确定性 preset、统一 CLI、Agent Skill、行为测试、实际效果墙和混合合集
User goal: 将前一轮扩展路线从文档规划变成可运行能力
Browser environment: agent-browser 0.27.0；Python http.server；2026-08-19
Canonical command: python -m http.server 8893 --bind 127.0.0.1
Canonical URL: http://127.0.0.1:8893/projects/stamp-edge-skill/showcase/
Observed evidence: 2201 字符正文；全部图片 naturalWidth > 0；无错误覆盖层；桌面与 390px 移动端横向溢出为 0；扩展区 6 个 article；页面仅 1 个 hero
Problem category: Capability expansion / information hierarchy / responsive asset gallery
Root cause: 旧页面只描述下一批 preset，没有脚本、Skill、输出或验证证据
Minimal intervention: 新增统一 Pillow CLI、六个 preset、Skill 路由、行为测试、扩展生成器、实际输出卡和混合合集
Adjacent regression surfaces: 上游基础邮票、场景选择器、背景切换、原始合集、桌面/移动端、键盘 Enter、Pages 资源复制
Observed result: 3 项行为测试通过；官方 skill validator 通过；项目综合验证通过；键盘切换 poster:true；移动端扩展区和页脚局部截图正常
Decision: pass
Next executable action: 无
New authority required: 推送、发布或合并仍需用户另行授权
```

## Revision 4 coverage

| 用户要求 | 产物／状态 | 所需证据 | 阶段 | 状态 | 下一步 |
| --- | --- | --- | --- | --- | --- |
| 不再继续深入实现 | 研究范围说明 | 页面明确“当前研究完成，不继续开发” | 3 | pass | 无 |
| 保留后期探索方向 | 可选路线摘要 | 仅描述质量、批量、邮票语义和可选 AI，不宣称已实现 | 3 | pass | 无 |
| 页面与文档一致 | README、展厅、验证 | 自动检查与桌面/移动端浏览器证据 | 7–9 | pass | 无 |

## Revision 4 refinement ledger

```text
Current stage: 9 / Engineering and delivery closure
User phase: 研究收口说明
Coverage item: 已完成范围、刻意停止范围、未来四类可选探索方向
User goal: 不再继续深入，只在网页保留后期方向说明
Browser environment: agent-browser 0.27.0；Python http.server；2026-08-19
Canonical command: python -m http.server 8894 --bind 127.0.0.1
Canonical URL: http://127.0.0.1:8894/projects/stamp-edge-skill/showcase/#closure
Observed evidence: 桌面收口区双栏结构清晰；390px 移动端转为单栏；横向溢出 0；全部图片加载成功；“本次研究到这里”和“不属于当前已经实现的能力”均存在
Problem category: Information boundary / scope closure
Root cause: 页面此前只有已实现扩展和未来路线，没有明确说明研究已经停止继续深入
Minimal intervention: 新增收口说明区，区分 completed、intentionally stopped 与 if reopened later
Adjacent regression surfaces: 扩展区、文档链接、页脚、桌面和移动端阅读流
Observed result: 自动验证通过，桌面和移动端浏览器观察通过
Decision: pass
Next executable action: 无；项目按用户决定收口
New authority required: 若未来恢复研究，需要新的用户指令
```
