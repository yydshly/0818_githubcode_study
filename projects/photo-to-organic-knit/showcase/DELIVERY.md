# Multi-effect lab delivery record

## Design contract

```text
Entry mode: Revision-led
Request revision: 2 — expand the existing single-effect showcase into concrete multi-effect demonstrations
Target user and context: A researcher evaluating whether visual essence extraction can be decoupled from material rendering
Desired first impression: One meaning can produce visibly different, still-recognizable art directions
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: Preserve the existing warm-fiber research language; let generated images lead; do not turn the page into a generic card gallery
Information constraints: Clearly separate shared semantic brief, effect-specific rules, observed result, use case, and capability boundary
Operation constraints: Mouse, touch, and keyboard-reachable effect tabs; no framework or build step
State constraints: Six selectable effects; active tab, image, metadata, material rules, and use-case copy must agree
Environment constraints: Static HTML/CSS/JS; canonical local route on port 8876; GitHub Pages deployment path must remain valid
Primary journey: Open effect lab -> understand shared brief -> select an effect -> inspect result and conversion rules -> compare all six
User-defined phases: Confirm expansion -> generate effects -> show concrete effects on web page
Required artifacts: Five new effect PNGs, effect prompt archive, interactive effect lab, updated docs/tests/index metadata
Autonomy authorization: User explicitly said “确定并继续” and authorized direct implementation
User-decision boundary: New external services, paid API/CLI fallback, publishing, or changing the upstream submodule
Observable completion criteria: Six effects render from one source and one brief; switching is coherent and accessible; local resources return 200; automated project checks pass; browser evidence or an explicit browser-tool blocker is recorded
```

## Coverage manifest

| User phase | Requirement or artifact | Surface / state | Evidence needed | Owning stage | Status | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| Generate effects | Five new material interpretations | Generated assets | Image inspection + files | 2 | pass | Five images inspected and saved at 1536×1024 |
| Show effects | Shared semantic brief is explicit | Effect lab intro | Source DOM + HTTP response | 3 | pass | Contract panel is present in served HTML |
| Show effects | Six effect states are selectable and coherent | Desktop active states | Real browser interaction | 4–6 | blocked | Browser opened, but this environment exposes no screenshot/DOM/click control tool |
| Show effects | All six remain browsable on narrow screens | Mobile layout | Real browser viewport observation | 7 | blocked | Responsive CSS exists; retest when programmable browser viewport control is available |
| Show effects | Generated images do not block readable fallback | Image loading/fallback | DOM + HTTP/resource check | 8 | pass | Alt text present; all five new assets return HTTP 200 |
| Delivery | Prompts, docs, tests and Pages paths are current | Repository artifacts | File/test/build output | 9 | pass | Project verifier, JS syntax check and diff check pass |

## Canonical runtime

- Start command: `python -m http.server 8876 --directory .`
- URL: `http://127.0.0.1:8876/projects/photo-to-organic-knit/showcase/#effect-lab`
- Supported theme: light editorial theme only
- Required viewports: wide desktop and narrow mobile
- Baseline: existing single-effect showcase is HTTP-accessible and its slider/scenario JavaScript passes syntax and structural tests

## Refinement ledger

The manifest above is updated at stage boundaries. Browser evidence is recorded below after implementation; automated checks support but do not replace visual evidence.

## Stage evidence

- Stage 2: five built-in ImageGen calls produced distinct paper, ceramic, glass, woodcut and miniature material systems; all preserve the red canoe, yellow traveler, route and mountain gate.
- Stage 3: served HTML contains the shared anchors, mood and metaphor before any effect-specific copy.
- Stages 4–6: the JavaScript state map contains six complete records and twelve controls point to those records. `node --check` passes. Real click evidence remains blocked.
- Stage 7: explicit 980px and 700px breakpoints collapse the stage, controls and gallery. Real narrow-viewport evidence remains blocked.
- Stage 8: the readable copy and controls are ordinary HTML; images are progressive enhancements with alt text. Every generated asset returns HTTP 200.
- Stage 9: `verify_project.py` passes and confirms resources, dimensions, prompt archives, router states, indexes and Pages paths.

## Browser capability blocker

Attempted routes:

1. Existing in-app browser route at the canonical URL.
2. Codex `open_in_codex` navigation to `#effect-lab`.
3. Tool discovery for browser tabs, screenshots, Playwright, Node browser runtime and computer-use controls.

Available capability can open/navigate the panel but cannot return screenshots, computed DOM, viewport changes or clicks. Therefore desktop interaction and mobile visual verification are not claimed complete. Retest trigger: a session exposing the Browser control runtime, screenshot/DOM inspection, or equivalent programmable in-app browser controls.

## Revision 3 — scenario-led examples

```text
Entry mode: Revision-led
Request revision: 3 — the user clarified that effect capability alone is insufficient; examples must be organized by target use scenario
Target user and context: A designer or product owner deciding which effect to use for a concrete deliverable
Desired first impression: Each effect has a reason, a target asset, and a believable source-to-result path
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: Preserve the existing research aesthetic; each case must lead with one strong result image and keep the source photo visible as evidence
Information constraints: Every case names target, audience, effect choice, source anchors, transformation idea, deliverables, and practical value
Operation constraints: No new framework; cases remain readable without JavaScript
State constraints: Four independent cases; no hidden essential copy
Environment constraints: Existing static route and light theme; desktop and mobile reading order
Primary journey: Capability lab -> scenario cases -> understand why an effect fits -> inspect source and result -> see deliverables
User-defined phases: Replace abstract capability-only display with several target-use examples
Required artifacts: Three new source photos, three new effect results, four scenario case blocks, scenario prompt archive, updated docs/tests/index
Autonomy authorization: User explicitly supplied the desired revision
User-decision boundary: New external services, publishing, or modifying upstream
Observable completion criteria: Four distinct target scenarios are visible; three contain newly generated before/after evidence and one reuses the verified travel pair; effect choice and deliverables are explicit; repository checks pass; browser verification boundary remains truthful
```

### Revision 3 coverage

| Requirement | Surface | Evidence | Stage | Status | Next action |
| --- | --- | --- | --- | --- | --- |
| Family memory matched to organic knit | Generated pair + case | Image inspection + files | 2–3 | pass | Two people, shared book, arch and orange cat remain recognizable |
| Community impact matched to stained glass | Generated pair + case | Image inspection + files | 2–3 | pass | Five-person care circle and central sapling become one glass symbol |
| Independent brand matched to layered paper | Generated pair + case | Image inspection + files | 2–3 | pass | Arch, baker, bread rhythm, awning and bicycle remain legible |
| Travel memory matched to woodcut | Existing pair + case | Existing files + case copy | 3 | pass | Existing canoe source and woodcut result are reused with scenario rationale |
| Scenario-first hierarchy and mobile reading | New web section | Browser observation | 3–7 | blocked | Desktop/mobile screenshots remain unavailable in the current browser-control surface |
| Prompt/archive/test updates | Repository | Tests + HTTP | 9 | pass | Scenario archive, six new files, four cases and Pages resources validate |

### Revision 3 evidence

- Three source photos and three matched results were generated with the built-in ImageGen path and visually inspected before being copied into the project.
- Served HTML contains exactly four `.scenario-case` articles and six new scenario image references.
- Each case exposes target audience, source anchors, effect choice, deliverables and actual value without JavaScript.
- The scenario section has explicit 980px and 700px layout adaptations; real viewport evidence remains covered by the existing browser capability blocker.
- `SCENARIO_PROMPTS.md` records all six new prompts and explains why final typography is intentionally deferred to professional layout tools.
- Project verification passes, the page returns HTTP 200, all local resources resolve, JavaScript syntax passes and `git diff --check` passes.

## Revision 4 — final deliverable mockups

```text
Entry mode: Revision-led
Request revision: 4 — continue from scenario examples into realistic final deliverables
Target user and context: A designer evaluating whether generated art can enter an ordinary layout and publishing workflow
Desired first impression: The AI image is only one layer; deterministic typography and information design complete the asset
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: Four clearly different output formats; use existing generated art; typography must be real HTML rather than pixels baked into images
Information constraints: Each mockup names AI layer, design layer, channel, aspect, safe-area intent and practical handoff
Operation constraints: Fully readable without JavaScript; no download/export claim
State constraints: Four static deliverables with visible final copy
Environment constraints: Static HTML/CSS, existing light theme and local/Pages paths
Primary journey: Scenario case -> final mockup -> understand what AI supplied and what the designer added
User-defined phases: Continue with the first-priority final-deliverable proof
Required artifacts: Family book cover, travel journal cover, community impact report cover, bakery campaign poster, updated docs/tests
Autonomy authorization: User said “继续” after the prioritized roadmap
User-decision boundary: Actual brand identity, commercial copy approval, downloadable production files or publishing
Observable completion criteria: Four code-native mockups appear with exact selectable text; each reuses the matched scenario art; dimensions and channels are explicit; no claim that mockups are press-ready; checks pass
```

### Revision 4 coverage

| Requirement | Surface | Evidence | Stage | Status | Next action |
| --- | --- | --- | --- | --- | --- |
| Family artwork becomes a memory-book cover | Deliverable 01 | Served DOM + source structure | 3 | pass | 3:4 cover contains selectable title, volume and family metadata |
| Travel artwork becomes a field-journal cover | Deliverable 02 | Served DOM + source structure | 3 | pass | 4:5 cover contains route title, coordinates, distance and year |
| Community artwork becomes an impact-report cover | Deliverable 03 | Served DOM + source structure | 3 | pass | A4 cover contains report identity, summary, metrics and disclaimer |
| Bakery artwork becomes a campaign poster | Deliverable 04 | Served DOM + source structure | 3 | pass | 4:5 poster contains brand placeholder, event title, timing and claim |
| Mockups adapt to desktop/mobile | Deliverable grid | Browser viewport observation | 7 | blocked | CSS breakpoints are present; programmable viewport evidence remains unavailable |
| Documentation and verification are current | Repository | Tests + HTTP | 9 | pass | README, usage guide, indexes and verifier are current |

### Revision 4 evidence

- The served page contains exactly four `.deliverable-card` elements and returns HTTP 200.
- All final copy is ordinary HTML text; generated PNGs contain only the artwork layer.
- The family cover declares 3:4, travel and bakery covers declare 4:5, and the impact report uses an A4-style ratio.
- Report numbers are explicitly labeled `SAMPLE LAYOUT · ILLUSTRATIVE DATA`; the section states that commercial brand, copy, font licensing, bleed and color configuration remain production work.
- The deliverable grid collapses to one column at the existing 980px breakpoint. Real desktop/mobile screenshots remain covered by the documented browser capability blocker.
- Project verification, JavaScript syntax, HTTP inspection and `git diff --check` pass.

## Revision 5 — target-driven Skill framework

```text
Entry mode: Revision-led
Request revision: 5 — continue from visual proof into a reusable long-term Skill implementation
Target user and context: A Codex user who supplies a photo and a publication goal rather than naming an art effect
Desired first impression: Goal, scenario, effect and delivery are separate, composable decisions
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: The webpage must show real file-backed architecture and compiler behavior, not speculative boxes
Information constraints: Distinguish essence schema, scenario routing, effect profile, delivery profile, compiled prompt and quality gates
Operation constraints: Python standard library only; deterministic CLI; explicit failures for invalid IDs or malformed essence
State constraints: Auto effect routing and explicit effect override both work
Environment constraints: Extension remains inside the research project; upstream submodule is untouched; static web page links to source files
Primary journey: Extract essence -> choose scenario/delivery -> auto-route effect -> compile prompt -> generate/review
User-defined phases: Implement the reusable target-driven Skill described in the prior recommendation
Required artifacts: SKILL.md, UI metadata, schema docs, machine-readable profiles, compiler, example essence, unit tests, webpage architecture section
Autonomy authorization: User explicitly said “请继续” after reviewing the target-driven architecture
User-decision boundary: Installing the Skill globally, publishing a plugin, running paid external APIs or modifying upstream
Observable completion criteria: Skill validator passes; compiler routes four scenarios; explicit override works; malformed essence and unknown profiles fail; project tests pass; webpage exposes actual paths and commands
```

### Revision 5 coverage

| Requirement | Surface | Evidence | Stage | Status | Next action |
| --- | --- | --- | --- | --- | --- |
| Discoverable target-driven Skill | Extension Skill | Quick validator | 1 | pass | Skill validator accepts SKILL.md and openai.yaml |
| Reusable essence contract | Schema + example | Unit validation | 3 | pass | Schema plus four valid example essence files are present |
| Effect/scenario/delivery profiles | Machine-readable JSON | Compiler tests | 3 | pass | Six effect, four scenario and four delivery profiles validate |
| Deterministic Prompt compiler | CLI | Unit and CLI output | 4–6 | pass | Auto routes, explicit override and fail-closed errors pass 9 tests |
| Webpage reflects running framework | Architecture section | DOM/browser observation | 3–7 | blocked | Served DOM and links pass; screenshot/viewport observation remains unavailable |
| Repository validation current | Project | Tests + HTTP | 9 | pass | Project verifier, Skill validator, unit tests, HTTP and diff checks pass |

### Revision 5 evidence

- `quick_validate.py` reports `Skill is valid!` for the extension.
- Nine standard-library unit tests pass: all profiles parse, four auto routes match, explicit effect override works, and malformed essence, missing effect and unlisted delivery fail.
- Project verification executes all four compiler routes and confirms 14 machine-readable profiles.
- The webpage architecture section links to the actual Skill, compiler, schema and four scenario profiles; each returns HTTP 200 on the canonical server.
- The upstream submodule remains unchanged. The extension is isolated under the research project and the Pages workflow now copies it.
- Browser navigation to `#framework` was requested, but visual screenshot and viewport evidence remain covered by the existing browser capability blocker.

## Revision 6 — unseen-photo forward test

```text
Entry mode: Revision-led
Request revision: 6 — confirm and continue with an unseen-photo end-to-end Skill test
Target user and context: A maintainer checking whether auto routing improves target fit compared with a valid manual override
Desired first impression: The test exposes a real tradeoff, not a staged winner
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: One unseen source, one shared essence, one shared delivery, two effect routes; no extra generated text
Information constraints: Preserve compiled prompts, routing reason, output paths, gate-by-gate review, and limitations
Operation constraints: Built-in ImageGen only; maximum one generation per route unless a single failed gate justifies one targeted correction
State constraints: Auto route = woodcut; override = layered-paper; both use field-journal
Environment constraints: Project-local assets and static showcase; upstream remains untouched
Primary journey: Generate unseen photo -> extract essence -> compile auto and override prompts -> generate both -> review gates -> publish comparison
User-defined phases: Confirm the framework with a real new-photo comparison
Required artifacts: New source PNG, essence JSON, two compiled prompts, two output PNGs, review record, comparison section, updated tests
Autonomy authorization: User explicitly confirmed and continued
User-decision boundary: Paid API fallback, global Skill install, publication, or a third effect route
Observable completion criteria: Both outputs originate from compiler output; target-fit review explains which route wins and why; failures are recorded; tests and HTTP checks pass
```

### Revision 6 coverage

| Requirement | Surface | Evidence | Stage | Status | Next action |
| --- | --- | --- | --- | --- | --- |
| Unseen travel source | Forward-test assets | Generated file + inspection | 1–2 | pass | New lighthouse/cyclist source generated and inspected |
| Shared essence and compiled routes | Forward-test record | Compiler JSON/prompt | 3–4 | pass | Shared essence compiles woodcut auto and paper override routes |
| Auto woodcut output | Forward-test assets | Image + gate review | 5–6 | pass | Initial metadata failure corrected once; final route scores 25/25 |
| Override paper output | Forward-test assets | Image + gate review | 5–6 | pass | Initial metadata failure corrected once; final route scores 24/25 |
| Target-fit comparison | Showcase section | DOM/browser observation | 3–7 | blocked | DOM, resources and review pass; screenshot/viewport evidence remains unavailable |
| Tests and publication paths | Repository | Tests + HTTP | 9 | pass | Skill, unit, project, JS, HTTP and diff checks pass |

### Revision 6 evidence

- The unseen source was generated in the current session and had not appeared in prior examples.
- One essence file compiled two prompts without hand editing: `auto` selected woodcut; explicit override selected layered paper; both retained `field-journal` and identical gates.
- Both first-round images failed the metadata-band gate. Each received exactly one targeted edit; no third attempt or hidden candidate was used.
- Final human gate review scored woodcut 25/25 and paper 24/25. The only difference was thumbnail silhouette; the paper override remains valid for a quieter editorial tone.
- The observed failure caused one narrow change to `field-journal.safe_area`: explicit nearly-unprinted top and bottom 10% bands. A new unit test protects that behavior.
- Ten Skill tests, the project verifier, JavaScript syntax and diff checks pass. The page and five forward-test resources return HTTP 200.
- Navigation to `#forward-test` was requested. Automated screenshot and viewport evidence remain covered by the existing browser capability blocker.

## Revision 7 — cross-subject pilot benchmark

```text
Entry mode: Revision-led
Request revision: 7 — continue from one travel comparison into a small cross-subject benchmark
Target user and context: A maintainer checking whether the Skill generalizes beyond one landscape route
Desired first impression: Three visibly different source classes travel through the same framework and expose their own gates
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: Person/relationship, product/still-life, and architecture/mobility samples; one result per auto route plus at most one targeted correction
Information constraints: Report sample size, route, gates, attempts, result, and limitation; do not claim statistical accuracy
Operation constraints: Built-in ImageGen only; compiled prompts passed without hand editing
State constraints: family-memory→organic-knit→book-cover; seasonal-campaign→layered-paper→campaign-poster; travel-cover→woodcut→field-journal
Environment constraints: Project-local benchmark files and static showcase; upstream unchanged
Primary journey: Generate three unseen sources -> extract essence -> auto compile -> generate -> gate review -> one correction if needed -> aggregate pilot
User-defined phases: Continue building a cross-topic success-rate baseline
Required artifacts: Three source images, three essence files, three outputs, benchmark manifest/result, webpage benchmark section, tests
Autonomy authorization: User explicitly said “继续”
User-decision boundary: Larger paid batch, more than one correction per sample, external evaluators, publication, or model comparison
Observable completion criteria: All three routes originate from compiler prompts; each gate result and attempt count is recorded; aggregate clearly says n=3 pilot; checks pass
```

### Revision 7 coverage

| Requirement | Surface | Evidence | Stage | Status | Next action |
| --- | --- | --- | --- | --- | --- |
| Person/relationship sample | Pilot benchmark | Source, essence, output, gates | 1–6 | pass | Family→knit→book cover passed on attempt 1 |
| Product/still-life sample | Pilot benchmark | Source, essence, output, gates | 1–6 | pass | Campaign→paper→poster passed on attempt 1 |
| Architecture/mobility sample | Pilot benchmark | Source, essence, output, gates | 1–6 | pass | Travel→woodcut→journal passed on attempt 1 |
| Aggregate without overclaim | Benchmark record | Manifest + result | 6 | pass | Manifest records n=3, 3/3 observed, and generalization=false |
| Web benchmark presentation | Showcase | DOM/browser observation | 3–7 | blocked | Served DOM/resources pass; screenshot/viewport evidence remains unavailable |
| Tests and publication paths | Repository | Tests + HTTP | 9 | pass | Skill, unit, project, JS, HTTP and diff checks pass |

### Revision 7 evidence

- Three new synthetic source images were generated and inspected in the current session: person/relationship, product/still-life, and architecture/mobility.
- Three essence files compiled automatic routes without hand editing: organic knit/book cover, layered paper/campaign poster, and woodcut/field journal.
- Each selected output passed declared anchors, quantities, material, wordless-art, scenario, and delivery gates on its first attempt. No targeted correction or hidden candidate was used.
- The architecture sample reproduced the evidence-backed top/bottom metadata bands from the updated field-journal profile.
- `manifest.json` records sample size 3, observed passes 3, one attempt each, no Skill change, and `generalization_claim=false`.
- Eleven Skill tests, the project verifier, JavaScript syntax and diff checks pass. The page, outputs, Result and Manifest return HTTP 200.
- Navigation to `#pilot-benchmark` was requested. Automated screenshot and viewport evidence remain covered by the existing browser capability blocker.

## Revision 8 — additive baseline lock and review recorder

```text
Entry mode: Revision-led
Request revision: 8 — preserve original samples visibly and continue by addition only
Target user and context: A reviewer who needs to distinguish immutable baseline evidence from later research layers
Desired first impression: Nothing was replaced; each new capability has an explicit stage and provenance
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: Add a baseline ledger near the top and a review protocol after the Pilot; do not move, remove, or replace existing sample sections or assets
Information constraints: Name original upstream evidence, independent reproduction, multi-effect lab, scenario cases, deliverables, framework, forward test, and Pilot as cumulative layers
Operation constraints: Standard-library review recorder; no automatic image-quality claim
State constraints: Review statuses are pass, fail, or unverified; missing/extra gates and invalid states fail closed
Environment constraints: Existing static route and project-local Skill; upstream unchanged
Primary journey: Confirm baseline preservation -> inspect additive stages -> record human gate evidence -> compute deterministic decision summary
User-defined phases: Fix perceived overwrite and continue additively
Required artifacts: Baseline ledger, review schema, score_review.py, valid review example, tests, review-protocol webpage section
Autonomy authorization: User explicitly instructed “做新增即可 继续”
User-decision boundary: Deleting/reordering prior evidence, automated CV scoring, publishing, or changing upstream
Observable completion criteria: Existing section IDs/assets remain; ledger links to all stages; scorer validates full gate coverage and decisions; tests and HTTP checks pass
```

### Revision 8 coverage

| Requirement | Surface | Evidence | Stage | Status | Next action |
| --- | --- | --- | --- | --- | --- |
| Existing samples remain unchanged | Baseline ledger | File/DOM invariants | 1–3 | pass | Ledger links nine cumulative layers; original sections/assets remain required |
| Human review has a schema | Skill reference | Validator/tests | 3 | pass | Review schema and lighthouse example record are present |
| Review summary is deterministic | CLI | Unit tests | 4–6 | pass | Scorer validates 8 gates and computes PASS 40/40 |
| Review protocol is visible | Showcase | DOM/browser observation | 3–7 | blocked | Served DOM and links pass; screenshot/viewport evidence remains unavailable |
| Tests protect additive behavior | Project | Tests + HTTP | 9 | pass | Original IDs/assets, ledger, protocol, scorer and links validate |

### Revision 8 evidence

- The original `demo`, `effect-lab`, `scenario-cases`, `deliverables`, `framework`, `forward-test`, `pilot-benchmark`, `method`, and `meaning` IDs remain in the served page.
- Original canoe, six-effect, family, community, and bakery assets remain on disk and in the project verifier's required-file list.
- The new ledger adds links to nine cumulative layers and states `BASELINE LOCKED`; no existing section was removed or replaced.
- `review-schema.md`, `score_review.py`, and `review-auto-v2.json` are new additive files. The scorer returns PASS 40/40 for eight complete evidence gates.
- Four scorer tests prove complete pass, valid failed decision, missing-gate failure, and invalid-status failure. The total Skill suite is 15/15.
- Both CLIs now configure UTF-8 output explicitly after a Windows code-page failure was reproduced; project verification passes without environment setup.
- The page and all prior sections return HTTP 200. Navigation to `#research-ledger` was requested; screenshot/viewport evidence remains covered by the browser capability blocker.

## Revision 9 — Chinese deterministic design layer

```text
Entry mode: Revision-led
Request revision: 9 — continue the installed Skill's Chinese invocation into publishable layout examples
Target user and context: A Chinese-speaking designer evaluating the handoff from wordless Key Art to editable campaign copy
Desired first impression: Chinese prompting works end-to-end, while exact Chinese text remains a deterministic design-system responsibility
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: Reuse the reviewed tea Key Art; add one 4:5 poster and one 16:9 header; no new image generation and no replacement of prior examples
Information constraints: Mark all brand/copy/data as sample content and distinguish Key Art from typography
Operation constraints: HTML/CSS text must remain selectable; file-relative paths must work without a server
State constraints: Portrait master and wide derivative expose the multi-crop tradeoff
Environment constraints: Static showcase plus research artifact; Pages workflow must publish research files
Primary journey: Chinese request -> reviewed Key Art -> editable Chinese poster -> wide social derivative
User-defined phases: Continue the Chinese invocation through the final deterministic design layer
Required artifacts: Chinese showcase section, portrait poster, wide header, research links, tests and Pages path
Autonomy authorization: User explicitly said “继续” after the Chinese Skill call
User-decision boundary: Real brand identity, approved commercial copy, font licensing, print-ready export or publication
Observable completion criteria: Both layouts reuse the reviewed art; Chinese copy exists as DOM text; prior sections remain; filesystem and project tests pass
```

### Revision 9 coverage

| Requirement | Surface | Evidence | Stage | Status | Next action |
| --- | --- | --- | --- | --- | --- |
| 4:5 Chinese campaign poster | Showcase | DOM/file observation | 3 | pass | Selectable Chinese title, date, CTA and sample brand overlay reviewed Key Art |
| 16:9 Chinese social header | Showcase | DOM/file observation | 3 | pass | Wide crop preserves product core and discloses lost lower decoration |
| Existing layers remain unchanged | Ledger/project | DOM/file invariants | 3 | pass | Ledger adds stage 10; original demo and sections remain required |
| Research artifacts publish | Pages workflow | File/path checks | 9 | pass | Pages assembly copies the research directory |
| Visual and responsive behavior | Chinese section | Browser viewport observation | 7 | blocked | File URL opened; screenshot/viewport control remains unavailable |
| Tests and cleanup | Project | Tests/cache check | 9 | pass | Project verifier, JS, diff and zero-cache checks pass |

### Revision 9 evidence

- The formally installed Skill appears in the available-skill catalog and handled a Chinese request, Chinese essence, and Chinese privacy notes.
- Auto routing produced `seasonal-campaign → layered-paper → campaign-poster`; the unedited compiled prompt generated the reviewed Key Art on attempt 1.
- Chinese review evidence covered seven required gates and the installed scorer returned PASS 34/35. The one-point crop tradeoff is visible in the 16:9 derivative.
- The new section reuses one reviewed raster asset. All Chinese brand, title, date, CTA, and disclaimers are selectable HTML text.
- Existing sections and images remain; the append-only ledger now links a tenth layer rather than replacing a prior one.
- Pages assembly includes `research/`; project verification, JavaScript syntax, diff checks and zero-cache checks pass.
- The local file URL for `#chinese-publish` was opened without restarting a server. Screenshot and viewport evidence remain covered by the browser capability blocker.

## Revision 10 — three additional effect validations

```text
Entry mode: Revision-led
Request revision: 10 — add several new samples after clarifying the current tea example is layered paper
Target user and context: A reviewer checking that the Skill supports materially different effects and route modes
Desired first impression: Three new sources produce knit, stained glass, and ceramic relief for reasons tied to their goals
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: New sources only; no reuse or replacement of prior result images; one output per route plus at most one targeted correction
Information constraints: State auto versus explicit override, preserved quantities, gate result, attempts, and limitations
Operation constraints: Installed Skill compiler and built-in ImageGen; Chinese essence and review evidence
State constraints: family-memory→organic-knit; impact-report→stained-glass; seasonal-campaign + ceramic-relief override
Environment constraints: Additive research directory and static showcase; installed Skill remains unchanged
Primary journey: Generate sources -> Chinese essence -> installed compiler -> ImageGen -> gate review -> append comparison cards
User-defined phases: Validate more of the Skill's effect range
Required artifacts: Three source images, three essence records, three results, three reviews, manifest/result, webpage section, tests
Autonomy authorization: User explicitly requested several more validation samples
User-decision boundary: More than one correction per sample, new effect Profile, paid API fallback, real brand publication
Observable completion criteria: Three distinct materials and route modes are visible; required counts/relationships survive; scorer records pass/fail; old samples remain; tests pass
```

### Revision 10 coverage

| Requirement | Surface | Evidence | Stage | Status | Next action |
| --- | --- | --- | --- | --- | --- |
| Family/pet knit auto route | Added validation | Source, essence, output, review | 1–6 | pass | Two people, one dog and care relationship pass 35/35 on attempt 1 |
| Community stained-glass auto route | Added validation | Source, essence, output, review | 1–6 | pass | Four people, blue barrel and water cycle pass 35/35 on attempt 1 |
| Honey ceramic-relief override | Added validation | Source, essence, output, review | 1–6 | pass | Product anchors and explicit ceramic override pass 34/35 on attempt 1 |
| Additive webpage presentation | Showcase/ledger | DOM/browser observation | 3–7 | blocked | Full before/after DOM pairs pass; screenshot/viewport evidence remains unavailable |
| Tests and cleanup | Project | Tests/cache check | 9 | pass | Reviews, files, original labels, JS, diff and zero-cache checks pass |

### Revision 10 evidence

- The earlier tea example remains identified as `layered-paper`; no existing result was replaced.
- Three new synthetic source photos were generated and preserved beside their outputs.
- Installed Skill routes: family/pet auto→organic knit/book cover; community auto→stained glass/impact report; honey explicit override→ceramic relief/campaign poster.
- All three results passed on attempt 1. Review scores are 35/35, 35/35, and 34/35; the ceramic deduction records wide-crop decoration loss.
- The new webpage section shows the complete source and complete result for every sample, with three explicit BEFORE labels and retain/transform/discard notes.
- The append-only ledger adds stage 11. Original sections and assets remain protected by the verifier.
- Project verification, JavaScript syntax, diff checks and zero-cache checks pass. The local file URL for `#additional-validation` was opened; screenshot/viewport evidence remains blocked by browser capability.

## Revision 11 — deterministic campaign publishing

The full design contract and coverage manifest are recorded in `../research/publishing-pipeline-v1/DESIGN-CONTRACT.md`.

### Scope

- Reuse the accepted Chinese tea Key Art without another ImageGen call.
- Read exact UTF-8 copy from `examples/chinese-tea-copy.json`.
- Render `campaign-poster` variants at 1200×1500 and 1920×1080.
- Fail closed on malformed or overflowing copy.
- Record exact-copy, overflow, contrast, protected-region, sample-disclosure and dimension checks.
- Add a new showcase section without replacing any prior section or asset.

### Evidence

- `render_layout.py` produced both PNG files and `render-report.json` with PASS across twelve variant gates.
- A negative unit test proves a missing CTA is rejected; another proves long copy creates a FAIL report and non-zero exit.
- The new page section shows the accepted art layer, both actual output files, the exact copy fields, six PASS categories and the commercial-approval boundary.
- The existing Chinese HTML/CSS mockups remain as earlier research evidence; the new raster exports are separate additive artifacts.

### Supported boundary

The V1 renderer supports only `campaign-poster` with 4:5 and 16:9 variants. Real brand approval, factual copy review, logo handling, final font licensing, legal copy and external publishing remain outside the renderer's PASS decision.

### Browser evidence boundary

The file URL for `#publishing-pipeline` was queued in the Codex browser panel. Both exported rasters were visually inspected directly, all linked resources resolve, and responsive CSS has explicit 980px/700px adaptations. This session does not expose the required programmable Browser screenshot, DOM, or viewport control, so desktop/mobile page-layout evidence is not claimed complete. Retest trigger: a session that exposes the in-app Browser control runtime.

## Revision 12 — remaining target-specific publication templates

The V2 contract is recorded in `../research/publishing-pipeline-v2/DESIGN-CONTRACT.md`.

### Scope and evidence

- `book-cover` renders the accepted family/pet knit art at 1200×1600. The title uses the calm upper field; the people, dog and care relationship remain uncovered.
- `impact-report` renders the accepted rain-garden stained-glass art at 1240×1754. Organization identity stays in a top band; title, summary and exactly three illustrative metrics use the lower report field.
- `field-journal` renders the corrected lighthouse woodcut at 1200×1500. It reuses the evidence-backed top and bottom metadata bands from the forward test.
- Each template has a strict UTF-8 copy example, machine-readable template, retained PNG master and six-gate PASS report.
- The earlier `campaign-poster` outputs and V1 boundary remain present. The research ledger adds stage 13 instead of replacing stage 12.
- Installed and source Skill copies contain 48 files with zero SHA-256 differences; 20 tests and the project verifier pass.

### Browser evidence boundary

All three exported masters were visually inspected directly. The file route for `#publishing-templates` can be opened and every referenced resource resolves, but this session still lacks programmable screenshot, DOM and viewport control. Desktop/mobile page-layout evidence remains blocked until the in-app Browser control runtime is available; no visual-readiness claim is made for that row.

### Production boundary

All family names, organization names, metrics, coordinates and journey metadata are labeled sample or illustrative. Layout PASS does not grant consent, verify facts, audit data, license fonts, prepare print files or authorize publication.

## Revision 13 — operable localhost Publication Studio

The Studio contract and retained verification record are:

- `../research/publication-studio-v1/DESIGN-CONTRACT.md`
- `../research/publication-studio-v1/RESULT.md`

### Completed operator journey

- Four target templates load from a read-only state endpoint with maintained copy examples and fixed reviewed art.
- The form exposes explicit fields rather than raw JSON; empty fields are rejected in the client and the renderer remains the server authority.
- Current-template rendering returns PNG links, report, submitted copy and all named gate states.
- Batch rendering uses the four current copy states and produces five PNG masters, four reports and four copy files in one ZIP.
- The server binds only to `127.0.0.1`, caps bodies at 256 KiB, rejects arbitrary template/path access, retains at most 24 temporary runs and deletes the temporary root on graceful shutdown.

### Evidence

- Six Studio tests pass, including HTTP flow, unknown template, oversized body, batch contents and temporary cleanup.
- A real port-8877 run returned HTTP 200 for the page, four templates from state, PASS for current rendering, HTTP 200 for the generated PNG, PASS for batch and a 13,247,339-byte ZIP.
- The test server was stopped; port 8877 no longer listens. The observed temporary directory and Python cache were explicitly removed after the PTY shutdown did not complete cleanup gracefully.
- The main showcase adds stage 14 and a Studio interface preview without removing V1/V2 publishing evidence.

### Browser evidence boundary

The localhost URL was requested in the Codex browser panel, but programmable screenshot, DOM and viewport control was unavailable. HTTP behavior, generated artifacts, source structure and responsive rules are verified; visual interaction readiness is not claimed for the blocked Stage 7 row.

## Revision 14 — honey cross-art campaign publication

The user correctly identified that tea alone could not demonstrate cross-art reuse. This revision adds a second product-art campaign without altering the retained tea V1 result.

### Evidence chain

- Original: `research/additional-validation-v2/honey-source.png`.
- Accepted Key Art: `research/additional-validation-v2/honey-ceramic.png`, previously reviewed PASS 34/35.
- Exact copy: `extension/photo-to-conceptual-art/examples/honey-campaign-copy.json`.
- Finals: 1200×1500 poster and 1920×1080 header under `research/honey-publication-validation/outputs/`.
- Machine report: PASS across twelve variant gates.

### Observed result

- The 4:5 copy panel does not cover the amber jar, honeycomb, dipper, flower branch or glaze path.
- The 16:9 re-layout preserves those primary anchors in the left art panel and places all exact copy in the right deterministic panel.
- No ImageGen call, template edit or renderer edit was needed. Tea and honey differ only by accepted art and copy input.
- A new unit test protects the second campaign example; the installed Skill suite is 21/21.
- The showcase adds source → Key Art → 4:5 → 16:9 as stage 15 rather than replacing tea or the ceramic validation card.

### Boundary

This is evidence for two selected product-art examples, not a production success rate. The sample brand and copy do not verify honey origin, nutrition, price, health claims, trademark rights, labeling law or commercial approval. Browser screenshot/viewport evidence remains covered by the existing tool-capability blocker.

## Revision 15 — approved-mode formal publication example

This revision answers why the sample image carried both a system disclosure and a channel/status field, then demonstrates the correct formal-mode behavior.

### Sample versus approved

- Sample mode keeps `copy_status=sample`, automatically renders `SAMPLE / 非商业发布`, and may use a placeholder channel such as `线上预览 · SAMPLE COPY`.
- Approved-mode demo sets `copy_status=approved`; the renderer draws no generated sample disclosure and retains `官方商城 · 秋季限定` as the right-bottom channel field.
- Both 4:5 and 16:9 approved outputs pass twelve layout gates and preserve all honey product anchors.
- A unit test explicitly rejects any generated sample-disclosure item in approved outputs and checks the channel copy.

### External approval contract

The webpage lists five required owners before a real caller may declare approved status:

1. Brand owner — identity and visual use.
2. Copy owner — titles, dates, CTA, channel and product text.
3. Legal/compliance — origin, price, nutrition, health claims, labels and notices.
4. Design/production — logo, font license, image rights, color, bleed and size.
5. Channel owner — destination, inventory, accessibility, tracking and timing.

The renderer does not create or verify these approvals. The formal artifact is labeled outside the image as an approval-mode demonstration; the fictional brand is not represented as commercially authorized.

### Evidence

- `research/honey-formal-publication-demo/outputs/` contains the 4:5, 16:9 and PASS report.
- `examples/honey-campaign-approved-demo.json` is installed as a maintained workflow example.
- The installed Skill suite is 22/22 and project/source installation contains 50 matching files.
- Web screenshot and viewport evidence remain blocked by the current programmable-browser capability boundary.

## Revision 17 — Ed25519 trusted signature and audit chain

Approved rendering now requires a detached Ed25519 signature, an active matching public key and a writable verified audit chain in addition to the Release Manifest.

### Retained evidence

- Demo key ID: `demo-release-key-2026`; owner `Demo Release Authority`; scope `demo`.
- The public trust record and detached signature are retained; no private PEM is present.
- Honey signature verification reports PASS against the exact Manifest bytes.
- Formal output hashes are unchanged, confirming security metadata did not alter the visual result.
- Audit sequence 1 binds manifest/copy/art hashes and both output hashes; the audit verifier reports PASS.

### Fail-closed coverage

- Missing signature/trust/audit inputs, unknown or revoked key, scope mismatch, signer mismatch, manifest tampering, signature tampering and audit-chain tampering are rejected.
- The existing audit chain is verified before append.
- Successful output bundles retain Manifest, signature, trust snapshot, audit log and the individual audit event.

### Cleanup and boundary

- The one-time Demo private key was created under a verified temporary directory and deleted after signing.
- Installed Skill tests: 28/28; source/install files: 56/56 with zero differences.
- The prototype does not replace enterprise identity, HSM/KMS custody, rotation/revocation, independent timestamping or remote immutable retention.
- The showcase adds stage 18; browser screenshot/viewport evidence remains under the known control limitation.

## Revision 18 — non-production Action Runbook

The user chose not to enter production and requested actions in the description. The project now has one maintained action source of truth rather than another infrastructure layer.

### Actions added

- Seven standard actions: goal lock, essence, route/generate, review, layout, verify and retain.
- Sample and Approved paths explicitly diverge at the layout/release stage.
- Seven failure responses cover visual gates, repeated failure, copy collision, post-approval hash changes, signature/trust failure, audit failure and private-key exposure.
- Every failure lists both the required response and the action that is forbidden.

### Non-production backlog

- Freeze/commit the baseline only after an explicit user request.
- Run a 20–50 item cross-subject benchmark.
- Add real viewport/keyboard/accessibility browser evidence when tooling permits.
- Demonstrate a Studio approval panel that creates drafts but cannot fabricate approvals.
- Run one authorized real-content pilot only after receiving assets, copy, permissions and reviewers.

### Explicit deferral

Public deployment, accounts, organization roles, real KMS/HSM custody, revocation, remote immutable audit, customer storage, arbitrary upload, billing and publishing integrations remain deferred until production is authorized.

The Skill links `references/action-runbook.md` before retained benchmark/publication handoff. The showcase adds stage 19; structural verification passes while browser screenshot/viewport evidence remains under the existing capability boundary.

## Revision 16 — hash-bound Release Manifest enforcement

Approved mode now fails closed unless the exact copy and art bytes are bound to five completed external approvals.

### Implementation

- `references/release-manifest.md` defines the strict packet and lifecycle.
- `scripts/release_manifest.py` builds a pending draft with copy/art SHA-256 values.
- `render_layout.py --release-manifest` validates release/campaign/template identity, both hashes, five fixed owner records, approved status, reviewer, timezone-aware timestamp and evidence ID.
- Sample copy rejects a supplied manifest; approved copy rejects a missing manifest.
- The exact accepted packet is copied into the output bundle and summarized in `render-report.json`.

### Fail-closed evidence

- Approved without manifest: rejected.
- Legal approval pending: rejected.
- Copy SHA mismatch: rejected.
- Art SHA mismatch: rejected by the shared validator.
- Valid demo packet: PASS; formal honey outputs remain byte-identical to the prior approved visual result.

### Validation and boundary

- Installed Skill tests: 25/25.
- Source and installed Skill: 53 files, zero SHA-256 differences.
- Release Manifest V1 detects integrity and completeness but does not authenticate reviewer identity, authority, signatures or revocation.
- The webpage adds stage 17 with the manifest chain, retained demo packet and failure matrix. Browser screenshot/viewport evidence remains blocked by the known control limitation.
