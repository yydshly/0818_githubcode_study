# Cross-subject pilot benchmark (n=3)

Date: 2026-08-19
Execution: built-in ImageGen
Mode: compiled `auto` route, one output per unseen synthetic source

## Purpose

Check whether the same target-driven Skill can route and generate across three source classes: person/relationship, product/still-life, and architecture/mobility.

This pilot does not estimate a production success rate. `3/3` is only the observed result for these three selected synthetic samples in this session.

## Source prompts

### Person and relationship

```text
Use case: photorealistic-natural
Asset type: unseen person-and-relationship source for a cross-subject Skill benchmark
Primary request: one East Asian father and his ten-year-old daughter sitting together at a plain wooden courtyard table repairing one red paper kite with a visible bamboo frame and one spool of blue string
Scene/backdrop: quiet ordinary courtyard with a pale wall, one open wooden doorway, and a small potted tree kept soft and secondary
Subject: exactly two people; both lean toward the same kite; father's hand steadies one bamboo spar while the child threads the blue string; faces and hands visible but naturally candid
Style/medium: photorealistic documentary family photography with real skin, paper, bamboo, string, cotton clothing, and worn wood textures
Composition/framing: landscape 3:2, medium-wide eye-level view; the diamond kite forms the center and the two bodies create a protective arc around it
Lighting/mood: soft morning shade, patient, collaborative, intimate, unstaged
Color palette: warm wood, cream wall, indigo clothing, red kite, blue string, muted green
Constraints: no text, no logos, no watermark, exactly two people, one kite, one string spool, no extra toys, no festive decorations, no fantasy elements
```

### Product still life

```text
Use case: product-mockup
Asset type: unseen product still-life source for a cross-subject Skill benchmark
Primary request: a premium but completely unbranded deep-green cylindrical loose-leaf tea tin beside one low matte-cream ceramic teapot and exactly two small cups, with a restrained scatter of dried tea leaves and one fresh tea branch
Scene/backdrop: warm pale stone tabletop against a simple off-white plaster wall, no packaging copy
Subject: one tea tin with a clean strong silhouette, one teapot, two cups arranged as a calm triangular family; the tin is the tallest focal object
Style/medium: photorealistic editorial product photography, authentic brushed metal, matte ceramic, dry leaves, stone grain, subtle imperfections
Composition/framing: landscape 3:2, straight-on slightly elevated view; generous clean negative space around the product group, especially above and to the right
Lighting/mood: soft angled morning window light, quiet, crafted, natural, premium without luxury gloss
Color palette: deep forest green, warm cream, tea brown, pale stone, small fresh green accent
Constraints: no text, no labels, no logo, no watermark, exactly one tin, one teapot, two cups, no food, no hands, no extra vessels, no decorative pattern
```

### Architecture and mobility

```text
Use case: photorealistic-natural
Asset type: unseen architecture-and-mobility source for a cross-subject Skill benchmark
Primary request: one bright red mountain cable car traveling along a single diagonal cable toward a compact brutalist concrete station embedded in a snowy rocky alpine pass
Scene/backdrop: broad snow fields, dark exposed rock, one concrete mountain station, pale winter sky, distant ridgeline kept simple
Subject: exactly one red cable car and one station; cable visibly connects them and defines a strong upward route; no visible people
Style/medium: photorealistic architectural travel photography, realistic painted metal, glass, concrete, snow and rock textures
Composition/framing: landscape 3:2, wide frame; cable begins in the lower left with the car and rises toward the station in the upper right; clear graphic diagonal
Lighting/mood: crisp cold morning light with long restrained shadows; purposeful, remote, engineered
Color palette: snow white, charcoal rock, concrete gray, bright red cable car, pale blue
Constraints: no text, no logos, no watermark, exactly one cable car, one station, one cable route, no skiers, no additional buildings, no dramatic avalanche or danger
```

## Compiler execution

```powershell
python scripts/build_prompt.py --essence forward-tests/pilot-n3/person-essence.json --scenario family-memory --effect auto --format json
python scripts/build_prompt.py --essence forward-tests/pilot-n3/product-essence.json --scenario seasonal-campaign --effect auto --format json
python scripts/build_prompt.py --essence forward-tests/pilot-n3/architecture-essence.json --scenario travel-cover --effect auto --format json
```

Each command's `prompt` field was passed to ImageGen without hand editing.

## Observed routes and results

| Source class | Auto route | Attempts | Gate result |
| --- | --- | ---: | --- |
| Person / relationship | `family-memory → organic-knit → book-cover` | 1 | pass |
| Product / still life | `seasonal-campaign → layered-paper → campaign-poster` | 1 | pass |
| Architecture / mobility | `travel-cover → woodcut → field-journal` | 1 | pass |

All three retained requested quantities and anchors, produced credible materials, remained wordless, and preserved the intended delivery-safe area. No correction pass was used.

## Important limitation

- Sources were generated specifically to make benchmark inputs legal and reproducible.
- Sample selection was deliberate, not random.
- Human review was performed on one output per sample.
- `3/3` therefore means only “all three pilot samples passed their declared gates.” It is not a model accuracy or production reliability claim.

## Skill change

None. Unlike the lighthouse test, this pilot did not reveal a repeated failure that justified changing a profile or universal instruction.
