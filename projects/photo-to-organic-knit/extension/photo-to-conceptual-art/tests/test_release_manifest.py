from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "release_manifest.py"
EXAMPLES = ROOT / "examples"


def run_builder(*args: str) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "utf-8"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=environment,
    )


class ReleaseManifestTests(unittest.TestCase):
    def test_builder_creates_hash_bound_pending_draft(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            art = root / "art.png"
            output = root / "release.json"
            art.write_bytes(b"test-art-bytes")
            copy = EXAMPLES / "honey-campaign-approved-demo.json"
            result = run_builder(
                "--copy", str(copy),
                "--art", str(art),
                "--release-id", "honey-release-test",
                "--scope", "demo",
                "--out", str(output),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["release_id"], "honey-release-test")
            self.assertEqual(payload["copy_sha256"], hashlib.sha256(copy.read_bytes()).hexdigest())
            self.assertEqual(payload["art_sha256"], hashlib.sha256(art.read_bytes()).hexdigest())
            self.assertEqual(set(payload["approvals"]), {"brand", "copy", "legal", "design", "channel"})
            self.assertTrue(all(record["status"] == "pending" for record in payload["approvals"].values()))
            repeated = run_builder(
                "--copy", str(copy),
                "--art", str(art),
                "--release-id", "honey-release-test",
                "--out", str(output),
            )
            self.assertEqual(repeated.returncode, 2)
            self.assertIn("already exists", repeated.stderr)

    def test_builder_rejects_sample_copy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            art = root / "art.png"
            art.write_bytes(b"test-art-bytes")
            result = run_builder(
                "--copy", str(EXAMPLES / "honey-campaign-copy.json"),
                "--art", str(art),
                "--release-id", "sample-must-fail",
                "--out", str(root / "release.json"),
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("copy_status=approved", result.stderr)


if __name__ == "__main__":
    unittest.main()
