# Release Security V1

Read this reference when an approved Release Manifest must be signed and audited. This layer uses detached Ed25519 signatures and a local hash-chained JSONL audit log.

## Key boundary

- Generate and store private keys outside the repository.
- Commit or distribute only public trust records, detached signatures, manifests, reports and audit evidence.
- V1 unencrypted private PEM output is for local demonstration/bootstrap only. Production keys belong in an HSM, KMS or equivalent controlled signer.

## Commands

Generate a local keypair and public trust store:

```text
python scripts/release_security.py keygen --key-id <id> --owner <name> --scope production --private-out <outside-repo.pem> --trust-out <trusted-keys.json>
```

Sign the exact manifest bytes offline:

```text
python scripts/release_security.py sign --manifest <release.json> --private-key <outside-repo.pem> --key-id <id> --signer <name> --out <signature.json>
```

Verify independently:

```text
python scripts/release_security.py verify --manifest <release.json> --signature <signature.json> --trusted-keys <trusted-keys.json>
python scripts/release_security.py audit-verify --audit-log <audit.jsonl>
```

Approved rendering requires manifest, signature, trust store and audit log:

```text
python scripts/render_layout.py --copy <copy.json> --art <art.png> --release-manifest <release.json> --release-signature <signature.json> --trusted-keys <trusted-keys.json> --audit-log <audit.jsonl> --out-dir <directory>
```

## Trust store

Each key record fixes algorithm, public key, status, scope and owner. Unknown or non-active keys fail. The signature signer must match the trusted owner, and the key scope must match the manifest release scope.

## Audit chain

Every successful approved render appends one event containing release/signing identity, exact input hashes, output hashes, the previous event hash and its own computed event hash. The existing chain is verified before append.

## Boundaries

- A verified signature proves control of a private key corresponding to a trusted public key; it does not prove the human's real-world identity or authority.
- A local JSONL hash chain exposes modification but cannot prevent deletion or rollback. Production audit belongs in remote append-only storage with independent retention and timestamping.
- Key rotation, revocation distribution, multi-signature quorum, hardware-backed signing and organizational authentication remain outside V1.
