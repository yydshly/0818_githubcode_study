#!/usr/bin/env python3
"""Compile visual essence plus scenario/effect/delivery profiles into a prompt."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILES = SKILL_ROOT / "profiles"
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_ESSENCE = {
    "orientation": str,
    "aspect_ratio": str,
    "subject": str,
    "anchors": list,
    "relationships": list,
    "emotion": list,
    "visual_path": str,
    "metaphor": str,
    "retain": list,
    "transform": list,
    "discard": list,
    "palette": list,
    "privacy_notes": list,
}
ARRAY_FIELDS = {key for key, value in REQUIRED_ESSENCE.items() if value is list}


class BriefError(ValueError):
    """Raised when essence or profile data cannot form a safe route."""


def read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise BriefError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise BriefError(f"invalid JSON in {path}: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise BriefError(f"expected a JSON object in {path}")
    return payload


def validate_id(value: str, label: str) -> None:
    if not ID_PATTERN.fullmatch(value):
        raise BriefError(f"invalid {label} id: {value!r}")


def load_profile(root: Path, kind: str, profile_id: str) -> dict[str, Any]:
    validate_id(profile_id, kind)
    path = root / kind / f"{profile_id}.json"
    profile = read_json(path)
    if profile.get("id") != profile_id:
        raise BriefError(f"profile id mismatch in {path}")
    return profile


def validate_essence(essence: dict[str, Any]) -> None:
    problems: list[str] = []
    for key, expected_type in REQUIRED_ESSENCE.items():
        if key not in essence:
            problems.append(f"missing {key}")
            continue
        if not isinstance(essence[key], expected_type):
            problems.append(f"{key} must be {expected_type.__name__}")
    if problems:
        raise BriefError("invalid essence: " + "; ".join(problems))
    if essence["orientation"] not in {"landscape", "portrait", "square"}:
        problems.append("orientation must be landscape, portrait, or square")
    if not re.fullmatch(r"\d+(?:\.\d+)?:\d+(?:\.\d+)?", essence["aspect_ratio"]):
        problems.append("aspect_ratio must look like 3:2, 4:5, or 1:1")
    for key in ARRAY_FIELDS:
        values = essence[key]
        if any(not isinstance(item, str) or not item.strip() for item in values):
            problems.append(f"{key} must contain non-empty strings")
    for key in ("anchors", "retain", "transform"):
        if not essence[key]:
            problems.append(f"{key} must not be empty")
    for key in ("subject", "visual_path", "metaphor"):
        if not essence[key].strip():
            problems.append(f"{key} must not be empty")
    if problems:
        raise BriefError("invalid essence: " + "; ".join(problems))


def select_effect(
    scenario: dict[str, Any],
    profiles_root: Path,
    requested: str,
) -> tuple[dict[str, Any], str]:
    recommendations = scenario.get("recommended_effects")
    if not isinstance(recommendations, list) or not recommendations:
        raise BriefError(f"scenario {scenario['id']} has no recommended effects")
    if requested != "auto":
        effect = load_profile(profiles_root, "effects", requested)
        reason = next(
            (item.get("reason", "User-selected effect override.") for item in recommendations if item.get("id") == requested),
            "User-selected effect override outside the scenario recommendation list.",
        )
        return effect, reason
    for item in recommendations:
        effect_id = item.get("id")
        if not isinstance(effect_id, str):
            continue
        try:
            return load_profile(profiles_root, "effects", effect_id), item.get("reason", "Scenario default.")
        except BriefError:
            continue
    raise BriefError(f"scenario {scenario['id']} has no available recommended effect profile")


def select_delivery(
    scenario: dict[str, Any],
    profiles_root: Path,
    requested: str | None,
) -> dict[str, Any]:
    delivery_id = requested or scenario.get("default_delivery")
    if not isinstance(delivery_id, str):
        raise BriefError(f"scenario {scenario['id']} has no default delivery")
    allowed = scenario.get("allowed_deliveries", [])
    if delivery_id not in allowed:
        raise BriefError(
            f"delivery {delivery_id!r} is not allowed for scenario {scenario['id']}; "
            f"choose one of: {', '.join(allowed)}"
        )
    return load_profile(profiles_root, "deliveries", delivery_id)


def join_items(values: list[str]) -> str:
    return "; ".join(value.strip() for value in values if value.strip())


def compile_route(
    essence: dict[str, Any],
    scenario: dict[str, Any],
    effect: dict[str, Any],
    delivery: dict[str, Any],
    route_reason: str,
) -> dict[str, Any]:
    gates = list(dict.fromkeys(scenario.get("quality_gates", []) + delivery.get("quality_gates", [])))
    avoid = effect.get("avoid", [])
    privacy = essence.get("privacy_notes", [])
    lines = [
        "Use case: style-transfer",
        f"Asset type: {delivery['label']} for {scenario['label']}",
        "Input image: Image 1 is the subject and semantic reference. Preserve required anchors and relationships; recompose rather than trace.",
        f"Source orientation: {essence['orientation']} {essence['aspect_ratio']}. Delivery aspect: {delivery['aspect_ratio']}.",
        f"Audience: {scenario['audience']}",
        f"Scenario goal: {scenario['goal']}",
        f"Subject: {essence['subject']}",
        f"Anchors: {join_items(essence['anchors'])}",
        f"Relationships: {join_items(essence['relationships'])}",
        f"Emotion: {join_items(essence['emotion'])}",
        f"Visual path: {essence['visual_path']}",
        f"Retain: {join_items(essence['retain'])}",
        f"Transform from source: {join_items(essence['transform'])}",
        f"Discard: {join_items(essence['discard'])}",
        f"Concept: {essence['metaphor']}",
        f"Effect: {effect['label']} — {effect['intent']}",
        f"Materials: {join_items(effect['materials'])}",
        f"Path treatment: {effect['path_treatment']}",
        f"Form treatment: {effect['form_treatment']}",
        f"Space treatment: {effect['space_treatment']}",
        f"Composition: {effect['composition']} {delivery['layout_intent']}",
        f"Delivery safety: {delivery['safe_area']}",
        f"Handmade variation: {join_items(effect['imperfections'])}",
        f"Palette anchors: {join_items(essence['palette']) or 'derive a restrained palette from the source'}",
        f"Text policy: {delivery['text_mode']}; do not generate title, logo, date, metrics, price, legal copy, or call to action inside the art layer.",
        f"Scenario requirements: {join_items(scenario.get('prompt_requirements', []))}",
        f"Quality gates: {join_items(gates)}",
        f"Privacy: {join_items(privacy) if privacy else 'no additional privacy transformation recorded'}",
        f"Avoid: {join_items(avoid)}; extra text; watermark; signature; unrelated objects.",
    ]
    return {
        "route": {
            "scenario": scenario["id"],
            "effect": effect["id"],
            "delivery": delivery["id"],
            "reason": route_reason,
        },
        "quality_gates": gates,
        "output_variants": delivery.get("output_variants", []),
        "prompt": "\n".join(lines),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--essence", type=Path, required=True)
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--effect", default="auto")
    parser.add_argument("--delivery")
    parser.add_argument("--profiles-root", type=Path, default=DEFAULT_PROFILES)
    parser.add_argument("--format", choices=("prompt", "json"), default="prompt")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        essence = read_json(args.essence)
        validate_essence(essence)
        scenario = load_profile(args.profiles_root, "scenarios", args.scenario)
        effect, reason = select_effect(scenario, args.profiles_root, args.effect)
        delivery = select_delivery(scenario, args.profiles_root, args.delivery)
        result = compile_route(essence, scenario, effect, delivery, reason)
    except BriefError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["prompt"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
