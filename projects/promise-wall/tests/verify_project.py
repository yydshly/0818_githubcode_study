#!/usr/bin/env python3
"""Verify the pinned upstream, research claims, showcase resources, and Pages wiring."""

from __future__ import annotations

import subprocess
from html.parser import HTMLParser
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parents[1]
UPSTREAM = PROJECT / "upstream"
SHOWCASE = PROJECT / "showcase"
PINNED_COMMIT = "0cb1b20c3952e4c4184b7e0e33fe5acfac2b4447"


class ResourceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.resources: list[str] = []
        self.scene_routes: list[str] = []
        self.scene_tabs: list[str] = []
        self.future_actions: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for name in ("href", "src"):
            value = values.get(name)
            if value:
                self.resources.append(value)
        if values.get("data-route-scene"):
            self.scene_routes.append(values["data-route-scene"] or "")
        if values.get("data-scene-select"):
            self.scene_tabs.append(values["data-scene-select"] or "")
        if values.get("data-future-action"):
            self.future_actions.append(values["data-future-action"] or "")


def git(*args: str) -> subprocess.CompletedProcess[str]:
    safe_path = UPSTREAM.resolve().as_posix()
    return subprocess.run(
        ["git", "-c", f"safe.directory={safe_path}", "-C", str(UPSTREAM), *args],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def main() -> int:
    failures: list[str] = []
    required = [
        PROJECT / "README.md",
        PROJECT / "docs" / "analysis.md",
        PROJECT / "docs" / "extension-scenarios.md",
        SHOWCASE / "index.html",
        SHOWCASE / "styles.css",
        SHOWCASE / "app.js",
        SHOWCASE / "DELIVERY.md",
        SHOWCASE / "assets" / "generated" / "promise-wall-six-scenes.png",
        SHOWCASE / "assets" / "generated" / "PROMPT.md",
        UPSTREAM / "index.html",
        UPSTREAM / "package.json",
    ]
    for path in required:
        if not path.is_file():
            failures.append(f"missing required file: {path}")
    if failures:
        return report(failures)

    commit = git("rev-parse", "HEAD").stdout.strip()
    if commit != PINNED_COMMIT:
        failures.append(f"upstream commit is not pinned to {PINNED_COMMIT}: {commit or 'unreadable'}")
    status = git("status", "--short").stdout.strip()
    if status:
        failures.append(f"upstream submodule is modified: {status}")

    upstream_index = (UPSTREAM / "index.html").read_text(encoding="utf-8")
    source_contracts = {
        "Three.js renderer": "new THREE.WebGLRenderer",
        "Canvas textures": "new THREE.CanvasTexture",
        "raycasting": "new THREE.Raycaster",
        "placement": "function finalizePlacement",
        "search": "function applyFilter",
        "serialization hook": "function wallStateJSON",
        "reduced motion": 'prefers-reduced-motion: reduce',
    }
    for label, marker in source_contracts.items():
        if marker not in upstream_index:
            failures.append(f"upstream capability marker missing: {label}")
    for forbidden in ("localStorage", "fetch("):
        if forbidden in upstream_index:
            failures.append(f"persistence boundary changed; unexpected marker found: {forbidden}")
    if any((UPSTREAM / name).exists() for name in ("LICENSE", "LICENSE.md", "LICENSE.txt")):
        failures.append("license boundary changed; update the research statement")

    readme = (PROJECT / "README.md").read_text(encoding="utf-8")
    analysis = (PROJECT / "docs" / "analysis.md").read_text(encoding="utf-8")
    extensions = (PROJECT / "docs" / "extension-scenarios.md").read_text(encoding="utf-8")
    html = (SHOWCASE / "index.html").read_text(encoding="utf-8")
    script = (SHOWCASE / "app.js").read_text(encoding="utf-8")
    delivery = (SHOWCASE / "DELIVERY.md").read_text(encoding="utf-8")
    root_readme = (REPO / "README.md").read_text(encoding="utf-8")
    site_index = (REPO / "site" / "index.html").read_text(encoding="utf-8")
    workflow = (REPO / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")

    for document, name in ((readme, "README"), (analysis, "analysis"), (delivery, "delivery")):
        if PINNED_COMMIT not in document and name != "delivery":
            failures.append(f"{name} does not record the pinned commit")
    for phrase in ("真实实现", "界面模拟", "研究扩展", "先操作原版，再谈能力", "五层协作", "看起来像产品", "同一面墙", "效果不是装饰"):
        if phrase not in html:
            failures.append(f"showcase missing capability boundary: {phrase}")
    for phrase in ("新年愿望墙", "毕业留言墙", "婚礼祝福墙", "企业目标墙", "员工感谢墙", "公益承诺墙", "匿名心声墙", "家庭记忆墙", "旅行记忆墙", "品牌故事展厅", "城市故事墙", "游戏线索板"):
        if phrase not in html:
            failures.append(f"showcase missing use case: {phrase}")
    for phrase in ("新年愿望墙", "毕业留言墙", "婚礼祝福墙", "企业目标墙", "员工感谢墙", "公益承诺墙", "匿名心声墙", "家庭记忆墙", "旅行记忆墙", "品牌故事墙", "城市故事墙", "游戏线索墙"):
        if (phrase not in html and phrase not in script) or phrase not in extensions:
            failures.append(f"experience scene missing from showcase or document: {phrase}")
    for key in ("data", "texture", "scene", "interaction", "product"):
        if f"{key}:" not in script:
            failures.append(f"capability workbench missing key: {key}")
    if 'src="../upstream/index.html"' not in html or 'href="../upstream/index.html"' not in html:
        failures.append("showcase does not expose the unchanged upstream runtime")
    for marker in ("sceneOrder", "startScenePlayback", "stopScenePlayback", "dataset.scene", "reducedMotion"):
        if marker not in script:
            failures.append(f"scene director missing marker: {marker}")
    for phrase in ("独立互动闭环", "让墙经历时间", "集体反馈改变整面墙", "生成可带走的成果", "活动现场模式", "个人长期空间", "让十二场景形成生命周期", "当前决定：完成研究，停止继续扩展", "何时重新启动"):
        if phrase not in html:
            failures.append(f"showcase missing future/archive content: {phrase}")

    parser = ResourceParser()
    parser.feed(html)
    for resource in parser.resources:
        if resource.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = (SHOWCASE / resource.split("#", 1)[0]).resolve()
        if not target.exists():
            failures.append(f"missing local showcase resource: {resource}")
    expected_scenes = ["newyear", "graduation", "wedding", "goals", "recognition", "publicgood", "anonymous", "family", "travel", "brand", "city", "game"]
    if len(parser.scene_routes) != 12:
        failures.append(f"expected 12 routed use cases, found {len(parser.scene_routes)}")
    if parser.scene_routes != expected_scenes:
        failures.append(f"use-case routes do not match canonical order: {parser.scene_routes}")
    if parser.scene_tabs != expected_scenes:
        failures.append(f"scene tabs do not match canonical order: {parser.scene_tabs}")
    if not set(parser.scene_routes).issubset(set(expected_scenes)):
        failures.append("use-case router targets an unknown scene")
    expected_actions = ["interaction-loop", "time-change", "collective-feedback", "takeaway-result", "live-event", "personal-space", "lifecycle"]
    if parser.future_actions != expected_actions:
        failures.append(f"future actions do not match canonical order: {parser.future_actions}")
    atmosphere = SHOWCASE / "assets" / "generated" / "promise-wall-six-scenes.png"
    if atmosphere.stat().st_size < 500_000:
        failures.append("ImageGen atmosphere atlas is unexpectedly small")

    if "Promise Wall" not in root_readme or "Promise Wall" not in site_index:
        failures.append("root research indexes do not include Promise Wall")
    for document, name in ((readme, "README"), (root_readme, "root README"), (site_index, "site index")):
        if "已归档" not in document:
            failures.append(f"{name} does not mark Promise Wall archived")
    if "projects/promise-wall/**" not in workflow:
        failures.append("Pages path trigger does not include Promise Wall")
    for phrase in ("projects/promise-wall/showcase", "projects/promise-wall/upstream/index.html", "projects/promise-wall/docs"):
        if phrase not in workflow:
            failures.append(f"Pages assembly missing: {phrase}")

    node_check = subprocess.run(
        ["node", "--check", str(SHOWCASE / "app.js")],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if node_check.returncode != 0:
        failures.append(f"showcase JavaScript syntax failed: {node_check.stderr.strip()}")

    return report(failures)


def report(failures: list[str]) -> int:
    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS")
    print("- upstream commit is pinned and unmodified")
    print("- runtime source markers and persistence boundary match the analysis")
    print("- live demo, five capability layers, twelve routed use cases, and twelve ordered scene prototypes are present")
    print("- ImageGen atmosphere atlas, prompt provenance, playback controls, and reduced-motion route pass")
    print("- seven future actions, reopen triggers, and archived status are consistent")
    print("- local resources, JavaScript syntax, root indexes, and Pages wiring pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
