# Release Security V1 Result

## Outcome

Approved rendering now requires three independent evidence layers:

```text
Release Manifest integrity
+ Ed25519 trusted signature
+ hash-chained audit destination
-> approved rendering allowed
```

## Retained honey evidence

- Key ID: `demo-release-key-2026`
- Trusted owner: `Demo Release Authority`
- Scope: `demo`
- Algorithm: Ed25519
- Manifest SHA-256: `8eae05ef5e515509d231fd0c58aa1347392f5d4a0fe1b842eff411d4769218ba`
- Signature SHA-256: `2e64c90e030b495d2d691c47b50493b7f6d0c3c457cd1ddf61b68544cf139bce`
- Trust-store SHA-256: `68f97a93c0517cbc10d9371791b8b75859c31b07d7b79d13a7589e582e811de8`
- Audit sequence: 1
- Audit head: `410dcb8f58c77855c060d24e75eb70ef75c355f8d2b3d0eab678fc52dd1b0991`

The formal honey PNG hashes are unchanged from the unsigned visual result. Security evidence is additive.

## Fail-closed coverage

- Missing signature or trust store: rejected.
- Unknown, revoked, non-Ed25519 or wrong-scope key: rejected.
- Signer differs from trusted owner: rejected.
- Manifest bytes changed after signing: rejected.
- Signature bytes changed: rejected.
- Audit chain sequence, previous hash or event body changed: rejected.
- Valid signature, trust and audit chain: PASS.

## Private-key cleanup

The one-time Demo private key was generated under the operating-system temporary directory, used once, and deleted after the retained public trust record and detached signature were created. No private PEM exists in the repository.

## Audit event

`release-audit-demo.jsonl` contains one event binding:

- Release and key identities;
- Manifest, copy and art hashes;
- 4:5 and 16:9 output hashes;
- Previous hash of all zeros;
- Current event hash.

The local audit verifier reports PASS with one event and the retained head hash.

## Boundary

Ed25519 proves control of a private key corresponding to a trusted public key. The Demo trust store does not establish a real person's identity or authority. A local JSONL chain exposes modification but cannot prevent deletion, rollback or filesystem replacement. Production requires managed identity, HSM/KMS key custody, rotation/revocation, independent timestamping and remote append-only audit retention.
