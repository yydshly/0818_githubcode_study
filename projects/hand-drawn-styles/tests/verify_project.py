#!/usr/bin/env python3
"""Verify the research showcase and exercise the pinned upstream renderer."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parents[1]
SHOWCASE = PROJECT / "showcase"
UPSTREAM = PROJECT / "upstream"
RENDERER = UPSTREAM / "scripts" / "render_prompt.py"
PINNED_COMMIT = "9f150d9f4c90f3a4ace78a751d2d8263d818220c"


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


def run_renderer(*args: str) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONUTF8"] = "1"
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(RENDERER), *args],
        cwd=UPSTREAM,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=environment,
    )


def main() -> int:
    failures: list[str] = []
    required = [
        PROJECT / "README.md",
        PROJECT / "STATUS.md",
        PROJECT / "docs" / "analysis.md",
        PROJECT / "docs" / "usage-guide.md",
        SHOWCASE / "index.html",
        SHOWCASE / "styles.css",
        SHOWCASE / "app.js",
        SHOWCASE / "DELIVERY.md",
        SHOWCASE / "assets" / "generated" / "project-cover.png",
        SHOWCASE / "assets" / "generated" / "method-explainer.png",
        SHOWCASE / "assets" / "generated" / "milestone-story.png",
        SHOWCASE / "assets" / "generated" / "README.md",
        SHOWCASE / "assets" / "generated" / "PROMPTS.md",
        SHOWCASE / "assets" / "generated" / "STORY.md",
        SHOWCASE / "assets" / "generated" / "MULTI-STYLE.md",
        SHOWCASE / "assets" / "generated" / "MULTI-STYLE-FLOWS.md",
        SHOWCASE / "assets" / "generated" / "story-01-problem.png",
        SHOWCASE / "assets" / "generated" / "story-03-route.png",
        SHOWCASE / "assets" / "generated" / "story-04-assemble.png",
        SHOWCASE / "assets" / "generated" / "story-05-review.png",
        SHOWCASE / "assets" / "generated" / "story-06-publish.png",
        SHOWCASE / "assets" / "generated" / "style-08-ink-archive.png",
        SHOWCASE / "assets" / "generated" / "style-09-pixel-workflow.png",
        SHOWCASE / "assets" / "generated" / "style-13-paper-system.png",
        SHOWCASE / "assets" / "generated" / "style-15-vinyl-researcher.png",
        SHOWCASE / "assets" / "generated" / "style-08-flow-01-chaos.png",
        SHOWCASE / "assets" / "generated" / "style-08-flow-03-order.png",
        SHOWCASE / "assets" / "generated" / "style-09-flow-01-start.png",
        SHOWCASE / "assets" / "generated" / "style-09-flow-03-complete.png",
        SHOWCASE / "assets" / "generated" / "style-13-flow-01-materials.png",
        SHOWCASE / "assets" / "generated" / "style-13-flow-03-exhibit.png",
        SHOWCASE / "assets" / "generated" / "style-15-flow-01-no-identity.png",
        SHOWCASE / "assets" / "generated" / "style-15-flow-03-guide.png",
        UPSTREAM / "STYLES.md",
        RENDERER,
    ]
    for path in required:
        if not path.is_file():
            failures.append(f"missing required file: {path}")

    readme = (PROJECT / "README.md").read_text(encoding="utf-8")
    analysis = (PROJECT / "docs" / "analysis.md").read_text(encoding="utf-8")
    status = (PROJECT / "STATUS.md").read_text(encoding="utf-8")
    html = (SHOWCASE / "index.html").read_text(encoding="utf-8")
    script = (SHOWCASE / "app.js").read_text(encoding="utf-8")
    workflow = (REPO / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
    root_index = (REPO / "site" / "index.html").read_text(encoding="utf-8")

    for document, name in ((readme, "README"), (analysis, "analysis")):
        if PINNED_COMMIT not in document:
            failures.append(f"{name} does not record pinned commit")

    for phrase in ("893c202", "1bd2d18", "32/32", "20张 ChatGPT ImageGen", "等待新PR"):
        if phrase not in status:
            failures.append(f"STATUS missing current-state evidence: {phrase}")

    for phrase in ("不是新的生图模型", "从混乱样图", "SCENE 01", "SCENE 06", "三种图片职责", "同一主题", "STYLE 08", "STYLE 15", "以后怎么用", "七类交付场景", "每个研究项目默认交付7张", "五步操作流程", "copy-usage-template", "五层实现", "日常场景调用工作台", "FAIL-CLOSED"):
        if phrase not in html:
            failures.append(f"showcase missing content: {phrase}")

    for scenario in ("method", "summary", "cover", "milestone", "family"):
        if f"{scenario}:" not in script:
            failures.append(f"daily router missing scenario: {scenario}")

    if html.count('class="style-card') < 10:
        failures.append("showcase must contain at least 10 upstream style cards")
    if html.count('class="story-scene') != 6:
        failures.append("showcase must contain exactly 6 connected story scenes")
    if html.count('class="multi-style-card') != 4:
        failures.append("showcase must contain exactly 4 multi-style application examples")
    if html.count('class="mini-flow') != 4:
        failures.append("showcase must contain exactly 4 multi-style flows")
    if html.count('class="style-preview') != 12:
        failures.append("multi-style flows must contain exactly 12 scene figures")

    parser = ResourceParser()
    parser.feed(html)
    for resource in parser.resources:
        if resource.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = (SHOWCASE / resource.split("#", 1)[0]).resolve()
        if not target.exists():
            failures.append(f"missing local showcase resource: {resource}")

    if "projects/hand-drawn-styles/**" not in workflow:
        failures.append("Pages workflow does not watch hand-drawn-styles")
    if "projects/hand-drawn-styles/showcase" not in workflow:
        failures.append("Pages workflow does not publish the showcase")
    if "Hand-drawn Styles" not in root_index:
        failures.append("root Pages index does not list Hand-drawn Styles")
    if "assets/generated/project-cover.png" not in root_index:
        failures.append("root Pages index does not use the generated project cover")

    regular = run_renderer(
        "--style", "4",
        "--var", "N=4",
        "--var", "分镜列表=1. 固定版本；2. 验证能力；3. 阅读源码；4. 形成结论",
        "--aspect", "3:4",
    )
    if regular.returncode != 0:
        failures.append(f"style 4 renderer failed: {(regular.stderr or '').strip()}")
    elif "【" in regular.stdout or "画幅比例:3:4" not in regular.stdout:
        failures.append("style 4 renderer left placeholders or lost aspect")

    formal = run_renderer(
        "--style", "3.1",
        "--subject", "两位团队成员站在白板前复盘失败实验",
        "--title", "失败样例也要留下",
        "--aspect", "3:4",
        "--format", "json",
    )
    if formal.returncode != 0:
        failures.append(f"style 3.1 renderer failed: {formal.stderr.strip()}")
    else:
        payload = json.loads(formal.stdout)
        stages = payload.get("workflow", {}).get("stages", [])
        if payload.get("style_contract") != "family-crayon-card-v3":
            failures.append("style 3.1 contract id changed")
        if [stage.get("id") for stage in stages] != [
            "base-generation",
            "scribble-correction",
            "scribble-chaos-correction",
        ]:
            failures.append("style 3.1 workflow stages changed")
        if stages and stages[-1].get("output_status") != "final":
            failures.append("style 3.1 final stage is not final")

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS")
    print("- research artifacts and pinned commit present")
    print("- current status snapshot distinguishes merged baseline from 5 pending enhancements")
    print("- 10 upstream style cards resolve locally")
    print("- 3 ChatGPT-generated content assets resolve locally")
    print("- 6-scene connected case and story archive resolve locally")
    print("- 4 multi-style application examples and prompt archive resolve locally")
    print("- 4 three-scene style flows and 8 additional flow images resolve locally")
    print("- 5 daily routing scenarios present")
    print("- long-term usage guide, 7 delivery scenarios, asset pack, SOP, and copy template present")
    print("- ordinary style 4 prompt rendering succeeds")
    print("- family-crayon-card-v3 three-stage contract succeeds")
    print("- root index and Pages workflow include the project")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
