# Release Manifest V1

Read this reference whenever `copy_status` is `approved`. Approved rendering is forbidden without a manifest that binds the exact copy and art inputs to five completed external approvals.

## Schema

```json
{
  "schema_version": "1.0",
  "release_id": "stable-kebab-case-id",
  "release_scope": "demo",
  "campaign_id": "must-match-copy",
  "template": "must-match-copy",
  "copy_sha256": "64 lowercase hex characters",
  "art_sha256": "64 lowercase hex characters",
  "approvals": {
    "brand": {
      "status": "approved",
      "reviewer": "named owner or accountable role",
      "approved_at": "2026-08-19T10:00:00+08:00",
      "evidence": "approval record identifier"
    },
    "copy": {},
    "legal": {},
    "design": {},
    "channel": {}
  }
}
```

Every approval object has exactly `status`, `reviewer`, `approved_at`, and `evidence`. The five owner IDs are fixed. `approved_at` must contain a timezone.

## Lifecycle

1. Create a draft after copy and Key Art are final:

   ```text
   python scripts/release_manifest.py --copy <copy.json> --art <art.png> --release-id <id> --scope production --out <manifest.json>
   ```

2. The draft contains input hashes and five `pending` approval records. External owners replace each pending record with real reviewer, timestamp, and evidence.
3. Do not edit the copy or art after approval. Any byte change alters its SHA-256 and invalidates the release.
4. Read `release-security.md`, sign the completed manifest, then render with the signature, trust store and audit destination:

   ```text
   python scripts/render_layout.py --copy <copy.json> --art <art.png> --release-manifest <manifest.json> --release-signature <signature.json> --trusted-keys <trusted-keys.json> --audit-log <audit.jsonl> --out-dir <directory>
   ```

## Boundaries

- `release_scope=demo` supports retained workflow demonstrations. It is not commercial authorization.
- `release_scope=production` identifies intended real use but does not verify reviewer identity, signature validity, legal authority, or revocation.
- The manifest is an auditable input contract, not a digital-signature system.
- Sample rendering must not receive a Release Manifest. Approved rendering must receive exactly one valid manifest.
