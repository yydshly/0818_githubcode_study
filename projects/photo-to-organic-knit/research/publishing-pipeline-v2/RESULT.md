# Publishing Pipeline V2 Result

## Outcome

Three previously reviewed wordless Key Art files were passed through the extended deterministic renderer. No ImageGen call was made in this phase.

| Delivery | Accepted art route | Master | Result |
| --- | --- | --- | --- |
| Book cover | family-memory → organic-knit → book-cover | 1200×1600 | PASS, 6/6 gates |
| Impact report | impact-report → stained-glass → impact-report | 1240×1754 | PASS, 6/6 gates |
| Field journal | travel-cover → woodcut → field-journal | 1200×1500 | PASS, 6/6 gates |

## Outputs

- `book-cover/family-memory-volume-01-sample-book-cover-3x4.png`
- `impact-report/community-rain-impact-2026-sample-impact-report-a4.png`
- `field-journal/lighthouse-field-journal-2026-sample-field-journal-4x5.png`
- One `render-report.json` beside each master.

## Reproduction

Each invocation uses the same command shape:

```text
python scripts/render_layout.py --copy <template-copy.json> --art <accepted-key-art.png> --out-dir <template-output-directory>
```

The renderer resolves `assets/templates/<copy.template>.json`; an explicit `--template` is an override and must match the copy's template ID.

## Validation

- 20 Skill tests pass.
- The existing campaign-poster still produces its 4:5 and 16:9 outputs.
- Missing fields fail before rendering.
- Impact reports require exactly three metric objects.
- Deliberately overflowing text creates a FAIL report and non-zero exit.
- Each retained V2 report records exact-copy, overflow, contrast, protected-region, sample-disclosure, and dimensions as PASS.

## Boundary

Every name, coordinate, distance and metric in these examples is sample data. The outputs demonstrate repeatable composition and exact rendering, not factual accuracy, family consent, nonprofit audit, geographic validation, brand approval, print prepress, or publication authorization.
