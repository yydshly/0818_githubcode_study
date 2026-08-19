# Publication Studio V1 Result

## Outcome

A local operator interface now wraps the four installed deterministic publication templates. It does not duplicate layout rules: every render calls `extension/photo-to-conceptual-art/scripts/render_layout.py`.

## Primary journey

```text
Select one of four target templates
-> edit explicit Chinese copy fields
-> render using the fixed reviewed Key Art
-> inspect PASS/FAIL and named gates
-> download PNG, render-report.json and copy.json
```

The batch action sends the four current copy states, renders five masters, and returns one ZIP containing:

- 5 PNG files;
- 4 `render-report.json` files;
- 4 `copy.json` files.

## Real localhost verification

The server was started at `http://127.0.0.1:8877/` and exercised through HTTP:

| Check | Observed |
| --- | --- |
| Studio page | HTTP 200, 5,388 bytes |
| State API | 4 whitelisted templates |
| Current-template render | PASS, 2 campaign outputs, 12 variant gates |
| Generated PNG | HTTP 200, 2,257,741 bytes |
| Batch render | PASS, 4 template results |
| Batch ZIP | HTTP 200, 13,247,339 bytes |

The test server was stopped after verification. Its operating-system temporary run directory and the local Python cache were removed; port 8877 no longer listened.

## Automated validation

Six Studio tests cover:

- the four-template state contract;
- rendering and resolving every template output;
- ZIP contents: four copies, four reports and five PNGs;
- unknown and mismatched template rejection;
- HTTP state/render/generated-file flow;
- oversized request rejection and temporary-directory cleanup.

## Safety boundary

- The server binds only to `127.0.0.1`.
- Art paths and template IDs are fixed in server configuration.
- Request bodies are capped at 256 KiB.
- Run-file resolution rejects paths outside the registered temporary run directory.
- Only the current process owns temporary results; the product has no account, upload, database or public deployment.
- Sample-data and layout PASS do not establish consent, factual accuracy, brand approval, licensing or publication authority.

## Browser evidence boundary

The live URL was requested in the Codex browser panel, but this session did not expose programmable screenshot, DOM or viewport control. HTTP behavior and generated rasters are verified; desktop/mobile visual interaction evidence remains pending until that control surface is available.
