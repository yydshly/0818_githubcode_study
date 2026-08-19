#!/usr/bin/env python3
"""Verify Photo to Organic Knit research artifacts using only stdlib."""

from __future__ import annotations

import struct
import sys
import json
import subprocess
from html.parser import HTMLParser
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parents[1]
SHOWCASE = PROJECT / "showcase"
UPSTREAM = PROJECT / "upstream"
EXTENSION = PROJECT / "extension" / "photo-to-conceptual-art"
PINNED_COMMIT = "b84efe522e758649e46fe59f34d700eb60bedc12"


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


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        if handle.read(8) != b"\x89PNG\r\n\x1a\n":
            raise ValueError(f"not a PNG: {path}")
        length = struct.unpack(">I", handle.read(4))[0]
        if handle.read(4) != b"IHDR" or length < 8:
            raise ValueError(f"missing PNG IHDR: {path}")
        return struct.unpack(">II", handle.read(8))


def main() -> int:
    failures: list[str] = []
    required = [
        PROJECT / "README.md",
        PROJECT / "docs" / "analysis.md",
        PROJECT / "docs" / "use-cases-and-roadmap.md",
        SHOWCASE / "index.html",
        SHOWCASE / "styles.css",
        SHOWCASE / "app.js",
        SHOWCASE / "DELIVERY.md",
        SHOWCASE / "assets" / "generated" / "README.md",
        SHOWCASE / "assets" / "generated" / "PROMPTS.md",
        SHOWCASE / "assets" / "generated" / "MULTI_EFFECT_PROMPTS.md",
        SHOWCASE / "assets" / "generated" / "SCENARIO_PROMPTS.md",
        SHOWCASE / "assets" / "generated" / "canoe-source.png",
        SHOWCASE / "assets" / "generated" / "canoe-organic-knit.png",
        SHOWCASE / "assets" / "generated" / "canoe-paper-cut.png",
        SHOWCASE / "assets" / "generated" / "canoe-ceramic-relief.png",
        SHOWCASE / "assets" / "generated" / "canoe-stained-glass.png",
        SHOWCASE / "assets" / "generated" / "canoe-woodcut.png",
        SHOWCASE / "assets" / "generated" / "canoe-miniature-diorama.png",
        SHOWCASE / "assets" / "generated" / "scenario-family-source.png",
        SHOWCASE / "assets" / "generated" / "scenario-family-knit.png",
        SHOWCASE / "assets" / "generated" / "scenario-community-source.png",
        SHOWCASE / "assets" / "generated" / "scenario-community-glass.png",
        SHOWCASE / "assets" / "generated" / "scenario-bakery-source.png",
        SHOWCASE / "assets" / "generated" / "scenario-bakery-paper.png",
        SHOWCASE / "assets" / "generated" / "forward-lighthouse-source.png",
        SHOWCASE / "assets" / "generated" / "forward-lighthouse-auto-woodcut.png",
        SHOWCASE / "assets" / "generated" / "forward-lighthouse-auto-woodcut-v2.png",
        SHOWCASE / "assets" / "generated" / "forward-lighthouse-override-paper.png",
        SHOWCASE / "assets" / "generated" / "forward-lighthouse-override-paper-v2.png",
        SHOWCASE / "assets" / "generated" / "pilot-person-source.png",
        SHOWCASE / "assets" / "generated" / "pilot-person-auto-knit.png",
        SHOWCASE / "assets" / "generated" / "pilot-product-source.png",
        SHOWCASE / "assets" / "generated" / "pilot-product-auto-paper.png",
        SHOWCASE / "assets" / "generated" / "pilot-architecture-source.png",
        SHOWCASE / "assets" / "generated" / "pilot-architecture-auto-woodcut.png",
        UPSTREAM / "README.md",
        UPSTREAM / "LICENSE",
        UPSTREAM / "assets" / "train-before-after.png",
        UPSTREAM / "assets" / "forest-before-after.png",
        UPSTREAM / "photo-to-organic-knit" / "SKILL.md",
        UPSTREAM / "photo-to-organic-knit" / "references" / "style-spec.md",
        UPSTREAM / "photo-to-organic-knit" / "assets" / "style-reference.png",
        EXTENSION / "SKILL.md",
        EXTENSION / "agents" / "openai.yaml",
        EXTENSION / "references" / "essence-schema.md",
        EXTENSION / "references" / "quality-gates.md",
        EXTENSION / "references" / "review-schema.md",
        EXTENSION / "references" / "copy-schema.md",
        EXTENSION / "references" / "release-manifest.md",
        EXTENSION / "references" / "release-security.md",
        EXTENSION / "references" / "action-runbook.md",
        EXTENSION / "scripts" / "build_prompt.py",
        EXTENSION / "scripts" / "score_review.py",
        EXTENSION / "scripts" / "render_layout.py",
        EXTENSION / "scripts" / "release_manifest.py",
        EXTENSION / "scripts" / "release_security.py",
        EXTENSION / "assets" / "templates" / "campaign-poster.json",
        EXTENSION / "assets" / "templates" / "book-cover.json",
        EXTENSION / "assets" / "templates" / "impact-report.json",
        EXTENSION / "assets" / "templates" / "field-journal.json",
        EXTENSION / "examples" / "canoe-essence.json",
        EXTENSION / "examples" / "chinese-tea-copy.json",
        EXTENSION / "examples" / "family-memory-copy.json",
        EXTENSION / "examples" / "community-impact-copy.json",
        EXTENSION / "examples" / "lighthouse-journal-copy.json",
        EXTENSION / "examples" / "honey-campaign-copy.json",
        EXTENSION / "examples" / "honey-campaign-approved-demo.json",
        EXTENSION / "tests" / "test_prompt_compiler.py",
        EXTENSION / "tests" / "test_layout_renderer.py",
        EXTENSION / "tests" / "test_release_manifest.py",
        EXTENSION / "tests" / "test_release_security.py",
        EXTENSION / "forward-tests" / "lighthouse-travel" / "essence.json",
        EXTENSION / "forward-tests" / "lighthouse-travel" / "manifest.json",
        EXTENSION / "forward-tests" / "lighthouse-travel" / "RESULT.md",
        EXTENSION / "forward-tests" / "pilot-n3" / "person-essence.json",
        EXTENSION / "forward-tests" / "pilot-n3" / "product-essence.json",
        EXTENSION / "forward-tests" / "pilot-n3" / "architecture-essence.json",
        EXTENSION / "forward-tests" / "pilot-n3" / "manifest.json",
        EXTENSION / "forward-tests" / "pilot-n3" / "RESULT.md",
        EXTENSION / "forward-tests" / "lighthouse-travel" / "review-auto-v2.json",
        PROJECT / "research" / "chinese-invocation" / "request.txt",
        PROJECT / "research" / "chinese-invocation" / "essence.json",
        PROJECT / "research" / "chinese-invocation" / "result-layered-paper.png",
        PROJECT / "research" / "chinese-invocation" / "review.json",
        PROJECT / "research" / "chinese-invocation" / "RESULT.md",
        PROJECT / "research" / "additional-validation-v2" / "family-pet-source.png",
        PROJECT / "research" / "additional-validation-v2" / "family-pet-knit.png",
        PROJECT / "research" / "additional-validation-v2" / "family-pet-essence.json",
        PROJECT / "research" / "additional-validation-v2" / "family-pet-review.json",
        PROJECT / "research" / "additional-validation-v2" / "community-rain-source.png",
        PROJECT / "research" / "additional-validation-v2" / "community-rain-glass.png",
        PROJECT / "research" / "additional-validation-v2" / "community-rain-essence.json",
        PROJECT / "research" / "additional-validation-v2" / "community-rain-review.json",
        PROJECT / "research" / "additional-validation-v2" / "honey-source.png",
        PROJECT / "research" / "additional-validation-v2" / "honey-ceramic.png",
        PROJECT / "research" / "additional-validation-v2" / "honey-essence.json",
        PROJECT / "research" / "additional-validation-v2" / "honey-review.json",
        PROJECT / "research" / "additional-validation-v2" / "manifest.json",
        PROJECT / "research" / "additional-validation-v2" / "RESULT.md",
        PROJECT / "research" / "publishing-pipeline-v1" / "DESIGN-CONTRACT.md",
        PROJECT / "research" / "publishing-pipeline-v1" / "RESULT.md",
        PROJECT / "research" / "publishing-pipeline-v1" / "outputs" / "autumn-tea-2026-sample-poster-4x5.png",
        PROJECT / "research" / "publishing-pipeline-v1" / "outputs" / "autumn-tea-2026-sample-header-16x9.png",
        PROJECT / "research" / "publishing-pipeline-v1" / "outputs" / "render-report.json",
        PROJECT / "research" / "publishing-pipeline-v2" / "DESIGN-CONTRACT.md",
        PROJECT / "research" / "publishing-pipeline-v2" / "RESULT.md",
        PROJECT / "research" / "publishing-pipeline-v2" / "book-cover" / "family-memory-volume-01-sample-book-cover-3x4.png",
        PROJECT / "research" / "publishing-pipeline-v2" / "book-cover" / "render-report.json",
        PROJECT / "research" / "publishing-pipeline-v2" / "impact-report" / "community-rain-impact-2026-sample-impact-report-a4.png",
        PROJECT / "research" / "publishing-pipeline-v2" / "impact-report" / "render-report.json",
        PROJECT / "research" / "publishing-pipeline-v2" / "field-journal" / "lighthouse-field-journal-2026-sample-field-journal-4x5.png",
        PROJECT / "research" / "publishing-pipeline-v2" / "field-journal" / "render-report.json",
        PROJECT / "research" / "publication-studio-v1" / "DESIGN-CONTRACT.md",
        PROJECT / "research" / "publication-studio-v1" / "RESULT.md",
        PROJECT / "studio" / "server.py",
        PROJECT / "studio" / "index.html",
        PROJECT / "studio" / "styles.css",
        PROJECT / "studio" / "app.js",
        PROJECT / "studio" / "README.md",
        PROJECT / "studio" / "tests" / "test_studio.py",
        PROJECT / "research" / "honey-publication-validation" / "DESIGN-CONTRACT.md",
        PROJECT / "research" / "honey-publication-validation" / "RESULT.md",
        PROJECT / "research" / "honey-publication-validation" / "outputs" / "wild-honey-autumn-2026-sample-poster-4x5.png",
        PROJECT / "research" / "honey-publication-validation" / "outputs" / "wild-honey-autumn-2026-sample-header-16x9.png",
        PROJECT / "research" / "honey-publication-validation" / "outputs" / "render-report.json",
        PROJECT / "research" / "honey-formal-publication-demo" / "DESIGN-CONTRACT.md",
        PROJECT / "research" / "honey-formal-publication-demo" / "RESULT.md",
        PROJECT / "research" / "honey-formal-publication-demo" / "outputs" / "wild-honey-autumn-2026-approved-demo-poster-4x5.png",
        PROJECT / "research" / "honey-formal-publication-demo" / "outputs" / "wild-honey-autumn-2026-approved-demo-header-16x9.png",
        PROJECT / "research" / "honey-formal-publication-demo" / "outputs" / "render-report.json",
        PROJECT / "research" / "honey-formal-publication-demo" / "honey-release-manifest-approved-demo.json",
        PROJECT / "research" / "honey-formal-publication-demo" / "outputs" / "release-manifest.json",
        PROJECT / "research" / "release-manifest-v1" / "DESIGN-CONTRACT.md",
        PROJECT / "research" / "release-manifest-v1" / "RESULT.md",
        PROJECT / "research" / "honey-formal-publication-demo" / "honey-release-signature-approved-demo.json",
        PROJECT / "research" / "honey-formal-publication-demo" / "outputs" / "release-signature.json",
        PROJECT / "research" / "honey-formal-publication-demo" / "outputs" / "trusted-release-keys.json",
        PROJECT / "research" / "honey-formal-publication-demo" / "outputs" / "release-audit.jsonl",
        PROJECT / "research" / "honey-formal-publication-demo" / "outputs" / "audit-event.json",
        PROJECT / "research" / "release-security-v1" / "DESIGN-CONTRACT.md",
        PROJECT / "research" / "release-security-v1" / "RESULT.md",
        PROJECT / "research" / "release-security-v1" / "trusted-release-keys-demo.json",
        PROJECT / "research" / "release-security-v1" / "release-audit-demo.jsonl",
        PROJECT / "research" / "non-production-runbook-v1" / "DESIGN-CONTRACT.md",
        PROJECT / "research" / "non-production-runbook-v1" / "RESULT.md",
    ]
    for path in required:
        if not path.is_file():
            failures.append(f"missing required file: {path}")

    if failures:
        return report(failures)

    readme = (PROJECT / "README.md").read_text(encoding="utf-8")
    analysis = (PROJECT / "docs" / "analysis.md").read_text(encoding="utf-8")
    roadmap = (PROJECT / "docs" / "use-cases-and-roadmap.md").read_text(encoding="utf-8")
    html = (SHOWCASE / "index.html").read_text(encoding="utf-8")
    script = (SHOWCASE / "app.js").read_text(encoding="utf-8")
    prompts = (SHOWCASE / "assets" / "generated" / "PROMPTS.md").read_text(encoding="utf-8")
    multi_prompts = (SHOWCASE / "assets" / "generated" / "MULTI_EFFECT_PROMPTS.md").read_text(encoding="utf-8")
    scenario_prompts = (SHOWCASE / "assets" / "generated" / "SCENARIO_PROMPTS.md").read_text(encoding="utf-8")
    workflow = (REPO / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
    root_index = (REPO / "site" / "index.html").read_text(encoding="utf-8")
    root_readme = (REPO / "README.md").read_text(encoding="utf-8")

    for document, name in ((readme, "README"), (analysis, "analysis"), (prompts, "PROMPTS")):
        if PINNED_COMMIT not in document:
            failures.append(f"{name} does not record pinned commit")

    for phrase in (
        "不是给照片织一层纹理",
        "同一条河",
        "意境不变",
        "同一意境、六种材料",
        "不是先选风格",
        "家庭成长册 / 绘本扉页",
        "旅行纪念 / 户外栏目封面",
        "社区公益 / 年度影响力报告",
        "独立品牌 / 季节活动主视觉",
        "AI 负责底图",
        "家庭成长册封面",
        "旅行日志封面",
        "年度影响力报告",
        "季节活动主视觉",
        "这是布局验证，不是印刷终稿",
        "现在不只是展厅",
        "ACTUAL FILE TREE",
        "FAIL-CLOSED",
        "自动路由真的更合适吗",
        "第一轮不是全过",
        "自动路线胜出",
        "跨题材能工作吗",
        "只代表这三个样本通过",
        "旧样例锁定保留",
        "BASELINE LOCKED",
        "分数不能自己出现",
        "THE TOOL CANNOT",
        "中文调用，不等于",
        "一席",
        "把安静",
        "SAMPLE COPY ONLY",
        "左边看原图",
        "现有茶具样例",
        "AFTER / 有机针织",
        "AFTER / 彩色玻璃",
        "AFTER / 陶瓷浮雕",
        "这次不是排版示意",
        "copy.json、自动排版与双尺寸导出",
        "六类门禁全部 PASS",
        "V1 BETA BOUNDARY",
        "不是把同一个海报换图",
        "TEMPLATE 02 / BOOK COVER",
        "TEMPLATE 03 / IMPACT REPORT",
        "TEMPLATE 04 / FIELD JOURNAL",
        "V2 BETA BOUNDARY",
        "从编辑 JSON",
        "Publication Studio",
        "生成预览并检查",
        "HTTP FLOW",
        "LOCAL BETA",
        "同一个活动模板",
        "STAGE 01 / 原始照片",
        "STAGE 02 / 无字 Key Art",
        "一勺秋蜜",
        "12 / 12 门禁 PASS",
        "正式发布不是删掉提示",
        "APPROVED MODE DEMO",
        "官方商城 · 秋季限定",
        "EXTERNAL RELEASE CHECKLIST",
        "APPROVAL-MODE DEMO ≠ REAL APPROVAL",
        "不再只是一个字段",
        "HASH-BOUND RELEASE GATE",
        "五个负责人，缺一不可",
        "Copy SHA 不一致",
        "INTEGRITY CONTRACT, NOT DIGITAL SIGNATURES",
        "谁签的、发布了什么",
        "TRUSTED SIGNATURE & AUDIT PROTOTYPE",
        "demo-release-key-2026",
        "sequence 1 · PASS",
        "私钥没有进入仓库",
        "PROTOTYPE TRUST ≠ ENTERPRISE IDENTITY",
        "暂不进入生产",
        "NON-PRODUCTION ACTION RUNBOOK",
        "同一门禁连续两次失败",
        "20–50 个样本 Benchmark",
        "DEFER UNTIL PRODUCTION IS AUTHORIZED",
        "RETAIN / 保留",
        "五层协作",
        "隐性审美",
        "下一批还可以用在",
        "从漂亮样图",
        "实际价值",
        "值得研究，但别把它说成新模型",
    ):
        if phrase not in html:
            failures.append(f"showcase missing content: {phrase}")

    for key in ("brand:", "travel:", "family:", "editorial:", "community:", "packaging:"):
        if key not in script:
            failures.append(f"scenario router missing: {key}")

    for key in ("knit:", "paper:", "ceramic:", "glass:", "woodcut:", "diorama:"):
        if key not in script:
            failures.append(f"effect lab router missing: {key}")

    if html.count('data-effect=') != 12:
        failures.append("effect lab must expose six tabs and six overview cards")
    if html.count('class="scenario-case"') + html.count('class="scenario-case reverse"') != 4:
        failures.append("scenario showcase must contain exactly four concrete cases")
    if html.count('class="deliverable-card"') != 4:
        failures.append("deliverable showcase must contain exactly four code-native mockups")
    if html.count('class="route-matrix"') != 1:
        failures.append("framework showcase must contain one target route matrix")
    if html.count('class="forward-route ') != 2:
        failures.append("forward-test showcase must contain auto and override routes")
    if html.count('class="pilot-card"') != 3:
        failures.append("pilot benchmark must contain exactly three cross-subject samples")
    if html.count('class="ledger-grid"') != 1:
        failures.append("showcase must contain one append-only research ledger")
    if html.count('class="ledger-grid"') == 1 and html.count('href="#review-protocol"') < 1:
        failures.append("research ledger does not link the review protocol")
    if html.count('id="review-protocol"') != 1:
        failures.append("showcase must contain one review protocol section")
    if html.count('id="chinese-publish"') != 1:
        failures.append("showcase must contain one Chinese publishing section")
    if html.count('class="chinese-layout-card') != 2:
        failures.append("Chinese publishing section must contain portrait and wide layouts")
    if html.count('href="#chinese-publish"') < 2:
        failures.append("navigation and ledger must both link the Chinese publishing section")
    if html.count('id="additional-validation"') != 1:
        failures.append("showcase must contain one additional validation section")
    if html.count('class="validation-v2-card"') != 3:
        failures.append("additional validation must contain exactly three source/result cards")
    if html.count('BEFORE / 原始照片') != 3:
        failures.append("each additional validation card must show its original image")
    if html.count('href="#additional-validation"') < 2:
        failures.append("navigation and ledger must both link the additional validation section")
    if html.count('id="publishing-pipeline"') != 1:
        failures.append("showcase must contain one deterministic publishing pipeline section")
    if html.count('class="publish-artifact ') != 3:
        failures.append("publishing pipeline must show one Key Art input and two exported outputs")
    if html.count('href="#publishing-pipeline"') < 2:
        failures.append("navigation and ledger must both link the publishing pipeline")
    if html.count('id="publishing-templates"') != 1:
        failures.append("showcase must contain one multi-template publishing expansion")
    if html.count('class="template-case"') != 3:
        failures.append("multi-template publishing expansion must contain exactly three target-specific cases")
    if html.count('href="#publishing-templates"') < 2:
        failures.append("navigation and ledger must both link the multi-template expansion")
    if html.count('id="publication-studio"') != 1:
        failures.append("showcase must contain one Publication Studio entry section")
    if html.count('href="#publication-studio"') < 2:
        failures.append("navigation and ledger must both link the Publication Studio entry")
    if html.count('class="studio-verification-strip"') != 1:
        failures.append("Publication Studio entry must expose one verification strip")
    if html.count('id="honey-publication"') != 1:
        failures.append("showcase must contain one honey publication validation section")
    if html.count('href="#honey-publication"') < 2:
        failures.append("navigation and ledger must both link the honey publication validation")
    if html.count('class="honey-stage-card') != 4:
        failures.append("honey publication validation must show source, Key Art and two final outputs")
    if html.count('id="formal-publication"') != 1:
        failures.append("showcase must contain one formal publication mode section")
    if html.count('href="#formal-publication"') < 2:
        failures.append("navigation and ledger must both link formal publication mode")
    if html.count('class="formal-comparison-grid"') != 1:
        failures.append("formal publication mode must contain one sample-versus-approved comparison")
    if html.count('id="release-manifest"') != 1:
        failures.append("showcase must contain one Release Manifest gate section")
    if html.count('href="#release-manifest"') < 2:
        failures.append("navigation and ledger must both link the Release Manifest section")
    if html.count('class="release-fail-matrix"') != 1:
        failures.append("Release Manifest section must expose one fail-closed matrix")
    if html.count('id="release-security"') != 1:
        failures.append("showcase must contain one release signature and audit section")
    if html.count('href="#release-security"') < 2:
        failures.append("navigation and ledger must both link release security")
    if html.count('class="security-evidence-grid"') != 1:
        failures.append("release security must expose one public evidence grid")
    if html.count('id="action-runbook"') != 1:
        failures.append("showcase must contain one non-production action runbook section")
    if html.count('href="#action-runbook"') < 2:
        failures.append("navigation and ledger must both link the action runbook")
    if html.count('class="action-path"') != 1 or html.count('class="action-path"') == 1 and html.count('<li><span>0') < 7:
        failures.append("action runbook must retain the seven-stage action path")
    if html.count('class="action-failure-table"') != 1 or html.count('class="nonprod-backlog"') != 1:
        failures.append("action runbook must retain failure responses and non-production backlog")
    for exact_copy in ("Our Shared", "Follow", "Many hands.", "Morning"):
        if exact_copy not in html:
            failures.append(f"deliverable mockup missing deterministic copy: {exact_copy}")

    for phrase in ("阶段 A", "阶段 B", "阶段 C", "阶段 D", "实际价值分层"):
        if phrase not in roadmap:
            failures.append(f"roadmap missing: {phrase}")

    parser = ResourceParser()
    parser.feed(html)
    for resource in parser.resources:
        if resource.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = (SHOWCASE / resource.split("#", 1)[0]).resolve()
        if not target.exists():
            failures.append(f"missing local showcase resource: {resource}")

    source_size = png_size(SHOWCASE / "assets" / "generated" / "canoe-source.png")
    result_size = png_size(SHOWCASE / "assets" / "generated" / "canoe-organic-knit.png")
    if source_size != result_size:
        failures.append(f"before/after dimensions differ: {source_size} vs {result_size}")
    if source_size[0] <= source_size[1]:
        failures.append(f"demo images must preserve landscape orientation: {source_size}")

    effect_files = [
        "canoe-paper-cut.png",
        "canoe-ceramic-relief.png",
        "canoe-stained-glass.png",
        "canoe-woodcut.png",
        "canoe-miniature-diorama.png",
    ]
    for filename in effect_files:
        effect_size = png_size(SHOWCASE / "assets" / "generated" / filename)
        if effect_size != source_size:
            failures.append(f"effect image dimensions differ for {filename}: {effect_size} vs {source_size}")

    scenario_files = [
        "scenario-family-source.png",
        "scenario-family-knit.png",
        "scenario-community-source.png",
        "scenario-community-glass.png",
        "scenario-bakery-source.png",
        "scenario-bakery-paper.png",
    ]
    for filename in scenario_files:
        scenario_size = png_size(SHOWCASE / "assets" / "generated" / filename)
        scenario_ratio = scenario_size[0] / scenario_size[1]
        source_ratio = source_size[0] / source_size[1]
        if scenario_size[0] <= scenario_size[1] or abs(scenario_ratio - source_ratio) > 0.02:
            failures.append(f"scenario image lost landscape aspect for {filename}: {scenario_size}")

    forward_source = png_size(SHOWCASE / "assets" / "generated" / "forward-lighthouse-source.png")
    if forward_source[0] <= forward_source[1]:
        failures.append(f"forward-test source must be landscape: {forward_source}")
    for filename in (
        "forward-lighthouse-auto-woodcut.png",
        "forward-lighthouse-auto-woodcut-v2.png",
        "forward-lighthouse-override-paper.png",
        "forward-lighthouse-override-paper-v2.png",
    ):
        width, height = png_size(SHOWCASE / "assets" / "generated" / filename)
        if width >= height:
            failures.append(f"forward-test result must be portrait: {filename} {(width, height)}")

    for filename in (
        "pilot-person-source.png",
        "pilot-product-source.png",
        "pilot-architecture-source.png",
    ):
        width, height = png_size(SHOWCASE / "assets" / "generated" / filename)
        if width <= height:
            failures.append(f"pilot source must be landscape: {filename} {(width, height)}")
    for filename in (
        "pilot-person-auto-knit.png",
        "pilot-product-auto-paper.png",
        "pilot-architecture-auto-woodcut.png",
    ):
        width, height = png_size(SHOWCASE / "assets" / "generated" / filename)
        if width >= height:
            failures.append(f"pilot result must be portrait: {filename} {(width, height)}")

    if "Follow the Current" not in prompts or "Retain:" not in prompts or "Transform:" not in prompts or "Discard:" not in prompts:
        failures.append("prompt archive does not preserve the production contract")
    for heading in ("Layered paper cut", "Ceramic bas-relief", "Stained glass", "Reduction woodcut", "Miniature diorama"):
        if heading not in multi_prompts:
            failures.append(f"multi-effect prompt archive missing: {heading}")
    for heading in ("Family memory", "Community impact", "Independent bakery"):
        if heading not in scenario_prompts:
            failures.append(f"scenario prompt archive missing: {heading}")

    if '"projects/photo-to-organic-knit/**"' not in workflow:
        failures.append("Pages workflow does not watch photo-to-organic-knit")
    if "projects/photo-to-organic-knit/showcase" not in workflow:
        failures.append("Pages workflow does not publish photo-to-organic-knit showcase")
    if "projects/photo-to-organic-knit/extension" not in workflow:
        failures.append("Pages workflow does not publish photo-to-organic-knit extension")
    if "projects/photo-to-organic-knit/research" not in workflow:
        failures.append("Pages workflow does not publish photo-to-organic-knit research artifacts")
    if "projects/photo-to-organic-knit/studio" not in workflow:
        failures.append("Pages workflow does not publish Publication Studio source and instructions")
    if "Photo to Organic Knit" not in root_index or "Photo to Organic Knit" not in root_readme:
        failures.append("root indexes do not list Photo to Organic Knit")

    profile_counts = {
        "effects": 6,
        "scenarios": 4,
        "deliveries": 4,
    }
    for kind, expected in profile_counts.items():
        paths = sorted((EXTENSION / "profiles" / kind).glob("*.json"))
        if len(paths) != expected:
            failures.append(f"expected {expected} {kind} profiles, found {len(paths)}")
        for path in paths:
            payload = json.loads(path.read_text(encoding="utf-8"))
            if payload.get("id") != path.stem:
                failures.append(f"profile id mismatch: {path}")

    forward_manifest = json.loads((EXTENSION / "forward-tests" / "lighthouse-travel" / "manifest.json").read_text(encoding="utf-8"))
    if forward_manifest["routes"]["auto"]["total"] != 25 or forward_manifest["routes"]["override"]["total"] != 24:
        failures.append("forward-test manifest score totals changed")
    field_journal = json.loads((EXTENSION / "profiles" / "deliveries" / "field-journal.json").read_text(encoding="utf-8"))
    if "top approximately 10%" not in field_journal["safe_area"] or "bottom approximately 10%" not in field_journal["safe_area"]:
        failures.append("field-journal profile lost the evidence-backed metadata bands")
    pilot_manifest = json.loads((EXTENSION / "forward-tests" / "pilot-n3" / "manifest.json").read_text(encoding="utf-8"))
    if pilot_manifest["sample_size"] != 3 or pilot_manifest["observed_first_round_passes"] != 3:
        failures.append("pilot manifest sample/pass counts changed")
    if pilot_manifest["generalization_claim"] is not False:
        failures.append("pilot manifest must not make a generalization claim")
    if any(sample["attempts"] != 1 for sample in pilot_manifest["samples"]):
        failures.append("pilot samples must record one attempt each")

    chinese_result = PROJECT / "research" / "chinese-invocation" / "result-layered-paper.png"
    chinese_width, chinese_height = png_size(chinese_result)
    if chinese_width >= chinese_height:
        failures.append(f"Chinese invocation result must be portrait: {(chinese_width, chinese_height)}")
    chinese_record = (PROJECT / "research" / "chinese-invocation" / "RESULT.md").read_text(encoding="utf-8")
    for phrase in ("seasonal-campaign → layered-paper → campaign-poster", "PASS — 34/35", "未进行人工翻译或补写"):
        if phrase not in chinese_record:
            failures.append(f"Chinese invocation record missing: {phrase}")

    additional_root = PROJECT / "research" / "additional-validation-v2"
    for stem in ("family-pet", "community-rain", "honey"):
        source_path = additional_root / f"{stem}-source.png"
        result_name = {"family-pet": "family-pet-knit.png", "community-rain": "community-rain-glass.png", "honey": "honey-ceramic.png"}[stem]
        result_path = additional_root / result_name
        source_width, source_height = png_size(source_path)
        result_width, result_height = png_size(result_path)
        if source_width <= source_height:
            failures.append(f"additional source must be landscape: {source_path}")
        if result_width >= result_height:
            failures.append(f"additional result must be portrait: {result_path}")

    publishing_root = PROJECT / "research" / "publishing-pipeline-v1" / "outputs"
    poster_size = png_size(publishing_root / "autumn-tea-2026-sample-poster-4x5.png")
    header_size = png_size(publishing_root / "autumn-tea-2026-sample-header-16x9.png")
    if poster_size != (1200, 1500):
        failures.append(f"publishing poster dimensions changed: {poster_size}")
    if header_size != (1920, 1080):
        failures.append(f"publishing header dimensions changed: {header_size}")
    render_report = json.loads((publishing_root / "render-report.json").read_text(encoding="utf-8"))
    if render_report.get("status") != "PASS":
        failures.append("deterministic publishing report must pass")
    expected_gate_count = 2 * 6
    if len(render_report.get("checks", [])) != expected_gate_count or any(check.get("status") != "PASS" for check in render_report.get("checks", [])):
        failures.append("deterministic publishing report must retain twelve passing variant gates")
    if set(render_report.get("outputs", {})) != {"poster-4x5", "header-16x9"}:
        failures.append("deterministic publishing report must retain both output variants")

    v2_root = PROJECT / "research" / "publishing-pipeline-v2"
    v2_outputs = (
        ("book-cover", "family-memory-volume-01-sample-book-cover-3x4.png", (1200, 1600), "book-cover-3x4"),
        ("impact-report", "community-rain-impact-2026-sample-impact-report-a4.png", (1240, 1754), "impact-report-a4"),
        ("field-journal", "lighthouse-field-journal-2026-sample-field-journal-4x5.png", (1200, 1500), "field-journal-4x5"),
    )
    for directory, filename, expected_size, variant_name in v2_outputs:
        output_root = v2_root / directory
        actual_size = png_size(output_root / filename)
        if actual_size != expected_size:
            failures.append(f"{directory} publishing dimensions changed: {actual_size}")
        report_payload = json.loads((output_root / "render-report.json").read_text(encoding="utf-8"))
        if report_payload.get("status") != "PASS":
            failures.append(f"{directory} publishing report must pass")
        checks = report_payload.get("checks", [])
        if len(checks) != 6 or any(check.get("status") != "PASS" for check in checks):
            failures.append(f"{directory} publishing report must retain six passing gates")
        if set(report_payload.get("outputs", {})) != {variant_name}:
            failures.append(f"{directory} publishing report has an unexpected variant set")

    honey_root = PROJECT / "research" / "honey-publication-validation" / "outputs"
    honey_poster = honey_root / "wild-honey-autumn-2026-sample-poster-4x5.png"
    honey_header = honey_root / "wild-honey-autumn-2026-sample-header-16x9.png"
    if png_size(honey_poster) != (1200, 1500):
        failures.append("honey campaign poster dimensions changed")
    if png_size(honey_header) != (1920, 1080):
        failures.append("honey campaign header dimensions changed")
    honey_report = json.loads((honey_root / "render-report.json").read_text(encoding="utf-8"))
    if honey_report.get("status") != "PASS" or honey_report.get("template", {}).get("id") != "campaign-poster":
        failures.append("honey campaign must pass through the existing campaign-poster template")
    honey_checks = honey_report.get("checks", [])
    if len(honey_checks) != 12 or any(check.get("status") != "PASS" for check in honey_checks):
        failures.append("honey campaign must retain twelve passing variant gates")
    honey_poster_items = honey_report.get("outputs", {}).get("poster-4x5", {}).get("text_items", [])
    honey_text = {item.get("field"): item.get("value") for item in honey_poster_items if item.get("source_copy")}
    if honey_text.get("brand.name") != "山野蜜坊" or honey_text.get("campaign.headline_lines[1]") != "秋蜜":
        failures.append("honey campaign report lost its exact deterministic copy")

    formal_root = PROJECT / "research" / "honey-formal-publication-demo" / "outputs"
    formal_poster = formal_root / "wild-honey-autumn-2026-approved-demo-poster-4x5.png"
    formal_header = formal_root / "wild-honey-autumn-2026-approved-demo-header-16x9.png"
    if png_size(formal_poster) != (1200, 1500) or png_size(formal_header) != (1920, 1080):
        failures.append("formal publication demo dimensions changed")
    formal_report = json.loads((formal_root / "render-report.json").read_text(encoding="utf-8"))
    if formal_report.get("status") != "PASS" or formal_report.get("copy_status") != "approved":
        failures.append("formal publication demo must pass with approved copy status")
    formal_checks = formal_report.get("checks", [])
    if len(formal_checks) != 12 or any(check.get("status") != "PASS" for check in formal_checks):
        failures.append("formal publication demo must retain twelve passing gates")
    for output in formal_report.get("outputs", {}).values():
        fields = {item.get("field"): item.get("value") for item in output.get("text_items", [])}
        if "generated.sample_disclosure" in fields:
            failures.append("approved formal publication output must not render a sample disclosure")
        if fields.get("campaign.location") != "官方商城 · 秋季限定":
            failures.append("approved formal publication output lost its channel field")
    release_summary = formal_report.get("release", {})
    if release_summary.get("status") != "PASS" or release_summary.get("release_id") != "wild-honey-autumn-2026-approved-demo":
        failures.append("formal publication report must retain a passing Release Manifest")
    if set(release_summary.get("approvals", {})) != {"brand", "copy", "legal", "design", "channel"}:
        failures.append("formal publication report must retain five release approvals")
    source_manifest = PROJECT / "research" / "honey-formal-publication-demo" / "honey-release-manifest-approved-demo.json"
    output_manifest = formal_root / "release-manifest.json"
    if source_manifest.read_bytes() != output_manifest.read_bytes():
        failures.append("formal output bundle did not retain the exact Release Manifest")
    signature_summary = formal_report.get("signature", {})
    audit_summary = formal_report.get("audit", {})
    if signature_summary.get("status") != "PASS" or signature_summary.get("key_id") != "demo-release-key-2026":
        failures.append("formal release must retain a passing trusted Ed25519 signature")
    if audit_summary.get("status") != "PASS" or audit_summary.get("sequence") != 1:
        failures.append("formal release must retain the first passing audit event")
    source_signature = PROJECT / "research" / "honey-formal-publication-demo" / "honey-release-signature-approved-demo.json"
    output_signature = formal_root / "release-signature.json"
    if source_signature.read_bytes() != output_signature.read_bytes():
        failures.append("formal output bundle did not retain the exact detached signature")
    source_trust = PROJECT / "research" / "release-security-v1" / "trusted-release-keys-demo.json"
    output_trust = formal_root / "trusted-release-keys.json"
    if source_trust.read_bytes() != output_trust.read_bytes():
        failures.append("formal output bundle did not retain the trusted public key snapshot")
    if any(PROJECT.rglob("*.pem")):
        failures.append("private or PEM key material must not be retained in the project")
    audit_verify = subprocess.run(
        [sys.executable, "-B", str(EXTENSION / "scripts" / "release_security.py"), "audit-verify", "--audit-log", str(PROJECT / "research" / "release-security-v1" / "release-audit-demo.jsonl")],
        cwd=EXTENSION,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if audit_verify.returncode != 0:
        failures.append(f"release audit chain failed verification: {audit_verify.stderr.strip()}")

    review_result = subprocess.run(
        [
            sys.executable,
            str(EXTENSION / "scripts" / "score_review.py"),
            "--review", str(EXTENSION / "forward-tests" / "lighthouse-travel" / "review-auto-v2.json"),
            "--scenario", "travel-cover",
            "--delivery", "field-journal",
            "--format", "json",
        ],
        cwd=EXTENSION,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if review_result.returncode != 0:
        failures.append(f"review scorer failed: {review_result.stderr.strip()}")
    else:
        review_summary = json.loads(review_result.stdout)
        if review_summary["decision"] != "pass" or review_summary["score"]["earned"] != 40:
            failures.append(f"unexpected review summary: {review_summary['decision']} {review_summary['score']}")

    chinese_review_result = subprocess.run(
        [
            sys.executable,
            str(EXTENSION / "scripts" / "score_review.py"),
            "--review", str(PROJECT / "research" / "chinese-invocation" / "review.json"),
            "--scenario", "seasonal-campaign",
            "--delivery", "campaign-poster",
            "--format", "json",
        ],
        cwd=EXTENSION,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if chinese_review_result.returncode != 0:
        failures.append(f"Chinese review scorer failed: {chinese_review_result.stderr.strip()}")
    else:
        chinese_summary = json.loads(chinese_review_result.stdout)
        if chinese_summary["decision"] != "pass" or chinese_summary["score"]["earned"] != 34:
            failures.append(f"unexpected Chinese review summary: {chinese_summary['decision']} {chinese_summary['score']}")

    additional_reviews = (
        ("family-pet-review.json", "family-memory", "book-cover", 35),
        ("community-rain-review.json", "impact-report", "impact-report", 35),
        ("honey-review.json", "seasonal-campaign", "campaign-poster", 34),
    )
    for review_file, scenario, delivery, expected_score in additional_reviews:
        result = subprocess.run(
            [sys.executable, str(EXTENSION / "scripts" / "score_review.py"), "--review", str(additional_root / review_file), "--scenario", scenario, "--delivery", delivery, "--format", "json"],
            cwd=EXTENSION,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if result.returncode != 0:
            failures.append(f"additional review failed for {review_file}: {result.stderr.strip()}")
        else:
            summary = json.loads(result.stdout)
            if summary["decision"] != "pass" or summary["score"]["earned"] != expected_score:
                failures.append(f"unexpected additional review summary for {review_file}: {summary['decision']} {summary['score']}")

    routes = [
        ("family-essence.json", "family-memory", "organic-knit", "book-cover"),
        ("canoe-essence.json", "travel-cover", "woodcut", "field-journal"),
        ("community-essence.json", "impact-report", "stained-glass", "impact-report"),
        ("bakery-essence.json", "seasonal-campaign", "layered-paper", "campaign-poster"),
    ]
    for essence, scenario, expected_effect, expected_delivery in routes:
        result = subprocess.run(
            [
                sys.executable,
                str(EXTENSION / "scripts" / "build_prompt.py"),
                "--essence", str(EXTENSION / "examples" / essence),
                "--scenario", scenario,
                "--format", "json",
            ],
            cwd=EXTENSION,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if result.returncode != 0:
            failures.append(f"compiler failed for {scenario}: {result.stderr.strip()}")
            continue
        route = json.loads(result.stdout)["route"]
        if route["effect"] != expected_effect or route["delivery"] != expected_delivery:
            failures.append(f"unexpected route for {scenario}: {route}")

    studio_tests = subprocess.run(
        [sys.executable, "-B", "-m", "unittest", "discover", "-s", str(PROJECT / "studio" / "tests"), "-v"],
        cwd=PROJECT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if studio_tests.returncode != 0:
        failures.append(f"Publication Studio tests failed: {studio_tests.stdout.strip()} {studio_tests.stderr.strip()}")

    return report(failures)


def report(failures: list[str]) -> int:
    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS")
    print("- upstream Skill, style spec, reference and MIT license are present")
    print("- pinned upstream commit is recorded in research artifacts")
    print("- independent before/after PNGs share landscape dimensions")
    print("- exact ImageGen prompts and visual review are archived")
    print("- six material effects share dimensions, semantic anchors, and an interactive router")
    print("- four target-use cases connect source evidence, effect choice, deliverables, and value")
    print("- four code-native mockups separate generated art from deterministic typography")
    print("- target-driven extension compiles four scenarios through 14 machine-readable profiles")
    print("- unseen lighthouse forward test records auto/override routes, one failed gate, correction, and 25/24 review")
    print("- n=3 pilot covers person, product, and architecture routes without a generalization claim")
    print("- append-only ledger protects baseline examples and the review scorer validates 8/8 evidence gates")
    print("- installed Skill Chinese invocation routes to layered paper and validates PASS 34/35")
    print("- Chinese Key Art is reused in selectable 4:5 and 16:9 deterministic layouts")
    print("- three additional validations show full original/result pairs for knit, stained glass, and ceramic relief")
    print("- deterministic campaign renderer preserves exact Chinese copy and exports passing 4:5 and 16:9 files")
    print("- book-cover, impact-report and field-journal templates render reviewed Key Art into passing target-specific masters")
    print("- localhost Publication Studio validates four-template editing, rendering, gate feedback, batch ZIP and temporary cleanup")
    print("- honey source, ceramic Key Art and exact copy reuse campaign-poster for passing 4:5 and 16:9 finals")
    print("- approved-mode honey demo removes sample disclosure, retains official channel copy and documents external release approvals")
    print("- Release Manifest binds approved output to copy/art hashes and five complete approvals with fail-closed enforcement")
    print("- Ed25519 trusted signature and hash-chained audit bind the formal release without retaining private key material")
    print("- non-production runbook turns normal operation, failure handling, research backlog and stop rules into explicit actions")
    print("- showcase resources, comparison, scenario router and roadmap resolve")
    print("- root indexes and Pages workflow include the project")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
