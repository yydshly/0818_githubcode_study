# Demo 生成说明

第二版 Demo 不再使用抽象几何卡片，而是使用六类真实内容场景：

1. 海岸旅行摄影；
2. 雨中现代建筑；
3. 早餐静物；
4. 植物温室；
5. 旅行社交长帖；
6. 建筑编辑海报。

前四张照片由 OpenAI 内置 ImageGen 生成并保存到
`showcase/assets/demo/sources/`；后两张由 `generate_demo.py` 使用这些照片和
Pillow 确定性组装。随后脚本调用固定在 `../upstream/` 的原版
`stamp_effect.py` 与 `stamp_sheet.py` 生成全部邮票和合集。

## 复现

```powershell
python -m pip install -r projects/stamp-edge-skill/requirements.txt
python projects/stamp-edge-skill/demo/generate_demo.py
```

主要输出位于 `showcase/assets/demo/outputs-v2/`：

- `*-stamp.png`：六张默认透明邮票；
- `travel-coast-margin.png`：白色纸边变体；
- `travel-coast-bg.png`：浅灰白成品背景变体；
- `social-travel-story-margin.png`：长帖白边变体；
- `collection-dark-4col.png`：对应上游 README 默认 4 列深色合集；
- `collection-paper-3col.png`：对应自定义 3 列纸色合集。

`showcase/assets/demo/manifest.json` 记录场景、来源、处理模式和固定上游版本。
脚本不会修改上游源码。

## 扩展效果 Demo

基础邮票 Demo 完成后，可继续运行：

```powershell
python projects/stamp-edge-skill/extension/image-style-skill/scripts/generate_demo.py
```

它会通过统一 CLI 生成拍立得、撕纸、胶片、票券、Riso 印刷和轮廓贴纸，输出到
`showcase/assets/extensions/`，并使用上游 `stamp_sheet.py` 生成三列混合效果合集。
