# Release Manifest V1 — Design Contract

```text
Entry mode: Revision-led continuation
Request revision: 6
Target user and context: A release operator who must not be able to produce an approved-looking asset by changing one copy field.
Desired first impression: Approved mode is cryptographically tied to the exact art and copy plus five explicit external approvals.
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: Preserve all existing sample outputs; re-render the formal honey demo only after a valid manifest passes.
Information constraints: Manifest records release ID, scope, campaign/template identity, art/copy SHA-256 and five approval records.
Operation constraints: Sample rendering remains manifest-free; approved rendering requires `--release-manifest`; missing, pending, malformed or hash-mismatched manifests fail before output.
State constraints: draft, incomplete, hash-mismatch and approved-pass paths are deterministic and testable.
Environment constraints: Python standard library plus existing Pillow renderer; no signatures, identity provider, database or external approval service in V1.
Primary journey: build draft -> external owners complete approvals -> hashes locked -> approved render validates manifest -> outputs and report retain release evidence.
User-defined phases: Continue with Release Manifest and enforce approved mode.
Required artifacts: Manifest schema, draft builder, validator integration, approved demo manifest, re-rendered honey outputs/report, tests, web evidence and installed-Skill sync.
Autonomy authorization: User said “继续”; reversible project-local Skill changes and installed synchronization are authorized.
User-decision boundary: Cryptographic signatures, identity verification, real reviewer identities, audit service, revocation, production secrets and publication remain outside scope.
Observable completion criteria: Approved rendering without manifest fails; incomplete/hash-mismatched manifests fail; valid manifest succeeds; report records release PASS; sample rendering remains compatible; project and installed tests pass.
Coverage record: See below.
```

## Coverage manifest

| Requirement | Surface/state | Evidence | Stage | Status | Next action |
| --- | --- | --- | --- | --- | --- |
| Manifest schema | Draft and approved packet | Reference and validator | Stage 3 | pass | Strict schema fixes release identity, scope, hashes and five approval owners. |
| Draft generation | Exact copy/art hashes | CLI and tests | Stage 4–5 | pass | Draft builder records hashes, pending approvals and refuses overwrite without force. |
| Approved render gate | Missing/pending/mismatch/pass | Renderer and tests | Stage 5–6 | pass | Missing manifest, pending legal approval and hash mismatch fail; valid packet passes. |
| Honey approved evidence | Valid demo packet | Manifest, outputs and report | Stage 6 | pass | Formal honey outputs retain exact manifest and report release.status=PASS. |
| Web explanation | Why approved is now locked | Additive section | Stage 3–7 | blocked | Section/resources pass structural verification; programmable browser screenshot/viewport evidence remains unavailable. |
| Delivery | Skill/source/install/project | Tests, hashes, verifier, cleanup | Stage 9 | pass | 25 installed tests pass; 53 source/install files match; project verifier and cleanup pass. |
