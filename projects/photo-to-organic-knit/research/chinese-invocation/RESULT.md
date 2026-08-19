# 中文调用测试

日期：2026-08-19
调用 Skill：已安装的 `$photo-to-conceptual-art`
图像执行：Codex 内置 ImageGen
输入：`showcase/assets/generated/pilot-product-source.png`

## 中文请求

```text
请使用 $photo-to-conceptual-art，把这张无品牌茶具照片制作成面向城市年轻消费者的秋季品牌活动 4:5 无字主视觉。强调安静、自然、手作，保留右上角标题空间；不要在图片内生成文字、Logo、产地、认证或产品功效声明。
```

## 自动路由

```text
seasonal-campaign → layered-paper → campaign-poster
```

路由原因：模块化纸层与负空间便于后续接入品牌字体和活动文案。

## 编译命令

```powershell
python -B C:\Users\yun68\.codex\skills\photo-to-conceptual-art\scripts\build_prompt.py `
  --essence E:\0818_codex_project\projects\photo-to-organic-knit\research\chinese-invocation\essence.json `
  --scenario seasonal-campaign `
  --effect auto `
  --format json
```

## 交给 ImageGen 的完整 Prompt

```text
Use case: style-transfer
Asset type: 4:5 Campaign Poster Key Art for Seasonal Campaign
Input image: Image 1 is the subject and semantic reference. Preserve required anchors and relationships; recompose rather than trace.
Source orientation: landscape 3:2. Delivery aspect: 4:5.
Audience: local customers and campaign viewers
Scenario goal: Create reusable brand-safe key art with a clear graphic hierarchy and generous space for exact campaign copy.
Subject: 一个无品牌的深绿色圆柱茶罐，与一把奶油色陶壶和两只茶杯组成安静的茶饮静物。
Anchors: 一个深绿色圆柱茶罐; 一把奶油色陶壶; 两只奶油色茶杯; 少量散茶叶; 一枝新鲜茶叶
Relationships: 茶罐是最高的主视觉锚点; 茶壶和两只杯子在茶罐旁形成稳定的三角关系; 散茶与鲜叶分别连接产品原料和自然气息
Emotion: 安静; 自然; 手作; 克制的品质感
Visual path: 视线从高处的绿色茶罐向右下移动，经过茶壶和两只杯子，最终停在鲜叶上。
Retain: 一个茶罐; 一把茶壶; 恰好两只茶杯; 深绿色与暖奶油色对比; 无品牌表面; 散茶和鲜叶
Transform from source: 圆柱茶罐轮廓; 茶具三角关系; 窗影与叶片节奏; 石质桌面层次
Discard: 墙面裂纹; 零散茶叶碎片细节; 写实石材噪点; 无关反射和背景信息
Concept: 一个封存茶叶的绿色容器，展开为两人共享的日常茶席。
Effect: Layered Paper Cut — Editorial hierarchy, clean negative space, and modular campaign composition
Materials: cotton paper; vellum; deckled paper; embossed paper
Path treatment: Turn the visual path into a continuous cut-paper ribbon with lifted deckled edges.
Form treatment: Reduce subjects into a few asymmetric overlapping paper planes and embossed motifs.
Space treatment: Let the background show between layers and preserve broad copy-safe paper fields.
Composition: Clear foreground, middle, and background planes with deliberate overlap and cast shadows. Reusable key art with one memorable silhouette and a deterministic copy zone.
Delivery safety: Reserve one broad low-detail field for brand, campaign title, date, and call to action.
Handmade variation: tiny cutting irregularities; lifted corners; subtle fiber variation; handmade embossing
Palette anchors: 森林深绿; 暖奶油色; 茶褐色; 浅石色; 鲜叶绿
Text policy: wordless-key-art; do not generate title, logo, date, metrics, price, legal copy, or call to action inside the art layer.
Scenario requirements: Preserve distinctive product or place anchors.; Remove incidental photographic noise.; Keep campaign copy outside the raster art.
Quality gates: brand-anchor retention; graphic hierarchy; copy-safe space; no generated brand text; copy-safe field; multi-crop resilience; no generated campaign text
Privacy: 不得生成品牌名、Logo、产地、认证标志或产品功效声明
Avoid: flat vector illustration; childlike construction paper; plastic 3D; continuous photo depth; excessive props; extra text; watermark; signature; unrelated objects.
```

该 Prompt 来自安装目录中的编译器输出，未进行人工翻译或补写。

## Review

评分器输入：`review.json`

```text
PASS — 34/35
pass=7 fail=0 unverified=0
```

七项必需门禁全部通过。`multi-crop resilience` 得 4/5：4:5 主版完整，宽横幅裁切会损失部分底部叶形，但核心产品组合仍可保留。

## 生产边界

结果是无字 Key Art。正式品牌名、活动标题、日期、价格、产品声明、字体许可和法律审核仍应在设计系统中完成。
