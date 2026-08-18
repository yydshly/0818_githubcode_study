# 多风格应用实验

## 实验问题

同一个核心主题——“把混乱 Prompt 变成可复用视觉系统”——是否应该始终使用同一种画风？

答案是否定的。六幕主案例使用18号暖色扁平绘本，是为了建立连续品牌叙事；当传播任务变化时，画风也应该跟随任务变化，而不是只做外观换皮。

## 四种传播任务

| 风格 | 新生成文件 | 传播任务 | 最适合 | 不适合 |
| --- | --- | --- | --- | --- |
| 8 水墨写意 | `style-08-ink-archive.png` | 把方法论表达成文化与战略隐喻 | 深度文章封面、策略报告、知识体系、文化主题 | 精确操作教程、产品UI、逐步教学 |
| 9 复古像素 | `style-09-pixel-workflow.png` | 把研究流程表达成可完成的游戏关卡 | 新手引导、进度机制、开发者内容、社媒轮播 | 高端品牌、情绪叙事、严肃审计正文 |
| 13 北欧纸雕 | `style-13-paper-system.png` | 把系统结构表达成手工编辑主视觉 | 设计报告、发布会、展览、创意行业提案 | 密集数据、快速操作说明、写实人物故事 |
| 15 大鼻软偶 | `style-15-vinyl-researcher.png` | 把抽象项目变成可重复出现的角色IP | 头像、贴纸、短视频、栏目主持人、帮助入口 | 证据图、架构图、正式研究结论 |

## 生成方法

每张图都把上游对应样图作为 `style-only` 参考：只继承材质、笔触、形体和光影，不复制人物、动物、构图或故事。

## 最终提示词

### Style 08 · 水墨写意

```text
Use case: stylized-concept
Asset type: Style 08 application example — cultural and strategic research cover
Input images: Image 1 is a pure visual-style reference only. Do not copy its horse, pose, composition, or subject.
Primary request: translate the research idea “scattered prompts become an ordered visual system” into a Chinese expressive ink-wash metaphor. Show many loose paper slips and broken brush marks drifting from the lower-left like chaotic wind, then converging into a disciplined ascending path of ink-stone archive blocks and one calm open scroll at the upper-right. A small simplified scholar-researcher figure stands beside the path, observing the transformation rather than dominating the image.
Style/medium: Chinese xieyi ink wash matching Image 1’s bold black brush energy, dry-brush flying-white edges, five tonal levels of ink, splashes, controlled negative space, handmade xuan-paper texture.
Composition/framing: portrait 3:4 editorial cover, dynamic diagonal movement from chaos to order, large untouched paper areas, one clear focal scroll.
Color palette: black and gray ink on warm rice paper, exactly one small cinnabar-red seal-like square accent with no readable characters.
Mood: strategic, reflective, culturally grounded, decisive.
Meaning: suitable for essays about methodology, strategy, knowledge systems, or Chinese cultural topics.
Constraints: no words, letters, readable seal text, logos, watermarks, horses, photorealism, digital gradients, colorful illustration, detailed UI, or crowded background.
```

### Style 09 · 复古像素

```text
Use case: stylized-concept
Asset type: Style 09 application example — gamified research workflow poster
Input images: Image 1 is a pure pixel-art style reference only. Do not copy its cat, pose, blue background, or composition.
Primary request: turn the workflow “collect prompts → enter style archive → combine content and style → publish coherent assets” into one readable retro game level. Show a small researcher avatar with dark hair and navy clothing moving from left to right across four connected stations: collecting scattered card pickups, entering an archive shelf checkpoint, placing two differently colored cards into a compact crafting machine, and reaching a final display with four matching image tiles. Use simple arrows, platforms, coins or checkpoint lights to make progress intuitive without text.
Style/medium: authentic 8/16-bit pixel art matching Image 1’s hard square pixels, crisp block edges, limited palette, sprite-like proportions, zero anti-aliasing.
Composition/framing: landscape 4:3 game-screen composition, side-scrolling level with four clearly separated but connected zones, strong silhouette and readable path at thumbnail size.
Color palette: dark navy, misty blue, coral orange, warm cream, muted gold, very limited palette.
Mood: playful, motivating, systematic.
Meaning: suitable for onboarding, tutorials, progress trackers, coding/game audiences, and social carousels.
Constraints: no words, letters, numbers, score counters, logos, watermarks, cats, gradients, smooth vector edges, 3D lighting, realistic textures, or tiny illegible UI.
```

### Style 13 · 北欧纸雕

```text
Use case: stylized-concept
Asset type: Style 13 application example — editorial event and report key visual
Input images: Image 1 is a pure visual-style reference only. Do not copy its girl, hair spirals, cloud pedestal, pose, or composition.
Primary request: create a layered paper-sculpture metaphor for “turning scattered prompts into a reusable visual system.” At the center, a small paper researcher arranges loose paper image cards around a structured circular archive. Layered paper ribbons flow from the archive into three distinct finished assets: a cover card, a workflow card, and a story card. Use Scandinavian folk-inspired leaves, stars, nested circles, and curled paper strips to connect the system, but keep the research archive clearly readable as the focal structure.
Style/medium: handcrafted Nordic paper sculpture and quilling matching Image 1’s visible cut-paper edges, rolled paper depth, tactile fiber, soft cast shadows, editorial craft polish.
Composition/framing: square or near-square editorial poster, centered radial system, balanced negative space, strong silhouette suitable for a report cover, event poster, or exhibition panel.
Color palette: warm ochre-brown backdrop, deep violet, berry magenta, coral orange, muted teal, mustard gold, warm cream.
Lighting/mood: soft museum-like side lighting, warm, crafted, premium, imaginative.
Meaning: suitable for design-system launches, editorial reports, event key visuals, and creative-industry presentations.
Constraints: no words, letters, numbers, logos, watermarks, copied character, photoreal human skin, plastic 3D, glossy materials, flat vector look, or cluttered tiny labels.
```

### Style 15 · 大鼻软偶

```text
Use case: stylized-concept
Asset type: Style 15 application example — research-project mascot and character IP
Input images: Image 1 is a pure visual-style reference only. Do not copy its male identity, beanie, facial hair, coral sweater, pose, or framing.
Primary request: design a new soft-vinyl researcher mascot for the Hand-drawn Styles study. Create a gender-neutral adult character with a very large soft downward tubular nose, tiny narrow sleepy eyes, no eyebrows, rounded ears, and a calm curious expression. The mascot wears a deep-navy overshirt over a warm-cream collar, misty-blue wide trousers, and coral sneakers. One hand holds a fan of three visual-style cards; the other hand holds a small archive box containing neatly organized cards. Keep the silhouette simple and instantly recognizable.
Style/medium: premium matte soft-vinyl art toy matching Image 1’s smooth rounded geometry, soft rubber finish, subtle studio texture, minimal facial features, slightly deadpan charm.
Composition/framing: full-body or three-quarter character portrait, centered on a clean warm golden background, generous padding, product-character presentation suitable for an avatar, sticker, short-video cover, or section mascot.
Lighting/mood: soft studio light, warm, playful, clever, approachable.
Color palette: deep navy, misty blue, coral orange, warm cream, muted gold.
Meaning: suitable for project avatars, recurring helper characters, stickers, social thumbnails, and short-video explainers.
Constraints: no words, letters, numbers, logos, watermarks, copied beanie, facial hair, photoreal skin, realistic human anatomy, glossy plastic, complex background, extra people, or large anime eyes.
```
