# Profile authoring

Profiles live under `profiles/effects`, `profiles/scenarios`, and `profiles/deliveries`. Each file is UTF-8 JSON and its `id` must match the filename.

## Effect profiles

An effect profile defines material behavior, not a business use case. Include:

- `label`, `intent`, and `materials`;
- `path_treatment`, `form_treatment`, and `space_treatment`;
- `composition`, believable `imperfections`, and an `avoid` list;
- `best_for` tags used as explanation, not automatic scoring.

Do not name living artists, copyrighted characters, or brands as shortcuts.

## Scenario profiles

A scenario defines audience and purpose. Include:

- `audience` and `goal`;
- ranked `recommended_effects` with a short reason;
- `default_delivery` and `allowed_deliveries`;
- target-specific `prompt_requirements` and `quality_gates`.

The first available recommended effect is the `auto` route. Changing its order is a behavioral change and requires tests.

## Delivery profiles

A delivery defines the target asset contract. Include:

- `aspect_ratio` and `text_mode`;
- `safe_area` and `layout_intent`;
- `output_variants` and `quality_gates`.

Keep exact production text outside the image-generation prompt when `text_mode` is `wordless-key-art`.

## Adding a profile

1. Copy the nearest profile and change the ID.
2. Remove inherited instructions that do not apply.
3. Add at least one route or explicit-use test.
4. Run `python -m unittest discover -s tests -v` and the Skill validator.
