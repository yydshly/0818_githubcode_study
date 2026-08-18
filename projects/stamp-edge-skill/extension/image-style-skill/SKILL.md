---
name: image-style-presets
description: 用确定性的 Pillow 预设把本地图片处理成拍立得、撕纸、胶片、票券、Riso 印刷或已有 Alpha 的轮廓贴纸。当用户要求这些具体效果、需要离线可复现输出，或想把图片做成一组混合风格素材时使用；不用于自动抠图或生成式改画。
---

# Image Style Presets

将用户意图映射到本目录 `scripts/style_effects.py` 的一个 preset：

- `polaroid`：拍立得纸框和底部题注区；
- `torn-paper`：不规则撕纸 Alpha 边缘；
- `film-frame`：黑色胶片框和透明齿孔；
- `ticket`：带侧边缺口和票根信息区的横向票券；
- `riso-print`：纸色底、双色映射、错版边缘和网点；
- `sticker-outline`：围绕输入 Alpha 扩展白色轮廓。若输入没有透明主体，不要宣称它能自动识别主体。

运行：

```bash
python scripts/style_effects.py <input> <output.png> --preset <name>
```

`polaroid` 和 `ticket` 可传 `--caption "..."`；撕纸形状可用 `--seed` 保持可复现变化。详细参数和选择依据见 [references/presets.md](references/presets.md)。

输出统一为 PNG。执行后检查图片模式、透明边缘、阴影是否裁切，以及所选 preset 是否匹配用户场景。批量任务逐张运行同一 CLI，再按需要调用上游 `stamp_sheet.py` 组成合集。

该扩展不修改 `stamp-edge-skill` 上游源码。用户只要求邮票边时继续使用原始 `stamp_effect.py`，不要改由本扩展模拟。
