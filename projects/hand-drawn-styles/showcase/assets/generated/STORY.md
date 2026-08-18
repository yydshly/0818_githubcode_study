# 连续案例：从混乱样图到可发布视觉系统

## 案例背景

GitHub Code Study 准备发布第二个研究项目 `hand-drawn-styles`。团队已经拥有大量上游风格样图，但这些图片彼此独立，只能回答“这种风格长什么样”，不能形成项目自己的视觉叙事。

问题不是缺图片，而是缺少：

- 图片之间的共同角色和视觉语言；
- 每张图片出现的原因；
- 前一张如何导致下一张；
- 最后形成什么可复用成果。

## 任务

把“研究一个 Prompt 风格库”讲成一个六幕连续故事：一位研究者先发现输出混乱，再建立档案、进行场景路由、组装生成合同、保留失败证据，最后发布一套统一视觉资产。

## 角色与视觉合同

| 字段 | 固定内容 |
| --- | --- |
| 主角 | `project-cover.png` 中的成年女性研究者 |
| 身份特征 | 黑色紧凑发髻、侧边碎发、极小深色眼睛、暖桃肤色 |
| 服装 | 深藏青长袖上衣与深藏青长裤 |
| 画风 | 当代扁平绘本、大块圆润几何形、极少描边、哑光局部色 |
| 色板 | 深藏青、雾蓝、珊瑚橙、金橙、暖桃、暖白 |
| 纸面 | 暖白、细微非涂布纸柔感、大留白 |
| 文字策略 | 图片内不生成文字；准确标题、原因和结果由 HTML 承担 |

## 六幕因果链

| 幕 | 文件 | 发生原因 | 画面行动 | 得到结果 | 下一幕 |
| --- | --- | --- | --- | --- | --- |
| 01 发现混乱 | `story-01-problem.png` | 同一项目的输出像来自不同品牌 | 研究者拿起两张风格不一致的图片进行比较 | 问题被定义为“缺少共同视觉语言” | 不能继续随机生成，必须先建立档案 |
| 02 建立档案 | `project-cover.png` | 图片多但不可检索、不可复用 | 研究者把散乱提示卡整理进编号风格盒 | 风格成为可选择的视觉资产 | 有了档案，下一步是按任务选风格 |
| 03 场景路由 | `story-03-route.png` | 不是所有任务都适合同一种画法 | 研究者把内容任务卡与一张珊瑚橙风格卡配对 | 风格选择从个人感觉变成任务路由 | 已选内容与风格需要被组装成正式请求 |
| 04 组装合同 | `story-04-assemble.png` | 单独写风格名仍会发生漂移 | 研究者将内容卡、风格卡和规则卡送入组装流程 | 得到受控且可重复的生成请求 | 第一张图仍可能有缺陷，需要回归检查 |
| 05 保留失败 | `story-05-review.png` | 首次生成过于统一、缺少目标细节 | 研究者并排保留失败图与修正图，并把失败连接到规则更新 | 失败不再被丢弃，而是成为回归证据 | 规则稳定后才能生产成套资产 |
| 06 发布系列 | `story-06-publish.png` | 配方、路由和修正规则已经稳定 | 研究者展示封面、流程图、故事图、分享卡组成的同一视觉家族 | 项目获得可持续复用的视觉系统 | 新内容可以沿同一流程继续扩展 |

## 生成关系

```text
project-cover.png（角色与画风锚点）
├── story-01-problem.png
├── story-03-route.png
│   └── story-04-assemble.png
│       └── story-05-review.png
│           └── story-06-publish.png
└── 作为第 02 幕直接复用
```

每个新场景都使用 `project-cover.png` 作为固定角色/画风参考，并从第04幕开始同时携带前一幕作为故事连续性参考。

## 最终生成提示词

### Scene 01 · 发现混乱

```text
Use case: illustration-story
Asset type: Scene 01 of a six-scene connected research case
Input images: Image 1 is the approved character and visual-style anchor only. Generate a new scene; do not edit or copy its composition.
Story background: before the researcher creates an organized visual archive, the project has many unrelated image outputs and no shared visual language.
Primary request: show the same researcher from Image 1 at the beginning of the story, seated at a worktable and looking concerned at a chaotic spread of visibly inconsistent generated-image sheets: one sheet looks like a rough black doodle, one like a soft watercolor, one like a toy-like 3D render, one like a flat illustration. She holds two sheets side by side and realizes they do not belong to the same project.
Character invariants: same adult woman, same black hair in a compact bun with loose side strands, same tiny dark eyes and warm peach skin, same deep-navy long-sleeve top, same gentle geometric proportions. Do not redesign her face, hair, age, outfit, or body proportions.
Style invariants: same clean contemporary flat picture-book illustration as Image 1; large rounded geometric silhouettes; almost no continuous outlines; smooth matte local colors; barely perceptible uncoated-paper softness.
Composition/framing: portrait 4:5, researcher in the lower-middle, chaotic sheets clearly visible around her, large calm negative space above; new composition distinct from Image 1.
Color palette: deep navy, misty blue, coral orange, golden orange, warm peach, warm near-white only.
Mood: confused but observant—the moment a real problem is discovered, not despair.
Constraints: no words, letters, numbers, logos, watermarks, UI screenshot, photorealism, glossy 3D scene, or extra people. Miniature styles may differ only inside the paper sheets; the overall frame must remain in the anchor style.
```

### Scene 02 · 建立档案

直接复用 `project-cover.png`；原始提示词见 [`PROMPTS.md`](PROMPTS.md)。

### Scene 03 · 场景路由

```text
Use case: illustration-story
Asset type: Scene 03 of a six-scene connected research case
Input images: Image 1 is both the approved character/style anchor and the previous story frame. Generate a new distinct scene after the archive has been built; do not edit Image 1 or reuse its composition.
Story continuity: in Scene 01 the researcher discovered inconsistent images; in Scene 02 she organized them into a reusable visual archive. Now she must choose the right visual language for a specific communication task.
Primary request: show the same researcher standing at a clean wall of organized visual-style cards. In one hand she holds a simple content brief card illustrated with a small research-table symbol; with the other hand she deliberately selects one coral-orange style card from several visibly different but neatly organized visual options. Place the chosen content card and style card close together so the routing decision is obvious without text.
Character invariants: same adult woman, same compact black hair bun and loose side strands, same face, age, tiny dark eyes, warm peach skin, deep-navy long-sleeve top, and gentle geometric proportions as Image 1.
Style invariants: same clean contemporary flat picture-book illustration, large rounded geometric silhouettes, almost no outlines, smooth matte colors, subtle paper softness.
Composition/framing: portrait 4:5, full or three-quarter body, organized style wall on one side and a clear area where the two chosen cards meet; distinct from prior scenes; generous warm-white negative space.
Color palette: deep navy, misty blue, coral orange, golden orange, warm peach, warm near-white only. Coral orange marks only the selected style.
Mood: focused and decisive—the project now has a rule for choosing, not guessing.
Constraints: no words, letters, numbers, logos, watermarks, extra people, UI screenshot, photorealism, or glossy 3D. Preserve character identity and outfit exactly.
```

### Scene 04 · 组装合同

```text
Use case: illustration-story
Asset type: Scene 04 of a six-scene connected research case
Input images: Image 1 is the approved character/style anchor. Image 2 is the previous routing scene. Generate a new scene; do not edit either reference or copy their compositions.
Story continuity: the researcher discovered inconsistent outputs, built a visual archive, then selected one content brief and one coral-orange style card. Now she assembles them into a controlled generation request.
Primary request: show the same researcher at a simple tabletop assembly station. She places the content brief card and the selected coral-orange style card into two separate slots of a friendly, non-technical visual assembly device. A clear curved path joins the two inputs, passes through a tidy stack of rule cards, and reaches one framed output illustration that visibly uses the selected blue-orange visual language. Her posture shows careful control rather than magical surprise.
Character invariants: same woman, compact black bun with loose side strands, identical face and age, tiny dark eyes, warm peach skin, deep-navy long-sleeve top and matching navy trousers, same gentle geometric body proportions.
Style invariants: same clean contemporary flat picture-book illustration; large rounded geometric silhouettes; minimal outlines; smooth matte local colors; barely perceptible paper softness.
Composition/framing: portrait 4:5, three-quarter view at the tabletop, inputs on one side and finished framed output on the other, visual flow readable without labels; distinct composition from prior scenes; generous warm-white negative space.
Color palette: deep navy, misty blue, coral orange, golden orange, warm peach, warm near-white only. Coral orange identifies the selected style and follows the path into the final output.
Mood: methodical and satisfying—the project now has a repeatable assembly process.
Constraints: no words, letters, numbers, logos, watermarks, extra people, realistic computer UI, photorealism, glossy 3D, fantasy magic, or redesigned clothing.
```

### Scene 05 · 保留失败

```text
Use case: illustration-story
Asset type: Scene 05 of a six-scene connected research case
Input images: Image 1 is the approved character/style anchor. Image 2 is the previous assembly scene. Generate a new distinct scene; do not edit the references.
Story continuity: the researcher assembled a controlled request and received an output, but a first result still contains a visible style defect. Instead of deleting it, she keeps it as evidence and corrects the process.
Primary request: show the same researcher at a sparse evidence wall. She pins one visibly imperfect output sheet to the wall beside a cleaner corrected output sheet. The failed sheet should look too uniform and generic inside its miniature image, while the corrected sheet clearly uses the chosen blue-orange language. She places one coral-orange evidence card beneath the failed sheet and uses a navy pencil to mark a connection from the failure to a small stack of revised rule cards on the table. Her expression is attentive and constructive.
Character invariants: same woman, compact black bun with loose side strands, identical face and age, tiny dark eyes, warm peach skin, deep-navy long-sleeve top and navy trousers, same geometric body proportions.
Style invariants: same clean contemporary flat picture-book illustration; rounded geometric silhouettes; minimal outlines; matte local colors; subtle warm paper texture.
Composition/framing: portrait 4:5, evidence wall and two contrasting output sheets clearly readable, researcher in three-quarter view, revised rule cards visible, large warm-white negative space; distinct composition from prior scenes.
Color palette: deep navy, misty blue, coral orange, golden orange, warm peach, warm near-white only. The single coral-orange evidence card is the focal point.
Mood: honest, analytical, quietly optimistic—failure becomes reusable knowledge.
Constraints: no words, letters, numbers, logos, watermarks, extra people, realistic UI, photorealism, glossy 3D, shame or frustration. Preserve character identity and outfit exactly.
```

### Scene 06 · 发布系列

```text
Use case: illustration-story
Asset type: Scene 06, the final scene of a six-scene connected research case
Input images: Image 1 is the approved character/style anchor. Image 2 is the previous review scene. Generate a new final scene; do not edit the references.
Story continuity: the researcher found inconsistent outputs, built a style archive, routed a task, assembled a controlled request, and converted a failed result into revised rules. Now the project is ready to publish as a coherent visual system.
Primary request: show the same researcher standing proudly but calmly beside a clean presentation wall containing a coordinated family of four finished assets: a project cover, a four-step workflow illustration, an evidence-wall story image, and a compact sharing card. All four assets should clearly belong to the same blue-orange visual family while having different compositions and purposes. On a nearby table, the organized archive box and a small stack of reusable rule cards remain visible, connecting the final result back to the process.
Character invariants: same woman, compact black bun with loose side strands, identical face and age, tiny dark eyes, warm peach skin, deep-navy long-sleeve top and navy trousers, same gentle geometric proportions.
Style invariants: same clean contemporary flat picture-book illustration, rounded geometric silhouettes, almost no outlines, smooth matte local colors, subtle warm-paper softness.
Composition/framing: portrait 4:5, researcher on one side and the coherent asset family clearly visible on the other, open celebratory negative space, distinct from previous scenes.
Color palette: deep navy, misty blue, coral orange, golden orange, warm peach, warm near-white only; consistent across every miniature asset.
Mood: complete, credible, quietly proud—not a party, but a system ready for repeated use.
Constraints: no words, letters, numbers, logos, watermarks, extra people, realistic website UI, photorealism, glossy 3D, confetti, trophies, or redesigned clothing. Preserve character identity exactly.
```
