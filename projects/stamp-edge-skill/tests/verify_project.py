#!/usr/bin/env python3
"""Verify research artifacts, rich image contracts, upstream pin, and Pages wiring."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

from PIL import Image, ImageDraw


PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parents[1]
SHOWCASE = PROJECT / "showcase"
ASSETS = SHOWCASE / "assets" / "demo"
SOURCES = ASSETS / "sources"
INPUTS = ASSETS / "inputs-v2"
OUTPUTS = ASSETS / "outputs-v2"
UPSTREAM = PROJECT / "upstream"
EXTENSION_SKILL = PROJECT / "extension" / "image-style-skill"
EXTENSION_OUTPUTS = SHOWCASE / "assets" / "extensions"
PINNED_COMMIT = "2b89ce823aa589e912fcfbb9b529fa893142ab63"

SCENES = (
    "travel-coast",
    "architecture-rain",
    "breakfast-table",
    "botanical-glasshouse",
    "social-travel-story",
    "field-notes-poster",
)


class ResourceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.resources: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for name in ("href", "src"):
            value = values.get(name)
            if value:
                self.resources.append(value)


def upstream_commit() -> str:
    safe_path = UPSTREAM.resolve().as_posix()
    result = subprocess.run(
        ["git", "-c", f"safe.directory={safe_path}", "-C", str(UPSTREAM), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def verify_alpha_replacement(failures: list[str]) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        source = temp / "alpha-source.png"
        output = temp / "alpha-output.png"
        image = Image.new("RGBA", (320, 240), (208, 69, 74, 255))
        ImageDraw.Draw(image).ellipse((100, 60, 220, 180), fill=(0, 0, 0, 0))
        image.save(source)
        result = subprocess.run(
            [sys.executable, str(UPSTREAM / "stamp_effect.py"), str(source), str(output)],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            failures.append(f"alpha limitation fixture failed: {result.stderr.strip()}")
            return
        rendered = Image.open(output).convert("RGBA")
        if rendered.getpixel((250, 210))[3] != 255:
            failures.append("expected upstream alpha replacement behavior was not reproduced")


def main() -> int:
    failures: list[str] = []
    required = [
        PROJECT / "README.md",
        PROJECT / "requirements.txt",
        PROJECT / "demo" / "generate_demo.py",
        PROJECT / "demo" / "README.md",
        PROJECT / "demo" / "PROMPTS.md",
        PROJECT / "docs" / "analysis.md",
        PROJECT / "docs" / "extension-roadmap.md",
        SHOWCASE / "index.html",
        SHOWCASE / "styles.css",
        SHOWCASE / "app.js",
        SHOWCASE / "DELIVERY.md",
        ASSETS / "manifest.json",
        UPSTREAM / "SKILL.md",
        UPSTREAM / "stamp_effect.py",
        UPSTREAM / "stamp_sheet.py",
        EXTENSION_SKILL / "SKILL.md",
        EXTENSION_SKILL / "references" / "presets.md",
        EXTENSION_SKILL / "scripts" / "style_effects.py",
        EXTENSION_SKILL / "scripts" / "generate_demo.py",
        EXTENSION_SKILL / "tests" / "test_presets.py",
        EXTENSION_OUTPUTS / "manifest.json",
    ]
    required.extend(SOURCES / name for name in (
        "travel-coast.png",
        "architecture-rain.png",
        "breakfast-table.png",
        "botanical-glasshouse.png",
    ))
    required.extend(INPUTS / f"{scene}.{'png' if scene in {'social-travel-story', 'field-notes-poster'} else 'jpg'}" for scene in SCENES)
    required.extend(OUTPUTS / f"{scene}-stamp.png" for scene in SCENES)
    required.extend(OUTPUTS / name for name in (
        "travel-coast-margin.png",
        "travel-coast-bg.png",
        "social-travel-story-margin.png",
        "collection-dark-4col.png",
        "collection-paper-3col.png",
    ))
    required.extend(EXTENSION_OUTPUTS / name for name in (
        "polaroid-travel.png",
        "torn-botanical.png",
        "film-architecture.png",
        "ticket-coast.png",
        "riso-breakfast.png",
        "sticker-architecture.png",
        "extension-collection-dark.png",
    ))
    for path in required:
        if not path.is_file():
            failures.append(f"missing required file: {path}")
    if failures:
        return report(failures)

    if upstream_commit() != PINNED_COMMIT:
        failures.append(f"upstream commit is not pinned to {PINNED_COMMIT}")

    readme = (PROJECT / "README.md").read_text(encoding="utf-8")
    analysis = (PROJECT / "docs" / "analysis.md").read_text(encoding="utf-8")
    roadmap = (PROJECT / "docs" / "extension-roadmap.md").read_text(encoding="utf-8")
    prompts = (PROJECT / "demo" / "PROMPTS.md").read_text(encoding="utf-8")
    html = (SHOWCASE / "index.html").read_text(encoding="utf-8")
    script = (SHOWCASE / "app.js").read_text(encoding="utf-8")
    workflow = (REPO / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
    root_readme = (REPO / "README.md").read_text(encoding="utf-8")
    site_index = (REPO / "site" / "index.html").read_text(encoding="utf-8")
    manifest = json.loads((ASSETS / "manifest.json").read_text(encoding="utf-8"))
    extension_manifest = json.loads((EXTENSION_OUTPUTS / "manifest.json").read_text(encoding="utf-8"))

    for document, name in ((readme, "README"), (analysis, "analysis")):
        if PINNED_COMMIT not in document:
            failures.append(f"{name} does not record the pinned commit")
    if len(manifest.get("sources", [])) != 6:
        failures.append("demo manifest must record exactly six source scenes")
    if manifest.get("collections") != ["4 columns / dark", "3 columns / paper"]:
        failures.append("demo manifest does not record both collection modes")
    expected_presets = ["polaroid", "torn-paper", "film-frame", "ticket", "riso-print", "sticker-outline"]
    if extension_manifest.get("presets") != expected_presets:
        failures.append("extension manifest does not record all six presets in canonical order")

    for phrase in ("六种真实场景", "原始库的第二项能力", "4 列深色合集", "3 列纸色合集", "stamp_sheet.py", "社交长帖", "编辑海报"):
        if phrase not in html:
            failures.append(f"showcase missing content: {phrase}")
    for phrase in ("六个 preset 已经可运行", "--preset polaroid", "--preset torn-paper", "--preset film-frame", "--preset ticket", "--preset riso-print", "--preset sticker-outline", "MIXED PRESET SHEET"):
        if phrase not in html:
            failures.append(f"showcase missing implemented extension: {phrase}")
    for phrase in ("本次研究到这里", "刻意不继续", "当前决定", "核心画质", "批量工作流", "邮票语义", "可选 AI", "不属于当前已经实现的能力"):
        if phrase not in html:
            failures.append(f"showcase missing research closure statement: {phrase}")
    for scene in ("travel", "architecture", "food", "botanical", "social", "poster"):
        if f"{scene}:" not in script:
            failures.append(f"scene switcher missing: {scene}")
    if "data-preview-background" not in html or "selectBackground" not in script:
        failures.append("showcase does not implement preview background switching")
    for phrase in ("travel-coast.png", "architecture-rain.png", "breakfast-table.png", "botanical-glasshouse.png"):
        if phrase not in prompts:
            failures.append(f"ImageGen prompt archive missing: {phrase}")
    for phrase in ("Phase 0", "Phase 1", "Phase 2", "Phase 3", "polaroid", "torn-paper"):
        if phrase not in roadmap:
            failures.append(f"extension roadmap missing: {phrase}")

    for scene in SCENES:
        stamp = Image.open(OUTPUTS / f"{scene}-stamp.png")
        if stamp.mode != "RGBA" or stamp.getchannel("A").getextrema() != (0, 255):
            failures.append(f"scene output is not true transparent RGBA: {scene}")

    travel = Image.open(OUTPUTS / "travel-coast-stamp.png")
    margin = Image.open(OUTPUTS / "travel-coast-margin.png")
    background = Image.open(OUTPUTS / "travel-coast-bg.png")
    if margin.size != (travel.width + 92, travel.height + 92):
        failures.append("margin output does not add the expected 46px border on each side")
    if background.mode != "RGB":
        failures.append("bg output must be flattened to RGB")

    for name in ("collection-dark-4col.png", "collection-paper-3col.png"):
        sheet = Image.open(OUTPUTS / name)
        if sheet.mode != "RGB" or min(sheet.size) <= 0:
            failures.append(f"invalid collection output: {name}")

    for name in extension_manifest.get("outputs", []):
        result = Image.open(EXTENSION_OUTPUTS / name)
        if result.mode != "RGBA" or result.getchannel("A").getextrema() != (0, 255):
            failures.append(f"extension output is not transparent RGBA: {name}")
    extension_sheet = Image.open(EXTENSION_OUTPUTS / "extension-collection-dark.png")
    if extension_sheet.mode != "RGB" or min(extension_sheet.size) <= 0:
        failures.append("extension collection is not a valid RGB sheet")

    preset_test = subprocess.run(
        [sys.executable, str(EXTENSION_SKILL / "tests" / "test_presets.py")],
        check=False,
        capture_output=True,
        text=True,
    )
    if preset_test.returncode != 0:
        failures.append(f"extension preset behavior tests failed: {preset_test.stderr.strip()}")

    verify_alpha_replacement(failures)

    parser = ResourceParser()
    parser.feed(html)
    for resource in parser.resources:
        if resource.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = (SHOWCASE / resource.split("#", 1)[0]).resolve()
        if not target.exists():
            failures.append(f"missing local showcase resource: {resource}")

    if "projects/stamp-edge-skill/**" not in workflow or "projects/stamp-edge-skill/showcase" not in workflow:
        failures.append("Pages workflow does not fully publish stamp-edge-skill")
    if "Stamp Edge" not in root_readme or "Stamp Edge" not in site_index:
        failures.append("root project indexes do not include Stamp Edge")
    if "outputs-v2/collection-paper-3col.png" not in site_index:
        failures.append("root Pages index does not use the improved collection cover")

    return report(failures)


def report(failures: list[str]) -> int:
    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS")
    print("- upstream commit and six-scene manifest are pinned")
    print("- six transparent stamps and three single-image modes pass")
    print("- default 4-column dark and custom 3-column paper collections pass")
    print("- ImageGen provenance, prompt archive, showcase resources, and Pages wiring pass")
    print("- six implemented extension presets, mixed collection, and behavior tests pass")
    print("- original-alpha replacement limitation remains reproduced")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
