from __future__ import annotations

import json
import hashlib
import base64
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_layout.py"
COPY = ROOT / "examples" / "chinese-tea-copy.json"
EXAMPLES = ROOT / "examples"


def run_renderer(
    copy: Path,
    art: Path,
    out_dir: Path,
    release_manifest: Path | None = None,
    release_signature: Path | None = None,
    trusted_keys: Path | None = None,
    audit_log: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "utf-8"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [
            sys.executable,
            str(SCRIPT),
            "--copy",
            str(copy),
            "--art",
            str(art),
            "--out-dir",
            str(out_dir),
        ]
    if release_manifest is not None:
        command.extend(["--release-manifest", str(release_manifest)])
    if release_signature is not None:
        command.extend(["--release-signature", str(release_signature)])
    if trusted_keys is not None:
        command.extend(["--trusted-keys", str(trusted_keys)])
    if audit_log is not None:
        command.extend(["--audit-log", str(audit_log)])
    return subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=environment,
    )


class LayoutRendererTests(unittest.TestCase):
    def make_art(self, path: Path) -> None:
        image = Image.new("RGB", (1122, 1402), (225, 218, 196))
        image.save(path, format="PNG")

    def make_approved_manifest(self, copy: Path, art: Path, path: Path) -> dict:
        copy_payload = json.loads(copy.read_text(encoding="utf-8"))
        payload = {
            "schema_version": "1.0",
            "release_id": "approved-layout-test",
            "release_scope": "demo",
            "campaign_id": copy_payload["campaign_id"],
            "template": copy_payload["template"],
            "copy_sha256": hashlib.sha256(copy.read_bytes()).hexdigest(),
            "art_sha256": hashlib.sha256(art.read_bytes()).hexdigest(),
            "approvals": {
                owner: {
                    "status": "approved",
                    "reviewer": f"Test {owner.title()} Owner",
                    "approved_at": "2026-08-19T10:00:00+08:00",
                    "evidence": f"test://approval/{owner}",
                }
                for owner in ("brand", "copy", "legal", "design", "channel")
            },
        }
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return payload

    def make_release_security(self, manifest: Path, root: Path) -> tuple[Path, Path, Path]:
        private_key = Ed25519PrivateKey.generate()
        public_bytes = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        signature_bytes = private_key.sign(manifest.read_bytes())
        trust = root / "trusted.json"
        signature = root / "signature.json"
        audit = root / "audit.jsonl"
        trust.write_text(json.dumps({
            "schema_version": "1.0",
            "keys": {
                "test-release-key": {
                    "algorithm": "Ed25519",
                    "public_key_base64": base64.b64encode(public_bytes).decode("ascii"),
                    "status": "active",
                    "scope": "demo",
                    "owner": "Test Release Authority",
                }
            },
        }), encoding="utf-8")
        signature.write_text(json.dumps({
            "schema_version": "1.0",
            "algorithm": "Ed25519",
            "key_id": "test-release-key",
            "manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(),
            "signature_base64": base64.b64encode(signature_bytes).decode("ascii"),
            "signed_at": "2026-08-19T10:30:00+08:00",
            "signer": "Test Release Authority",
        }), encoding="utf-8")
        return signature, trust, audit

    def test_valid_copy_renders_both_variants_and_passes_gates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            art = root / "art.png"
            out_dir = root / "out"
            self.make_art(art)
            result = run_renderer(COPY, art, out_dir)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads((out_dir / "render-report.json").read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(set(report["outputs"]), {"poster-4x5", "header-16x9"})
            with Image.open(out_dir / report["outputs"]["poster-4x5"]["path"]) as poster:
                self.assertEqual(poster.size, (1200, 1500))
            with Image.open(out_dir / report["outputs"]["header-16x9"]["path"]) as header:
                self.assertEqual(header.size, (1920, 1080))
            self.assertTrue(all(check["status"] == "PASS" for check in report["checks"]))
            rendered = {
                item["field"]: item["value"]
                for item in report["outputs"]["poster-4x5"]["text_items"]
                if item["source_copy"]
            }
            self.assertEqual(rendered["brand.name"], "林间茶事")
            self.assertEqual(rendered["campaign.cta"], "预约周末茶席")

    def test_missing_copy_field_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            art = root / "art.png"
            invalid = root / "invalid.json"
            self.make_art(art)
            payload = json.loads(COPY.read_text(encoding="utf-8"))
            del payload["campaign"]["cta"]
            invalid.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            result = run_renderer(invalid, art, root / "out")
            self.assertEqual(result.returncode, 2)
            self.assertIn("missing", result.stderr)

    def test_remaining_delivery_templates_render_primary_masters(self) -> None:
        cases = (
            ("family-memory-copy.json", "book-cover-3x4", (1200, 1600), "publication.title_lines[0]"),
            ("community-impact-copy.json", "impact-report-a4", (1240, 1754), "report.metrics[2].label"),
            ("lighthouse-journal-copy.json", "field-journal-4x5", (1200, 1500), "journal.coordinates"),
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            art = root / "art.png"
            self.make_art(art)
            for copy_name, variant, dimensions, required_field in cases:
                with self.subTest(template=copy_name):
                    out_dir = root / variant
                    result = run_renderer(EXAMPLES / copy_name, art, out_dir)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    report = json.loads((out_dir / "render-report.json").read_text(encoding="utf-8"))
                    self.assertEqual(report["status"], "PASS")
                    self.assertEqual(set(report["outputs"]), {variant})
                    output = report["outputs"][variant]
                    self.assertEqual((output["width"], output["height"]), dimensions)
                    rendered_fields = {item["field"] for item in output["text_items"] if item["source_copy"]}
                    self.assertIn(required_field, rendered_fields)
                    self.assertTrue(all(check["status"] == "PASS" for check in report["checks"]))

    def test_impact_report_requires_exactly_three_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            art = root / "art.png"
            invalid = root / "invalid-impact.json"
            self.make_art(art)
            payload = json.loads((EXAMPLES / "community-impact-copy.json").read_text(encoding="utf-8"))
            payload["report"]["metrics"] = payload["report"]["metrics"][:2]
            invalid.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            result = run_renderer(invalid, art, root / "out")
            self.assertEqual(result.returncode, 2)
            self.assertIn("exactly three", result.stderr)

    def test_second_campaign_art_uses_same_template_with_honey_copy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            art = root / "art.png"
            out_dir = root / "honey"
            self.make_art(art)
            result = run_renderer(EXAMPLES / "honey-campaign-copy.json", art, out_dir)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads((out_dir / "render-report.json").read_text(encoding="utf-8"))
            self.assertEqual(report["template"]["id"], "campaign-poster")
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(set(report["outputs"]), {"poster-4x5", "header-16x9"})
            poster_items = report["outputs"]["poster-4x5"]["text_items"]
            rendered = {item["field"]: item["value"] for item in poster_items if item["source_copy"]}
            self.assertEqual(rendered["brand.name"], "山野蜜坊")
            self.assertEqual(rendered["campaign.headline_lines[1]"], "秋蜜")

    def test_approved_campaign_removes_sample_disclosure_and_keeps_channel(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            art = root / "art.png"
            out_dir = root / "approved"
            manifest = root / "release.json"
            self.make_art(art)
            approved_copy = EXAMPLES / "honey-campaign-approved-demo.json"
            missing = run_renderer(approved_copy, art, out_dir)
            self.assertEqual(missing.returncode, 2)
            self.assertIn("requires --release-manifest", missing.stderr)
            self.make_approved_manifest(approved_copy, art, manifest)
            missing_signature = run_renderer(approved_copy, art, out_dir, manifest)
            self.assertEqual(missing_signature.returncode, 2)
            self.assertIn("requires --release-signature", missing_signature.stderr)
            signature, trust, audit = self.make_release_security(manifest, root)
            result = run_renderer(approved_copy, art, out_dir, manifest, signature, trust, audit)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads((out_dir / "render-report.json").read_text(encoding="utf-8"))
            self.assertEqual(report["copy_status"], "approved")
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["release"]["status"], "PASS")
            self.assertEqual(report["release"]["release_id"], "approved-layout-test")
            self.assertEqual(report["signature"]["status"], "PASS")
            self.assertEqual(report["audit"]["status"], "PASS")
            self.assertTrue((out_dir / "release-manifest.json").is_file())
            self.assertTrue((out_dir / "release-signature.json").is_file())
            self.assertTrue((out_dir / "release-audit.jsonl").is_file())
            for output in report["outputs"].values():
                fields = {item["field"]: item["value"] for item in output["text_items"]}
                self.assertNotIn("generated.sample_disclosure", fields)
                self.assertEqual(fields["campaign.location"], "官方商城 · 秋季限定")
            disclosure_checks = [check for check in report["checks"] if check["id"] == "sample-disclosure"]
            self.assertTrue(disclosure_checks)
            self.assertTrue(all(check["status"] == "PASS" for check in disclosure_checks))

    def test_approved_campaign_rejects_pending_and_hash_mismatched_manifests(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            art = root / "art.png"
            manifest = root / "release.json"
            approved_copy = EXAMPLES / "honey-campaign-approved-demo.json"
            self.make_art(art)
            payload = self.make_approved_manifest(approved_copy, art, manifest)
            signature, trust, audit = self.make_release_security(manifest, root)
            payload["approvals"]["legal"] = {"status": "pending", "reviewer": "", "approved_at": "", "evidence": ""}
            manifest.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            pending = run_renderer(approved_copy, art, root / "pending", manifest, signature, trust, audit)
            self.assertEqual(pending.returncode, 2)
            self.assertIn("approval legal is not approved", pending.stderr)
            payload = self.make_approved_manifest(approved_copy, art, manifest)
            signature, trust, audit = self.make_release_security(manifest, root)
            payload["copy_sha256"] = "0" * 64
            manifest.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            mismatch = run_renderer(approved_copy, art, root / "mismatch", manifest, signature, trust, audit)
            self.assertEqual(mismatch.returncode, 2)
            self.assertIn("copy_sha256 does not match", mismatch.stderr)

    def test_overflowing_copy_creates_fail_report_and_nonzero_exit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            art = root / "art.png"
            overflowing = root / "overflowing.json"
            out_dir = root / "out"
            self.make_art(art)
            payload = json.loads(COPY.read_text(encoding="utf-8"))
            payload["campaign"]["headline_lines"] = ["非常非常非常非常非常非常非常非常长的活动标题"]
            overflowing.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            result = run_renderer(overflowing, art, out_dir)
            self.assertEqual(result.returncode, 2)
            report = json.loads((out_dir / "render-report.json").read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "FAIL")
            failed = {(check["variant"], check["id"]) for check in report["checks"] if check["status"] == "FAIL"}
            self.assertIn(("poster-4x5", "overflow"), failed)
            self.assertIn(("header-16x9", "overflow"), failed)


if __name__ == "__main__":
    unittest.main()
