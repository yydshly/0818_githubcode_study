#!/usr/bin/env python3
"""Behavior checks for every deterministic image-style preset."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "style_effects.py"
SPEC = importlib.util.spec_from_file_location("style_effects", SCRIPT)
assert SPEC and SPEC.loader
style_effects = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = style_effects
SPEC.loader.exec_module(style_effects)


def rgb_fixture() -> Image.Image:
    image = Image.new("RGB", (360, 260), "#e8d5ac")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 150, 360, 260), fill="#234b66")
    draw.ellipse((195, 42, 315, 162), fill="#cf5642")
    draw.polygon(((30, 170), (132, 48), (232, 170)), fill="#537b5a")
    return image


def alpha_fixture() -> Image.Image:
    image = Image.new("RGBA", (320, 260), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((42, 30, 278, 230), radius=38, fill="#315b78")
    draw.ellipse((112, 72, 238, 198), fill="#e7b65f")
    return image


class PresetTests(unittest.TestCase):
    def test_all_presets_return_transparent_rgba_canvas(self) -> None:
        for preset in style_effects.PRESETS:
            source = alpha_fixture() if preset == "sticker-outline" else rgb_fixture()
            with self.subTest(preset=preset):
                result = style_effects.render(source, preset, caption="FIELD TEST", seed=41)
                self.assertEqual(result.mode, "RGBA")
                self.assertEqual(result.getchannel("A").getextrema(), (0, 255))
                self.assertGreater(result.width, 360)
                self.assertGreater(result.height, 260)

    def test_torn_paper_seed_is_deterministic(self) -> None:
        first = style_effects.render(rgb_fixture(), "torn-paper", seed=73)
        second = style_effects.render(rgb_fixture(), "torn-paper", seed=73)
        different = style_effects.render(rgb_fixture(), "torn-paper", seed=74)
        self.assertEqual(first.tobytes(), second.tobytes())
        self.assertNotEqual(first.tobytes(), different.tobytes())

    def test_sticker_outline_expands_existing_alpha(self) -> None:
        source = alpha_fixture()
        result = style_effects.render(source, "sticker-outline")
        self.assertGreater(result.getbbox()[2] - result.getbbox()[0], source.getbbox()[2] - source.getbbox()[0])


if __name__ == "__main__":
    unittest.main()
