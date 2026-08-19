#!/usr/bin/env python3
"""Render deterministic publication variants from exact copy and accepted Key Art."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from release_manifest import load_json as load_release_json, validate_approved_manifest  # noqa: E402
from release_security import append_audit_event, validate_signature, verify_audit_log  # noqa: E402


TEMPLATE_DIR = ROOT / "assets" / "templates"
SUPPORTED_TEMPLATES = {
    "campaign-poster": {"variants": {"poster-4x5", "header-16x9"}, "palette": {"forest", "paper", "paper_translucent", "gold", "white"}},
    "book-cover": {"variants": {"book-cover-3x4"}, "palette": {"ink", "paper", "panel_translucent", "accent", "muted", "white"}},
    "impact-report": {"variants": {"impact-report-a4"}, "palette": {"ink", "paper", "panel_translucent", "accent", "muted", "white"}},
    "field-journal": {"variants": {"field-journal-4x5"}, "palette": {"ink", "paper", "panel_translucent", "accent", "muted", "white"}},
}
FONT_CANDIDATES = (
    Path("C:/Windows/Fonts/msyh.ttc"),
    Path("C:/Windows/Fonts/msyhbd.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    Path("/System/Library/Fonts/PingFang.ttc"),
)
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
HEX_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?$")


@dataclass(frozen=True)
class FontBook:
    path: Path

    def regular(self, size: int) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(str(self.path), size=size)

    def bold(self, size: int) -> ImageFont.FreeTypeFont:
        bold_candidate = Path("C:/Windows/Fonts/msyhbd.ttc")
        path = bold_candidate if bold_candidate.is_file() else self.path
        return ImageFont.truetype(str(path), size=size)


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return payload


def require_exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    if missing or unexpected:
        details = []
        if missing:
            details.append(f"missing {missing}")
        if unexpected:
            details.append(f"unexpected {unexpected}")
        raise ValueError(f"{label} has invalid keys: {', '.join(details)}")


def require_text(value: Any, label: str, *, maximum: int = 80) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    if value != value.strip():
        raise ValueError(f"{label} must not have leading or trailing whitespace")
    if len(value) > maximum:
        raise ValueError(f"{label} exceeds {maximum} characters")
    if any(ord(character) < 32 for character in value):
        raise ValueError(f"{label} contains control characters")
    return value


def require_lines(value: Any, label: str, *, maximum_lines: int, maximum_line: int) -> list[str]:
    if not isinstance(value, list) or not 1 <= len(value) <= maximum_lines:
        raise ValueError(f"{label} must contain 1 to {maximum_lines} explicit lines")
    return [require_text(line, f"{label}[{index}]", maximum=maximum_line) for index, line in enumerate(value)]


def validate_copy(payload: dict[str, Any]) -> dict[str, Any]:
    template_id = payload.get("template")
    if template_id not in SUPPORTED_TEMPLATES:
        raise ValueError(f"template must be one of {sorted(SUPPORTED_TEMPLATES)}")
    shared = {"schema_version", "template", "campaign_id", "copy_status", "locale", "accessibility"}
    content_keys = {
        "campaign-poster": {"brand", "campaign"},
        "book-cover": {"publication"},
        "impact-report": {"organization", "report"},
        "field-journal": {"journal"},
    }[template_id]
    require_exact_keys(
        payload,
        shared | content_keys,
        "copy",
    )
    if payload["schema_version"] != "1.0":
        raise ValueError("schema_version must be 1.0")
    campaign_id = require_text(payload["campaign_id"], "campaign_id", maximum=64)
    if not ID_PATTERN.fullmatch(campaign_id):
        raise ValueError("campaign_id must be stable kebab-case")
    if payload["copy_status"] not in {"sample", "approved"}:
        raise ValueError("copy_status must be sample or approved")
    if payload["locale"] not in {"zh-CN", "en-US"}:
        raise ValueError("locale must be zh-CN or en-US")

    accessibility = payload["accessibility"]
    if not isinstance(accessibility, dict):
        raise ValueError("accessibility must be an object")
    require_exact_keys(accessibility, {"art_alt"}, "accessibility")
    require_text(accessibility["art_alt"], "accessibility.art_alt", maximum=240)

    if template_id == "campaign-poster":
        brand, campaign = payload["brand"], payload["campaign"]
        if not isinstance(brand, dict) or not isinstance(campaign, dict):
            raise ValueError("brand and campaign must be objects")
        require_exact_keys(brand, {"name", "qualifier"}, "brand")
        require_exact_keys(campaign, {"kicker", "headline_lines", "body_lines", "cta", "date", "location"}, "campaign")
        require_text(brand["name"], "brand.name", maximum=40)
        require_text(brand["qualifier"], "brand.qualifier", maximum=60)
        require_text(campaign["kicker"], "campaign.kicker", maximum=60)
        require_lines(campaign["headline_lines"], "campaign.headline_lines", maximum_lines=3, maximum_line=80)
        require_lines(campaign["body_lines"], "campaign.body_lines", maximum_lines=3, maximum_line=80)
        for key, maximum in (("cta", 40), ("date", 40), ("location", 60)):
            require_text(campaign[key], f"campaign.{key}", maximum=maximum)
    elif template_id == "book-cover":
        publication = payload["publication"]
        if not isinstance(publication, dict):
            raise ValueError("publication must be an object")
        require_exact_keys(publication, {"qualifier", "title_lines", "subtitle", "edition", "date", "footer"}, "publication")
        require_text(publication["qualifier"], "publication.qualifier", maximum=60)
        require_lines(publication["title_lines"], "publication.title_lines", maximum_lines=2, maximum_line=80)
        for key, maximum in (("subtitle", 80), ("edition", 50), ("date", 20), ("footer", 80)):
            require_text(publication[key], f"publication.{key}", maximum=maximum)
    elif template_id == "impact-report":
        organization, report = payload["organization"], payload["report"]
        if not isinstance(organization, dict) or not isinstance(report, dict):
            raise ValueError("organization and report must be objects")
        require_exact_keys(organization, {"name", "qualifier"}, "organization")
        require_exact_keys(report, {"kicker", "title_lines", "summary", "period", "metrics", "footer"}, "report")
        require_text(organization["name"], "organization.name", maximum=40)
        require_text(organization["qualifier"], "organization.qualifier", maximum=70)
        require_text(report["kicker"], "report.kicker", maximum=60)
        require_lines(report["title_lines"], "report.title_lines", maximum_lines=2, maximum_line=80)
        for key, maximum in (("summary", 100), ("period", 40), ("footer", 80)):
            require_text(report[key], f"report.{key}", maximum=maximum)
        if not isinstance(report["metrics"], list) or len(report["metrics"]) != 3:
            raise ValueError("report.metrics must contain exactly three items")
        for index, metric in enumerate(report["metrics"]):
            if not isinstance(metric, dict):
                raise ValueError(f"report.metrics[{index}] must be an object")
            require_exact_keys(metric, {"value", "label"}, f"report.metrics[{index}]")
            require_text(metric["value"], f"report.metrics[{index}].value", maximum=20)
            require_text(metric["label"], f"report.metrics[{index}].label", maximum=40)
    elif template_id == "field-journal":
        journal = payload["journal"]
        if not isinstance(journal, dict):
            raise ValueError("journal must be an object")
        require_exact_keys(journal, {"qualifier", "kicker", "title_lines", "subtitle", "coordinates", "distance", "year", "footer"}, "journal")
        require_text(journal["qualifier"], "journal.qualifier", maximum=70)
        require_text(journal["kicker"], "journal.kicker", maximum=60)
        require_lines(journal["title_lines"], "journal.title_lines", maximum_lines=1, maximum_line=80)
        for key, maximum in (("subtitle", 90), ("coordinates", 40), ("distance", 20), ("year", 20), ("footer", 70)):
            require_text(journal[key], f"journal.{key}", maximum=maximum)
    return payload


def validate_template(payload: dict[str, Any]) -> dict[str, Any]:
    require_exact_keys(payload, {"id", "version", "palette", "contrast_pairs", "variants"}, "template")
    template_id = payload["id"]
    if template_id not in SUPPORTED_TEMPLATES or payload["version"] != "1.0":
        raise ValueError("unsupported template id or version")
    palette = payload["palette"]
    variants = payload["variants"]
    contrast_pairs = payload["contrast_pairs"]
    if not isinstance(palette, dict) or not isinstance(variants, dict) or not isinstance(contrast_pairs, list):
        raise ValueError("template palette, contrast_pairs and variants have invalid types")
    require_exact_keys(palette, SUPPORTED_TEMPLATES[template_id]["palette"], "template.palette")
    for name, color in palette.items():
        if not isinstance(color, str) or not HEX_PATTERN.fullmatch(color):
            raise ValueError(f"template.palette.{name} must be a hex color")
    if set(variants) != SUPPORTED_TEMPLATES[template_id]["variants"]:
        raise ValueError(f"template {template_id} has an invalid variant set")
    if len(contrast_pairs) < 1:
        raise ValueError("template contrast_pairs must not be empty")
    for index, pair in enumerate(contrast_pairs):
        if not isinstance(pair, list) or len(pair) != 2 or any(key not in palette for key in pair):
            raise ValueError(f"template contrast_pairs[{index}] references an unknown color")
    for name, variant in variants.items():
        if not isinstance(variant, dict):
            raise ValueError(f"template variant {name} must be an object")
        require_exact_keys(variant, {"canvas", "layout", "art_box", "art_center", "copy_panel", "metadata_panel", "protected_regions"}, f"template.variants.{name}")
        canvas = variant["canvas"]
        if not isinstance(canvas, list) or len(canvas) != 2 or any(not isinstance(value, int) or value < 800 for value in canvas):
            raise ValueError(f"template.variants.{name}.canvas is invalid")
    return payload


def resolve_font(explicit: Path | None) -> Path:
    if explicit is not None:
        path = explicit.expanduser().resolve()
        if not path.is_file():
            raise ValueError(f"font file not found: {path}")
        return path
    for path in FONT_CANDIDATES:
        if path.is_file():
            return path.resolve()
    raise ValueError("no Chinese-capable font found; pass --font <font-file>")


def rgba(hex_color: str) -> tuple[int, int, int, int]:
    value = hex_color.removeprefix("#")
    if len(value) == 6:
        value += "FF"
    return tuple(int(value[index:index + 2], 16) for index in range(0, 8, 2))  # type: ignore[return-value]


def rgb(hex_color: str) -> tuple[int, int, int]:
    return rgba(hex_color)[:3]


def relative_box(box: list[float], width: int, height: int) -> tuple[int, int, int, int]:
    if len(box) != 4 or any(not isinstance(item, (int, float)) for item in box):
        raise ValueError(f"invalid relative box: {box}")
    x1, y1, x2, y2 = box
    if not (0 <= x1 < x2 <= 1 and 0 <= y1 < y2 <= 1):
        raise ValueError(f"relative box must be inside canvas: {box}")
    return (round(x1 * width), round(y1 * height), round(x2 * width), round(y2 * height))


def place_art(canvas: Image.Image, art: Image.Image, box: tuple[int, int, int, int], centering: list[float]) -> None:
    x1, y1, x2, y2 = box
    fitted = ImageOps.fit(
        art.convert("RGB"),
        (x2 - x1, y2 - y1),
        method=Image.Resampling.LANCZOS,
        centering=(float(centering[0]), float(centering[1])),
    )
    canvas.paste(fitted, (x1, y1))


def contains(container: tuple[int, int, int, int], item: tuple[int, int, int, int], tolerance: int = 1) -> bool:
    return (
        item[0] >= container[0] - tolerance
        and item[1] >= container[1] - tolerance
        and item[2] <= container[2] + tolerance
        and item[3] <= container[3] + tolerance
    )


def intersects(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> bool:
    return max(a[0], b[0]) < min(a[2], b[2]) and max(a[1], b[1]) < min(a[3], b[3])


def luminance(color: tuple[int, int, int]) -> float:
    channels = []
    for value in color:
        normalized = value / 255
        channels.append(normalized / 12.92 if normalized <= 0.04045 else ((normalized + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast_ratio(foreground: tuple[int, int, int], background: tuple[int, int, int]) -> float:
    high, low = sorted((luminance(foreground), luminance(background)), reverse=True)
    return (high + 0.05) / (low + 0.05)


class RenderRecorder:
    def __init__(self, draw: ImageDraw.ImageDraw) -> None:
        self.draw = draw
        self.items: list[dict[str, Any]] = []

    def text(
        self,
        field: str,
        value: str,
        xy: tuple[int, int],
        font: ImageFont.FreeTypeFont,
        fill: tuple[int, int, int] | tuple[int, int, int, int],
        container: tuple[int, int, int, int],
        *,
        anchor: str = "lt",
        source_copy: bool = True,
    ) -> tuple[int, int, int, int]:
        bbox = tuple(int(value) for value in self.draw.textbbox(xy, value, font=font, anchor=anchor))
        self.draw.text(xy, value, font=font, fill=fill, anchor=anchor)
        self.items.append(
            {
                "field": field,
                "value": value,
                "bbox": list(bbox),
                "container": list(container),
                "inside_container": contains(container, bbox),
                "source_copy": source_copy,
            }
        )
        return bbox


def draw_button(
    recorder: RenderRecorder,
    field: str,
    value: str,
    box: tuple[int, int, int, int],
    font: ImageFont.FreeTypeFont,
    background: tuple[int, int, int],
    foreground: tuple[int, int, int],
) -> None:
    recorder.draw.rounded_rectangle(box, radius=8, fill=background)
    x = (box[0] + box[2]) // 2
    y = (box[1] + box[3]) // 2
    recorder.text(field, value, (x, y), font, foreground, box, anchor="mm")


def render_poster(
    art: Image.Image,
    copy: dict[str, Any],
    variant: dict[str, Any],
    palette: dict[str, str],
    fonts: FontBook,
) -> tuple[Image.Image, list[dict[str, Any]], list[tuple[int, int, int, int]]]:
    width, height = (int(value) for value in variant["canvas"])
    canvas = Image.new("RGB", (width, height), rgb(palette["paper"]))
    art_box = relative_box(variant["art_box"], width, height)
    place_art(canvas, art, art_box, variant["art_center"])
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    copy_panel = relative_box(variant["copy_panel"], width, height)
    metadata_panel = relative_box(variant["metadata_panel"], width, height)
    overlay_draw.rounded_rectangle(copy_panel, radius=18, fill=rgba(palette["paper_translucent"]))
    overlay_draw.rectangle(metadata_panel, fill=rgba(palette["forest"]))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    recorder = RenderRecorder(ImageDraw.Draw(canvas))
    forest, white = rgb(palette["forest"]), rgb(palette["white"])
    brand, campaign = copy["brand"], copy["campaign"]
    px1, py1, px2, py2 = copy_panel
    pad = 34
    text_container = (px1 + pad, py1 + 24, px2 - pad, py2 - 24)
    y = py1 + 30
    recorder.text("brand.qualifier", brand["qualifier"], (px1 + pad, y), fonts.bold(20), forest, text_container)
    y += 38
    recorder.text("brand.name", brand["name"], (px1 + pad, y), fonts.bold(42), forest, text_container)
    y += 78
    recorder.text("campaign.kicker", campaign["kicker"], (px1 + pad, y), fonts.bold(22), forest, text_container)
    y += 48
    for index, line in enumerate(campaign["headline_lines"]):
        recorder.text(f"campaign.headline_lines[{index}]", line, (px1 + pad, y), fonts.bold(104), forest, text_container)
        y += 108
    y += 18
    for index, line in enumerate(campaign["body_lines"]):
        recorder.text(f"campaign.body_lines[{index}]", line, (px1 + pad, y), fonts.regular(34), forest, text_container)
        y += 48
    button_box = (px1 + pad, min(y + 18, py2 - 118), px1 + pad + 252, min(y + 18, py2 - 118) + 64)
    draw_button(recorder, "campaign.cta", campaign["cta"], button_box, fonts.bold(24), forest, white)
    if copy["copy_status"] == "sample":
        recorder.text(
            "generated.sample_disclosure",
            "SAMPLE / 非商业发布",
            (px2 - pad, py2 - 28),
            fonts.bold(18),
            forest,
            text_container,
            anchor="rb",
            source_copy=False,
        )
    mx1, my1, mx2, my2 = metadata_panel
    meta_container = (mx1 + 48, my1 + 20, mx2 - 48, my2 - 20)
    recorder.text("campaign.date", campaign["date"], (mx1 + 48, (my1 + my2) // 2), fonts.bold(24), white, meta_container, anchor="lm")
    recorder.text("campaign.location", campaign["location"], (mx2 - 48, (my1 + my2) // 2), fonts.bold(20), white, meta_container, anchor="rm")
    protected = [relative_box(box, width, height) for box in variant["protected_regions"]]
    return canvas, recorder.items, protected


def render_header(
    art: Image.Image,
    copy: dict[str, Any],
    variant: dict[str, Any],
    palette: dict[str, str],
    fonts: FontBook,
) -> tuple[Image.Image, list[dict[str, Any]], list[tuple[int, int, int, int]]]:
    width, height = (int(value) for value in variant["canvas"])
    canvas = Image.new("RGB", (width, height), rgb(palette["paper"]))
    art_box = relative_box(variant["art_box"], width, height)
    copy_panel = relative_box(variant["copy_panel"], width, height)
    place_art(canvas, art, art_box, variant["art_center"])
    draw = ImageDraw.Draw(canvas)
    draw.rectangle(copy_panel, fill=rgb(palette["paper"]))
    draw.rectangle((art_box[2] - 8, 0, art_box[2] + 8, height), fill=rgb(palette["gold"]))
    recorder = RenderRecorder(draw)
    forest, white = rgb(palette["forest"]), rgb(palette["white"])
    brand, campaign = copy["brand"], copy["campaign"]
    px1, py1, px2, py2 = copy_panel
    left, right = px1 + 72, px2 - 72
    text_container = (left, 58, right, height - 58)
    recorder.text("brand.qualifier", brand["qualifier"], (left, 62), fonts.bold(20), forest, text_container)
    recorder.text("brand.name", brand["name"], (left, 105), fonts.bold(44), forest, text_container)
    recorder.text("campaign.kicker", campaign["kicker"], (left, 210), fonts.bold(22), forest, text_container)
    y = 265
    for index, line in enumerate(campaign["headline_lines"]):
        recorder.text(f"campaign.headline_lines[{index}]", line, (left, y), fonts.bold(92), forest, text_container)
        y += 98
    y += 24
    for index, line in enumerate(campaign["body_lines"]):
        recorder.text(f"campaign.body_lines[{index}]", line, (left, y), fonts.regular(34), forest, text_container)
        y += 48
    button_box = (left, min(y + 28, 710), left + 268, min(y + 28, 710) + 68)
    draw_button(recorder, "campaign.cta", campaign["cta"], button_box, fonts.bold(24), forest, white)
    metadata_panel = relative_box(variant["metadata_panel"], width, height)
    recorder.text("campaign.date", campaign["date"], (metadata_panel[0], metadata_panel[1]), fonts.bold(23), forest, metadata_panel)
    recorder.text("campaign.location", campaign["location"], (metadata_panel[2], metadata_panel[3]), fonts.bold(18), forest, metadata_panel, anchor="rb")
    if copy["copy_status"] == "sample":
        recorder.text(
            "generated.sample_disclosure",
            "SAMPLE / 非商业发布",
            (right, 62),
            fonts.bold(18),
            forest,
            text_container,
            anchor="rt",
            source_copy=False,
        )
    protected = [relative_box(box, width, height) for box in variant["protected_regions"]]
    return canvas, recorder.items, protected


def render_book_cover(
    art: Image.Image,
    copy: dict[str, Any],
    variant: dict[str, Any],
    palette: dict[str, str],
    fonts: FontBook,
) -> tuple[Image.Image, list[dict[str, Any]], list[tuple[int, int, int, int]]]:
    width, height = (int(value) for value in variant["canvas"])
    canvas = Image.new("RGB", (width, height), rgb(palette["paper"]))
    art_box = relative_box(variant["art_box"], width, height)
    copy_panel = relative_box(variant["copy_panel"], width, height)
    metadata_panel = relative_box(variant["metadata_panel"], width, height)
    place_art(canvas, art, art_box, variant["art_center"])
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle(copy_panel, radius=20, fill=rgba(palette["panel_translucent"]))
    overlay_draw.rectangle(metadata_panel, fill=rgba(palette["ink"]))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    recorder = RenderRecorder(ImageDraw.Draw(canvas))
    publication = copy["publication"]
    ink, white = rgb(palette["ink"]), rgb(palette["white"])
    px1, py1, px2, py2 = copy_panel
    container = (px1 + 34, py1 + 20, px2 - 34, py2 - 20)
    recorder.text("publication.qualifier", publication["qualifier"], (container[0], py1 + 24), fonts.bold(20), ink, container)
    recorder.text("publication.edition", publication["edition"], (container[2], py1 + 24), fonts.bold(18), ink, container, anchor="rt")
    y = py1 + 62
    for index, line in enumerate(publication["title_lines"]):
        recorder.text(f"publication.title_lines[{index}]", line, (container[0], y), fonts.bold(68), ink, container)
        y += 72
    recorder.text("publication.subtitle", publication["subtitle"], (container[0], py2 - 28), fonts.regular(24), ink, container, anchor="lb")
    if copy["copy_status"] == "sample":
        recorder.text("generated.sample_disclosure", "SAMPLE / 非商业发布", (container[2], py2 - 28), fonts.bold(17), ink, container, anchor="rb", source_copy=False)
    mx1, my1, mx2, my2 = metadata_panel
    meta = (mx1 + 48, my1 + 18, mx2 - 48, my2 - 18)
    recorder.text("publication.date", publication["date"], (meta[0], (my1 + my2) // 2), fonts.bold(26), white, meta, anchor="lm")
    recorder.text("publication.footer", publication["footer"], (meta[2], (my1 + my2) // 2), fonts.bold(19), white, meta, anchor="rm")
    protected = [relative_box(box, width, height) for box in variant["protected_regions"]]
    return canvas, recorder.items, protected


def render_impact_report(
    art: Image.Image,
    copy: dict[str, Any],
    variant: dict[str, Any],
    palette: dict[str, str],
    fonts: FontBook,
) -> tuple[Image.Image, list[dict[str, Any]], list[tuple[int, int, int, int]]]:
    width, height = (int(value) for value in variant["canvas"])
    canvas = Image.new("RGB", (width, height), rgb(palette["paper"]))
    art_box = relative_box(variant["art_box"], width, height)
    copy_panel = relative_box(variant["copy_panel"], width, height)
    metadata_panel = relative_box(variant["metadata_panel"], width, height)
    place_art(canvas, art, art_box, variant["art_center"])
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle(metadata_panel, fill=rgba(palette["ink"]))
    overlay_draw.rounded_rectangle(copy_panel, radius=18, fill=rgba(palette["panel_translucent"]))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    recorder = RenderRecorder(ImageDraw.Draw(canvas))
    organization, report = copy["organization"], copy["report"]
    ink, white, accent = rgb(palette["ink"]), rgb(palette["white"]), rgb(palette["accent"])
    mx1, my1, mx2, my2 = metadata_panel
    meta = (mx1 + 48, my1 + 18, mx2 - 48, my2 - 18)
    recorder.text("organization.name", organization["name"], (meta[0], (my1 + my2) // 2), fonts.bold(28), white, meta, anchor="lm")
    recorder.text("organization.qualifier", organization["qualifier"], (meta[2], (my1 + my2) // 2), fonts.bold(18), white, meta, anchor="rm")
    px1, py1, px2, py2 = copy_panel
    container = (px1 + 34, py1 + 24, px2 - 34, py2 - 24)
    recorder.text("report.kicker", report["kicker"], (container[0], py1 + 24), fonts.bold(18), ink, container)
    recorder.text("report.period", report["period"], (container[2], py1 + 24), fonts.bold(18), ink, container, anchor="rt")
    y = py1 + 64
    for index, line in enumerate(report["title_lines"]):
        recorder.text(f"report.title_lines[{index}]", line, (container[0], y), fonts.bold(58), ink, container)
        y += 62
    recorder.text("report.summary", report["summary"], (container[0], py1 + 194), fonts.regular(23), ink, container)
    metrics_top = py1 + 252
    available = container[2] - container[0]
    metric_width = available // 3
    for index, metric in enumerate(report["metrics"]):
        left = container[0] + metric_width * index
        right = container[0] + metric_width * (index + 1) - 18
        metric_container = (left, metrics_top, right, py2 - 54)
        recorder.draw.line((left, metrics_top, right, metrics_top), fill=accent, width=3)
        recorder.text(f"report.metrics[{index}].value", metric["value"], (left, metrics_top + 14), fonts.bold(42), ink, metric_container)
        recorder.text(f"report.metrics[{index}].label", metric["label"], (left, metrics_top + 68), fonts.regular(18), ink, metric_container)
    recorder.text("report.footer", report["footer"], (container[0], py2 - 26), fonts.bold(17), ink, container, anchor="lb")
    if copy["copy_status"] == "sample":
        recorder.text("generated.sample_disclosure", "SAMPLE / 非商业发布", (container[2], py2 - 26), fonts.bold(17), ink, container, anchor="rb", source_copy=False)
    protected = [relative_box(box, width, height) for box in variant["protected_regions"]]
    return canvas, recorder.items, protected


def render_field_journal(
    art: Image.Image,
    copy: dict[str, Any],
    variant: dict[str, Any],
    palette: dict[str, str],
    fonts: FontBook,
) -> tuple[Image.Image, list[dict[str, Any]], list[tuple[int, int, int, int]]]:
    width, height = (int(value) for value in variant["canvas"])
    canvas = Image.new("RGB", (width, height), rgb(palette["paper"]))
    art_box = relative_box(variant["art_box"], width, height)
    copy_panel = relative_box(variant["copy_panel"], width, height)
    metadata_panel = relative_box(variant["metadata_panel"], width, height)
    place_art(canvas, art, art_box, variant["art_center"])
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle(copy_panel, radius=14, fill=rgba(palette["panel_translucent"]))
    overlay_draw.rounded_rectangle(metadata_panel, radius=14, fill=rgba(palette["ink"]))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    recorder = RenderRecorder(ImageDraw.Draw(canvas))
    journal = copy["journal"]
    ink, white = rgb(palette["ink"]), rgb(palette["white"])
    px1, py1, px2, py2 = copy_panel
    container = (px1 + 28, py1 + 16, px2 - 28, py2 - 16)
    recorder.text("journal.qualifier", journal["qualifier"], (container[0], py1 + 17), fonts.bold(17), ink, container)
    recorder.text("journal.kicker", journal["kicker"], (container[2], py1 + 17), fonts.bold(17), ink, container, anchor="rt")
    recorder.text("journal.title_lines[0]", journal["title_lines"][0], (container[0], py1 + 50), fonts.bold(58), ink, container)
    recorder.text("journal.subtitle", journal["subtitle"], (container[0], py2 - 18), fonts.regular(21), ink, container, anchor="lb")
    mx1, my1, mx2, my2 = metadata_panel
    meta = (mx1 + 30, my1 + 18, mx2 - 30, my2 - 18)
    recorder.text("journal.coordinates", journal["coordinates"], (meta[0], my1 + 22), fonts.bold(21), white, meta)
    recorder.text("journal.distance", journal["distance"], ((mx1 + mx2) // 2, my1 + 22), fonts.bold(21), white, meta, anchor="mt")
    recorder.text("journal.year", journal["year"], (meta[2], my1 + 22), fonts.bold(21), white, meta, anchor="rt")
    recorder.text("journal.footer", journal["footer"], (meta[0], my2 - 22), fonts.bold(16), white, meta, anchor="lb")
    if copy["copy_status"] == "sample":
        recorder.text("generated.sample_disclosure", "SAMPLE / 非商业发布", (meta[2], my2 - 22), fonts.bold(16), white, meta, anchor="rb", source_copy=False)
    protected = [relative_box(box, width, height) for box in variant["protected_regions"]]
    return canvas, recorder.items, protected


def expected_copy_fields(copy: dict[str, Any]) -> dict[str, str]:
    template_id = copy["template"]
    fields: dict[str, str] = {}
    if template_id == "campaign-poster":
        fields.update(
            {
                "brand.qualifier": copy["brand"]["qualifier"],
                "brand.name": copy["brand"]["name"],
                "campaign.kicker": copy["campaign"]["kicker"],
                "campaign.cta": copy["campaign"]["cta"],
                "campaign.date": copy["campaign"]["date"],
                "campaign.location": copy["campaign"]["location"],
            }
        )
        for index, value in enumerate(copy["campaign"]["headline_lines"]):
            fields[f"campaign.headline_lines[{index}]"] = value
        for index, value in enumerate(copy["campaign"]["body_lines"]):
            fields[f"campaign.body_lines[{index}]"] = value
    elif template_id == "book-cover":
        publication = copy["publication"]
        for key in ("qualifier", "subtitle", "edition", "date", "footer"):
            fields[f"publication.{key}"] = publication[key]
        for index, value in enumerate(publication["title_lines"]):
            fields[f"publication.title_lines[{index}]"] = value
    elif template_id == "impact-report":
        organization, report = copy["organization"], copy["report"]
        fields.update({"organization.name": organization["name"], "organization.qualifier": organization["qualifier"]})
        for key in ("kicker", "summary", "period", "footer"):
            fields[f"report.{key}"] = report[key]
        for index, value in enumerate(report["title_lines"]):
            fields[f"report.title_lines[{index}]"] = value
        for index, metric in enumerate(report["metrics"]):
            fields[f"report.metrics[{index}].value"] = metric["value"]
            fields[f"report.metrics[{index}].label"] = metric["label"]
    elif template_id == "field-journal":
        journal = copy["journal"]
        for key in ("qualifier", "kicker", "subtitle", "coordinates", "distance", "year", "footer"):
            fields[f"journal.{key}"] = journal[key]
        for index, value in enumerate(journal["title_lines"]):
            fields[f"journal.title_lines[{index}]"] = value
    return fields


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_variant(
    name: str,
    image: Image.Image,
    items: list[dict[str, Any]],
    protected_regions: list[tuple[int, int, int, int]],
    copy: dict[str, Any],
    variant: dict[str, Any],
    template: dict[str, Any],
) -> list[dict[str, Any]]:
    expected = expected_copy_fields(copy)
    actual = {item["field"]: item["value"] for item in items if item["source_copy"]}
    overflow = [item["field"] for item in items if not item["inside_container"]]
    collisions = []
    for item in items:
        item_box = tuple(item["bbox"])
        if any(intersects(item_box, protected) for protected in protected_regions):
            collisions.append(item["field"])
    palette = template["palette"]
    contrast_evidence = {}
    for foreground, background in template["contrast_pairs"]:
        contrast_evidence[f"{foreground}_on_{background}"] = round(contrast_ratio(rgb(palette[foreground]), rgb(palette[background])), 2)
    expected_dimensions = tuple(int(value) for value in variant["canvas"])
    return [
        {
            "id": "dimensions",
            "status": "PASS" if image.size == expected_dimensions else "FAIL",
            "evidence": {"actual": list(image.size), "expected": list(expected_dimensions)},
        },
        {
            "id": "exact-copy",
            "status": "PASS" if actual == expected else "FAIL",
            "evidence": {"expected": expected, "rendered": actual},
        },
        {
            "id": "overflow",
            "status": "PASS" if not overflow else "FAIL",
            "evidence": {"overflow_fields": overflow},
        },
        {
            "id": "protected-region",
            "status": "PASS" if not collisions else "FAIL",
            "evidence": {"colliding_fields": collisions, "protected_regions": [list(box) for box in protected_regions]},
        },
        {
            "id": "contrast",
            "status": "PASS" if all(value >= 4.5 for value in contrast_evidence.values()) else "FAIL",
            "evidence": {**contrast_evidence, "minimum": 4.5},
        },
        {
            "id": "sample-disclosure",
            "status": "PASS" if copy["copy_status"] != "sample" or any(item["field"] == "generated.sample_disclosure" for item in items) else "FAIL",
            "evidence": {"copy_status": copy["copy_status"]},
        },
    ]


def render(
    copy_path: Path,
    art_path: Path,
    out_dir: Path,
    template_path: Path | None,
    font_path: Path | None,
    release_manifest_path: Path | None = None,
    release_signature_path: Path | None = None,
    trusted_keys_path: Path | None = None,
    audit_log_path: Path | None = None,
) -> dict[str, Any]:
    copy = validate_copy(load_json(copy_path))
    resolved_template_path = template_path or (TEMPLATE_DIR / f"{copy['template']}.json")
    template = validate_template(load_json(resolved_template_path))
    if template["id"] != copy["template"]:
        raise ValueError(f"copy requests {copy['template']} but template file is {template['id']}")
    release_summary: dict[str, Any]
    if copy["copy_status"] == "approved":
        if release_manifest_path is None:
            raise ValueError("approved copy requires --release-manifest")
        if release_signature_path is None or trusted_keys_path is None:
            raise ValueError("approved copy requires --release-signature and --trusted-keys")
        if audit_log_path is None:
            raise ValueError("approved copy requires --audit-log")
        release_payload = load_release_json(release_manifest_path)
        release_summary = validate_approved_manifest(
            release_payload,
            manifest_path=release_manifest_path,
            copy_payload=copy,
            copy_path=copy_path,
            art_path=art_path,
        )
        signature_summary = validate_signature(
            release_manifest_path,
            release_signature_path,
            trusted_keys_path,
            release_payload,
        )
        verify_audit_log(audit_log_path)
    else:
        if any(path is not None for path in (release_manifest_path, release_signature_path, trusted_keys_path, audit_log_path)):
            raise ValueError("sample copy must not receive release security inputs")
        release_summary = {"required": False, "status": "NOT_REQUIRED"}
        signature_summary = {"required": False, "status": "NOT_REQUIRED"}
    resolved_font = resolve_font(font_path)
    fonts = FontBook(resolved_font)
    try:
        with Image.open(art_path) as opened:
            art = ImageOps.exif_transpose(opened).convert("RGB")
    except OSError as exc:
        raise ValueError(f"cannot read Key Art {art_path}: {exc}") from exc

    if art.width < 800 or art.height < 800:
        raise ValueError("Key Art must be at least 800 × 800 pixels")
    out_dir.mkdir(parents=True, exist_ok=True)
    if release_manifest_path is not None:
        (out_dir / "release-manifest.json").write_bytes(release_manifest_path.read_bytes())
        (out_dir / "release-signature.json").write_bytes(release_signature_path.read_bytes())
        (out_dir / "trusted-release-keys.json").write_bytes(trusted_keys_path.read_bytes())
    outputs: dict[str, Any] = {}
    all_checks: list[dict[str, Any]] = []
    for variant_name, variant in template["variants"].items():
        if variant["layout"] == "poster":
            image, items, protected = render_poster(art, copy, variant, template["palette"], fonts)
        elif variant["layout"] == "header":
            image, items, protected = render_header(art, copy, variant, template["palette"], fonts)
        elif variant["layout"] == "book-cover":
            image, items, protected = render_book_cover(art, copy, variant, template["palette"], fonts)
        elif variant["layout"] == "impact-report":
            image, items, protected = render_impact_report(art, copy, variant, template["palette"], fonts)
        elif variant["layout"] == "field-journal":
            image, items, protected = render_field_journal(art, copy, variant, template["palette"], fonts)
        else:
            raise ValueError(f"unsupported layout: {variant['layout']}")
        output_path = out_dir / f"{copy['campaign_id']}-{variant_name}.png"
        image.save(output_path, format="PNG", optimize=True)
        checks = inspect_variant(variant_name, image, items, protected, copy, variant, template)
        all_checks.extend({"variant": variant_name, **check} for check in checks)
        outputs[variant_name] = {
            "path": output_path.name,
            "width": image.width,
            "height": image.height,
            "sha256": file_sha256(output_path),
            "text_items": items,
        }

    status = "PASS" if all(check["status"] == "PASS" for check in all_checks) else "FAIL"
    if copy["copy_status"] == "approved" and status == "PASS":
        audit_event = append_audit_event(audit_log_path, release_summary, signature_summary, outputs)
        (out_dir / "release-audit.jsonl").write_bytes(audit_log_path.read_bytes())
        (out_dir / "audit-event.json").write_text(json.dumps(audit_event, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        audit_summary: dict[str, Any] = {
            "required": True,
            "status": "PASS",
            "sequence": audit_event["sequence"],
            "event_hash": audit_event["event_hash"],
            "previous_event_hash": audit_event["previous_event_hash"],
            "audit_log_sha256": file_sha256(audit_log_path),
        }
    elif copy["copy_status"] == "approved":
        audit_summary = {"required": True, "status": "NOT_APPENDED", "reason": "layout gates failed"}
    else:
        audit_summary = {"required": False, "status": "NOT_REQUIRED"}
    report = {
        "schema_version": "1.0",
        "status": status,
        "template": {"id": template["id"], "version": template["version"]},
        "campaign_id": copy["campaign_id"],
        "copy_status": copy["copy_status"],
        "locale": copy["locale"],
        "inputs": {
            "copy": str(copy_path.resolve()),
            "art": str(art_path.resolve()),
            "art_sha256": file_sha256(art_path),
            "font": str(resolved_font),
            "template": str(resolved_template_path.resolve()),
            "release_manifest": str(release_manifest_path.resolve()) if release_manifest_path is not None else None,
            "release_signature": str(release_signature_path.resolve()) if release_signature_path is not None else None,
            "trusted_keys": str(trusted_keys_path.resolve()) if trusted_keys_path is not None else None,
            "audit_log": str(audit_log_path.resolve()) if audit_log_path is not None else None,
        },
        "release": release_summary,
        "signature": signature_summary,
        "audit": audit_summary,
        "checks": all_checks,
        "outputs": outputs,
        "boundary": "PASS covers deterministic layout gates only; brand, factual, legal, font-license and publication approval remain external.",
    }
    report_path = out_dir / "render-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--copy", required=True, type=Path, help="UTF-8 copy JSON following references/copy-schema.md")
    parser.add_argument("--art", required=True, type=Path, help="Accepted wordless Key Art raster")
    parser.add_argument("--out-dir", required=True, type=Path, help="Output directory for PNG variants and report")
    parser.add_argument("--template", type=Path, help="Optional template JSON override; defaults to assets/templates/<copy.template>.json")
    parser.add_argument("--font", type=Path, help="Optional production font file")
    parser.add_argument("--release-manifest", type=Path, help="Required for copy_status=approved; forbidden for sample copy")
    parser.add_argument("--release-signature", type=Path, help="Detached Ed25519 signature required for approved copy")
    parser.add_argument("--trusted-keys", type=Path, help="Trusted public-key store required for approved copy")
    parser.add_argument("--audit-log", type=Path, help="Hash-chained JSONL audit log required for approved copy")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        report = render(
            args.copy,
            args.art,
            args.out_dir,
            args.template,
            args.font,
            args.release_manifest,
            args.release_signature,
            args.trusted_keys,
            args.audit_log,
        )
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"status": report["status"], "outputs": report["outputs"]}, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
