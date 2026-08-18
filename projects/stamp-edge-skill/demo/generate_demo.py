"""Build rich demo sources and run the unmodified upstream renderers.

Four photographic source assets are generated with the built-in ImageGen tool
and stored under ``showcase/assets/demo/sources``. This script normalizes those
assets, creates two deterministic editorial fixtures, then invokes the pinned
upstream scripts for every stamp and both collection sheets.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


PROJECT = Path(__file__).resolve().parents[1]
UPSTREAM = PROJECT / "upstream"
ASSETS = PROJECT / "showcase" / "assets" / "demo"
SOURCES = ASSETS / "sources"
INPUTS = ASSETS / "inputs-v2"
OUTPUTS = ASSETS / "outputs-v2"

AI_SOURCES = {
    "travel-coast": "travel-coast.png",
    "architecture-rain": "architecture-rain.png",
    "breakfast-table": "breakfast-table.png",
    "botanical-glasshouse": "botanical-glasshouse.png",
}


def font(size: int, *, bold: bool = False, serif: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if serif:
        names = ["georgiab.ttf" if bold else "georgia.ttf", "timesbd.ttf" if bold else "times.ttf"]
    else:
        names = ["arialbd.ttf" if bold else "arial.ttf", "seguisb.ttf" if bold else "segoeui.ttf"]
    for name in names:
        candidate = Path("C:/Windows/Fonts") / name
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    try:
        fallback = "DejaVuSerif-Bold.ttf" if serif and bold else "DejaVuSerif.ttf" if serif else "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        return ImageFont.truetype(fallback, size)
    except OSError:
        return ImageFont.load_default()


def fit(source: Image.Image, size: tuple[int, int]) -> Image.Image:
    return ImageOps.fit(source.convert("RGB"), size, method=Image.Resampling.LANCZOS)


def normalize_sources() -> dict[str, Path]:
    INPUTS.mkdir(parents=True, exist_ok=True)
    normalized: dict[str, Path] = {}
    for slug, filename in AI_SOURCES.items():
        source_path = SOURCES / filename
        if not source_path.is_file():
            raise FileNotFoundError(f"Missing ImageGen source: {source_path}")
        image = Image.open(source_path).convert("RGB")
        image.thumbnail((1400, 1400), Image.Resampling.LANCZOS)
        destination = INPUTS / f"{slug}.jpg"
        image.save(destination, "JPEG", quality=90, optimize=True, progressive=True)
        normalized[slug] = destination
    return normalized


def create_social_story(images: dict[str, Path], path: Path) -> None:
    canvas = Image.new("RGB", (1000, 1500), "#f8f5ef")
    draw = ImageDraw.Draw(canvas)
    ink = "#17212e"
    muted = "#69727d"
    red = "#c6523d"

    draw.ellipse((58, 48, 126, 116), fill=red)
    draw.text((146, 55), "ATLAS WEEKEND", font=font(25, bold=True), fill=ink)
    draw.text((146, 87), "FIELD DISPATCH / 024", font=font(14, bold=True), fill=muted)
    draw.rounded_rectangle((810, 54, 936, 102), radius=24, outline="#c8c2b8", width=2)
    draw.text((839, 69), "FOLLOW", font=font(13, bold=True), fill=ink)
    draw.line((58, 146, 942, 146), fill="#d6d0c6", width=2)

    draw.text((58, 188), "48 HOURS ON THE", font=font(22, bold=True), fill=red)
    draw.text((58, 224), "COASTAL ROAD", font=font(62, bold=True, serif=True), fill=ink)
    draw.multiline_text(
        (58, 306),
        "A field note about warm stone, blue distance,\nand the objects that make a place memorable.",
        font=font(22),
        fill=muted,
        spacing=8,
    )

    travel = fit(Image.open(images["travel-coast"]), (884, 520))
    canvas.paste(travel, (58, 410))
    draw.rectangle((58, 410, 942, 930), outline="#17212e", width=2)
    draw.rectangle((80, 870, 330, 915), fill="#f8f5ef")
    draw.text((97, 884), "STOP 01 / THE OVERLOOK", font=font(14, bold=True), fill=ink)

    food = fit(Image.open(images["breakfast-table"]), (426, 300))
    plants = fit(Image.open(images["botanical-glasshouse"]), (426, 300))
    canvas.paste(food, (58, 972))
    canvas.paste(plants, (516, 972))
    draw.text((58, 1292), "MORNING TABLE", font=font(15, bold=True), fill=ink)
    draw.text((516, 1292), "GREENHOUSE NOTES", font=font(15, bold=True), fill=ink)
    draw.line((58, 1345, 942, 1345), fill="#d6d0c6", width=2)
    draw.text((58, 1376), "SAVE  2.4K", font=font(15, bold=True), fill=ink)
    draw.text((242, 1376), "SHARE  318", font=font(15, bold=True), fill=ink)
    draw.text((765, 1376), "SUMMER / 2026", font=font(15, bold=True), fill=muted)
    canvas.save(path)


def create_field_notes(images: dict[str, Path], path: Path) -> None:
    canvas = Image.new("RGB", (900, 1200), "#eee3cf")
    draw = ImageDraw.Draw(canvas)
    ink = "#17212e"
    red = "#c6523d"
    draw.rectangle((44, 42, 856, 1158), outline=ink, width=3)
    draw.text((72, 68), "FIELD NOTES", font=font(22, bold=True), fill=red)
    draw.text((676, 71), "ISSUE NO. 03", font=font(15, bold=True), fill=ink)
    draw.line((72, 116, 828, 116), fill=ink, width=2)
    draw.multiline_text((68, 154), "THE CITY\nAFTER RAIN", font=font(72, bold=True, serif=True), fill=ink, spacing=-5)
    draw.text((70, 348), "CONCRETE / REFLECTION / WARM LIGHT", font=font(15, bold=True), fill=red)
    architecture = fit(Image.open(images["architecture-rain"]), (500, 650))
    canvas.paste(architecture, (328, 428))
    draw.rectangle((328, 428, 828, 1078), outline=ink, width=2)
    draw.rectangle((70, 454, 284, 724), fill="#23315f")
    draw.text((94, 483), "01", font=font(52, bold=True, serif=True), fill="#f2c96f")
    draw.multiline_text((94, 558), "SURFACE\nHOLDS\nMEMORY", font=font(25, bold=True), fill="white", spacing=10)
    draw.line((70, 760, 284, 760), fill=ink, width=2)
    draw.multiline_text((70, 792), "Soft weather reveals\nwhat hard geometry\nusually hides.", font=font(21, serif=True), fill=ink, spacing=8)
    draw.text((70, 1100), "ARCHITECTURE OBSERVATION SERIES", font=font(13, bold=True), fill=ink)
    canvas.save(path)


def run(*args: str | Path) -> None:
    subprocess.run([sys.executable, *(str(arg) for arg in args)], check=True)


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    images = normalize_sources()
    social = INPUTS / "social-travel-story.png"
    poster = INPUTS / "field-notes-poster.png"
    create_social_story(images, social)
    create_field_notes(images, poster)
    images["social-travel-story"] = social
    images["field-notes-poster"] = poster

    effect = UPSTREAM / "stamp_effect.py"
    sheet = UPSTREAM / "stamp_sheet.py"
    stamp_paths: list[Path] = []
    for slug, source in images.items():
        output = OUTPUTS / f"{slug}-stamp.png"
        run(effect, source, output)
        stamp_paths.append(output)

    run(effect, images["travel-coast"], OUTPUTS / "travel-coast-margin.png", "margin")
    run(effect, images["travel-coast"], OUTPUTS / "travel-coast-bg.png", "bg")
    run(effect, images["social-travel-story"], OUTPUTS / "social-travel-story-margin.png", "margin")

    run(
        sheet,
        OUTPUTS / "collection-dark-4col.png",
        "--cols",
        "4",
        "--bg",
        "#0e0e0e",
        "--colw",
        "340",
        "--",
        *stamp_paths,
    )
    run(
        sheet,
        OUTPUTS / "collection-paper-3col.png",
        "--cols",
        "3",
        "--bg",
        "#f5f2ea",
        "--colw",
        "390",
        "--",
        *stamp_paths,
    )

    manifest = {
        "upstream_commit": "2b89ce823aa589e912fcfbb9b529fa893142ab63",
        "sources": [
            {"slug": "travel-coast", "scene": "旅行风景", "origin": "OpenAI built-in ImageGen"},
            {"slug": "architecture-rain", "scene": "建筑观察", "origin": "OpenAI built-in ImageGen"},
            {"slug": "breakfast-table", "scene": "餐饮静物", "origin": "OpenAI built-in ImageGen"},
            {"slug": "botanical-glasshouse", "scene": "自然与研究", "origin": "OpenAI built-in ImageGen"},
            {"slug": "social-travel-story", "scene": "社交长帖", "origin": "Local deterministic composition"},
            {"slug": "field-notes-poster", "scene": "编辑海报", "origin": "Local deterministic composition"},
        ],
        "effects": ["default transparent", "margin transparent", "bg flattened"],
        "collections": ["4 columns / dark", "3 columns / paper"],
    }
    (ASSETS / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Rich demo assets written to {ASSETS}")


if __name__ == "__main__":
    main()
