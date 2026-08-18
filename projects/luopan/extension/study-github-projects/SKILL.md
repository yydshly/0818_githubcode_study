---
name: study-github-projects
description: Analyze, reproduce, evaluate, and extend GitHub repositories for a research index. Use when Codex receives a GitHub repository URL or local checkout and needs to explain what the project can do, how it works, what it is useful for, which claims are actually verified, whether it fits the current product or research context, and how to build a demonstrable extension without blurring upstream and local work.
---

# Study GitHub Projects

Produce decisions backed by repository evidence. Do not turn an upstream README into a second README.

## Workflow

1. **Pin the subject.** Record upstream URL, default branch, exact commit, license, study date, and local path. Preserve upstream history with a fork, submodule, or separate checkout; do not silently vendor code.
2. **Read the repository contract.** Inspect `README`, contribution instructions, `AGENTS.md`, manifests, entry points, tests, examples, CI, releases, and license before forming conclusions.
3. **Create a deterministic snapshot.** Run:

   ```shell
   python scripts/inspect_repo.py <repo-path> --output <scan.json>
   ```

4. **Separate claims from proof.** Read [references/methodology.md](references/methodology.md) completely and classify every capability as `verified`, `declared`, `external`, or `gap`.
5. **Verify the shortest real path.** Run the repository's tests and one representative example or primary journey. Record the exact command, environment, exit code, workaround, and artifact. A passing command with a required workaround is not an unqualified default-platform pass.
6. **Explain the mechanism.** Trace input → router/orchestrator → core logic/data → validation → output. Cite files and line numbers or stable GitHub links. Distinguish prompt policy, deterministic code, external tools, and human judgment.
7. **Judge usefulness and fit.** State the decisions the project improves, target users, required dependencies, failure modes, and whether to adopt, adapt, reference, or reject it in the current context.
8. **Design one coherent extension.** Start from the host project's real workflow. Preserve the useful invariant, replace domain-specific assumptions, and define a minimal testable loop. Keep upstream, local extension, and speculative ideas visibly separate.
9. **Generate durable outputs.** Read [references/report-schema.md](references/report-schema.md), create one canonical JSON report, then run:

   ```shell
   python scripts/render_report.py <report.json> --output-dir <dir>
   ```

10. **Update the parent index.** Link the study record, runnable demo, upstream source, pinned commit, status, and extension from the parent repository without duplicating the full report.

## Evidence rules

- Prefer execution, source, tests, CI, release artifacts, and first-party docs over marketing language.
- Keep facts, calculations, inferences, and recommendations separate.
- Cite the exact evidence behind each major conclusion.
- Record missing dependencies and inaccessible services as boundaries, not hidden assumptions.
- Check the license before copying or modifying code and preserve required attribution.
- Do not claim production readiness from sample outputs or unit tests alone.

## Quality gate

Do not deliver until all are true:

- [ ] The exact upstream commit and license are recorded.
- [ ] Existing capability claims are divided into verified, declared, external, and gap.
- [ ] At least one real capability path and the available automated tests were exercised.
- [ ] The principle section cites concrete implementation files.
- [ ] The extension is tied to the current repository's workflow and has an acceptance test.
- [ ] Canonical JSON, Markdown, and HTML agree.
- [ ] The parent index links upstream, research, demo, and extension.
- [ ] Limitations and unverified claims remain visible in the final presentation.
