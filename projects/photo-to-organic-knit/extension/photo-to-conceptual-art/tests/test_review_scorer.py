from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "score_review.py"
EXAMPLE = ROOT / "forward-tests" / "lighthouse-travel" / "review-auto-v2.json"


def run_scorer(review: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--review", str(review),
            "--scenario", "travel-cover",
            "--delivery", "field-journal",
            "--format", "json",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


class ReviewScorerTests(unittest.TestCase):
    def test_valid_review_passes(self) -> None:
        result = run_scorer(EXAMPLE)
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["decision"], "pass")
        self.assertEqual(summary["score"]["earned"], 40)
        self.assertEqual(summary["counts"]["pass"], 8)

    def test_missing_gate_fails_closed(self) -> None:
        payload = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        payload["gates"].pop("route clarity")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            result = run_scorer(path)
        self.assertEqual(result.returncode, 2)
        self.assertIn("missing: route clarity", result.stderr)

    def test_valid_failed_gate_produces_fail_decision(self) -> None:
        payload = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        payload["gates"]["thumbnail silhouette"] = {
            "status": "fail",
            "score": 2,
            "evidence": "Traveler and bicycle merge into the background at thumbnail size."
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "failed.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            result = run_scorer(path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["decision"], "fail")

    def test_invalid_status_fails_closed(self) -> None:
        payload = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        payload["gates"]["direction"]["status"] = "maybe"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid-status.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            result = run_scorer(path)
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid status", result.stderr)


if __name__ == "__main__":
    unittest.main()
