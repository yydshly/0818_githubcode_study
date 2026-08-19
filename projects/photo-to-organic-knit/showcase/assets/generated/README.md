# Generated demo assets

本目录保存研究展厅使用的独立演示资产。两张图片均由 2026-08-19 的 Codex 内置 ImageGen 生成并复制到工作区。

| 文件 | 角色 | 说明 |
| --- | --- | --- |
| `canoe-source.png` | 输入照片 | 无外部摄影版权依赖的横版旅行场景 |
| `canoe-organic-knit.png` | Skill 输出 | 以输入照片和上游 `style-reference.png` 为参考，按上游工作流重构 |
| `canoe-paper-cut.png` | 扩展效果 | 分层棉纸、描图纸和毛边剪纸 |
| `canoe-ceramic-relief.png` | 扩展效果 | 手塑石陶浮雕与釉色河槽 |
| `canoe-stained-glass.png` | 扩展效果 | 手工玻璃、铅线与透光色块 |
| `canoe-woodcut.png` | 扩展效果 | 双色减版木刻和高对比刀痕 |
| `canoe-miniature-diorama.png` | 扩展效果 | 树脂、软木、石膏和棉雾微缩模型 |
| `scenario-family-source.png` | 场景源图 | 家庭成长册：祖孙共读与橘猫 |
| `scenario-family-knit.png` | 场景结果 | 家庭成长册 × 有机针织 |
| `scenario-community-source.png` | 场景源图 | 公益报告：五人共同种树 |
| `scenario-community-glass.png` | 场景结果 | 公益报告 × 彩色玻璃 |
| `scenario-bakery-source.png` | 场景源图 | 独立品牌：街角面包店 |
| `scenario-bakery-paper.png` | 场景结果 | 季节活动 KV × 分层剪纸 |
| `forward-lighthouse-source.png` | 前向测试源图 | 未见海岸骑行照片 |
| `forward-lighthouse-auto-woodcut.png` | 首轮自动结果 | 木刻；元数据安全区失败 |
| `forward-lighthouse-auto-woodcut-v2.png` | 最终自动结果 | 木刻；针对安全区修正后通过 |
| `forward-lighthouse-override-paper.png` | 首轮覆盖结果 | 剪纸；元数据安全区失败 |
| `forward-lighthouse-override-paper-v2.png` | 最终覆盖结果 | 剪纸；针对安全区修正后通过 |
| `pilot-person-source.png` | Pilot 源图 | 人物关系：父女修风筝 |
| `pilot-person-auto-knit.png` | Pilot 结果 | 家庭纪念自动路由为针织书封 |
| `pilot-product-source.png` | Pilot 源图 | 产品静物：无品牌茶具组合 |
| `pilot-product-auto-paper.png` | Pilot 结果 | 季节活动自动路由为剪纸海报 |
| `pilot-architecture-source.png` | Pilot 源图 | 建筑交通：雪山缆车与山站 |
| `pilot-architecture-auto-woodcut.png` | Pilot 结果 | 旅行内容自动路由为木刻日志 |

针织提示与设计决策见 [PROMPTS.md](PROMPTS.md)，五种扩展效果见 [MULTI_EFFECT_PROMPTS.md](MULTI_EFFECT_PROMPTS.md)，目标场景案例见 [SCENARIO_PROMPTS.md](SCENARIO_PROMPTS.md)。

未见照片前向测试的 Essence、路由、修正和评分见 `../../../extension/photo-to-conceptual-art/forward-tests/lighthouse-travel/`。

跨题材 `n=3` Pilot 的 Essence、路由与限制见 `../../../extension/photo-to-conceptual-art/forward-tests/pilot-n3/`。

这些资产用于研究展示，不代表上游作者生成或背书。上游自带案例仍位于 submodule 的 `upstream/assets/`。
