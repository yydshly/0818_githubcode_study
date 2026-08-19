# Release Security V1 — Design Contract

```text
Entry mode: Revision-led continuation
Request revision: 7
Target user and context: A release operator who needs evidence that a trusted signing key approved the exact Release Manifest and that release events form a tamper-evident history.
Desired first impression: Approved output now requires manifest integrity, trusted Ed25519 verification, and a recorded audit event.
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: Formal honey pixels remain unchanged; security evidence is additive and visible in the web record.
Information constraints: Signature records algorithm, key ID, signer, timestamp and manifest hash; trust store records active public keys; audit events chain sequence, previous hash, release inputs and output hashes.
Operation constraints: Private keys never enter the repository; approved rendering requires signature and trust store; demo audit log is append-only and chain-verified before append.
State constraints: missing signature, unknown/revoked key, altered manifest, bad signature and broken audit chain fail closed.
Environment constraints: Python plus cryptography 49.0.0; no HSM, OAuth, enterprise identity, remote timestamping or transparency service.
Primary journey: offline private-key signing -> trusted public-key verification -> approved render -> output hashes -> chained audit event.
User-defined phases: Continue from Release Manifest into identity/signature and tamper-evident audit.
Required artifacts: Security schema, key/sign/verify CLI, demo public trust store and detached signature, renderer enforcement, audit chain, tests, web section and installed sync.
Autonomy authorization: User said “继续”; project-local public evidence, temporary demo key generation and installed Skill synchronization are authorized.
User-decision boundary: Real private keys, real personnel identities, enterprise PKI, HSM/KMS, key rotation/revocation service, remote immutable storage and production publication remain outside scope.
Observable completion criteria: Approved render without signature/trust fails; correct signature passes; tampered manifest/signature and untrusted key fail; audit event records outputs and chain verifies; no private key remains after tests.
Coverage record: See below.
```

## Coverage manifest

| Requirement | Surface/state | Evidence | Stage | Status | Next action |
| --- | --- | --- | --- | --- | --- |
| Ed25519 signing | Offline key and detached signature | CLI and tests | Stage 3–5 | pass | Keygen/sign/verify CLIs use strict schemas and detached Ed25519 signatures. |
| Trust policy | Active/revoked/unknown key | Trust store and tests | Stage 5–6 | pass | Key ID, active status, scope, algorithm, signer and owner are enforced. |
| Renderer gate | Missing/tampered/pass | CLI integration | Stage 5–6 | pass | Approved rendering requires manifest, signature, trust and audit paths. |
| Audit chain | First/next/tampered events | JSONL verifier and tests | Stage 6 | pass | Output hashes append to a verified previous-hash chain; tampering fails. |
| Honey signed release | Retained demo evidence | Public key, signature, audit event, report | Stage 6 | pass | Signature PASS and audit sequence 1 are retained with unchanged PNG hashes. |
| Web evidence | Security chain and limits | Additive section | Stage 3–7 | blocked | Security section/resources pass structural verification; programmable screenshot/viewport evidence remains unavailable. |
| Delivery | Skill/source/install/project | Tests, hashes, verifier, cleanup | Stage 9 | pass | 28 installed tests pass; 56 source/install files match; no project PEM or temporary private key remains. |
