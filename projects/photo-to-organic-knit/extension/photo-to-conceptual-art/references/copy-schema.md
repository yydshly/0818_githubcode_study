# Deterministic Copy Schema

Read this reference only when an accepted Key Art must become a supported publication asset. The generated image remains an art layer; every exact character comes from a UTF-8 JSON file and is drawn by the renderer.

## Shared envelope

```json
{
  "schema_version": "1.0",
  "template": "campaign-poster | book-cover | impact-report | field-journal",
  "campaign_id": "stable-kebab-case-id",
  "copy_status": "sample",
  "locale": "zh-CN",
  "<template-content>": {},
  "accessibility": {
    "art_alt": "绿色茶罐、茶壶和两只茶杯组成的分层剪纸无字主视觉"
  }
}
```

The content object is strict and template-specific:

| Template | Content objects | Primary master | Maintained example |
| --- | --- | --- | --- |
| `campaign-poster` | `brand`, `campaign` | 4:5 poster + 16:9 header | `examples/chinese-tea-copy.json`, `examples/honey-campaign-copy.json`, `examples/honey-campaign-approved-demo.json` |
| `book-cover` | `publication` | 1200×1600 cover | `examples/family-memory-copy.json` |
| `impact-report` | `organization`, `report` | 1240×1754 A4-style cover | `examples/community-impact-copy.json` |
| `field-journal` | `journal` | 1200×1500 journal cover | `examples/lighthouse-journal-copy.json` |

Read the matching example before authoring copy. Keys are contracts, not suggestions; do not copy fields from one template into another.

## Invariants

- `template` must be one of the four maintained IDs. Unknown templates and mismatched content objects fail closed.
- `copy_status` is `sample` or `approved`. `sample` forces a visible `SAMPLE / 非商业发布` mark. `approved` means the caller supplied approved copy; the script does not verify legal or brand approval.
- Every `title_lines`, `headline_lines`, or `body_lines` field is an explicit line array. The renderer never paraphrases, translates, or invents line breaks.
- `impact-report.report.metrics` contains exactly three `{value, label}` objects. Sample metrics must say they are illustrative in the visible copy.
- Empty strings, control characters, missing fields, unsupported locales, and unexpected keys fail closed.
- The renderer records every supplied string, output dimension, SHA-256 digest, font path, overflow decision, contrast decision, and protected-region decision in `render-report.json`.
- A PASS report proves deterministic layout checks, not factual correctness, brand authorization, font licensing, or publication approval.

## Command

```text
python scripts/render_layout.py --copy <copy.json> --art <accepted-key-art.png> --out-dir <directory>
```

Use `--font <font-file>` when a production font is supplied. Without it, the script selects the first available Chinese-capable system font and records the exact path.
