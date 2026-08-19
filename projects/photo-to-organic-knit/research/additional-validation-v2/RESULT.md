# Additional Skill validation samples v2

日期：2026-08-19
执行：正式安装的 `$photo-to-conceptual-art` + 内置 ImageGen
样本：3 个新生成的合成源图

## 路由

| 样本 | 路由模式 | Scenario → Effect → Delivery | 尝试 | Review |
| --- | --- | --- | ---: | ---: |
| 家庭宠物照料 | auto | `family-memory → organic-knit → book-cover` | 1 | 35/35 |
| 社区雨水花园 | auto | `impact-report → stained-glass → impact-report` | 1 | 35/35 |
| 无品牌蜂蜜产品 | explicit override | `seasonal-campaign → ceramic-relief → campaign-poster` | 1 | 34/35 |

三个 ImageGen Prompt 均由安装目录中的编译器从对应中文 Essence 生成，未进行人工翻译或补写。

## 为什么保留源图

网页和本目录同时保留 `*-source.png` 与处理结果，方便直接检查：

- 数量和主体是否保留；
- 关系、路径和色彩锚点是否发生合理转化；
- 背景细节是否被主动舍弃；
- 结果是否只是表面滤镜。

## 观察

- 针织样例保留两人一犬和共同照料关系，并形成书封标题区。
- 彩玻璃样例保留四人、蓝色雨桶和水道循环，底部形成报告层级空间。
- 陶瓷浮雕样例证明显式效果覆盖可用，保留一个罐、蜂蜜棒、蜂巢与野花，并形成右上文案区。

## 限制

这是有意选择的合成 `n=3` 样本。分数来自公开人工 Review，不能解释为模型准确率、真实用户照片成功率或商业发布质量。
