# Target-specific quality gates

Evaluate the generated art before layout. A visually attractive result can still fail the target.

## Universal gates

1. **Anchor retention:** required people, products, colors, quantities, and relationships remain recognizable.
2. **Conceptual change:** hierarchy, scale, spacing, continuity, layering, silhouette, negative space, or visual path changes meaningfully; the result is not a surface filter.
3. **Scenario fit:** the first impression supports the audience and goal recorded in the scenario profile.
4. **Material credibility:** material construction, edges, light, imperfections, and depth agree with the effect profile.
5. **Delivery safety:** essential anchors survive the target aspect and the intended text-safe region remains usable.
6. **Reference isolation:** no unrelated subject, caption, palette signature, watermark, or brand leaks from a material reference.
7. **Privacy:** private details identified in the essence record are omitted, abstracted, or handled according to the user's authorization.
8. **Production boundary:** exact copy, metrics, logos, pricing, dates, legal text, and accessibility metadata remain editable outside the raster artwork.

## Review output

Report each gate as `pass`, `fail`, or `unverified`, with one sentence of evidence. Regenerate for one failed gate at a time. After two targeted attempts on the same gate, stop and hand the issue back for human judgment.

## Scenario emphasis

- Family memory: relationship and participant count outrank decorative detail.
- Travel cover: route, direction, and thumbnail silhouette outrank atmospheric realism.
- Impact report: shared action and credible symbolism outrank individual portrait fidelity.
- Seasonal campaign: brand-safe whitespace and reusable graphic hierarchy outrank complete storefront reconstruction.
