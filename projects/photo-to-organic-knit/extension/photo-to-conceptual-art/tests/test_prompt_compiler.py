from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_prompt.py"
EXAMPLES = ROOT / "examples"


def run_compiler(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


class PromptCompilerTests(unittest.TestCase):
    def test_all_profiles_are_valid_json_with_matching_ids(self) -> None:
        for kind in ("effects", "scenarios", "deliveries"):
            paths = sorted((ROOT / "profiles" / kind).glob("*.json"))
            self.assertTrue(paths, f"no profiles found for {kind}")
            for path in paths:
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(payload["id"], path.stem)

    def assert_route(self, example: str, scenario: str, effect: str, delivery: str) -> None:
        result = run_compiler(
            "--essence", str(EXAMPLES / example),
            "--scenario", scenario,
            "--format", "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["route"]["effect"], effect)
        self.assertEqual(payload["route"]["delivery"], delivery)
        self.assertIn("wordless-key-art", payload["prompt"])
        self.assertIn("Quality gates:", payload["prompt"])

    def test_auto_routes_family(self) -> None:
        self.assert_route("family-essence.json", "family-memory", "organic-knit", "book-cover")

    def test_auto_routes_travel(self) -> None:
        self.assert_route("canoe-essence.json", "travel-cover", "woodcut", "field-journal")

    def test_unseen_lighthouse_route_includes_explicit_metadata_bands(self) -> None:
        result = run_compiler(
            "--essence", str(ROOT / "forward-tests" / "lighthouse-travel" / "essence.json"),
            "--scenario", "travel-cover",
            "--format", "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["route"]["effect"], "woodcut")
        self.assertIn("top approximately 10%", payload["prompt"])
        self.assertIn("bottom approximately 10%", payload["prompt"])

    def test_cross_subject_pilot_routes(self) -> None:
        cases = (
            ("person-essence.json", "family-memory", "organic-knit", "book-cover"),
            ("product-essence.json", "seasonal-campaign", "layered-paper", "campaign-poster"),
            ("architecture-essence.json", "travel-cover", "woodcut", "field-journal"),
        )
        for essence, scenario, effect, delivery in cases:
            result = run_compiler(
                "--essence", str(ROOT / "forward-tests" / "pilot-n3" / essence),
                "--scenario", scenario,
                "--format", "json",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            route = json.loads(result.stdout)["route"]
            self.assertEqual(route["effect"], effect)
            self.assertEqual(route["delivery"], delivery)

    def test_auto_routes_impact(self) -> None:
        self.assert_route("community-essence.json", "impact-report", "stained-glass", "impact-report")

    def test_auto_routes_campaign(self) -> None:
        self.assert_route("bakery-essence.json", "seasonal-campaign", "layered-paper", "campaign-poster")

    def test_explicit_effect_override(self) -> None:
        result = run_compiler(
            "--essence", str(EXAMPLES / "canoe-essence.json"),
            "--scenario", "travel-cover",
            "--effect", "layered-paper",
            "--format", "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["route"]["effect"], "layered-paper")
        self.assertIn("Paper", payload["prompt"])

    def test_unknown_effect_fails(self) -> None:
        result = run_compiler(
            "--essence", str(EXAMPLES / "canoe-essence.json"),
            "--scenario", "travel-cover",
            "--effect", "missing-effect",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("file not found", result.stderr)

    def test_unlisted_delivery_fails(self) -> None:
        result = run_compiler(
            "--essence", str(EXAMPLES / "family-essence.json"),
            "--scenario", "family-memory",
            "--delivery", "impact-report",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("not allowed", result.stderr)

    def test_malformed_essence_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            invalid = Path(directory) / "invalid.json"
            invalid.write_text(json.dumps({"orientation": "landscape"}), encoding="utf-8")
            result = run_compiler(
                "--essence", str(invalid),
                "--scenario", "travel-cover",
            )
        self.assertEqual(result.returncode, 2)
        self.assertIn("missing anchors", result.stderr)


if __name__ == "__main__":
    unittest.main()
