# Promise Wall 项目研究

> 一个把社区留言、目标和故事转化为可浏览 3D 空间的单页 Three.js 原型；本研究重点验证其真实交互、程序化材质、DOM/WebGL 混合结构及产品化边界。

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 上游项目 | `thebuggeddev/promise-wall` |
| 上游地址 | https://github.com/thebuggeddev/promise-wall |
| 研究版本 | `0cb1b20c3952e4c4184b7e0e33fe5acfac2b4447` |
| 研究状态 | 已完成 · 已归档 |
| 开始日期 | 2026-08-19 |
| 最后更新 | 2026-08-19 |
| 本地实验 | `projects/promise-wall/` |
| 在线演示 | `projects/promise-wall/showcase/`（合并到 `main` 后由 Pages 发布） |

## 一句话结论

它不是可复用的 npm 库，而是一个 **Three.js 空间舞台 + Canvas 程序化内容 + DOM 产品界面** 的完整交互样例。视觉和交互研究价值高，直接产品复用价值有限。

## 已验证能力

| 能力层 | 上游真实实现 | 证据 |
| --- | --- | --- |
| 3D 空间 | 墙面、地板、踢脚线、灯光、阴影、雾、漂浮灰尘 | `index.html:2458–2620` |
| 程序化材质 | 纸张、撕边、横线、方格、纤维、照片、石墙和木纹均由 Canvas 生成 | `index.html:2017–2456` |
| 空间卡片 | 弯曲网格、图钉、胶带、夹子、物理叠放高度 | `index.html:2654–2810` |
| 浏览交互 | 拖拽平移、滚轮缩放、Raycaster 拾取、悬停浮起、镜头聚焦 | `index.html:2835–3084` |
| 内容交互 | 搜索、分类过滤、详情、支持、反思、收藏、创建与墙面放置 | `index.html:3088–3428` |
| 反馈与适配 | GSAP 时间线、Web Audio 提示音、移动端布局、reduced-motion | `index.html:1097–1128`、`2814–2833`、`3289–3358` |

展厅直接在同源 iframe 中运行固定上游的 `index.html`，没有重写或伪造原版效果。

## 能力边界

- `store` 只存在于内存；源码明确没有使用 `localStorage`，刷新即还原。
- 没有 API、数据库、身份认证、实时协作、上传或管理后台。
- 支持、反思、收藏与举报都是前端状态或提示，不会发送到服务端。
- 照片是 Canvas 绘制的内部样例，不是用户上传的真实照片。
- Three.js r128 与 GSAP 3.12.5 通过 CDN 加载，离线环境不能启动 3D 引擎。
- 真实入口是 3587 行的根 `index.html`；`src/` 仍是 Vite 默认模板。

## 场景体验扩展

研究展厅第二版把效果与使用场景放到技术之前，新增两层可操作内容：

- **12 类使用场景**：新年、毕业、婚礼、企业目标、员工感谢、公益行动、匿名心声、家庭记忆、旅行、品牌故事、城市故事和游戏线索；
- **12 幕独立效果舞台**：每个使用场景都有自己的第一版空间、材料、反馈与记忆点，不再复用六个通用状态。

每个使用场景都可以直接路由到对应舞台。舞台支持标签选择、键盘左右方向键、上一幕／下一幕和自动顺序播放；reduced-motion 下自动播放会关闭，但十二个场景仍可手动切换。

`showcase/assets/generated/promise-wall-six-scenes.png` 是使用 OpenAI 内置 ImageGen 生成的气氛总览，提示词和能力边界保存在同目录 `PROMPT.md`。生成图片不承担交互或产品能力证明，实际场景状态由本地 HTML、CSS 和 JavaScript 呈现。

## 快速查看

从研究仓库根目录启动静态服务器：

```powershell
git submodule update --init --recursive
python -m http.server 8000
```

然后打开：

- 研究展厅：`http://127.0.0.1:8000/projects/promise-wall/showcase/`
- 固定上游原版：`http://127.0.0.1:8000/projects/promise-wall/upstream/`

如需验证上游 Vite 构建：

```powershell
cd projects/promise-wall/upstream
npm ci
npm run build
```

## 研究目录

```text
projects/promise-wall/
├── upstream/                    # Git submodule：未修改的固定上游版本
├── docs/analysis.md             # 技术结构、真实能力与风险
├── docs/extension-scenarios.md  # 使用场景、扩展场景与产品化路线
├── showcase/                    # 真实 Demo + 研究解释工作台
│   └── assets/generated/        # ImageGen 六场景气氛总览与提示词
├── tests/verify_project.py      # 上游 pin、内容、资源与 Pages 接线验证
└── README.md
```

## 上游与本地修改边界

- `upstream/` 固定在 `0cb1b20c3952e4c4184b7e0e33fe5acfac2b4447`，没有修改上游文件。
- `showcase/`、`docs/` 和 `tests/` 是本研究仓库新增的解释、展示与验证产物。
- 固定上游版本没有 `LICENSE`。子模块只保存来源与 commit 关系；复制、修改、再分发或商用前必须先获得明确许可。

## 归档决定

本子项目已经完成固定上游、真实原版展示、五层能力分析、十二类使用场景、十二幕独立第一版效果、ImageGen 气氛资产、后期行动地图和跨端验证，现正式归档，不继续增加相似场景或视觉效果。

未来仅在出现以下条件时重新启动：

- 有一个具体真实场景、活动日期和目标用户；
- 有可用于验证的真实内容与完整参与流程；
- 明确最终产物、成功指标、隐私边界和运营责任。

后期可扩展动作保留在展厅 `#future-actions`：独立互动闭环、时间变化、集体反馈、可带走成果、活动现场、个人长期空间和跨场景生命周期。它们均为未来可选方向，不属于当前已实现能力。

## 推荐阅读

- [能力、架构与限制](docs/analysis.md)
- [使用场景与扩展路线](docs/extension-scenarios.md)
- [研究展厅](showcase/index.html)
- [交付与浏览器验收](showcase/DELIVERY.md)
