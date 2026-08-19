# Publishing Pipeline V1 Result

## Outcome

The installed Skill's accepted Chinese tea Key Art was reused without another ImageGen call. One UTF-8 copy file produced two deterministic publication previews:

- `outputs/autumn-tea-2026-sample-poster-4x5.png` — 1200 × 1500
- `outputs/autumn-tea-2026-sample-header-16x9.png` — 1920 × 1080
- `outputs/render-report.json` — PASS

## Reproduction

Run from the project root:

```text
python -B extension/photo-to-conceptual-art/scripts/render_layout.py \
  --copy extension/photo-to-conceptual-art/examples/chinese-tea-copy.json \
  --art research/chinese-invocation/result-layered-paper.png \
  --out-dir research/publishing-pipeline-v1/outputs
```

The renderer used `C:\Windows\Fonts\msyh.ttc` for this fixture and recorded the resolved font path in the report. A production caller may supply `--font` explicitly.

## Gates

Both variants passed:

- exact UTF-8 copy equality;
- container overflow;
- protected product-region collision;
- forest-on-paper and white-on-forest contrast;
- visible sample-only disclosure;
- expected output dimensions.

The test suite also confirms that a missing CTA fails before rendering and deliberately overflowing copy creates a FAIL report with a non-zero exit code.

## Boundary

This is a deterministic layout and export result, not a commercial approval. `林间茶事`, the campaign dates, CTA, and location are sample copy. Brand authorization, factual review, logo assets, final font licensing, legal claims, accessibility approval, and channel upload remain external.
