# Review record schema

Use this record only after visually inspecting a generated result. The scorer validates completeness and arithmetic; it does not inspect the image.

```json
{
  "id": "stable-review-id",
  "artifact": "relative/or/absolute/path.png",
  "attempt": 1,
  "reviewer": "human or declared review process",
  "gates": {
    "exact gate label from scenario or delivery profile": {
      "status": "pass",
      "score": 5,
      "evidence": "one concrete observation tied to the artifact"
    }
  },
  "notes": []
}
```

## Rules

- Record every gate from the selected scenario and delivery profiles exactly once.
- Do not add unrelated gates to improve or dilute the score.
- `pass` uses score 3–5; `fail` uses 0–2; `unverified` uses 0.
- Evidence must name an observable fact, not an intention such as “the prompt asked for it.”
- `attempt` is a positive integer and counts the displayed generation round.
- A valid record with any failed gate has decision `fail`.
- A valid record with no failures but at least one unverified gate has decision `needs-review`.
- Decision `pass` requires every required gate to pass.

## Boundaries

Scores compare results reviewed under the same declared rubric. They are not calibrated model probabilities, benchmark confidence intervals, accessibility certification, privacy approval, or publication authorization.
