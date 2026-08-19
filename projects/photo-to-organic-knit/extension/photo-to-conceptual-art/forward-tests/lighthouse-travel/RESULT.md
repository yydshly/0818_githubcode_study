# Unseen-photo forward test: lighthouse travel cover

Date: 2026-08-19
Execution: built-in ImageGen
Scenario: `travel-cover`
Delivery: `field-journal`

## Test question

Does automatic `woodcut` routing better satisfy route clarity and thumbnail recognition than a valid `layered-paper` override when both receive the same unseen photo, essence, delivery, and quality gates?

## Source generation prompt

```text
Use case: photorealistic-natural
Asset type: unseen source photograph for a forward test of a goal-driven travel-cover Skill
Primary request: one lone adult cyclist in a burnt-orange wind jacket walking beside a sea-green touring bicycle along a narrow curving coastal path toward a small white lighthouse on a distant headland
Scene/backdrop: windswept northern coastline, dark slate sea cliffs, silver-blue ocean, long pale grasses bending in the wind, low layered clouds
Subject: exactly one traveler and one bicycle; traveler seen from behind at medium distance; lighthouse clearly recognizable but small
Style/medium: photorealistic editorial outdoor travel photography, realistic fabric, metal bicycle frame, grass and rock textures, natural atmosphere
Composition/framing: landscape 3:2; an S-shaped path begins in the lower foreground and points toward the lighthouse; the traveler and bicycle sit on the lower third; the lighthouse creates a clear destination anchor
Lighting/mood: cool late-afternoon coastal light with one restrained warm break in the clouds; determined, solitary, forward-moving
Color palette: slate blue, sea green, pale grass, white lighthouse, burnt-orange jacket
Constraints: no text, no logos, no watermark, no extra people, no cars, no buildings except the lighthouse, no fantasy elements, no dramatic storm danger, no staged advertising pose
```

## Compiler commands

```powershell
python scripts/build_prompt.py --essence forward-tests/lighthouse-travel/essence.json --scenario travel-cover --effect auto --format json
python scripts/build_prompt.py --essence forward-tests/lighthouse-travel/essence.json --scenario travel-cover --effect layered-paper --format json
```

The `prompt` field from each command was passed to ImageGen without hand editing.

## First-round finding

Both routes passed anchor, direction, material, and wordless-art gates. Both failed the delivery-specific metadata-band gate: their compositions occupied nearly the full portrait canvas.

Each route received one allowed targeted correction: preserve every subject, material, color, and relationship while reserving calm nearly unprinted top and bottom bands. No third attempt was made.

## Targeted correction prompt pattern

```text
Correct only the delivery-safe layout. Scale the complete approved scene down slightly and center it so the top approximately 10% and bottom approximately 10% become calm metadata bands. Preserve the effect, palette, traveler, bicycle, lighthouse, continuous route, orientation, and all relationships. Add no text or new objects.
```

### Exact woodcut correction

```text
Use case: precise-object-edit
Asset type: corrected 4:5 field-journal key art
Input image: Image 1 is the edit target and approved Reduction Woodcut route.
Primary request: correct only the delivery-safe layout. Scale the complete existing woodcut scene down slightly and center it so the top approximately 10% and bottom approximately 10% of the portrait canvas become calm, nearly unprinted warm fibrous paper metadata bands.
Preserve exactly: reduction woodcut material, indigo/olive/rust palette, one burnt-orange traveler, one sea-green touring bicycle, one white lighthouse, the continuous S-shaped route, headland silhouette, carved marks, deckled print character, portrait orientation, and all existing subject relationships.
Top band: mostly plain warm paper with at most a few very faint sparse carved marks; suitable for a journal title.
Bottom band: mostly plain warm paper with at most a thin registration mark; suitable for coordinates, distance, and year.
Constraints: no text, no letters, no numbers, no logo, no watermark, no new objects, no extra people, no crop of the traveler, bicycle, path, or lighthouse.
Avoid: redesigning the scene, changing effect, adding a border illustration, changing colors, turning it into a poster mockup.
```

### Exact layered-paper correction

```text
Use case: precise-object-edit
Asset type: corrected 4:5 field-journal key art
Input image: Image 1 is the edit target and approved Layered Paper Cut override route.
Primary request: correct only the delivery-safe layout. Scale the complete existing layered-paper scene down slightly and center it so the top approximately 10% and bottom approximately 10% of the portrait canvas become calm plain warm paper metadata bands.
Preserve exactly: sophisticated layered cotton-paper construction, slate/sea-green/pale-grass/burnt-orange palette, one traveler, one touring bicycle, one lighthouse, the continuous S-shaped paper route, headland silhouette, lifted deckled edges, cast shadows, portrait orientation, and all subject relationships.
Top band: quiet unprinted warm cotton paper with subtle fiber texture; suitable for a journal title.
Bottom band: quiet unprinted warm cotton paper with subtle fiber texture; suitable for coordinates, distance, and year.
Constraints: no text, no letters, no numbers, no logo, no watermark, no new objects, no extra people, no crop of traveler, bicycle, route, or lighthouse.
Avoid: redesigning the scene, changing effect, adding decorative border objects, changing colors, flattening the paper layers, turning it into a poster mockup.
```

## Result

| Gate | Auto woodcut | Paper override |
| --- | ---: | ---: |
| Anchor retention | 5 | 5 |
| Route and direction | 5 | 5 |
| Thumbnail silhouette | 5 | 4 |
| Material credibility | 5 | 5 |
| Metadata safety after correction | 5 | 5 |
| **Total** | **25** | **24** |

The automatic route wins narrowly for the stated goal. Woodcut makes the cyclist-path-lighthouse sequence more forceful at small sizes. Paper is a valid override for a quieter editorial tone.

Scores are a disclosed human review of one selected generation per round, not statistical model performance.

## Supported Skill change

The observed failure justified one narrow profile update: `field-journal.safe_area` now explicitly requests nearly unprinted top and bottom 10% bands. No universal composition rule was added to other deliveries.
