#!/usr/bin/env python3
"""Generate six extension preset outputs and one mixed collection."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[3]
SKILL = Path(__file__).resolve().parents[1]
ENGINE = SKILL / "scripts" / "style_effects.py"
INPUTS = PROJECT / "showcase" / "assets" / "demo" / "inputs-v2"
BASE_OUTPUTS = PROJECT / "showcase" / "assets" / "demo" / "outputs-v2"
OUTPUTS = PROJECT / "showcase" / "assets" / "extensions"
UPSTREAM_SHEET = PROJECT / "upstream" / "stamp_sheet.py"


CASES = [
    ("polaroid", INPUTS / "travel-coast.jpg", "polaroid-travel.png", ["--caption", "COASTAL ROAD / 2026"]),
    ("torn-paper", INPUTS / "botanical-glasshouse.jpg", "torn-botanical.png", ["--seed", "31"]),
    ("film-frame", INPUTS / "architecture-rain.jpg", "film-architecture.png", []),
    ("ticket", INPUTS / "travel-coast.jpg", "ticket-coast.png", ["--caption", "COASTAL PASS"]),
    ("riso-print", INPUTS / "breakfast-table.jpg", "riso-breakfast.png", ["--seed", "17"]),
    ("sticker-outline", BASE_OUTPUTS / "architecture-rain-stamp.png", "sticker-architecture.png", []),
]


def run(*args: str | Path) -> None:
    subprocess.run([sys.executable, *(str(arg) for arg in args)], check=True)


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    generated: list[Path] = []
    for preset, source, filename, extra in CASES:
        output = OUTPUTS / filename
        run(ENGINE, source, output, "--preset", preset, *extra)
        generated.append(output)
    collection = OUTPUTS / "extension-collection-dark.png"
    run(
        UPSTREAM_SHEET,
        collection,
        "--cols",
        "3",
        "--bg",
        "#101925",
        "--colw",
        "400",
        "--",
        *generated,
    )
    manifest = {
        "engine": "extension/image-style-skill/scripts/style_effects.py",
        "presets": [case[0] for case in CASES],
        "outputs": [case[2] for case in CASES],
        "collection": collection.name,
    }
    (OUTPUTS / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Extension demo written to {OUTPUTS}")


if __name__ == "__main__":
    main()
