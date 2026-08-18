# Stamp Edge Skill 项目研究

> 一个把普通图片稳定处理为“邮票齿孔卡片”的微型 Agent Skill；本研究重点验证它的真实效果、实现边界，以及如何扩展为通用图片风格化引擎。

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 上游项目 | `xianxie6/stamp-edge-skill` |
| 上游地址 | https://github.com/xianxie6/stamp-edge-skill |
| 研究版本 | `2b89ce823aa589e912fcfbb9b529fa893142ab63`（v1.2.0 内容） |
| 研究状态 | 已复现并收口；仅保留未来可选方向 |
| 开始日期 | 2026-08-18 |
| 最后更新 | 2026-08-19 |
| 本地实验 | `projects/stamp-edge-skill/` |
| 在线演示 | `projects/stamp-edge-skill/showcase/`（合并到 `main` 后由 Pages 发布） |

## 一句话结论

它不是图像生成模型，而是 **`SKILL.md` 自然语言路由 + 两个 Pillow 确定性脚本**：一个雕刻邮票齿孔、透明画布和投影，另一个把多张结果贪心排成瀑布流合集。

## 已验证能力

| 能力 | 上游入口 | 本地复现 |
| --- | --- | --- |
| 无白边透明邮票 | `stamp_effect.py input output` | 六张 `outputs-v2/*-stamp.png` |
| 白色纸边 | `stamp_effect.py input output margin` | `travel-coast-margin.png`、`social-travel-story-margin.png` |
| 浅灰白成品背景 | `stamp_effect.py input output bg` | `travel-coast-bg.png` |
| 参数组合 | `margin bg` | 源码与 CLI 路径确认 |
| 默认多图瀑布流 | `stamp_sheet.py` | `collection-dark-4col.png` |
| 自定义多图瀑布流 | `stamp_sheet.py --cols 3 --bg ...` | `collection-paper-3col.png` |
| Agent 自然语言触发 | `SKILL.md` | 触发词与执行协议审阅完成 |

新版展示使用四张 OpenAI 内置 ImageGen 原创摄影，以及由本地脚本确定性组装的社交长帖和编辑海报。全部邮票与合集仍由固定的上游源码生成，没有修改上游效果算法。图片提示词归档在 `demo/PROMPTS.md`。

## 本地扩展能力

在不修改上游的前提下，`extension/image-style-skill/` 已实现统一 Pillow CLI 和六个可运行 preset：

| Preset | 效果 | 关键边界 |
| --- | --- | --- |
| `polaroid` | 拍立得暖白纸框和题注 | 保留完整画幅 |
| `torn-paper` | 不规则撕纸 Alpha 边缘 | `--seed` 可复现 |
| `film-frame` | 黑色片框、透明齿孔和帧号 | 不改变图片内容 |
| `ticket` | 横向旅行票券与票根信息区 | 会按票券画幅裁切 |
| `riso-print` | 蓝红双色、错版和网点 | 确定性印刷模拟 |
| `sticker-outline` | 围绕已有 Alpha 的白色轮廓 | 不提供自动抠图 |

## 快速复现

从仓库根目录执行：

```powershell
git submodule update --init --recursive
python -m venv projects/stamp-edge-skill/.venv
projects\stamp-edge-skill\.venv\Scripts\python.exe -m pip install -r projects\stamp-edge-skill\requirements.txt
projects\stamp-edge-skill\.venv\Scripts\python.exe projects\stamp-edge-skill\demo\generate_demo.py
projects\stamp-edge-skill\.venv\Scripts\python.exe projects\stamp-edge-skill\extension\image-style-skill\scripts\generate_demo.py
projects\stamp-edge-skill\.venv\Scripts\python.exe projects\stamp-edge-skill\extension\image-style-skill\tests\test_presets.py
projects\stamp-edge-skill\.venv\Scripts\python.exe projects\stamp-edge-skill\tests\verify_project.py
```

macOS/Linux 将虚拟环境解释器替换为：

```bash
projects/stamp-edge-skill/.venv/bin/python
```

直接查看静态展厅：

```powershell
python -m http.server 8000
# http://127.0.0.1:8000/projects/stamp-edge-skill/showcase/
```

## 研究目录

```text
projects/stamp-edge-skill/
├── upstream/                  # Git submodule：未修改的上游版本
├── demo/generate_demo.py      # 生成本地输入并调用上游脚本
├── demo/PROMPTS.md            # 四张原创摄影素材提示词归档
├── docs/analysis.md           # 能力、算法、实验与限制
├── docs/extension-roadmap.md  # 通用图片风格引擎扩展设计
├── extension/image-style-skill/
│   ├── SKILL.md               # Agent 触发、路由与能力边界
│   ├── scripts/style_effects.py
│   └── tests/test_presets.py
├── showcase/                  # 可部署的效果展厅
├── tests/verify_project.py    # 文件、图片合同和站点集成检查
└── requirements.txt           # 固定复现依赖
```

## 上游与本地修改边界

- `upstream/` 固定在 `2b89ce823aa589e912fcfbb9b529fa893142ab63`，没有修改上游源码。
- 本地新增的 Demo 输入、展厅、测试和文档属于研究仓库产物。
- 当前固定版本的上游根目录没有 `LICENSE` 文件。研究仓库使用 submodule 保存来源与 commit 关系，不将上游源码复制进本仓库历史；商用、修改或再分发前应先取得明确许可。

## 研究收口

当前研究已经完成能力确认、真实场景复现、合集展示、六个扩展 preset、Skill 包装和自动化验证，不再继续实现 `stamp-v2` 或更多相似滤镜。

未来如果出现真实使用需求，可从四个方向恢复：核心画质、批量工作流、邮票语义元素和可选 AI。它们仅作为探索索引，不属于当前已实现能力或后续承诺。

## 推荐阅读

- [能力、原理与限制](docs/analysis.md)
- [从邮票效果扩展为图片风格系统](docs/extension-roadmap.md)
- [Demo 生成说明](demo/README.md)
- [ImageGen 提示词归档](demo/PROMPTS.md)
- [已实现的扩展 Skill](extension/image-style-skill/SKILL.md)
- [可视化展厅](showcase/index.html)
