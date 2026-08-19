# Publication Studio V1 — Design Contract

```text
Entry mode: Revision-led continuation
Request revision: 3
Target user and context: A local Chinese-speaking content operator who should not need to edit JSON or run the renderer manually.
Desired first impression: The Skill is now an operable publishing tool, while every output remains traceable to exact copy, accepted art, template and gates.
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: Reuse the showcase's paper/forest research language; one dominant preview; forms remain secondary but readable; no new ImageGen assets.
Information constraints: Show template, exact editable fields, sample-data boundary, output dimensions, gate status, and download links.
Operation constraints: Localhost only; whitelisted templates and accepted art; bounded JSON body; no arbitrary filesystem paths; no external network.
State constraints: Initial sample, edited/dirty, rendering, PASS, FAIL and batch-ready states must be visible; last successful output remains visible after a failed edit.
Environment constraints: Python 3, Pillow, static HTML/CSS/JS, temporary run directory removed on server shutdown.
Primary journey: Select template -> edit copy -> render -> inspect gates and output -> download PNG/report/copy JSON or batch ZIP.
User-defined phases: Continue from deterministic scripts to an ordinary-user web interface; preserve existing showcase and examples.
Required artifacts: Local server, studio HTML/CSS/JS, four template forms, render and batch endpoints, temporary artifact lifecycle, tests, showcase entry, run instructions and delivery record.
Autonomy authorization: User said “继续”; reversible project-local implementation, local server testing and installed-Skill synchronization are authorized.
User-decision boundary: Arbitrary image upload, public hosting, authentication, real brand approval, persistent job storage, external publication and production asset management remain outside scope.
Observable completion criteria: Four templates load; editing exact fields changes the submitted copy; render endpoint returns PASS/FAIL and files; batch endpoint returns four masters in one ZIP; malformed/oversized/unknown requests fail closed; tests and project verifier pass; temporary server and artifacts are cleaned after verification.
Coverage record: See table below.
```

## Coverage manifest

| User phase | Requirement or artifact | Surface / state | Evidence needed | Owning stage | Status | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| Operable studio | Four template selector and editable copy form | Initial and dirty states | DOM/source and browser evidence | Stage 3–4 | pass | Schema-driven fields, reset, dirty state and template switching are implemented. |
| Operable studio | Deterministic current-template render | Rendering, PASS and FAIL | API integration test and output | Stage 5–6 | pass | Real localhost render returned PASS, two campaign outputs and twelve variant gates. |
| Batch export | Four masters plus reports and copies | Batch-ready ZIP | Integration test and archive inspection | Stage 5–6 | pass | Batch returned four template results and a ZIP containing five PNGs, four reports and four copies. |
| Safety and cleanup | Whitelist, body limit, temporary lifecycle | Invalid request and shutdown | Tests and filesystem check | Stage 6–8 | pass | Unknown/mismatched IDs and oversized bodies fail closed; test and manual temporary directories were removed. |
| Showcase handoff | Additive studio entry from research page | Existing static page | Resource and browser evidence | Stage 7 | blocked | Entry, source and resources pass structural verification; live URL was requested, but programmable screenshot/DOM/viewport control remains unavailable. |
| Delivery | Installed Skill, docs and checks | Source/install/project | Hashes, tests and verifier | Stage 9 | pass | Project verifier, 20 Skill tests, 6 Studio tests and JavaScript syntax checks pass; installed Skill remains source-identical. |

## Design direction

| Decision | Direction | Observable constraint | Acceptance criterion |
| --- | --- | --- | --- |
| Composition | Preview-led two-column workspace | Preview remains the largest region on desktop; form leads on mobile | User can identify current template and result without scrolling through unrelated research. |
| State feedback | Persistent status bar and six-gate list | Rendering, PASS and FAIL never rely on color alone | Text state and gate names update after every request. |
| Editing | Schema-driven explicit fields | No free-form JSON or arbitrary paths in the primary UI | Every visible field maps to one maintained copy key. |
| Downloads | Output-specific actions plus one batch action | Links appear only after a successful server result | PNG/report/copy and batch ZIP are addressable local URLs. |
| Boundary | Prominent local/sample notice | No implication of approval or cloud storage | UI states local-only, temporary, and sample-data boundaries. |
