# Visual essence schema

Use the schema to separate source understanding from effect and delivery decisions. Every assertion must be visible in the source or explicitly supplied by the user.

## Required object

```json
{
  "orientation": "landscape",
  "aspect_ratio": "3:2",
  "subject": "one sentence naming the primary subject and action",
  "anchors": ["two to six indispensable visible anchors"],
  "relationships": ["spatial or emotional relationships that must survive"],
  "emotion": ["one to four source-grounded qualities"],
  "visual_path": "the dominant eye path or compositional movement",
  "metaphor": "one concise visual idea derived from the source and goal",
  "retain": ["elements that remain recognizable"],
  "transform": ["elements that may become symbols, paths, blocks, gaps, or material forms"],
  "discard": ["secondary detail that weakens the concept"],
  "palette": ["source colors worth preserving"],
  "privacy_notes": []
}
```

## Validation rules

- `orientation` is `landscape`, `portrait`, or `square`.
- `aspect_ratio` is a short ratio such as `3:2`, `4:5`, or `1:1`.
- `anchors`, `retain`, and `transform` must be non-empty arrays of strings.
- Keep anchors concrete: `orange cat`, not `warmth`; put warmth under `emotion`.
- Record relationships before style: `grandmother and child lean over one shared book` is more useful than `cozy composition`.
- Use one metaphor. If the sentence contains several unrelated concepts, choose the one most aligned with the delivery goal.
- `discard` removes background information; it must not silently remove a person, product, logo, or fact the user requires.
- Add privacy notes for children, private homes, faces, badges, addresses, screens, or other sensitive details.

## Failure conditions

Reject the essence record when it invents unseen objects, describes an art effect, contradicts user preservation requirements, omits a required person/product, or treats a desired marketing claim as a visible source fact.
