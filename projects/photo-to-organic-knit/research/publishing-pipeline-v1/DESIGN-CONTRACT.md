# Publishing Pipeline V1 — Design Contract

```text
Entry mode: Revision-led continuation
Request revision: 1
Target user and context: A content or brand team turning an accepted conceptual Key Art into channel-ready campaign assets.
Desired first impression: The same visual idea becomes a controlled publication system, not a one-off mockup.
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: Preserve the reviewed tea product cluster; use the existing cream/forest palette; exact Chinese copy must remain selectable in source data and rendered deterministically; no generated lettering.
Information constraints: One brand, one campaign title, one supporting line, one CTA, one date range, one location/status line, and a visible sample-only disclosure.
Operation constraints: One local command renders all declared variants from one copy JSON file and one accepted art file.
State constraints: Valid input produces PASS outputs and a machine-readable report; malformed or overflowing copy fails closed with a non-zero exit code.
Environment constraints: Python 3 plus Pillow; no network, browser service, or external design account required.
Primary journey: copy.json + accepted Key Art -> render -> automated layout gates -> 4:5 and 16:9 publication previews.
User-defined phases: Extend the existing Skill; show concrete results on the existing web page; preserve prior examples.
Required artifacts: copy schema, campaign template, renderer, two PNG exports, render report, tests, additive showcase section, reproducible handoff record.
Autonomy authorization: User said “确定并继续”; reversible in-scope implementation and local validation are authorized.
User-decision boundary: Real brand authorization, final commercial copy, logo files, licensed production fonts, and external publishing remain outside this scope.
Observable completion criteria: Both outputs exist at declared dimensions; checks report PASS; exact supplied copy is preserved; tests and project verifier pass; new web section displays inputs, outputs, and boundary; prior sections remain present.
Coverage record: See table below.
```

## Coverage manifest

| User phase | Requirement or artifact | Surface / state | Evidence needed | Owning stage | Status | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| Skill extension | Copy schema and sample | Valid and malformed JSON | Unit tests and files | Stage 3 | pass | Schema rejects missing fields and preserves explicit Chinese lines. |
| Skill extension | Campaign renderer | 4:5 and 16:9 | Executed local command | Stage 5 | pass | Both declared PNG variants were generated from one copy file. |
| Quality control | Exact copy, overflow, contrast, safe area, dimensions | PASS and fail-closed states | Machine-readable report and tests | Stage 6 | pass | Twelve variant gates pass; malformed and overflow fixtures fail closed. |
| Concrete web display | Additive publishing-pipeline section | Desktop and narrow viewport | Browser or rendered-page evidence | Stage 7 | blocked | Output rasters were visually inspected and page structure/resources pass, but this session exposes no programmable Browser screenshot, viewport or DOM control; retest the file URL when that control is available. |
| Delivery | Installed Skill matches project source | Source and installed copies | SHA-256 comparison | Stage 9 | pass | 42 source files and 42 installed files have zero SHA-256 differences. |
| Delivery | Repository and Skill checks | Full project | Automated checks | Stage 9 | pass | 18 Skill tests, project verifier, JS syntax and diff checks pass. |

## Design direction

| Decision | Chosen direction | Observable constraint | Acceptance criterion |
| --- | --- | --- | --- |
| Hierarchy | Art-led poster, copy-led wide header | One dominant campaign statement per variant | Title is the first text read and never covers the protected product cluster. |
| Typography | Microsoft YaHei on this Windows fixture, configurable font override in CLI | Exact Unicode strings, no AI lettering | Render report records the font and all supplied strings. |
| Palette | Forest green, warm paper, muted gold | Text sits on known solid or controlled translucent panels | Declared text/background pairs meet WCAG AA for normal text. |
| Responsive web display | Two exported rasters in a readable comparison grid | No clipped cards or horizontal page overflow | Wide and narrow layouts retain full previews and artifact links. |
| Production boundary | Visible sample disclosure | No implication of commercial approval | Both preview and page state that brand/copy are examples. |
