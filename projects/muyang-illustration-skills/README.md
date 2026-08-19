# Muyang Illustration Skills 项目研究

> 研究一套固定插画 Prompt 如何被封装为 Codex Skills，并用统一主体生成 8 个分类的自有对照样例；上游 25 张示意图降为辅助参考，调用工作台继续只演示文字入参。

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 上游项目 | `yokel1121/muyang-illustration-skills` |
| 上游地址 | <https://github.com/yokel1121/muyang-illustration-skills> |
| 研究版本 | `8c35300b74eaf8b34221b138082b8d7acd0363d5` |
| 研究状态 | 基础能力已复现 · 8 类自有样例已生成 |
| 开始日期 | 2026-08-19 |
| 上游源码 | [`upstream/`](upstream/)（Git submodule） |
| 研究展厅 | [`showcase/`](showcase/) |
| 原理分析 | [`docs/analysis.md`](docs/analysis.md) |
| 后期路线 | [`docs/extension-roadmap.md`](docs/extension-roadmap.md) |
| 许可证 | Skill、Prompt 整理和文档为 MIT；上游示意图不包含在 MIT 授权中 |

## 一句话结论

它不是图像模型，也不是图生图处理器；它是位于用户和外部图像模型之间的固定 Prompt 路由层：接收用户提供的**主体文字 + 具体风格**，只替换配方中的主体占位符，然后调用宿主已有的图像生成工具。

## 本阶段完成内容

1. 按上游结构安装 1 个总入口与 8 个风格子 Skill。
2. 固定上游 commit，保留全部 25 套配方与原始示意图的证据关系。
3. 以“一个女孩在窗边读书”为统一主体，为 8 个分类各生成 1 张代表样例，形成可直接比较的第一版实测证据。
4. 将 25 张上游示意图完整、直接展示，并与 8 张本研究生成样例分别标注来源与权利边界。
5. 建立文字入参工作台：生成可复制的 Skill 调用文本，但不重复执行图片生成，也不展示内部完整 Prompt。
6. 解释输入、路由、配方填槽、ImageGen 调用和返回图片五层原理。
7. 在网页中描述两条产品化路径：参考图 + 保留合同的图生图一致性，以及无字底图 + 确定性排版的文字成品流程。
8. 记录适用场景、当前限制、模型偏差与后期扩展路线。

## 目录

```text
muyang-illustration-skills/
├── README.md
├── docs/
│   ├── analysis.md
│   └── extension-roadmap.md
├── showcase/
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   ├── assets/generated/      # 本研究生成的 8 张统一主体样例
│   └── DELIVERY.md
├── tests/
│   └── verify_project.py
└── upstream/                 # 固定上游 Git submodule
```

## 运行展厅

在主仓根目录执行：

```powershell
git submodule update --init --recursive
python -m http.server 4178 --bind 127.0.0.1 --directory .
```

浏览器打开：<http://127.0.0.1:4178/projects/muyang-illustration-skills/showcase/>

## 基础调用

通过总入口调用：

```text
$muyang-illustration
主体：一个女孩在窗边读书
风格：庭院手绘插画
```

也可以直接调用对应子 Skill：

```text
$muyang-fashion-colorblock
主体：一个穿白色 T 恤、手持黑色雨伞的人
风格：黄黑撞色插画
画幅：9:16
```

必填入参只有两项：

- `主体`：用户亲自提供的文字描述；
- `风格`：25 个固定风格名称之一。

画幅或其他硬限制是可选项，按上游规则只能原样追加到固定配方末尾。

## 当前边界

- 主展示区的 8 张图由本研究生成，统一主体、每类一个代表风格；它们能证明基本路由与明显风格差异，但单次入选结果不等于稳定性测试。
- 上游原样例区的 25 张图来自固定上游子模块，现在直接完整展示；它们只证明作者希望表达的风格方向。
- 上游流程是文生图，不会把示意图自动作为参考图传给图像模型。
- 展厅工作台只构造用户可见的调用文本，不读取或公开完整内部配方。
- 没有模型、Seed、生成参数、自动评测或回归基准，因此不能把它视为可复现的图像算法。
- “柔纱纯白插画”样例出现模型自动添加的杂志文字，已作为可见偏差保留，说明固定配方无法完全控制底层模型。
- 网页描述的图生图一致性和文字排版层是后期架构，不代表当前已经实现：前者需要真正传入参考图并调用图像编辑工具，后者需要 HTML、SVG 或 Canvas 的确定性排版。

## 验证

```powershell
python projects/muyang-illustration-skills/tests/verify_project.py
```

验证脚本检查：9 个 Skill 目录、25 张上游资产、8 张自有样例、25 个配方标题、8 个分类、展厅数据项、关键文档和相对路径。

## 相对上游增加了什么

本研究没有修改上游 Skill 和 Prompt，只增加了：

- 固定版本和安装记录；
- 能力、原理、限制与权利边界分析；
- 统一主体、覆盖 8 个分类的自有基础样例；
- 作为辅助资料保留的上游示意图档案；
- 不执行生图的文字调用演示；
- 面向评测、兼容性、图生图和产品化的后期研究路线。
