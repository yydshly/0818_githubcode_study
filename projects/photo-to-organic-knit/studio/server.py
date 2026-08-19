#!/usr/bin/env python3
"""Local-only publication studio for the photo-to-conceptual-art Skill."""

from __future__ import annotations

import argparse
import importlib.util
import json
import mimetypes
import shutil
import sys
import tempfile
import threading
import uuid
import zipfile
from collections import deque
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


STUDIO = Path(__file__).resolve().parent
PROJECT = STUDIO.parent
SKILL = PROJECT / "extension" / "photo-to-conceptual-art"
RENDERER_PATH = SKILL / "scripts" / "render_layout.py"
MAX_BODY_BYTES = 256 * 1024
MAX_RETAINED_RUNS = 24


def load_renderer() -> Any:
    spec = importlib.util.spec_from_file_location("photo_publication_renderer", RENDERER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load renderer: {RENDERER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


RENDERER = load_renderer()


TEMPLATES: dict[str, dict[str, Any]] = {
    "campaign-poster": {
        "label": "季节活动海报",
        "route": "seasonal-campaign → layered-paper → campaign-poster",
        "copy": SKILL / "examples" / "chinese-tea-copy.json",
        "art": PROJECT / "research" / "chinese-invocation" / "result-layered-paper.png",
        "sample": PROJECT / "research" / "publishing-pipeline-v1" / "outputs" / "autumn-tea-2026-sample-poster-4x5.png",
        "primary_variant": "poster-4x5",
        "dimensions": "1200 × 1500 + 1920 × 1080",
        "fields": [
            ("brand.name", "品牌名"), ("brand.qualifier", "品牌说明"),
            ("campaign.kicker", "活动眉题"),
            ("campaign.headline_lines.0", "标题第一行"), ("campaign.headline_lines.1", "标题第二行"),
            ("campaign.body_lines.0", "正文第一行"), ("campaign.body_lines.1", "正文第二行"),
            ("campaign.cta", "行动按钮"), ("campaign.date", "日期"), ("campaign.location", "地点 / 状态"),
        ],
    },
    "book-cover": {
        "label": "家庭纪念册",
        "route": "family-memory → organic-knit → book-cover",
        "copy": SKILL / "examples" / "family-memory-copy.json",
        "art": PROJECT / "research" / "additional-validation-v2" / "family-pet-knit.png",
        "sample": PROJECT / "research" / "publishing-pipeline-v2" / "book-cover" / "family-memory-volume-01-sample-book-cover-3x4.png",
        "primary_variant": "book-cover-3x4",
        "dimensions": "1200 × 1600",
        "fields": [
            ("publication.qualifier", "书册说明"),
            ("publication.title_lines.0", "标题第一行"), ("publication.title_lines.1", "标题第二行"),
            ("publication.subtitle", "副标题"), ("publication.edition", "卷次"),
            ("publication.date", "年份"), ("publication.footer", "底部说明"),
        ],
    },
    "impact-report": {
        "label": "影响力报告",
        "route": "impact-report → stained-glass → impact-report",
        "copy": SKILL / "examples" / "community-impact-copy.json",
        "art": PROJECT / "research" / "additional-validation-v2" / "community-rain-glass.png",
        "sample": PROJECT / "research" / "publishing-pipeline-v2" / "impact-report" / "community-rain-impact-2026-sample-impact-report-a4.png",
        "primary_variant": "impact-report-a4",
        "dimensions": "1240 × 1754",
        "fields": [
            ("organization.name", "机构名"), ("organization.qualifier", "机构说明"),
            ("report.kicker", "报告眉题"),
            ("report.title_lines.0", "标题第一行"), ("report.title_lines.1", "标题第二行"),
            ("report.summary", "摘要"), ("report.period", "报告周期"),
            ("report.metrics.0.value", "指标一数值"), ("report.metrics.0.label", "指标一说明"),
            ("report.metrics.1.value", "指标二数值"), ("report.metrics.1.label", "指标二说明"),
            ("report.metrics.2.value", "指标三数值"), ("report.metrics.2.label", "指标三说明"),
            ("report.footer", "报告声明"),
        ],
    },
    "field-journal": {
        "label": "旅行日志",
        "route": "travel-cover → woodcut → field-journal",
        "copy": SKILL / "examples" / "lighthouse-journal-copy.json",
        "art": PROJECT / "showcase" / "assets" / "generated" / "forward-lighthouse-auto-woodcut-v2.png",
        "sample": PROJECT / "research" / "publishing-pipeline-v2" / "field-journal" / "lighthouse-field-journal-2026-sample-field-journal-4x5.png",
        "primary_variant": "field-journal-4x5",
        "dimensions": "1200 × 1500",
        "fields": [
            ("journal.qualifier", "路线说明"), ("journal.kicker", "日志眉题"),
            ("journal.title_lines.0", "标题"), ("journal.subtitle", "副标题"),
            ("journal.coordinates", "坐标"), ("journal.distance", "距离"),
            ("journal.year", "年份"), ("journal.footer", "底部声明"),
        ],
    },
}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class StudioApp:
    def __init__(self) -> None:
        self._temporary = tempfile.TemporaryDirectory(prefix="photo-publication-studio-")
        self.root = Path(self._temporary.name).resolve()
        self._runs: dict[str, Path] = {}
        self._order: deque[str] = deque()
        self._lock = threading.Lock()

    def close(self) -> None:
        self._temporary.cleanup()

    def state(self) -> dict[str, Any]:
        templates = []
        for template_id, config in TEMPLATES.items():
            templates.append(
                {
                    "id": template_id,
                    "label": config["label"],
                    "route": config["route"],
                    "dimensions": config["dimensions"],
                    "primary_variant": config["primary_variant"],
                    "art_url": f"/api/art/{template_id}",
                    "sample_url": f"/api/sample/{template_id}",
                    "copy": read_json(config["copy"]),
                    "fields": [{"path": path, "label": label} for path, label in config["fields"]],
                }
            )
        return {
            "templates": templates,
            "showcase_url": (PROJECT / "showcase" / "index.html").resolve().as_uri(),
            "limits": {"max_body_bytes": MAX_BODY_BYTES, "retained_runs": MAX_RETAINED_RUNS},
            "boundary": "Local temporary sample workspace. No upload, brand approval, factual verification or publication authority.",
        }

    def _new_run(self, prefix: str) -> tuple[str, Path]:
        run_id = f"{prefix}-{uuid.uuid4().hex[:12]}"
        with self._lock:
            run_dir = (self.root / run_id).resolve()
            run_dir.mkdir(parents=True, exist_ok=False)
            self._runs[run_id] = run_dir
            self._order.append(run_id)
            while len(self._order) > MAX_RETAINED_RUNS:
                stale_id = self._order.popleft()
                stale = self._runs.pop(stale_id, None)
                if stale is not None and stale.is_dir():
                    shutil.rmtree(stale)
        return run_id, run_dir

    def resolve_run_file(self, run_id: str, relative: str) -> Path | None:
        with self._lock:
            run_dir = self._runs.get(run_id)
        if run_dir is None:
            return None
        candidate = (run_dir / unquote(relative)).resolve()
        try:
            candidate.relative_to(run_dir)
        except ValueError:
            return None
        return candidate if candidate.is_file() else None

    def render_one(self, template_id: str, copy_payload: dict[str, Any]) -> dict[str, Any]:
        config = TEMPLATES.get(template_id)
        if config is None:
            raise ValueError("unknown template_id")
        if copy_payload.get("template") != template_id:
            raise ValueError("copy.template does not match template_id")
        run_id, run_dir = self._new_run(template_id)
        copy_path = run_dir / "copy.json"
        write_json(copy_path, copy_payload)
        report = RENDERER.render(copy_path, config["art"], run_dir, None, None)
        return self._public_result(run_id, run_dir, template_id, report)

    def render_batch(self, copies: dict[str, Any]) -> dict[str, Any]:
        if set(copies) != set(TEMPLATES):
            raise ValueError("batch copies must contain exactly the four supported templates")
        batch_id, batch_dir = self._new_run("batch")
        results = []
        for template_id, config in TEMPLATES.items():
            copy_payload = copies[template_id]
            if not isinstance(copy_payload, dict) or copy_payload.get("template") != template_id:
                raise ValueError(f"invalid batch copy for {template_id}")
            output_dir = batch_dir / template_id
            output_dir.mkdir()
            copy_path = output_dir / "copy.json"
            write_json(copy_path, copy_payload)
            report = RENDERER.render(copy_path, config["art"], output_dir, None, None)
            if report["status"] != "PASS":
                raise ValueError(f"batch render failed for {template_id}")
            results.append(self._public_result(batch_id, batch_dir, template_id, report, prefix=f"{template_id}/"))
        zip_path = batch_dir / "photo-publication-batch.zip"
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(batch_dir.rglob("*")):
                if path.is_file() and path != zip_path:
                    archive.write(path, path.relative_to(batch_dir).as_posix())
        return {
            "status": "PASS",
            "batch_id": batch_id,
            "templates": results,
            "zip_url": f"/runs/{batch_id}/{zip_path.name}",
        }

    def _public_result(
        self,
        run_id: str,
        run_dir: Path,
        template_id: str,
        report: dict[str, Any],
        *,
        prefix: str = "",
    ) -> dict[str, Any]:
        outputs = []
        for variant, output in report["outputs"].items():
            relative = f"{prefix}{output['path']}"
            outputs.append(
                {
                    "variant": variant,
                    "url": f"/runs/{run_id}/{relative}",
                    "width": output["width"],
                    "height": output["height"],
                    "sha256": output["sha256"],
                }
            )
        report_relative = f"{prefix}render-report.json"
        copy_relative = f"{prefix}copy.json"
        return {
            "status": report["status"],
            "run_id": run_id,
            "template_id": template_id,
            "outputs": outputs,
            "report_url": f"/runs/{run_id}/{report_relative}",
            "copy_url": f"/runs/{run_id}/{copy_relative}",
            "checks": report["checks"],
            "boundary": report["boundary"],
        }


class StudioHandler(BaseHTTPRequestHandler):
    server_version = "PhotoPublicationStudio/1.0"
    app: StudioApp

    def log_message(self, format: str, *args: Any) -> None:
        return

    def end_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/state":
            self._send_json(HTTPStatus.OK, self.app.state())
            return
        if path.startswith("/api/art/") or path.startswith("/api/sample/"):
            kind, template_id = path.strip("/").split("/")[1:]
            config = TEMPLATES.get(template_id)
            key = "art" if kind == "art" else "sample"
            if config is None:
                self._send_json(HTTPStatus.NOT_FOUND, {"error": "unknown template"})
                return
            self._send_file(config[key])
            return
        if path.startswith("/runs/"):
            parts = path.strip("/").split("/", 2)
            if len(parts) != 3:
                self._send_json(HTTPStatus.NOT_FOUND, {"error": "run file not found"})
                return
            file_path = self.app.resolve_run_file(parts[1], parts[2])
            if file_path is None:
                self._send_json(HTTPStatus.NOT_FOUND, {"error": "run file not found"})
                return
            self._send_file(file_path)
            return
        static_name = "index.html" if path in {"", "/"} else path.lstrip("/")
        if static_name not in {"index.html", "styles.css", "app.js"}:
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return
        self._send_file(STUDIO / static_name)

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        try:
            payload = self._read_json_body()
            if path == "/api/render":
                if set(payload) != {"template_id", "copy"} or not isinstance(payload["copy"], dict):
                    raise ValueError("render payload must contain template_id and copy")
                result = self.app.render_one(str(payload["template_id"]), payload["copy"])
                status = HTTPStatus.OK if result["status"] == "PASS" else HTTPStatus.UNPROCESSABLE_ENTITY
                self._send_json(status, result)
                return
            if path == "/api/render-batch":
                if set(payload) != {"copies"} or not isinstance(payload["copies"], dict):
                    raise ValueError("batch payload must contain copies")
                self._send_json(HTTPStatus.OK, self.app.render_batch(payload["copies"]))
                return
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
        except ValueError as exc:
            self._send_json(HTTPStatus.BAD_REQUEST, {"status": "FAIL", "error": str(exc)})
        except Exception as exc:  # keep local UI recoverable without exposing a traceback
            self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"status": "FAIL", "error": f"internal render error: {exc}"})

    def _read_json_body(self) -> dict[str, Any]:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ValueError("invalid Content-Length") from exc
        if length <= 0:
            raise ValueError(f"request body must be between 1 and {MAX_BODY_BYTES} bytes")
        if length > MAX_BODY_BYTES:
            # Drain one bounded oversized payload so Windows clients can receive
            # the deterministic error response instead of an early connection reset.
            self.rfile.read(min(length, MAX_BODY_BYTES + 1))
            self.close_connection = True
            raise ValueError(f"request body must be between 1 and {MAX_BODY_BYTES} bytes")
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("request body must be UTF-8 JSON") from exc
        if not isinstance(payload, dict):
            raise ValueError("request JSON root must be an object")
        return payload

    def _send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path) -> None:
        if not path.is_file():
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "file not found"})
            return
        body = path.read_bytes()
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def create_server(port: int = 8877) -> tuple[ThreadingHTTPServer, StudioApp]:
    app = StudioApp()
    handler = type("BoundStudioHandler", (StudioHandler,), {"app": app})
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    return server, app


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8877, help="localhost port (default: 8877)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not 1024 <= args.port <= 65535:
        raise SystemExit("port must be between 1024 and 65535")
    server, app = create_server(args.port)
    print(f"Publication Studio: http://127.0.0.1:{args.port}/", flush=True)
    print(f"Temporary runs: {app.root}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        app.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
