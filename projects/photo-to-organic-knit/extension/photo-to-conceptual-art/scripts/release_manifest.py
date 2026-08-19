#!/usr/bin/env python3
"""Build draft Release Manifest files and validate approved release packets."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


APPROVAL_OWNERS = ("brand", "copy", "legal", "design", "channel")
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")


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


def parse_approved_at(value: Any, label: str) -> str:
    text = require_text(value, label, maximum=40)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{label} must include a timezone")
    return text


def build_draft(copy_path: Path, art_path: Path, release_id: str, scope: str) -> dict[str, Any]:
    copy = load_json(copy_path)
    if copy.get("copy_status") != "approved":
        raise ValueError("a Release Manifest draft requires copy_status=approved")
    campaign_id = require_text(copy.get("campaign_id"), "copy.campaign_id", maximum=64)
    template = require_text(copy.get("template"), "copy.template", maximum=64)
    if not ID_PATTERN.fullmatch(release_id):
        raise ValueError("release_id must be stable kebab-case")
    if scope not in {"demo", "production"}:
        raise ValueError("release_scope must be demo or production")
    if not art_path.is_file():
        raise ValueError(f"art file not found: {art_path}")
    return {
        "schema_version": "1.0",
        "release_id": release_id,
        "release_scope": scope,
        "campaign_id": campaign_id,
        "template": template,
        "copy_sha256": file_sha256(copy_path),
        "art_sha256": file_sha256(art_path),
        "approvals": {
            owner: {"status": "pending", "reviewer": "", "approved_at": "", "evidence": ""}
            for owner in APPROVAL_OWNERS
        },
    }


def validate_approved_manifest(
    payload: dict[str, Any],
    *,
    manifest_path: Path,
    copy_payload: dict[str, Any],
    copy_path: Path,
    art_path: Path,
) -> dict[str, Any]:
    require_exact_keys(
        payload,
        {"schema_version", "release_id", "release_scope", "campaign_id", "template", "copy_sha256", "art_sha256", "approvals"},
        "release manifest",
    )
    if payload["schema_version"] != "1.0":
        raise ValueError("release manifest schema_version must be 1.0")
    release_id = require_text(payload["release_id"], "release_id", maximum=64)
    if not ID_PATTERN.fullmatch(release_id):
        raise ValueError("release_id must be stable kebab-case")
    if payload["release_scope"] not in {"demo", "production"}:
        raise ValueError("release_scope must be demo or production")
    if payload["campaign_id"] != copy_payload.get("campaign_id"):
        raise ValueError("release manifest campaign_id does not match copy")
    if payload["template"] != copy_payload.get("template"):
        raise ValueError("release manifest template does not match copy")
    for key in ("copy_sha256", "art_sha256"):
        if not isinstance(payload[key], str) or not HASH_PATTERN.fullmatch(payload[key]):
            raise ValueError(f"release manifest {key} must be lowercase SHA-256")
    actual_copy_hash = file_sha256(copy_path)
    actual_art_hash = file_sha256(art_path)
    if payload["copy_sha256"] != actual_copy_hash:
        raise ValueError("release manifest copy_sha256 does not match current copy")
    if payload["art_sha256"] != actual_art_hash:
        raise ValueError("release manifest art_sha256 does not match current art")
    approvals = payload["approvals"]
    if not isinstance(approvals, dict):
        raise ValueError("release manifest approvals must be an object")
    require_exact_keys(approvals, set(APPROVAL_OWNERS), "release manifest approvals")
    approval_summary: dict[str, Any] = {}
    for owner in APPROVAL_OWNERS:
        approval = approvals[owner]
        if not isinstance(approval, dict):
            raise ValueError(f"approval {owner} must be an object")
        require_exact_keys(approval, {"status", "reviewer", "approved_at", "evidence"}, f"approval {owner}")
        if approval["status"] != "approved":
            raise ValueError(f"approval {owner} is not approved")
        reviewer = require_text(approval["reviewer"], f"approval {owner}.reviewer", maximum=80)
        approved_at = parse_approved_at(approval["approved_at"], f"approval {owner}.approved_at")
        evidence = require_text(approval["evidence"], f"approval {owner}.evidence", maximum=160)
        approval_summary[owner] = {"status": "approved", "reviewer": reviewer, "approved_at": approved_at, "evidence": evidence}
    return {
        "required": True,
        "status": "PASS",
        "release_id": release_id,
        "release_scope": payload["release_scope"],
        "manifest_sha256": file_sha256(manifest_path),
        "copy_sha256": actual_copy_hash,
        "art_sha256": actual_art_hash,
        "approvals": approval_summary,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--copy", required=True, type=Path)
    parser.add_argument("--art", required=True, type=Path)
    parser.add_argument("--release-id", required=True)
    parser.add_argument("--scope", choices=("demo", "production"), default="production")
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--force", action="store_true", help="Replace an existing draft file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.out.exists() and not args.force:
            raise ValueError(f"output already exists: {args.out}; pass --force to replace")
        payload = build_draft(args.copy, args.art, args.release_id, args.scope)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"status": "DRAFT", "path": str(args.out.resolve()), "release_id": payload["release_id"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
