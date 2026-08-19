# Non-Production Action Runbook — Design Contract

```text
Entry mode: Revision-led continuation
Request revision: 8
Target user and context: A researcher or designer operating the Skill before any production rollout.
Desired first impression: Every stage has a named action, owner handoff, stop rule and failure response.
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: Add an action-oriented section without replacing research evidence or implying production readiness.
Information constraints: Separate ordinary Sample flow, approved demo flow, failure actions, current research backlog and production-only deferrals.
Operation constraints: Descriptions point to maintained files/commands; no new external service or live publication.
State constraints: Every failure row ends in an explicit action; no “retry until it works” advice.
Environment constraints: Existing static showcase and installed Skill references.
Primary journey: choose intent -> produce/review art -> choose sample or approved path -> render/verify -> retain evidence -> stop at scope boundary.
User-defined phases: Identify any remaining additions and put actions into the description.
Required artifacts: Skill action runbook, SKILL routing link, additive web section, README entry and verifier coverage.
Autonomy authorization: User explicitly allowed actions to be added to the description.
User-decision boundary: Committing/pushing, real private assets, public deployment, real approvals and enterprise system selection remain outside this documentation update.
Observable completion criteria: Normal actions, failure responses, near-term non-production tasks and production-only deferrals are visible and linked; tests and project checks pass.
Coverage record: See below.
```

## Coverage manifest

| Requirement | Surface | Evidence | Stage | Status | Next action |
| --- | --- | --- | --- | --- | --- |
| Normal operating actions | Skill reference and web | Maintained runbook | Stage 3 | pass | Seven actions cover goal lock through retained evidence. |
| Failure responses | Web and reference | Explicit action matrix | Stage 6 | pass | Seven failure classes map to required and forbidden actions. |
| Non-production backlog | Web | Prioritized list | Stage 3 | pass | Benchmark, browser evidence, Studio approval demo and authorized pilot are separated from production work. |
| Delivery | Source/install/project | Tests, hashes, verifier | Stage 9 | pass | Installed runbook is source-identical; project verifier and Skill validation pass. |
