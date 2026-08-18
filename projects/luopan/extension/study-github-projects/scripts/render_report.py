#!/usr/bin/env python3
"""Validate one project-study JSON file and render Markdown plus self-contained HTML."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path


REQUIRED = ("project", "verdict", "capabilities", "mechanism", "verification", "limitations", "extensions", "sources")
STATUSES = {"verified", "declared", "external", "gap"}
STATUS_LABELS = {"verified": "已验证", "declared": "官方宣称", "external": "外部依赖", "gap": "实现缺口"}
VERDICT_LABELS = {"what": "能力", "purpose": "作用", "mechanism": "原理", "fit": "适配判断"}


def validate(model: dict) -> None:
    missing = [key for key in REQUIRED if key not in model]
    if missing:
        raise ValueError("missing top-level fields: " + ", ".join(missing))

    project = model["project"]
    for key in ("name", "upstream_url", "upstream_commit", "license", "study_date"):
        if not project.get(key):
            raise ValueError(f"project.{key} is required")
    if not re.fullmatch(r"[0-9a-fA-F]{40}", project["upstream_commit"]):
        raise ValueError("project.upstream_commit must be a 40-character SHA")

    source_ids = {item.get("id") for item in model["sources"]}
    if None in source_ids or len(source_ids) != len(model["sources"]):
        raise ValueError("source ids must exist and be unique")

    for capability in model["capabilities"]:
        if capability.get("status") not in STATUSES:
            raise ValueError(f"invalid capability status: {capability.get('status')}")
        check_source_ids(capability, source_ids, "capability")
    for stage in model["mechanism"]:
        check_source_ids(stage, source_ids, "mechanism stage")

    verification = model["verification"]
    for key in ("passed", "failed"):
        if not isinstance(verification.get(key), int) or verification[key] < 0:
            raise ValueError(f"verification.{key} must be a non-negative integer")


def check_source_ids(item: dict, known: set[str], label: str) -> None:
    ids = item.get("source_ids", [])
    if not isinstance(ids, list) or not set(ids) <= known:
        raise ValueError(f"{label} references an unknown source")


def escape(value: object) -> str:
    return html.escape(str(value))


def source_links(ids: list[str], source_map: dict[str, dict]) -> str:
    return " · ".join(
        f'<a href="{html.escape(source_map[item]["url"], quote=True)}" target="_blank" rel="noopener">{escape(source_map[item]["title"])}</a>'
        for item in ids if item in source_map
    )


def markdown(model: dict) -> str:
    project = model["project"]
    sources = {item["id"]: item for item in model["sources"]}
    out = [
        f'# {project["name"]} 项目研究', '',
        f'- 上游：[{project["upstream_url"]}]({project["upstream_url"]})',
        f'- 研究版本：`{project["upstream_commit"]}`',
        f'- 许可证：{project["license"]}',
        f'- 研究日期：{project["study_date"]}', '',
        '## 30 秒结论', '',
    ]
    for key in ("what", "purpose", "mechanism", "fit"):
        out += [f'- **{VERDICT_LABELS[key]}：** {model["verdict"][key]}']

    out += ['', '## 能力核验', '', '| 能力 | 状态 | 边界 |', '| --- | --- | --- |']
    for item in model["capabilities"]:
        out.append(f'| {item["name"]} | {STATUS_LABELS[item["status"]]} | {item["description"]} |')
        if item.get("evidence"):
            out += [''] + [f'  - {evidence}' for evidence in item["evidence"]]
        links = "; ".join(f'[{sources[sid]["title"]}]({sources[sid]["url"]})' for sid in item.get("source_ids", []) if sid in sources)
        if links:
            out += [f'  - 来源：{links}']

    out += ['', '## 原理：五层工作链', '']
    for index, stage in enumerate(model["mechanism"], 1):
        out += [f'### {index}. {stage["stage"]}', '', stage["description"], '']

    verification = model["verification"]
    out += [
        '## 实际验证', '',
        f'- 环境：{verification["environment"]}',
        f'- 测试：{verification["passed"]} 通过 / {verification["failed"]} 失败', '',
        '```shell', *verification.get("commands", []), '```', '',
    ]
    out += [f'- {note}' for note in verification.get("notes", [])]
    out += ['', '## 已知边界', ''] + [f'- {item}' for item in model["limitations"]]
    out += ['', '## 面向主仓库的扩展', '']
    for item in model["extensions"]:
        out += [f'### {item["name"]}', '', item["description"], '', f'**验收：** {item["acceptance"]}', '']
    out += ['## 来源', '']
    out += [f'- **{item["level"]} 级** [{item["title"]}]({item["url"]})' for item in model["sources"]]
    return "\n".join(out).rstrip() + "\n"


def html_report(model: dict, css: str, js: str) -> str:
    project = model["project"]
    source_map = {item["id"]: item for item in model["sources"]}

    verdicts = "".join(
        f'<article class="verdict"><small>{escape(VERDICT_LABELS[key])}</small><h3>{escape(model["verdict"][key])}</h3></article>'
        for key in ("what", "purpose", "mechanism", "fit")
    )
    capabilities = "".join(
        '<article class="capability" data-cap-status="{status}">'
        '<div class="cap-top"><div><span class="status status-{status}">{label}</span><h3>{name}</h3></div></div>'
        '<p>{description}</p><ul class="evidence">{evidence}</ul><p class="refs">{links}</p></article>'.format(
            status=escape(item["status"]),
            label=escape(STATUS_LABELS[item["status"]]),
            name=escape(item["name"]),
            description=escape(item["description"]),
            evidence="".join(f'<li>{escape(entry)}</li>' for entry in item.get("evidence", [])),
            links=source_links(item.get("source_ids", []), source_map),
        ) for item in model["capabilities"]
    )
    mechanism = "".join(
        f'<article class="mechanism-step"><h3>{escape(item["stage"])}</h3><p>{escape(item["description"])}</p><p class="refs">{source_links(item.get("source_ids", []), source_map)}</p></article>'
        for item in model["mechanism"]
    )
    verification = model["verification"]
    commands = "".join(f'<div class="command">{escape(command)}</div>' for command in verification.get("commands", []))
    notes = "".join(f'<li>{escape(note)}</li>' for note in verification.get("notes", []))
    limitations = "".join(f'<li>{escape(item)}</li>' for item in model["limitations"])
    extensions = "".join(
        f'<article class="extension-card"><small>可交付扩展</small><h3>{escape(item["name"])}</h3><p>{escape(item["description"])}</p><p class="acceptance"><strong>验收：</strong>{escape(item["acceptance"])}</p></article>'
        for item in model["extensions"]
    )
    sources = "".join(
        f'<li><span class="level">{escape(item["level"])}</span><a href="{html.escape(item["url"], quote=True)}" target="_blank" rel="noopener">{escape(item["title"])}</a></li>'
        for item in model["sources"]
    )

    return f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(project['name'])} 的能力、原理、边界与项目研究扩展">
  <title>{escape(project['name'])} · 项目研究 01</title>
  <style>{css}</style>
</head>
<body>
  <noscript><div class="noscript">JavaScript 已关闭：全部研究内容仍然可读，视角切换和筛选不可用。</div></noscript>
  <header class="masthead shell">
    <div class="topline">
      <div class="brand"><span class="brand-mark" aria-hidden="true"></span>CODE STUDY / 01</div>
      <a class="source-link" href="{html.escape(project['upstream_url'], quote=True)}" target="_blank" rel="noopener">查看上游源码 ↗</a>
    </div>
    <div class="hero">
      <div>
        <p class="eyebrow">能力不是宣称，证据才是边界</p>
        <h1>{escape(project['name'])}<br>研究罗盘</h1>
        <p class="hero-lede">{escape(model['verdict']['what'])} {escape(model['verdict']['purpose'])}</p>
      </div>
      <aside class="hero-side" aria-label="研究版本">
        <strong>{escape(project['upstream_commit'][:7])}</strong>
        <span>{escape(project['study_date'])} 固定研究版本</span>
        <span>{escape(project['license'])} License</span>
      </aside>
    </div>
  </header>

  <main class="shell">
    <nav class="viewbar" aria-label="研究视角">
      <span class="viewbar-label">切换阅读视角</span>
      <div class="segmented">
        <button type="button" data-set-view="upstream" aria-pressed="false">上游能力</button>
        <button type="button" data-set-view="extension" aria-pressed="false">项目扩展</button>
        <button type="button" data-set-view="all" aria-pressed="true">完整研究</button>
      </div>
    </nav>

    <section class="section" data-view-scope="upstream extension">
      <div class="section-head"><span class="section-no">00 / VERDICT</span><div><h2>它值得参考，但不该被当成开箱即用的数据产品。</h2><p class="section-intro">先给判断，再展开证据。四张卡分别回答能力、作用、原理和与当前主仓库的关系。</p></div></div>
      <div class="verdict-grid">{verdicts}</div>
    </section>

    <section class="section" data-view-scope="upstream">
      <div class="section-head"><span class="section-no">01 / CAPABILITY</span><div><h2>原生能力被拆成四种状态，避免 README 代替验证。</h2><p class="section-intro">“已验证”只代表本次固定环境中的可复现范围；外部依赖和实现缺口不会被藏在脚注里。</p></div></div>
      <div class="filters" role="group" aria-label="按能力状态筛选">
        <button type="button" data-cap-filter="all" aria-pressed="true">全部</button>
        <button type="button" data-cap-filter="verified" aria-pressed="false">已验证</button>
        <button type="button" data-cap-filter="declared" aria-pressed="false">官方宣称</button>
        <button type="button" data-cap-filter="external" aria-pressed="false">外部依赖</button>
        <button type="button" data-cap-filter="gap" aria-pressed="false">实现缺口</button>
      </div>
      <p id="filter-status" class="refs" aria-live="polite">已显示 {len(model['capabilities'])} 项能力</p>
      <div class="capability-grid">{capabilities}</div>
    </section>

    <section class="section" data-view-scope="upstream">
      <div class="section-head"><span class="section-no">02 / MECHANISM</span><div><h2>它的核心不是模型，而是把研究判断变成一条受约束的工作链。</h2><p class="section-intro">路由、证据、对抗验证与单一事实源共同减少“写得像、证据弱”的报告。</p></div></div>
      <div class="mechanism">{mechanism}</div>
    </section>

    <section class="section" data-view-scope="upstream">
      <div class="section-head"><span class="section-no">03 / PROOF</span><div><h2>确定性代码可以运行；业务研究仍依赖宿主 AI 与外部数据。</h2><p class="section-intro">这里展示实际执行命令、测试结果和 Windows 编码边界。</p></div></div>
      <div class="proof-layout">
        <div class="scoreboard"><strong>{verification['passed']}/{verification['passed'] + verification['failed']}</strong><span>使用 UTF-8 模式通过的上游自动化测试</span></div>
        <div><div class="command-list">{commands}</div><ul class="notes">{notes}</ul></div>
      </div>
    </section>

    <section class="section" data-view-scope="upstream extension">
      <div class="section-head"><span class="section-no">04 / BOUNDARY</span><div><h2>最值得研究的地方，也恰好暴露了它还不是完整产品。</h2><p class="section-intro">方法论很强，但数据依赖、可移植性和部分指标定义需要二次校正。</p></div></div>
      <ul class="warning-list">{limitations}</ul>
    </section>

    <section class="section" data-view-scope="extension">
      <div class="section-head"><span class="section-no">05 / EXTENSION</span><div><h2>把“商业研究罗盘”改造成主仓库的“GitHub 项目研究罗盘”。</h2><p class="section-intro">保留证据分级、路由、对抗验证和单一事实源，替换行业/公司领域假设。</p></div></div>
      <div class="extension-hero">
        <p class="eyebrow">LUOPAN → CODE STUDY</p>
        <h3>从一个仓库链接，到可验证、可展示、可继续扩展的研究条目。</h3>
        <p>{escape(model['verdict']['fit'])}</p>
        <div class="route" aria-label="扩展流程"><span>仓库 URL</span><span>固定 commit</span><span>能力核验</span><span>原理追踪</span><span>适配判断</span><span>扩展实现</span><span>主索引</span></div>
      </div>
      <div class="extension-grid">{extensions}</div>
    </section>

    <section class="section" data-view-scope="upstream extension">
      <div class="section-head"><span class="section-no">06 / SOURCES</span><div><h2>所有关键结论都回到固定版本、源码、测试和上游说明。</h2></div></div>
      <ul class="sources">{sources}</ul>
    </section>
  </main>

  <footer class="shell">研究对象归原作者所有；本页为独立研究与扩展，不代表上游维护者观点。上游代码遵循其 MIT License。</footer>
  <script>{js}</script>
</body>
</html>'''


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    model = json.loads(args.input.read_text(encoding="utf-8"))
    validate(model)
    root = Path(__file__).resolve().parent.parent
    css = (root / "assets" / "report.css").read_text(encoding="utf-8")
    js = (root / "assets" / "report.js").read_text(encoding="utf-8")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.output_dir.joinpath("index.html").write_text(html_report(model, css, js), encoding="utf-8")
    args.output_dir.joinpath("analysis.md").write_text(markdown(model), encoding="utf-8")


if __name__ == "__main__":
    main()
