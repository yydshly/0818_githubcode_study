# Publishing Pipeline V2 — Remaining Delivery Templates

```text
Entry mode: Revision-led continuation
Request revision: 2
Target user and context: A family editor, nonprofit communications team, or travel publisher reusing accepted conceptual Key Art.
Desired first impression: One reusable Skill can finish several distinct publication goals without forcing every image into one poster layout.
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: Preserve each accepted artwork's target-specific calm area; retain the family relationship, four-person water-cycle symbol, and lighthouse route; exact Chinese text remains deterministic.
Information constraints: Each template accepts only its declared fields and explicit title lines; sample status must remain visible.
Operation constraints: The existing render_layout.py command resolves the template from copy.json and generates the declared primary master.
State constraints: book-cover, impact-report, and field-journal each produce PASS or fail closed; the existing campaign-poster route must remain unchanged.
Environment constraints: Python 3 plus Pillow, local system font, no network or external design account.
Primary journey: accepted Key Art + template-specific copy.json -> one deterministic publication master -> machine-readable gate report.
User-defined phases: Continue the Skill; extend the remaining delivery templates; add concrete web results; preserve previous samples.
Required artifacts: Three copy examples, three template JSON files, renderer support, three PNG masters, three reports, tests, additive web presentation, reproducible result record.
Autonomy authorization: User said “继续”; reversible in-scope implementation and installed-Skill synchronization are authorized.
User-decision boundary: Real family names, nonprofit data, geographic facts, brand authorization, logos, licensed production fonts, print prepress, and external publishing remain outside scope.
Observable completion criteria: All three templates render at declared dimensions and pass exact-copy, overflow, contrast, protected-region, disclosure, and dimension gates; the campaign renderer still passes; all outputs appear in a new additive web subsection; tests and project verifier pass.
Coverage record: See table below.
```

## Coverage manifest

| User phase | Requirement or artifact | Surface / state | Evidence needed | Owning stage | Status | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| Extend Skill | Template-specific copy validation | Valid, missing and overflowing fields | Unit tests | Stage 3 | pass | Three strict content contracts and maintained examples validate. |
| Extend Skill | Book-cover renderer | 1200×1600 family master | PNG and report | Stage 5 | pass | Output visually preserves the two people, dog and care circle; 6/6 gates pass. |
| Extend Skill | Impact-report renderer | 1240×1754 report master | PNG and report | Stage 5 | pass | Output preserves four volunteers and the blue water cycle; 6/6 gates pass. |
| Extend Skill | Field-journal renderer | 1200×1500 travel master | PNG and report | Stage 5 | pass | Output uses the evidence-backed upper/lower bands; 6/6 gates pass. |
| Preserve baseline | Existing campaign-poster behavior | 4:5 and 16:9 | Regression tests | Stage 6 | pass | Existing campaign test and retained V1 report remain PASS. |
| Concrete web results | Additive multi-template subsection | Wide and narrow page | Browser or rendered artifact evidence | Stage 7 | blocked | All three final rasters were directly inspected and page resources/structure pass, but programmable Browser screenshot and viewport control remain unavailable; retest `#publishing-templates` when exposed. |
| Delivery | Installed Skill, checks and cleanup | Project and installed copy | Hashes, tests, verifier, cache/server check | Stage 9 | pass | 20 installed tests pass; 48 source and installed files have zero hash differences; project verifier passes. |

## Design direction

| Template | Focal hierarchy | Protected visual | Copy zone | Acceptance criterion |
| --- | --- | --- | --- | --- |
| book-cover | Family title before edition metadata | Two people, dog, care circle | Calm upper field and narrow bottom folio | No text intersects the relationship cluster. |
| impact-report | Report purpose, then three illustrative metrics | Four volunteers, blue barrel, water path | Existing lower pale-glass field | Metrics remain explicitly labeled illustrative. |
| field-journal | Journey title, then coordinates/distance/year | Traveler, bicycle, route, lighthouse | Top and bottom ~10% bands | The evidence-backed art rectangle remains untouched. |
