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

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for name in ("href", "src"):
            value = values.get(name)
            if value:
                self.resources.append(value)


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
    for phrase in ("真实实现", "界面模拟", "研究扩展", "先操作原版，再谈能力", "五层协作", "看起来像产品", "从漂亮 Demo 到可信产品"):
        if phrase not in html:
            failures.append(f"showcase missing capability boundary: {phrase}")
    for phrase in ("校园／公益心愿墙", "企业目标墙", "活动留言墙", "品牌故事展厅", "研究灵感墙", "游戏线索板", "私人反思墙", "纪念与故事墙"):
        if phrase not in html:
            failures.append(f"showcase missing use case: {phrase}")
    for phrase in ("真实多人社区", "可分享空间", "关系图／调查板", "时间与进度", "多媒体卡片", "AI 辅助组织", "自动导览", "千级卡片引擎"):
        if phrase not in html or phrase not in extensions:
            failures.append(f"extension route missing from showcase or document: {phrase}")
    for key in ("data", "texture", "scene", "interaction", "product"):
        if f"{key}:" not in script:
            failures.append(f"capability workbench missing key: {key}")
    if 'src="../upstream/index.html"' not in html or 'href="../upstream/index.html"' not in html:
        failures.append("showcase does not expose the unchanged upstream runtime")

    parser = ResourceParser()
    parser.feed(html)
    for resource in parser.resources:
        if resource.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = (SHOWCASE / resource.split("#", 1)[0]).resolve()
        if not target.exists():
            failures.append(f"missing local showcase resource: {resource}")

    if "Promise Wall" not in root_readme or "Promise Wall" not in site_index:
        failures.append("root research indexes do not include Promise Wall")
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
    print("- live demo, five capability layers, eight use cases, and eight extension routes are present")
    print("- local resources, JavaScript syntax, root indexes, and Pages wiring pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
