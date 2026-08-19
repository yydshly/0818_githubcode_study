# Honey Formal Publication Mode Demo — Design Contract

```text
Entry mode: Revision-led continuation
Request revision: 5
Target user and context: A publishing team deciding how an approved campaign differs from a research/sample preview.
Desired first impression: Formal mode removes duplicate sample warnings, restores the channel field, and keeps approval responsibilities explicit outside the image.
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: Reuse the accepted honey ceramic Key Art and unchanged campaign template; preserve jar, honeycomb, dipper, flowers and glaze path.
Information constraints: Visible artwork contains only approved-demo brand/campaign/channel copy; the web explanation must state that this is a simulated approval workflow, not a real authorized brand campaign.
Operation constraints: `copy_status=approved` removes the generated sample disclosure; `campaign.location` contains a real-purpose channel value rather than another warning.
State constraints: Both 4:5 and 16:9 outputs pass; no generated.sample_disclosure item exists; all exact copy fields remain present.
Environment constraints: Existing renderer and template, no ImageGen, no external publishing.
Primary journey: externally approved copy packet -> approved JSON status -> deterministic render -> final QA -> channel handoff.
User-defined phases: Explain formal publication, provide one example, and write it into the web page.
Required artifacts: Approved-mode demo JSON, two PNGs, report, publication checklist, additive web comparison, tests and installed-Skill sync.
Autonomy authorization: User explicitly requested the example and web update.
User-decision boundary: Real authorization, trademark, product facts, health/nutrition claims, price, legal labeling, logo assets, licensed production font, publication and distribution remain external.
Observable completion criteria: Sample and approved modes are visibly compared; approved outputs contain no sample disclosure; the channel field reads as a channel; report and test prove the behavior; all project checks pass.
Coverage record: See below.
```

## Coverage manifest

| Requirement | Surface/state | Evidence | Stage | Status | Next action |
| --- | --- | --- | --- | --- | --- |
| Approved-mode copy packet | JSON and exact fields | Example and schema validation | Stage 3 | pass | Approved demo copy is strict, named as a demo, and preserves the official-channel field. |
| Formal 4:5 and 16:9 | Approved mode | PNGs, report and direct inspection | Stage 5–6 | pass | Both formal-looking outputs retain product anchors and pass 12/12 gates. |
| Sample disclosure removal | Approved mode | Text-item and gate evidence | Stage 6 | pass | Neither output contains generated.sample_disclosure; the approved disclosure gates pass. |
| Formal publication explanation | Sample vs approved | Additive web section and checklist | Stage 3–7 | blocked | Web resources and structure pass, but programmable browser screenshot/viewport evidence remains unavailable. |
| Delivery | Skill/source/install/project | Tests, hashes, verifier, cleanup | Stage 9 | pass | 22 installed tests pass; 50 source/install files match; project verifier and cleanup checks pass. |
