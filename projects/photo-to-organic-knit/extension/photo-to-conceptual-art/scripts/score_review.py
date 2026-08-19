#!/usr/bin/env python3
"""Validate a human gate review and compute a deterministic summary."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from build_prompt import BriefError, DEFAULT_PROFILES, load_profile, read_json


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


VALID_STATUSES = {"pass", "fail", "unverified"}


def required_gates(scenario: dict[str, Any], delivery: dict[str, Any]) -> list[str]:
    return list(dict.fromkeys(scenario.get("quality_gates", []) + delivery.get("quality_gates", [])))


def validate_review(review: dict[str, Any], required: list[str]) -> dict[str, Any]:
    for field in ("id", "artifact", "reviewer"):
        if not isinstance(review.get(field), str) or not review[field].strip():
            raise BriefError(f"review {field} must be a non-empty string")
    if not isinstance(review.get("attempt"), int) or review["attempt"] < 1:
        raise BriefError("review attempt must be a positive integer")
    gates = review.get("gates")
    if not isinstance(gates, dict):
        raise BriefError("review gates must be an object")
    required_set = set(required)
    actual_set = set(gates)
    missing = sorted(required_set - actual_set)
    extra = sorted(actual_set - required_set)
    if missing or extra:
        parts = []
        if missing:
            parts.append("missing: " + ", ".join(missing))
        if extra:
            parts.append("extra: " + ", ".join(extra))
        raise BriefError("review gate mismatch (" + "; ".join(parts) + ")")

    normalized: list[dict[str, Any]] = []
    counts = {"pass": 0, "fail": 0, "unverified": 0}
    earned = 0
    for gate in required:
        item = gates[gate]
        if not isinstance(item, dict):
            raise BriefError(f"gate {gate!r} must be an object")
        status = item.get("status")
        score = item.get("score")
        evidence = item.get("evidence")
        if status not in VALID_STATUSES:
            raise BriefError(f"gate {gate!r} has invalid status: {status!r}")
        if not isinstance(score, int) or not 0 <= score <= 5:
            raise BriefError(f"gate {gate!r} score must be an integer from 0 to 5")
        if not isinstance(evidence, str) or not evidence.strip():
            raise BriefError(f"gate {gate!r} requires concrete evidence")
        if status == "pass" and score < 3:
            raise BriefError(f"gate {gate!r} pass score must be 3 to 5")
        if status == "fail" and score > 2:
            raise BriefError(f"gate {gate!r} fail score must be 0 to 2")
        if status == "unverified" and score != 0:
            raise BriefError(f"gate {gate!r} unverified score must be 0")
        counts[status] += 1
        earned += score
        normalized.append({"gate": gate, "status": status, "score": score, "evidence": evidence.strip()})

    decision = "fail" if counts["fail"] else "needs-review" if counts["unverified"] else "pass"
    maximum = len(required) * 5
    return {
        "review_id": review["id"],
        "artifact": review["artifact"],
        "attempt": review["attempt"],
        "decision": decision,
        "counts": counts,
        "score": {
            "earned": earned,
            "maximum": maximum,
            "percent": round((earned / maximum) * 100, 1) if maximum else 0.0,
        },
        "gates": normalized,
        "notes": review.get("notes", []),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--delivery", required=True)
    parser.add_argument("--profiles-root", type=Path, default=DEFAULT_PROFILES)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        scenario = load_profile(args.profiles_root, "scenarios", args.scenario)
        if args.delivery not in scenario.get("allowed_deliveries", []):
            raise BriefError(f"delivery {args.delivery!r} is not allowed for scenario {args.scenario}")
        delivery = load_profile(args.profiles_root, "deliveries", args.delivery)
        review = read_json(args.review)
        summary = validate_review(review, required_gates(scenario, delivery))
    except BriefError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        score = summary["score"]
        counts = summary["counts"]
        print(f"{summary['decision'].upper()} — {score['earned']}/{score['maximum']} ({score['percent']}%)")
        print(f"pass={counts['pass']} fail={counts['fail']} unverified={counts['unverified']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
