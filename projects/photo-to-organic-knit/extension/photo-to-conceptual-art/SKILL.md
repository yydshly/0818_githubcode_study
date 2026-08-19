---
name: photo-to-conceptual-art
description: Turn a user-provided photograph into a goal-driven conceptual visual asset by extracting reusable visual essence, routing through scenario, effect, and delivery profiles, compiling an ImageGen prompt, reviewing target-specific gates, and optionally composing accepted art with exact copy in a supported deterministic publication template. Use for covers, campaigns, reports, memory books, editorial art, or other publication-oriented photo reinterpretation. Do not use for faithful identity restoration, factual photo editing, manufacturing-ready craft patterns, standalone logo design, or unsupported free-form typesetting.
---

# Photo to Conceptual Art

Produce an asset that is fit for the user's intended audience and delivery, not merely an attractive style transfer. Treat the generated image as an art layer; keep exact titles, dates, prices, metrics, legal copy, and brand marks in a deterministic design layer unless the user explicitly requests otherwise.

## Workflow

1. Inspect the source photograph. Ask for missing information only when audience, intended delivery, or a consequential preservation requirement cannot be inferred safely.
2. Read [references/essence-schema.md](references/essence-schema.md) and write an essence JSON file. Record only source-grounded anchors, relationships, emotion, visual path, metaphor, retain/transform/discard decisions, palette, and privacy notes.
3. Select a scenario ID from `profiles/scenarios/`. Prefer the user's stated purpose over aesthetic preference.
4. Choose an effect:
   - use `auto` when the user delegates the choice;
   - use an explicit ID from `profiles/effects/` when the user chooses a material language;
   - never invent an unrecorded profile silently.
5. Choose a delivery ID from `profiles/deliveries/`, defaulting to the scenario profile. Generated art is wordless by default so typography can remain editable.
6. Compile the production prompt with:

   ```text
   python scripts/build_prompt.py --essence <path.json> --scenario <scenario-id> --effect auto --format prompt
   ```

   Add `--delivery <delivery-id>` or an explicit `--effect <effect-id>` when needed. Use `--format json` when downstream automation needs route metadata and gates.
7. Generate or edit the raster image using the compiled prompt. The source photo is the subject reference; any material reference is style-quality guidance only and must not contribute unrelated objects or text.
8. Read [references/quality-gates.md](references/quality-gates.md). Reject results that fail required source anchors, scenario purpose, delivery safety, material credibility, reference isolation, or privacy constraints. Correct one failure at a time.
9. For a retained benchmark or production review, read [references/review-schema.md](references/review-schema.md), record evidence for every scenario and delivery gate, then validate the record with:

   ```text
   python scripts/score_review.py --review <review.json> --scenario <scenario-id> --delivery <delivery-id> --format json
   ```

   The scorer checks evidence completeness and computes a deterministic summary; it does not inspect pixels or replace human judgment.
10. Hand the accepted wordless art layer to the relevant design template or design system. When the delivery is `campaign-poster`, `book-cover`, `impact-report`, or `field-journal` and the user wants publication previews, read [references/copy-schema.md](references/copy-schema.md), start from the matching maintained example, put exact approved or explicitly labeled sample copy in a UTF-8 JSON file, and render the supported variants with:

    ```text
    python scripts/render_layout.py --copy <copy.json> --art <accepted-key-art.png> --out-dir <directory>
    ```

    When `copy_status` is `approved`, also read [references/release-manifest.md](references/release-manifest.md) and [references/release-security.md](references/release-security.md). Build a hash-bound draft, obtain the five external approvals, sign the exact manifest with an out-of-repository Ed25519 key, and pass the completed release packet:

    ```text
    python scripts/release_manifest.py --copy <copy.json> --art <accepted-key-art.png> --release-id <id> --scope production --out <manifest.json>
    python scripts/release_security.py sign --manifest <manifest.json> --private-key <outside-repo.pem> --key-id <id> --signer <trusted-owner> --out <signature.json>
    python scripts/render_layout.py --copy <copy.json> --art <accepted-key-art.png> --release-manifest <manifest.json> --release-signature <signature.json> --trusted-keys <trusted-keys.json> --audit-log <audit.jsonl> --out-dir <directory>
    ```

    Approved rendering must fail before output when the manifest, signature, trust store, or audit path is missing; an approval is pending; hashes mismatch; the signing key is unknown, inactive, or wrong-scope; or signature verification fails. A PASS report must include release, signature and audit evidence plus exact-copy, overflow, contrast, protected-region, sample-disclosure, and dimension checks for every declared output. Treat malformed, mismatched, or overflowing copy as a failed delivery; do not shrink text indefinitely or ask ImageGen to repair lettering. Unsupported delivery templates still require an external design system until a recorded renderer exists.
11. For a retained benchmark, publication demo, or approved packet, read [references/action-runbook.md](references/action-runbook.md). Follow its normal actions, failure responses and stop rules; do not turn an unresolved gate into an unrecorded retry or infer production authorization.
12. Report the route, prompt, result path, review decision, publication artifacts, deterministic report status, remaining production approvals, and any unverified gate.

## Routing boundaries

- Preserve source orientation unless the delivery profile explicitly requires another aspect; when it does, recompose rather than crop essential anchors.
- Scenario purpose outranks effect novelty. A family memory may route to organic knit; an impact report may route to stained glass; the user can override when the tradeoff is stated.
- The compiler validates and assembles instructions; it does not inspect images or prove artistic quality.
- The review scorer validates a human evidence record; it does not generate evidence or estimate model accuracy.
- Do not imply that generated lettering, statistics, brand marks, or legal information are publication-ready.
- A deterministic layout PASS proves only that supplied strings fit the recorded template with declared contrast and safe-area checks. It does not prove factual accuracy, brand authorization, font licensing, legal approval, or channel acceptance.
- A Release Manifest records caller-supplied approval evidence and detects input changes; it does not authenticate reviewers, signatures, authority, or revocation.
- Ed25519 verification proves control of a trusted private key; the local audit chain exposes edits but cannot prevent deletion or rollback. Real identity, key custody, revocation, timestamping, and remote immutable retention remain external.
- Do not upload or publish private source photographs without explicit authorization.
- Stop after two targeted regeneration attempts for the same failed gate and report the unresolved issue instead of retrying indefinitely.

## Profile maintenance

Read [references/profile-authoring.md](references/profile-authoring.md) only when adding or revising scenario, effect, or delivery profiles. Keep IDs stable, machine-readable files valid, and tests aligned with intentional routing changes.
