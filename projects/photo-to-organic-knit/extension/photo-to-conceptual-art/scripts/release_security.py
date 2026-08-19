#!/usr/bin/env python3
"""Ed25519 release signatures and hash-chained audit evidence."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey


HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ZERO_HASH = "0" * 64


def canonical_json(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return payload


def require_exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    if missing or unexpected:
        details = []
        if missing:
            details.append(f"missing {missing}")
        if unexpected:
            details.append(f"unexpected {unexpected}")
        raise ValueError(f"{label} has invalid keys: {', '.join(details)}")


def require_text(value: Any, label: str, maximum: int = 160) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ValueError(f"{label} must be a trimmed non-empty string")
    if len(value) > maximum or any(ord(character) < 32 for character in value):
        raise ValueError(f"{label} is invalid")
    return value


def parse_timestamp(value: Any, label: str) -> str:
    text = require_text(value, label, maximum=40)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{label} must include a timezone")
    return text


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def generate_keypair(key_id: str, owner: str, scope: str, private_out: Path, trust_out: Path) -> dict[str, Any]:
    if not ID_PATTERN.fullmatch(key_id):
        raise ValueError("key_id must be stable kebab-case")
    owner = require_text(owner, "owner", maximum=80)
    if scope not in {"demo", "production"}:
        raise ValueError("scope must be demo or production")
    for path in (private_out, trust_out):
        if path.exists():
            raise ValueError(f"refusing to replace existing file: {path}")
    private_key = Ed25519PrivateKey.generate()
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_bytes = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    trust = {
        "schema_version": "1.0",
        "keys": {
            key_id: {
                "algorithm": "Ed25519",
                "public_key_base64": base64.b64encode(public_bytes).decode("ascii"),
                "status": "active",
                "scope": scope,
                "owner": owner,
            }
        },
    }
    private_out.parent.mkdir(parents=True, exist_ok=True)
    trust_out.parent.mkdir(parents=True, exist_ok=True)
    private_out.write_bytes(private_bytes)
    try:
        os.chmod(private_out, 0o600)
    except OSError:
        pass
    trust_out.write_text(json.dumps(trust, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return trust


def sign_manifest(
    manifest_path: Path,
    private_key_path: Path,
    key_id: str,
    signer: str,
    signature_out: Path,
    signed_at: str | None = None,
) -> dict[str, Any]:
    if signature_out.exists():
        raise ValueError(f"refusing to replace existing file: {signature_out}")
    if not ID_PATTERN.fullmatch(key_id):
        raise ValueError("key_id must be stable kebab-case")
    signer = require_text(signer, "signer", maximum=80)
    timestamp = parse_timestamp(signed_at or now_utc(), "signed_at")
    try:
        private_key = serialization.load_pem_private_key(private_key_path.read_bytes(), password=None)
    except (OSError, ValueError, TypeError) as exc:
        raise ValueError(f"cannot load Ed25519 private key: {exc}") from exc
    if not isinstance(private_key, Ed25519PrivateKey):
        raise ValueError("private key must be Ed25519")
    manifest_bytes = manifest_path.read_bytes()
    signature = private_key.sign(manifest_bytes)
    payload = {
        "schema_version": "1.0",
        "algorithm": "Ed25519",
        "key_id": key_id,
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "signature_base64": base64.b64encode(signature).decode("ascii"),
        "signed_at": timestamp,
        "signer": signer,
    }
    signature_out.parent.mkdir(parents=True, exist_ok=True)
    signature_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def validate_signature(
    manifest_path: Path,
    signature_path: Path,
    trust_store_path: Path,
    manifest_payload: dict[str, Any],
) -> dict[str, Any]:
    signature = load_json(signature_path)
    trust = load_json(trust_store_path)
    require_exact_keys(signature, {"schema_version", "algorithm", "key_id", "manifest_sha256", "signature_base64", "signed_at", "signer"}, "release signature")
    require_exact_keys(trust, {"schema_version", "keys"}, "trusted keys")
    if signature["schema_version"] != "1.0" or trust["schema_version"] != "1.0":
        raise ValueError("signature and trust schemas must be 1.0")
    if signature["algorithm"] != "Ed25519":
        raise ValueError("release signature algorithm must be Ed25519")
    key_id = require_text(signature["key_id"], "signature.key_id", maximum=64)
    if not ID_PATTERN.fullmatch(key_id):
        raise ValueError("signature key_id must be stable kebab-case")
    keys = trust["keys"]
    if not isinstance(keys, dict) or key_id not in keys:
        raise ValueError("release signature key_id is not trusted")
    record = keys[key_id]
    if not isinstance(record, dict):
        raise ValueError("trusted key record must be an object")
    require_exact_keys(record, {"algorithm", "public_key_base64", "status", "scope", "owner"}, f"trusted key {key_id}")
    if record["algorithm"] != "Ed25519" or record["status"] != "active":
        raise ValueError("trusted release key is not active Ed25519")
    if record["scope"] != manifest_payload.get("release_scope"):
        raise ValueError("trusted release key scope does not match manifest")
    signer = require_text(signature["signer"], "signature.signer", maximum=80)
    if signer != record["owner"]:
        raise ValueError("release signature signer does not match trusted owner")
    parse_timestamp(signature["signed_at"], "signature.signed_at")
    manifest_bytes = manifest_path.read_bytes()
    manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
    if signature["manifest_sha256"] != manifest_hash:
        raise ValueError("release signature manifest hash does not match")
    try:
        public_bytes = base64.b64decode(record["public_key_base64"], validate=True)
        signature_bytes = base64.b64decode(signature["signature_base64"], validate=True)
    except (ValueError, TypeError) as exc:
        raise ValueError("release signature or public key is invalid base64") from exc
    if len(public_bytes) != 32 or len(signature_bytes) != 64:
        raise ValueError("release signature or Ed25519 public key has invalid length")
    try:
        Ed25519PublicKey.from_public_bytes(public_bytes).verify(signature_bytes, manifest_bytes)
    except InvalidSignature as exc:
        raise ValueError("release signature verification failed") from exc
    return {
        "required": True,
        "status": "PASS",
        "algorithm": "Ed25519",
        "key_id": key_id,
        "signer": signer,
        "signed_at": signature["signed_at"],
        "manifest_sha256": manifest_hash,
        "signature_sha256": file_sha256(signature_path),
        "trust_store_sha256": file_sha256(trust_store_path),
        "key_scope": record["scope"],
    }


def _event_hash(event_without_hash: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(event_without_hash)).hexdigest()


def verify_audit_log(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    previous = ZERO_HASH
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            raise ValueError("audit log contains a blank line")
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"audit log line {index} is invalid JSON") from exc
        if not isinstance(event, dict):
            raise ValueError(f"audit log line {index} must be an object")
        require_exact_keys(event, {"schema_version", "sequence", "event_type", "recorded_at", "release_id", "release_scope", "manifest_sha256", "key_id", "copy_sha256", "art_sha256", "outputs", "previous_event_hash", "event_hash"}, f"audit event {index}")
        if event["schema_version"] != "1.0" or event["event_type"] != "release-rendered":
            raise ValueError(f"audit event {index} has unsupported schema or type")
        if event["sequence"] != index or event["previous_event_hash"] != previous:
            raise ValueError(f"audit event {index} breaks sequence or previous hash")
        parse_timestamp(event["recorded_at"], f"audit event {index}.recorded_at")
        if not isinstance(event["outputs"], dict) or not event["outputs"]:
            raise ValueError(f"audit event {index} outputs must be a non-empty object")
        for name, value in event["outputs"].items():
            require_text(name, f"audit event {index} output name", maximum=80)
            if not isinstance(value, str) or not HASH_PATTERN.fullmatch(value):
                raise ValueError(f"audit event {index} output hash is invalid")
        claimed = event["event_hash"]
        if not isinstance(claimed, str) or not HASH_PATTERN.fullmatch(claimed):
            raise ValueError(f"audit event {index} hash is invalid")
        body = dict(event)
        del body["event_hash"]
        if _event_hash(body) != claimed:
            raise ValueError(f"audit event {index} hash does not verify")
        previous = claimed
        events.append(event)
    return events


def append_audit_event(
    path: Path,
    release_summary: dict[str, Any],
    signature_summary: dict[str, Any],
    outputs: dict[str, Any],
    recorded_at: str | None = None,
) -> dict[str, Any]:
    existing = verify_audit_log(path)
    output_hashes = {variant: data["sha256"] for variant, data in outputs.items()}
    body = {
        "schema_version": "1.0",
        "sequence": len(existing) + 1,
        "event_type": "release-rendered",
        "recorded_at": parse_timestamp(recorded_at or now_utc(), "audit.recorded_at"),
        "release_id": release_summary["release_id"],
        "release_scope": release_summary["release_scope"],
        "manifest_sha256": release_summary["manifest_sha256"],
        "key_id": signature_summary["key_id"],
        "copy_sha256": release_summary["copy_sha256"],
        "art_sha256": release_summary["art_sha256"],
        "outputs": output_hashes,
        "previous_event_hash": existing[-1]["event_hash"] if existing else ZERO_HASH,
    }
    event = {**body, "event_hash": _event_hash(body)}
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
    return event


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    keygen = subparsers.add_parser("keygen")
    keygen.add_argument("--key-id", required=True)
    keygen.add_argument("--owner", required=True)
    keygen.add_argument("--scope", choices=("demo", "production"), required=True)
    keygen.add_argument("--private-out", required=True, type=Path)
    keygen.add_argument("--trust-out", required=True, type=Path)
    sign = subparsers.add_parser("sign")
    sign.add_argument("--manifest", required=True, type=Path)
    sign.add_argument("--private-key", required=True, type=Path)
    sign.add_argument("--key-id", required=True)
    sign.add_argument("--signer", required=True)
    sign.add_argument("--signed-at")
    sign.add_argument("--out", required=True, type=Path)
    verify = subparsers.add_parser("verify")
    verify.add_argument("--manifest", required=True, type=Path)
    verify.add_argument("--signature", required=True, type=Path)
    verify.add_argument("--trusted-keys", required=True, type=Path)
    audit = subparsers.add_parser("audit-verify")
    audit.add_argument("--audit-log", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.command == "keygen":
            result = generate_keypair(args.key_id, args.owner, args.scope, args.private_out, args.trust_out)
            output = {"status": "KEY_GENERATED", "key_id": args.key_id, "trust_store": str(args.trust_out.resolve())}
        elif args.command == "sign":
            result = sign_manifest(args.manifest, args.private_key, args.key_id, args.signer, args.out, args.signed_at)
            output = {"status": "SIGNED", "key_id": result["key_id"], "signature": str(args.out.resolve())}
        elif args.command == "verify":
            manifest = load_json(args.manifest)
            result = validate_signature(args.manifest, args.signature, args.trusted_keys, manifest)
            output = result
        else:
            events = verify_audit_log(args.audit_log)
            output = {"status": "PASS", "events": len(events), "head": events[-1]["event_hash"] if events else ZERO_HASH}
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
