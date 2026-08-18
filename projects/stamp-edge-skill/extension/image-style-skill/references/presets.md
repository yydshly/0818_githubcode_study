# Preset 选择与参数

| Preset | 最适合 | 关键行为 | 输出透明性 |
| --- | --- | --- | --- |
| `polaroid` | 旅行、人物、活动照片 | 暖白纸框、加厚底边、题注 | 外部透明 |
| `torn-paper` | moodboard、自然笔记、拼贴 | 可复现不规则纸边、柔和投影 | 外部与撕裂边透明 |
| `film-frame` | 建筑、街拍、连续叙事 | 黑色框、上下透明齿孔、帧号 | 外部和齿孔透明 |
| `ticket` | 旅行、活动、展览、优惠券 | 横向裁切、侧边缺口、票根区 | 外部与缺口透明 |
| `riso-print` | 海报、静物、编辑图片 | 蓝红双色、错版边缘、网点和纸色 | 外部透明，纸面不透明 |
| `sticker-outline` | 已抠图 PNG、已有形状素材 | Alpha 膨胀成白色轮廓和投影 | 外部透明 |

## CLI

```bash
python scripts/style_effects.py input.jpg output.png --preset polaroid --caption "SUMMER / 2026"
python scripts/style_effects.py input.jpg output.png --preset torn-paper --seed 42
python scripts/style_effects.py input.jpg output.png --preset film-frame
python scripts/style_effects.py input.jpg output.png --preset ticket --caption "FIELD PASS"
python scripts/style_effects.py input.jpg output.png --preset riso-print --seed 24
python scripts/style_effects.py transparent.png output.png --preset sticker-outline
```

所有 preset 都只使用 Pillow，不调用网络或图像模型。`ticket` 会为了横向票券构图裁切输入；其他预设尽量保留完整画幅。
