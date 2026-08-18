#!/usr/bin/env python3
"""Deterministic Pillow presets that extend the stamp-edge research project."""

from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps


PRESETS = ("polaroid", "torn-paper", "film-frame", "ticket", "riso-print", "sticker-outline")


def font(size: int, *, bold: bool = False, serif: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if serif:
        names = ["georgiab.ttf" if bold else "georgia.ttf", "timesbd.ttf" if bold else "times.ttf"]
    else:
        names = ["arialbd.ttf" if bold else "arial.ttf", "segoeui.ttf"]
    for name in names:
        candidate = Path("C:/Windows/Fonts") / name
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    try:
        fallback = "DejaVuSerif-Bold.ttf" if serif and bold else "DejaVuSerif.ttf" if serif else "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        return ImageFont.truetype(fallback, size)
    except OSError:
        return ImageFont.load_default()


def limit_size(image: Image.Image, max_edge: int = 1400) -> Image.Image:
    result = image.copy()
    result.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)
    return result


def with_shadow(foreground: Image.Image, *, pad: int = 72, offset: tuple[int, int] = (8, 14), blur: int = 18) -> Image.Image:
    foreground = foreground.convert("RGBA")
    canvas = Image.new("RGBA", (foreground.width + pad * 2, foreground.height + pad * 2), (0, 0, 0, 0))
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    alpha = foreground.getchannel("A").filter(ImageFilter.GaussianBlur(blur))
    shade = Image.new("RGBA", foreground.size, (16, 21, 28, 86))
    shadow.paste(shade, (pad + offset[0], pad + offset[1]), alpha)
    canvas.alpha_composite(shadow)
    canvas.alpha_composite(foreground, (pad, pad))
    return canvas


def polaroid(image: Image.Image, caption: str) -> Image.Image:
    image = limit_size(image.convert("RGB"), 1200)
    border = max(32, round(min(image.size) * 0.055))
    bottom = round(border * 2.35)
    paper = Image.new("RGBA", (image.width + border * 2, image.height + border + bottom), "#fffdf5")
    paper.paste(image, (border, border))
    draw = ImageDraw.Draw(paper)
    draw.rectangle((border, border, border + image.width - 1, border + image.height - 1), outline="#d9d2c5", width=2)
    label = (caption or "FIELD NOTE / 2026").upper()
    draw.text((border, border + image.height + round(bottom * 0.35)), label, font=font(max(18, border // 2), bold=True), fill="#26313c")
    return with_shadow(paper, pad=max(70, border * 2))


def torn_paper(image: Image.Image, seed: int) -> Image.Image:
    image = limit_size(image.convert("RGB"), 1200)
    margin = max(26, round(min(image.size) * 0.035))
    paper = Image.new("RGBA", (image.width + margin * 2, image.height + margin * 2), "#fffaf0")
    paper.paste(image, (margin, margin))
    width, height = paper.size
    step = max(14, min(width, height) // 55)
    jitter = max(7, step // 2)
    rng = random.Random(seed)
    points: list[tuple[int, int]] = []
    for x in range(0, width + step, step):
        points.append((min(x, width), rng.randint(1, jitter)))
    for y in range(step, height + step, step):
        points.append((width - rng.randint(1, jitter), min(y, height)))
    for x in range(width - step, -step, -step):
        points.append((max(x, 0), height - rng.randint(1, jitter)))
    for y in range(height - step, 0, -step):
        points.append((rng.randint(1, jitter), y))
    mask = Image.new("L", paper.size, 0)
    ImageDraw.Draw(mask).polygon(points, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(0.75))
    paper.putalpha(mask)
    return with_shadow(paper, pad=78, offset=(10, 16), blur=20)


def film_frame(image: Image.Image) -> Image.Image:
    image = limit_size(image.convert("RGB"), 1200)
    side = max(28, round(image.width * 0.028))
    rail = max(76, round(image.height * 0.09))
    frame = Image.new("RGBA", (image.width + side * 2, image.height + rail * 2), "#101113")
    frame.paste(image, (side, rail))
    mask = Image.new("L", frame.size, 255)
    draw_mask = ImageDraw.Draw(mask)
    pitch = max(48, frame.width // 20)
    hole_w = round(pitch * 0.48)
    hole_h = round(rail * 0.42)
    for x in range(round(pitch * 0.3), frame.width - hole_w, pitch):
        draw_mask.rounded_rectangle((x, round(rail * 0.2), x + hole_w, round(rail * 0.2) + hole_h), radius=5, fill=0)
        y = frame.height - round(rail * 0.2) - hole_h
        draw_mask.rounded_rectangle((x, y, x + hole_w, y + hole_h), radius=5, fill=0)
    frame.putalpha(mask)
    draw = ImageDraw.Draw(frame)
    draw.text((side + 8, 12), "FRAME 24", font=font(max(15, rail // 4), bold=True), fill="#e4b75b")
    draw.text((frame.width - side - 116, frame.height - rail + 18), "35 MM", font=font(max(14, rail // 5), bold=True), fill="#e4b75b")
    return with_shadow(frame, pad=72, offset=(8, 14), blur=17)


def ticket(image: Image.Image, caption: str) -> Image.Image:
    source = limit_size(image.convert("RGB"), 1400)
    width = 1240
    height = 620
    image_width = 790
    card = Image.new("RGBA", (width, height), "#f6ead0")
    card.paste(ImageOps.fit(source, (image_width, height), method=Image.Resampling.LANCZOS), (0, 0))
    draw = ImageDraw.Draw(card)
    draw.rectangle((image_width, 0, width, height), fill="#ead5ac")
    for y in range(22, height - 22, 28):
        draw.line((image_width + 36, y, image_width + 36, min(y + 14, height - 22)), fill="#9c7d57", width=3)
    draw.text((image_width + 76, 68), (caption or "FIELD PASS").upper(), font=font(34, bold=True, serif=True), fill="#192635")
    draw.text((image_width + 76, 128), "ADMIT ONE", font=font(17, bold=True), fill="#bf4f3e")
    draw.text((image_width + 76, 238), "ROUTE  /  024", font=font(22, bold=True), fill="#192635")
    draw.text((image_width + 76, 282), "DATE   /  18 AUG", font=font(22, bold=True), fill="#192635")
    draw.rectangle((image_width + 76, 382, width - 68, 496), outline="#192635", width=3)
    for x in range(image_width + 88, width - 80, 13):
        draw.line((x, 394, x, 482), fill="#192635", width=5 if x % 3 else 2)
    draw.text((image_width + 76, 526), "KEEP THIS STUB", font=font(15, bold=True), fill="#765b3c")
    mask = Image.new("L", card.size, 255)
    mask_draw = ImageDraw.Draw(mask)
    notch = 38
    mask_draw.ellipse((-notch, height // 2 - notch, notch, height // 2 + notch), fill=0)
    mask_draw.ellipse((width - notch, height // 2 - notch, width + notch, height // 2 + notch), fill=0)
    for x in range(40, width - 40, 64):
        mask_draw.ellipse((x - 10, -10, x + 10, 10), fill=0)
        mask_draw.ellipse((x - 10, height - 10, x + 10, height + 10), fill=0)
    card.putalpha(mask)
    return with_shadow(card, pad=72, offset=(9, 14), blur=18)


def riso_print(image: Image.Image, seed: int) -> Image.Image:
    image = limit_size(image.convert("RGB"), 1100)
    gray = ImageOps.grayscale(image)
    blue = ImageOps.colorize(gray, black="#163b72", white="#f1e2c3")
    edges = gray.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.GaussianBlur(0.7))
    edges = edges.point(lambda value: 210 if value > 38 else 0)
    red = Image.new("RGBA", image.size, "#d94f43")
    red.putalpha(edges)
    composite = blue.convert("RGBA")
    shifted = Image.new("RGBA", image.size, (0, 0, 0, 0))
    shifted.alpha_composite(red, (5, -3))
    composite.alpha_composite(shifted)
    draw = ImageDraw.Draw(composite, "RGBA")
    rng = random.Random(seed)
    step = max(9, min(image.size) // 105)
    pixels = gray.load()
    for y in range(step // 2, image.height, step):
        for x in range(step // 2, image.width, step):
            darkness = 255 - pixels[x, y]
            if darkness > 58:
                radius = 1 + round((darkness / 255) * step * 0.23)
                color = (18, 42, 93, rng.randint(42, 78))
                draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)
    border = max(32, min(image.size) // 24)
    paper = Image.new("RGBA", (image.width + border * 2, image.height + border * 2), "#f1e2c3")
    paper.alpha_composite(composite, (border, border))
    paper_draw = ImageDraw.Draw(paper)
    paper_draw.rectangle((border, border, border + image.width - 1, border + image.height - 1), outline="#c8ae83", width=2)
    paper_draw.text((border, paper.height - border + 7), "TWO-COLOR STUDY / RISO 03", font=font(max(14, border // 2), bold=True), fill="#163b72")
    return with_shadow(paper, pad=70, offset=(8, 13), blur=16)


def sticker_outline(image: Image.Image) -> Image.Image:
    content = limit_size(image.convert("RGBA"), 1200)
    alpha = content.getchannel("A")
    radius = max(13, min(45, round(min(content.size) * 0.035)))
    kernel = radius * 2 + 1
    outline_alpha = alpha.filter(ImageFilter.MaxFilter(kernel))
    outline = Image.new("RGBA", content.size, "white")
    outline.putalpha(outline_alpha)
    outlined = Image.new("RGBA", content.size, (0, 0, 0, 0))
    outlined.alpha_composite(outline)
    outlined.alpha_composite(content)
    return with_shadow(outlined, pad=88, offset=(10, 16), blur=19)


def render(image: Image.Image, preset: str, *, caption: str = "", seed: int = 24) -> Image.Image:
    if preset == "polaroid":
        return polaroid(image, caption)
    if preset == "torn-paper":
        return torn_paper(image, seed)
    if preset == "film-frame":
        return film_frame(image)
    if preset == "ticket":
        return ticket(image, caption)
    if preset == "riso-print":
        return riso_print(image, seed)
    if preset == "sticker-outline":
        return sticker_outline(image)
    raise ValueError(f"Unknown preset: {preset}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--preset", required=True, choices=PRESETS)
    parser.add_argument("--caption", default="")
    parser.add_argument("--seed", type=int, default=24)
    args = parser.parse_args()
    if not args.input.is_file():
        parser.error(f"input does not exist: {args.input}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result = render(Image.open(args.input), args.preset, caption=args.caption, seed=args.seed)
    result.save(args.output, "PNG")
    print(f"saved: {args.output.resolve()} {result.mode} {result.size} preset={args.preset}")


if __name__ == "__main__":
    main()
