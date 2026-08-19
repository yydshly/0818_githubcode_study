# Visual Memory Translator 项目研究

> 把照片或一句话编译成“编辑式记忆页”的 Agent Skill；本研究固定上游版本，并直接完成照片预览、照片成品与文本隐喻三条能力实演。

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 上游项目 | `TanShilongMario/visual-memory-translator-SKILL` |
| 上游地址 | https://github.com/TanShilongMario/visual-memory-translator-SKILL |
| 研究版本 | `e0d04509a40e104a68ed9f3fbf5a779fe529d8c2` |
| 上游版本 | Skill `1.4` |
| 研究状态 | 已获取 · 基础能力已实演 |
| 开始日期 | 2026-08-19 |
| 最后更新 | 2026-08-19 |
| 本地上游 | `projects/visual-memory-translator/upstream/`（Git submodule） |
| 在线演示 | `projects/visual-memory-translator/showcase/` |
| 许可证 | MIT |

## 研究目标

- 理解仓库真实提供的是模型、代码还是 Agent 视觉编排能力。
- 直接执行 photo 与 text 两条主路径，不做 Skill 开关对照。
- 展示默认 6 格风格试衣间，以及从原图重新生成所选方向的流程。
- 说明可扩展接口、适用场景、模型依赖和产品化边界。

## 已完成的效果演示

### 照片路径

本研究先生成一张具有清晰前、中、远景的原创演示照片，再按上游默认交互执行：

1. 原始照片进入 `input_mode: photo`。
2. 未指定风格，因此生成 6 格 `preview_mode: auto` 风格预览。
3. 六个方向覆盖线稿水彩、极致抽象、分层贴纸、展览档案、长虹玻璃和结构解构。
4. 选择 `03 layered_sticker_reassembly`。
5. 成品重新使用原始照片生成，没有放大预览格。

演示参数：

```yaml
preset: layered_sticker_memory
input_mode: photo
preview_mode: auto
preview_count: 6
original_display_mode: extracted_sticker_layers
layout_mode: sticker_layer_reassembly
style_mode: layered_sticker_reassembly
layer_count: 3
whitespace_level: very_high
holiday_mode: skip
ratio: 3:4
```

### 文本路径

输入句子：

> 不是所有答案，都需要立刻被填满。

Skill 将它压缩成一个“空容器 + 停在入口前的线”隐喻，保持原句、单一视觉隐喻、一个强调色和大面积留白。

```yaml
input_mode: text
preview_mode: skip
original_display_mode: translation_only
layout_mode: large_whitespace_small_art
style_mode: editorial_metaphor_card
text_mode: user_text
whitespace_level: very_high
ratio: 3:4
```

## 核心结论

它不是图像模型或风格迁移算法，而是位于用户、视觉 Agent 与外部图像模型之间的艺术指导层：

```text
照片 / 句子
  → 输入路由与视觉理解
  → Display / Layout / Style / Abstraction 等参数选择
  → Prompt 合同与禁止项
  → 外部 ImageGen 生成像素
  → 质量清单与定向重试
```

仓库不包含 Python、JavaScript、模型权重、训练数据或确定性图像处理脚本。能力来自 Markdown 中的流程、参数、风格库和质检规则；真正生成像素的是宿主提供的图像模型。

## 演示观察

- 6 格预览在一次生成中正确完成了 2×3 网格、六种明显不同的视觉语言和同一场景约束。
- 分层贴纸成品正确保留了人物、建筑、水面与远山，并形成三张可区分的白边层。
- 文本隐喻卡正确保留了中文原句，只使用一个容器隐喻和一个强调色。
- 预览第 04 格又额外生成了一个大号 `4`。这违反“图内只放两位编号”的硬规则，说明精确文字、计数和复杂约束仍取决于底层模型，不是 Skill 能强制保证的确定性结果。

## 研究入口

- [能力、原理与真实边界](docs/analysis.md)
- [可扩展方向与使用场景](docs/use-cases-and-extension.md)
- [效果演示展厅](showcase/index.html)
- [完整生成记录](showcase/assets/generated/PROMPTS.md)
- [固定上游版本](upstream)

## 相对上游的新增内容

- 原创照片输入、6 格预览、分层贴纸成品和文本隐喻卡。
- 面向研究阅读的能力分层、实现边界与扩展地图。
- 可直接部署到 GitHub Pages 的静态效果展厅。
- 未修改上游 Skill，本项目的研究材料与生成资产均位于 submodule 外。

## 复现方式

此仓库本身没有可执行 CLI。要复现生成效果，需要：

1. 在支持 Agent Skills 与图像生成/编辑的宿主中加载 `upstream/visual-memory-translator/`。
2. 上传照片并调用“启用影像转译编辑器”，或直接提供一句待转译文本。
3. photo 路径未指定风格时先选择预览编号；成品必须回到原始照片生成。
4. 使用上游 `quality.md` 检查结果；每次只针对一个失败点重试。

本地查看展厅可直接打开 `showcase/index.html`，或用任意静态 HTTP 服务运行该目录。

