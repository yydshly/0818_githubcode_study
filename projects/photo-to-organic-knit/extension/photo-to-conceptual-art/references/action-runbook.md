# Non-Production Action Runbook

Read this reference before operating a retained benchmark, publication demo, or approved release packet. It defines actions and stop rules; it does not authorize external publication.

## Standard actions

| Stage | Action | Required evidence | Stop condition |
| --- | --- | --- | --- |
| 1. Goal lock | Record audience, delivery, privacy and preservation requirements. | Request and intended delivery. | A consequential requirement is unknown. |
| 2. Essence | Write source-grounded retain/transform/discard decisions. | Essence JSON and source path. | Identity, quantity or permission cannot be established. |
| 3. Route | Compile scenario, effect and delivery without hand-editing the compiled prompt. | Route JSON and prompt. | Route is disallowed or conflicts with purpose. |
| 4. Generate | Produce wordless Key Art; correct one failed visual gate at a time. | Output path and attempts. | The same gate fails after two targeted corrections. |
| 5. Review | Record evidence for every scenario and delivery gate. | Review JSON and deterministic score summary. | Any required gate is fail or unverified. |
| 6A. Sample publish | Use `copy_status=sample`; render without release-security inputs. | Copy JSON, PNGs and report. | Exact-copy, overflow, contrast, protected-region or dimension gate fails. |
| 6B. Approved publish | Finalize copy/art, build Manifest, complete five approvals, sign offline, verify trust, render and append audit. | Manifest, signature, trust snapshot, outputs, report and audit event. | Any approval, hash, signature, trust or audit check fails. |
| 7. Retain | Preserve exact inputs, output hashes, reports and boundaries. | Reproducible result record. | Private key or unapproved private source would enter the retained package. |

## Failure actions

| Failure | Required action | Do not do |
| --- | --- | --- |
| Source anchors are uncertain | Stop and obtain source/permission clarification. | Invent quantities, identity or provenance. |
| Key Art misses one declared gate | Correct only that gate and re-review. | Change multiple variables or hide the failed attempt. |
| Same art gate fails twice | Stop generation and report the unresolved gate. | Retry indefinitely or cherry-pick an unrecorded candidate. |
| Copy overflows | Shorten or explicitly re-break approved copy; rerun all layout gates. | Shrink text indefinitely or ask ImageGen to draw words. |
| Copy intersects a protected region | Change template composition or regenerate a safer Key Art field. | Cover a required subject anchor. |
| Copy/art hash changes after approval | Invalidate prior approvals and build a new Manifest draft. | Reuse the old Manifest or signature. |
| Approval remains pending | Stop approved rendering. | Mark it approved on behalf of the owner. |
| Signature or trusted key fails | Freeze the release; verify key ID, status, scope, signer and exact manifest bytes. | Bypass verification or silently switch keys. |
| Audit chain fails | Freeze the release, preserve the failing log, and recover from an independently verified head. | Truncate, rewrite or start a replacement chain without recording the incident. |
| Private key appears in project/output | Stop, remove it from retained artifacts, rotate the key if exposure was real, and re-sign. | Commit, upload or include the private key in a release ZIP. |

## Current non-production backlog

1. Freeze the current research baseline in version control after the user explicitly requests a commit.
2. Run a 20–50 item benchmark across people, products, communities and travel; record route choice, attempts, gate failures and human time.
3. Add real browser viewport, keyboard and accessibility evidence when programmable browser control is available.
4. Add a Studio approval-panel demo that creates Manifest drafts but never fabricates completed approvals.
5. Run one authorized real-content pilot only after the user supplies the assets, copy, permissions and reviewers.

## Defer until production is authorized

- Public hosting, accounts, authentication and organization roles.
- Real KMS/HSM private-key custody, rotation and revocation distribution.
- Remote immutable audit storage and independent trusted timestamps.
- Persistent customer asset storage, arbitrary uploads, billing, analytics and publication integrations.

These are not missing demo polish. They require real external systems, authority, privacy decisions and operating ownership.
