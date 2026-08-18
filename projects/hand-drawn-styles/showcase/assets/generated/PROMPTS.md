# Final ImageGen prompts

执行方式：ChatGPT 内置 `image_gen`。

六幕连续案例的5张新增场景使用 `project-cover.png` 作为角色/画风锚点，并从第04幕起同时携带前一幕作为连续性参考。完整逐幕提示词见 [`STORY.md`](STORY.md)。

水墨、像素、纸雕和软偶4种传播任务样例的提示词见 [`MULTI-STYLE.md`](MULTI-STYLE.md)。

## `project-cover.png`

```text
Use case: illustration-story
Asset type: portrait website hero and research project cover
Primary request: create a meaningful cover illustration for a research project about turning scattered image prompts into a controlled, reusable visual style system
Scene/backdrop: vast warm near-white paper background with generous calm negative space
Subject: one thoughtful researcher at a table organizes many loose prompt cards and hand-drawn sample sheets into a tidy numbered archive; a clear curved visual path connects the archive to one glowing image-generation frame showing a single finished illustration; the relationship should read instantly as scattered prompts becoming a repeatable visual contract
Style/medium: clean contemporary flat picture-book illustration built from large rounded geometric silhouettes, almost no continuous outer contour lines, smooth matte local colors with barely perceptible paper softness
Composition/framing: portrait 4:5, full scene centered in the lower-middle, clear silhouette, large empty upper area suitable for surrounding website copy but do not draw any text
Color palette: deep navy, misty blue, coral orange, golden orange, warm peach, warm near-white only
Mood: intelligent, warm, organized, quietly optimistic
Constraints: no words, no letters, no numbers, no logos, no watermark; no UI screenshot; no photorealism; no glossy 3D; the archive and transformation path must be visually understandable without labels
```

## `method-explainer.png`

```text
Use case: infographic-diagram
Asset type: portrait website section illustration explaining a workflow
Primary request: create a four-panel hand-drawn visual explainer showing how an image request becomes a controlled generated image
Scene/backdrop: warm off-white paper, four stacked panels separated by thin hand-drawn black lines
Subject: the same simple round black bean-like helper character appears in every panel; panel 1 gathers scattered idea cards, panel 2 places the cards into a clearly organized style archive, panel 3 combines one content card with one selected style card through a small hand-drawn funnel or assembly device, panel 4 presents one clean finished illustration in a frame; use curved arrows to make the top-to-bottom sequence unmistakable
Style/medium: minimalist black marker doodle infographic, wobbly closed outlines, outline-only objects with white interiors, solid black helper character with two white dot eyes
Composition/framing: vertical 3:4 poster, four balanced stacked panels, large whitespace, actions readable at thumbnail size
Color palette: black and warm off-white, with coral-orange used only on the selected style card and final image glow
Mood: clear, practical, friendly
Constraints: no words, no letters, no numbers, no fake labels, no logos, no watermark; no shading; no gradients; no extra colors; the flow must be understandable without text
```

## `milestone-story.png`

```text
Use case: illustration-story
Asset type: portrait website section illustration for a research milestone story
Primary request: illustrate the idea that failed examples are valuable evidence in an AI research project
Scene/backdrop: clean warm white paper with very large negative space and only a sparse evidence wall
Subject: two teammates late in the evening stand beside a simple evidence wall; one person carefully pins a visibly imperfect failed image sheet back onto the wall instead of discarding it, while the other records the finding in a notebook; several earlier attempt sheets are loosely arranged, and one single coral-orange sticky note becomes the emotional focal point
Style/medium: delicate emotional narrative sketch, loose indigo-blue pen search lines with very light transparent watercolor, human proportions, understated expressions, intentionally hand-drawn rather than digitally polished
Composition/framing: portrait 3:4, people concentrated in the lower-left and middle, evidence wall readable as the key prop, generous empty paper around them
Color palette: indigo and pale blue-gray linework, warm white paper, exactly one saturated coral-orange sticky note, tiny soft cheek blush only
Mood: thoughtful, honest, quietly hopeful after a failed experiment
Constraints: no words, no letters, no numbers, no logos, no watermark; no dense hatching; no fully painted background; no anime faces; no glossy digital finish; preserve the single orange focal object
```
