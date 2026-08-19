# Release Manifest V1 Result

## Outcome

Approved rendering is no longer enabled by `copy_status=approved` alone.

```text
approved copy
+ exact copy SHA-256
+ exact art SHA-256
+ brand approval
+ copy approval
+ legal approval
+ design approval
+ channel approval
-> render allowed
```

Release Security V1 now adds a second gate: the accepted manifest must also carry a valid Ed25519 signature from an active trusted public key, and every approved render must append an audit event.

Any missing, pending, malformed, or mismatched input fails before the renderer creates a new output directory.

## Maintained implementation

- `references/release-manifest.md` — schema and lifecycle.
- `scripts/release_manifest.py` — hash-bound draft builder and shared validator.
- `scripts/render_layout.py --release-manifest` — approved-mode enforcement.
- `research/honey-formal-publication-demo/honey-release-manifest-approved-demo.json` — retained demo packet.
- `research/honey-formal-publication-demo/outputs/release-manifest.json` — exact packet copied into the output bundle.
- `references/release-security.md` and `scripts/release_security.py` — key, signature, trust and audit contracts.

## Observed paths

| Case | Decision |
| --- | --- |
| Sample copy without manifest | Allowed; disclosure remains |
| Sample copy with manifest | Rejected |
| Approved copy without manifest | Rejected |
| Approved copy with pending legal approval | Rejected |
| Approved copy with changed copy hash | Rejected |
| Approved copy with changed art hash | Rejected |
| Approved copy with valid manifest | PASS |

## Honey demo binding

- Release ID: `wild-honey-autumn-2026-approved-demo`
- Scope: `demo`
- Template: `campaign-poster`
- Campaign ID: `wild-honey-autumn-2026-approved-demo`
- Copy SHA-256: `37b7f2ff112cbe35ad0f7aeca14a1fb32d12c9c818dade4254123e8cd1e4ab6c`
- Art SHA-256: `8b8a0f2660685195a4ec89c4c864464c2c3d0ed3d8b329bd69d226615018b9da`
- Approvals: brand, copy, legal, design, channel — all demo records marked approved.

## Tests

The Skill suite now covers:

- draft creation with pending approvals and exact hashes;
- refusal to overwrite a draft without `--force`;
- refusal to build a manifest for sample copy;
- approved rendering without a manifest;
- pending approval rejection;
- copy-hash mismatch rejection;
- successful approved rendering and retained manifest;
- no generated sample disclosure and exact official-channel copy.

## Boundary

V1 is an integrity and completeness contract, not a signature or identity system. It cannot prove who a reviewer is, whether they had authority, whether evidence was revoked, or whether the campaign may legally ship. `release_scope=demo` must never be interpreted as commercial authorization.
