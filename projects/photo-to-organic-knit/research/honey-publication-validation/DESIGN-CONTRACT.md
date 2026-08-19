# Honey Publication Validation — Design Contract

```text
Entry mode: Revision-led correction
Request revision: 4
Target user and context: A reviewer checking whether campaign-poster is reusable across product Key Art rather than fitted only to the tea example.
Desired first impression: The same deterministic template can finish a materially different ceramic honey visual without losing the product or inventing lettering.
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: Preserve the amber jar, honey dipper, honeycomb, flowers and ceramic glaze path; use the existing right/top copy-safe field; retain visible sample-only status.
Information constraints: Show original product photo, reviewed wordless Key Art, exact honey copy, 4:5 master, 16:9 derivative and all gate decisions.
Operation constraints: Reuse the existing campaign-poster template and renderer without code changes unless the observed honey result exposes a real failure.
State constraints: Both variants must PASS or the failed gate must be recorded; the tea V1 baseline remains unchanged.
Environment constraints: Existing project assets, Python/Pillow, no ImageGen call, no external network.
Primary journey: honey source -> accepted ceramic Key Art -> honey copy.json -> campaign-poster renderer -> 4:5 + 16:9 -> web comparison.
User-defined phases: Continue with the honey image; adapt exact text and show final effect.
Required artifacts: Honey copy example, two PNG outputs, report, result record, additive showcase case, regression tests and installed-Skill synchronization.
Autonomy authorization: User said “继续”; reversible project-local rendering and installed example synchronization are authorized.
User-decision boundary: Real honey brand, factual product claims, pricing, nutrition/legal copy, logo, font license and publication remain outside scope.
Observable completion criteria: Original/Key Art/final outputs are all visible; both variants preserve product anchors and pass twelve gates; the output differs from tea only through copy and art input, not template code; all checks pass.
Coverage record: See below.
```

## Coverage manifest

| Requirement | Surface / state | Evidence | Stage | Status | Next action |
| --- | --- | --- | --- | --- | --- |
| Honey-specific exact copy | Valid and overflow input | JSON and renderer test | Stage 3 | pass | Maintained example renders exact honey brand, title, body, CTA, date and status. |
| 4:5 honey master | Product and copy-safe region | PNG, direct inspection, report | Stage 5–6 | pass | Jar, dipper, honeycomb, flowers and glaze path remain visible; 6/6 gates pass. |
| 16:9 honey derivative | Multi-crop resilience | PNG, direct inspection, report | Stage 5–6 | pass | All primary product anchors remain in the left art panel; 6/6 gates pass. |
| Cross-art proof | Source -> Key Art -> final | Additive showcase section | Stage 3–7 | blocked | All four stages and resources pass structural verification, but programmable browser screenshot/viewport evidence remains unavailable. |
| Delivery | Skill/source/install/project | Tests, hashes, verifier, cleanup | Stage 9 | pass | 21 installed tests pass; 49 source/install files match; project verifier and diff checks pass. |
