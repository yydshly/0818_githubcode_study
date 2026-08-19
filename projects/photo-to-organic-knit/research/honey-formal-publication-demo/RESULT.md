# Honey Formal Publication Mode Demo Result

## Outcome

An approved-mode copy packet was rendered through the unchanged honey Key Art, `campaign-poster` template and renderer.

- `outputs/wild-honey-autumn-2026-approved-demo-poster-4x5.png`
- `outputs/wild-honey-autumn-2026-approved-demo-header-16x9.png`
- `outputs/render-report.json`
- `outputs/release-manifest.json`
- `outputs/release-signature.json`
- `outputs/trusted-release-keys.json`
- `outputs/release-audit.jsonl`
- `outputs/audit-event.json`
- Result: PASS, 12/12 variant gates.

No ImageGen, template or renderer change was made.

## Visible difference from sample mode

| Field | Sample mode | Approved-mode demo |
| --- | --- | --- |
| `copy_status` | `sample` | `approved` |
| System disclosure | `SAMPLE / 非商业发布` | Not rendered |
| Qualifier | `示例品牌 · CONCEPT ONLY` | `山野秋蜜系列 · 2026` |
| Channel | `线上预览 · SAMPLE COPY` | `官方商城 · 秋季限定` |
| CTA | `查看秋季限定` | `前往官方商城` |

The renderer report contains no `generated.sample_disclosure` text item in either approved output. Its `sample-disclosure` gate still passes because the status explicitly declares approved mode.

Approved rendering is now additionally locked by `honey-release-manifest-approved-demo.json`. The report records `release.status=PASS`, the manifest SHA-256, exact copy/art hashes, release scope, and all five approval records. Running the same approved copy without `--release-manifest` fails before output.

The manifest is detached-signed with Demo Ed25519 key `demo-release-key-2026`. `signature.status=PASS` records the trusted key, signer, signature hash and trust-store hash. The successful render appends audit sequence 1 with both output hashes and a verified event hash. The one-time demo private key was deleted after signing; only public evidence is retained.

## Exact approved-demo copy

- Brand: `山野蜜坊`
- Qualifier: `山野秋蜜系列 · 2026`
- Kicker: `秋季限定 · 09.20 上新`
- Headline: `一勺 / 秋蜜`
- Body: `把一季金黄， / 收进一勺甜。`
- CTA: `前往官方商城`
- Date: `09.20 — 10.18`
- Channel: `官方商城 · 秋季限定`

## How a real team reaches `approved`

Before changing `copy_status` from `sample` to `approved`, an external release packet must record:

1. Brand owner approval for the name, logo, campaign identity and visual use.
2. Copy owner approval for every title, date, CTA, channel and product statement.
3. Legal/regulatory approval for labels, claims, price, nutrition, origin and required notices when applicable.
4. Asset approval for the final logo, licensed production font, image rights, color mode, bleed and output size.
5. Channel approval for destination URL, storefront availability, tracking, accessibility text and release timing.

The renderer validates that all five records are complete and that the manifest hashes match the current files. It does not authenticate the people, signatures, authority, or revocation behind those records.

## Important boundary

This artifact demonstrates the approved workflow but is not itself a real authorized campaign. `山野蜜坊` remains a fictional example and the page must retain this external disclaimer even though the formal-looking image contains no sample label.
