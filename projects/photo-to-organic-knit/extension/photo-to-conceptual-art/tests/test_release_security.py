from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "release_security.py"
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import release_security  # noqa: E402


def run_security(*args: str) -> subprocess.CompletedProcess[str]:
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


class ReleaseSecurityTests(unittest.TestCase):
    def make_manifest(self, path: Path) -> dict:
        payload = {
            "schema_version": "1.0",
            "release_id": "signed-release-test",
            "release_scope": "demo",
            "campaign_id": "signed-release-test",
            "template": "campaign-poster",
            "copy_sha256": "1" * 64,
            "art_sha256": "2" * 64,
            "approvals": {},
        }
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return payload

    def test_keygen_sign_and_verify_cli(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "manifest.json"
            private_key = root / "private.pem"
            trust = root / "trust.json"
            signature = root / "signature.json"
            self.make_manifest(manifest)
            generated = run_security(
                "keygen", "--key-id", "demo-signing-key", "--owner", "Demo Signer", "--scope", "demo",
                "--private-out", str(private_key), "--trust-out", str(trust),
            )
            self.assertEqual(generated.returncode, 0, generated.stderr)
            self.assertTrue(private_key.is_file())
            signed = run_security(
                "sign", "--manifest", str(manifest), "--private-key", str(private_key),
                "--key-id", "demo-signing-key", "--signer", "Demo Signer",
                "--signed-at", "2026-08-19T11:00:00+08:00", "--out", str(signature),
            )
            self.assertEqual(signed.returncode, 0, signed.stderr)
            verified = run_security(
                "verify", "--manifest", str(manifest), "--signature", str(signature), "--trusted-keys", str(trust),
            )
            self.assertEqual(verified.returncode, 0, verified.stderr)
            self.assertEqual(json.loads(verified.stdout)["status"], "PASS")

    def test_tampered_manifest_and_revoked_key_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "manifest.json"
            private_key = root / "private.pem"
            trust = root / "trust.json"
            signature = root / "signature.json"
            payload = self.make_manifest(manifest)
            release_security.generate_keypair("demo-signing-key", "Demo Signer", "demo", private_key, trust)
            release_security.sign_manifest(manifest, private_key, "demo-signing-key", "Demo Signer", signature, "2026-08-19T11:00:00+08:00")
            payload["campaign_id"] = "tampered"
            manifest.write_text(json.dumps(payload), encoding="utf-8")
            tampered = run_security("verify", "--manifest", str(manifest), "--signature", str(signature), "--trusted-keys", str(trust))
            self.assertEqual(tampered.returncode, 2)
            self.assertIn("manifest hash does not match", tampered.stderr)
            self.make_manifest(manifest)
            release_security.sign_manifest(manifest, private_key, "demo-signing-key", "Demo Signer", root / "signature-2.json", "2026-08-19T11:05:00+08:00")
            trust_payload = json.loads(trust.read_text(encoding="utf-8"))
            trust_payload["keys"]["demo-signing-key"]["status"] = "revoked"
            trust.write_text(json.dumps(trust_payload), encoding="utf-8")
            revoked = run_security("verify", "--manifest", str(manifest), "--signature", str(root / "signature-2.json"), "--trusted-keys", str(trust))
            self.assertEqual(revoked.returncode, 2)
            self.assertIn("not active", revoked.stderr)

    def test_audit_chain_verifies_and_detects_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            audit = Path(directory) / "audit.jsonl"
            release = {
                "release_id": "audit-release",
                "release_scope": "demo",
                "manifest_sha256": "3" * 64,
                "copy_sha256": "4" * 64,
                "art_sha256": "5" * 64,
            }
            signature = {"key_id": "audit-key"}
            outputs = {"poster": {"sha256": "6" * 64}}
            first = release_security.append_audit_event(audit, release, signature, outputs, "2026-08-19T11:10:00+08:00")
            second = release_security.append_audit_event(audit, release, signature, outputs, "2026-08-19T11:15:00+08:00")
            self.assertEqual(second["previous_event_hash"], first["event_hash"])
            self.assertEqual(len(release_security.verify_audit_log(audit)), 2)
            lines = audit.read_text(encoding="utf-8").splitlines()
            event = json.loads(lines[0])
            event["outputs"]["poster"] = "7" * 64
            lines[0] = json.dumps(event, sort_keys=True, separators=(",", ":"))
            audit.write_text("\n".join(lines) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "hash does not verify"):
                release_security.verify_audit_log(audit)


if __name__ == "__main__":
    unittest.main()
