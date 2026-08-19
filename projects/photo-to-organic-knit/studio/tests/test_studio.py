from __future__ import annotations

import importlib.util
import json
import threading
import unittest
import urllib.error
import urllib.request
import zipfile
from pathlib import Path


STUDIO = Path(__file__).resolve().parents[1]
SERVER_PATH = STUDIO / "server.py"
SPEC = importlib.util.spec_from_file_location("publication_studio_server", SERVER_PATH)
assert SPEC is not None and SPEC.loader is not None
SERVER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SERVER)


def post_json(url: str, payload: dict) -> tuple[int, dict]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read().decode("utf-8"))


class StudioAppTests(unittest.TestCase):
    def test_state_exposes_only_four_whitelisted_templates(self) -> None:
        app = SERVER.StudioApp()
        try:
            state = app.state()
            self.assertEqual({item["id"] for item in state["templates"]}, set(SERVER.TEMPLATES))
            self.assertTrue(state["showcase_url"].startswith("file:///"))
            self.assertEqual(state["limits"]["retained_runs"], SERVER.MAX_RETAINED_RUNS)
        finally:
            root = app.root
            app.close()
        self.assertFalse(root.exists())

    def test_each_template_renders_and_resolves_output_files(self) -> None:
        app = SERVER.StudioApp()
        try:
            for template in app.state()["templates"]:
                with self.subTest(template=template["id"]):
                    result = app.render_one(template["id"], template["copy"])
                    self.assertEqual(result["status"], "PASS")
                    self.assertTrue(result["outputs"])
                    self.assertTrue(all(check["status"] == "PASS" for check in result["checks"]))
                    output_url = result["outputs"][0]["url"]
                    _, run_id, relative = output_url.strip("/").split("/", 2)
                    self.assertIsNotNone(app.resolve_run_file(run_id, relative))
        finally:
            app.close()

    def test_batch_zip_contains_four_copies_reports_and_five_pngs(self) -> None:
        app = SERVER.StudioApp()
        try:
            copies = {item["id"]: item["copy"] for item in app.state()["templates"]}
            result = app.render_batch(copies)
            self.assertEqual(result["status"], "PASS")
            zip_relative = result["zip_url"].split("/", 3)[3]
            zip_path = app.resolve_run_file(result["batch_id"], zip_relative)
            self.assertIsNotNone(zip_path)
            with zipfile.ZipFile(zip_path) as archive:
                names = archive.namelist()
            self.assertEqual(sum(name.endswith("copy.json") for name in names), 4)
            self.assertEqual(sum(name.endswith("render-report.json") for name in names), 4)
            self.assertEqual(sum(name.endswith(".png") for name in names), 5)
        finally:
            app.close()

    def test_unknown_and_mismatched_templates_fail_closed(self) -> None:
        app = SERVER.StudioApp()
        try:
            campaign = app.state()["templates"][0]["copy"]
            with self.assertRaisesRegex(ValueError, "unknown"):
                app.render_one("not-a-template", campaign)
            with self.assertRaisesRegex(ValueError, "does not match"):
                app.render_one("book-cover", campaign)
            self.assertIsNone(app.resolve_run_file("missing", "anything.png"))
        finally:
            app.close()


class StudioHttpTests(unittest.TestCase):
    def setUp(self) -> None:
        self.server, self.app = SERVER.create_server(0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)
        root = self.app.root
        self.app.close()
        self.assertFalse(root.exists())

    def test_state_render_and_generated_png_are_http_accessible(self) -> None:
        with urllib.request.urlopen(f"{self.base}/api/state", timeout=10) as response:
            state = json.loads(response.read().decode("utf-8"))
        template = state["templates"][0]
        status, result = post_json(f"{self.base}/api/render", {"template_id": template["id"], "copy": template["copy"]})
        self.assertEqual(status, 200)
        self.assertEqual(result["status"], "PASS")
        with urllib.request.urlopen(f"{self.base}{result['outputs'][0]['url']}", timeout=10) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.headers.get_content_type(), "image/png")
            self.assertGreater(len(response.read()), 1000)

    def test_invalid_template_and_oversized_body_return_400(self) -> None:
        status, payload = post_json(f"{self.base}/api/render", {"template_id": "missing", "copy": {}})
        self.assertEqual(status, 400)
        self.assertEqual(payload["status"], "FAIL")
        request = urllib.request.Request(
            f"{self.base}/api/render",
            data=b"x" * (SERVER.MAX_BODY_BYTES + 1),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(request, timeout=10)
        self.assertEqual(caught.exception.code, 400)


if __name__ == "__main__":
    unittest.main()
