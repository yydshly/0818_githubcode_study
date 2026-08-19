from __future__ import annotations

import re
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parents[1]
UPSTREAM = PROJECT / "upstream"

CHILD_SKILLS = [
    "muyang-editorial-minimal",
    "muyang-fashion-colorblock",
    "muyang-soft-dream",
    "muyang-white-couture",
    "muyang-dark-fashion",
    "muyang-oriental-poetry",
    "muyang-print-poster",
    "muyang-cinematic-narrative",
]

ALL_SKILLS = ["muyang-illustration", *CHILD_SKILLS]

EXPECTED_COUNTS = {
    "muyang-editorial-minimal": 3,
    "muyang-fashion-colorblock": 4,
    "muyang-soft-dream": 5,
    "muyang-white-couture": 2,
    "muyang-dark-fashion": 3,
    "muyang-oriental-poetry": 3,
    "muyang-print-poster": 3,
    "muyang-cinematic-narrative": 2,
}

GENERATED_SAMPLES = [
    "01-editorial-minimal.png",
    "02-fashion-colorblock.png",
    "03-soft-dream.png",
    "04-white-couture.png",
    "05-dark-fashion.png",
    "06-oriental-poetry.png",
    "07-print-poster.png",
    "08-cinematic-narrative.png",
]

CHECK_COUNT = 0


def check(condition: bool, message: str, failures: list[str]) -> None:
    global CHECK_COUNT
    CHECK_COUNT += 1
    if condition:
        print(f"[PASS] {message}")
    else:
        print(f"[FAIL] {message}")
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    skills_root = UPSTREAM / "skills"

    check(UPSTREAM.exists(), "fixed upstream submodule exists", failures)

    for skill in ALL_SKILLS:
        skill_root = skills_root / skill
        check((skill_root / "SKILL.md").is_file(), f"{skill} has SKILL.md", failures)
        check((skill_root / "agents" / "openai.yaml").is_file(), f"{skill} has agents/openai.yaml", failures)

    total_recipes = 0
    total_assets = 0
    asset_names: list[str] = []

    for skill, expected in EXPECTED_COUNTS.items():
        skill_root = skills_root / skill
        recipe_file = skill_root / "references" / "recipes.md"
        check(recipe_file.is_file(), f"{skill} has recipes.md", failures)
        recipe_text = recipe_file.read_text(encoding="utf-8") if recipe_file.is_file() else ""
        recipe_count = len(re.findall(r"^## ", recipe_text, flags=re.MULTILINE))
        assets = sorted((skill_root / "assets").glob("*.png"))
        check(recipe_count == expected, f"{skill} exposes {expected} recipe headings", failures)
        check(len(assets) == expected, f"{skill} exposes {expected} PNG references", failures)
        total_recipes += recipe_count
        total_assets += len(assets)
        asset_names.extend(asset.name for asset in assets)

    check(total_recipes == 25, "upstream exposes exactly 25 recipes", failures)
    check(total_assets == 25, "upstream exposes exactly 25 reference images", failures)

    showcase = PROJECT / "showcase"
    html = (showcase / "index.html").read_text(encoding="utf-8")
    js = (showcase / "app.js").read_text(encoding="utf-8")
    css = (showcase / "styles.css").read_text(encoding="utf-8")

    js_style_count = len(re.findall(r"\{ id: \d+, name:", js))
    check(js_style_count == 25, "showcase data contains exactly 25 style records", failures)
    check(len(re.findall(r"\{ styleId: \d+, asset:", js)) == 8, "showcase data contains exactly 8 generated sample records", failures)
    check(js.count("skill:") == 8, "showcase data contains exactly 8 child-skill routes", failures)
    check(html.count('<button class="filter') == 9, "showcase exposes all filter plus 8 categories", failures)
    check('id="demo-form"' in html and 'id="call-output"' in html, "text-only invocation demo is present", failures)
    check("本页到此为止" in html and "不调用 ImageGen" in html, "demo states its non-generation boundary", failures)
    check("prefers-reduced-motion" in css, "showcase honors reduced-motion preference", failures)
    check('id="generated-gallery"' in html and "同一主体，8 个分类实测" in html, "own generated samples are the primary showcase", failures)
    check("25 张上游原样例完整保留" in html and "非本研究生成" in html, "all upstream originals are directly presented and clearly sourced", failures)
    check("参考图驱动的图生图" in html and "保留合同" in html and "图像编辑" in html, "web explains the image-to-image consistency path", failures)
    check("确定性文字产品化" in html and "HTML / SVG / Canvas" in html and "成品质检" in html, "web explains deterministic typography productization", failures)

    generated_dir = showcase / "assets" / "generated"
    check(generated_dir.is_dir(), "generated sample asset directory exists", failures)
    for sample_name in GENERATED_SAMPLES:
        sample_path = generated_dir / sample_name
        valid_png = sample_path.is_file() and sample_path.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
        check(valid_png, f"generated sample is a valid PNG: {sample_name}", failures)

    for asset_name in asset_names:
        check(asset_name in js, f"showcase references {asset_name}", failures)

    for required in [
        PROJECT / "README.md",
        PROJECT / "docs" / "analysis.md",
        PROJECT / "docs" / "extension-roadmap.md",
        showcase / "DELIVERY.md",
    ]:
        check(required.is_file(), f"required artifact exists: {required.relative_to(PROJECT)}", failures)

    gitmodules = (REPO / ".gitmodules").read_text(encoding="utf-8")
    check("projects/muyang-illustration-skills/upstream" in gitmodules, "upstream is registered as a Git submodule", failures)

    root_readme = (REPO / "README.md").read_text(encoding="utf-8")
    site_index = (REPO / "site" / "index.html").read_text(encoding="utf-8")
    workflow = (REPO / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
    check("Muyang Illustration Skills 项目研究" in root_readme, "root research index includes the project", failures)
    check("Muyang Illustration Skills · 固定插画 Prompt 路由" in site_index, "Pages index includes the project card", failures)
    check("projects/muyang-illustration-skills/**" in workflow, "Pages workflow watches the project", failures)

    print(f"\nResults: {CHECK_COUNT} checks, {len(failures)} failure(s)")
    if failures:
        print("Failed checks:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
