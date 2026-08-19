# Photo to Organic Knit — Research Archive V1

Archive date: 2026-08-19

Archive tag: `photo-to-organic-knit/v1`

Implementation baseline: `5d3c3b9` (`feat: add photo-to-conceptual-art research pipeline`)

Status: frozen non-production research baseline

## Included scope

- Upstream `NalaZhang27/photo-to-organic-knit` retained as a Git submodule.
- Goal-driven `photo-to-conceptual-art` Skill and installed copy.
- Six visual effects, four scenario profiles and four delivery templates.
- Independent before/after, forward tests and cross-subject pilot evidence.
- Chinese sample and approved-mode publication layouts.
- Deterministic 4:5, 16:9, 3:4 and A4-style publication outputs.
- Local Publication Studio with single-template and batch ZIP flows.
- Release Manifest, Ed25519 detached signature, trusted public-key demo and hash-chained audit evidence.
- Non-production Action Runbook with explicit stop and failure rules.

## Fixed dependencies and evidence

- Upstream commit: `b84efe522e758649e46fe59f34d700eb60bedc12`
- Branch: `codex/photo-to-organic-knit-research`
- Installed Skill source files: 57
- Source/install SHA-256 differences at archive time: 0
- Skill tests: 28/28 passed
- Publication Studio tests: 6/6 passed repeatedly
- Project verifier: PASS
- Retained private-key or PEM files: 0
- Python cache directories: 0

## Archive boundary

This archive is a research and local-demonstration baseline. It is not a production publishing system and does not authorize real brands, product claims, customer assets, public deployment, organizational identities, KMS/HSM custody or commercial release.

The retained Demo public key, detached signature and audit event are workflow evidence only. The one-time Demo private key was deleted before archival.

## Resume criteria

Reopen this archive only for one of these explicitly authorized tracks:

1. A 20–50 item cross-subject benchmark.
2. Real browser viewport, keyboard and accessibility evidence.
3. A Studio approval-panel demo that cannot fabricate approvals.
4. One authorized real-content pilot with supplied assets, copy, permissions and reviewers.
5. A separately approved production architecture with real identity, KMS/HSM and remote immutable audit decisions.

## Restore

```text
git switch codex/photo-to-organic-knit-research
git checkout photo-to-organic-knit/v1
git submodule update --init --recursive
```

Use the branch to continue work. Use the tag for a read-only historical checkout.
