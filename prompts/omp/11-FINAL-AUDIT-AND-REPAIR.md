# 11 — Final audit and repair

## Purpose

Run a repository-wide correctness, privacy, security, model-integrity, and responsible-use review; fix verified defects with the smallest safe changes.

## Required context

Read these files before editing:
- all `docs/research/01-executive-summary.md` through `docs/research/12-references.md`
- `prompts/ponytail/00-PONYTAIL-USAGE-AND-INTEGRATION.md`
- `prompts/ponytail/01-MINIMAL-IMPLEMENTATION-GUARDRAILS.md`
- `prompts/ponytail/02-SECURITY-AND-CORRECTNESS-REVIEW.md`
- `prompts/ponytail/03-FINAL-PROTOTYPE-AUDIT.md`
- `README.md`, source tree, tests, and reports from stages 01–10
Also inspect `AGENTS.md`, `README.md`, `pyproject.toml`, and the nearest relevant source/tests if they exist. If a named research file is missing, stop and report the missing prerequisite; do not guess.

## Starting conditions

All prior stages have been attempted. Inspect current diff/status and files; do not assume all stages passed. Preserve user changes.

## Task instructions

Audit the full data path and product copy against requirements; verify real model ID/revision/hash and four class map; verify no audio outbound, no persisted audio/logging, bounded parser, local bind/origin, safe errors, clear control, tests and docs. Run `/skill:ponytail-audit` if installed and enabled, then `/skill:ponytail-review` on relevant uncommitted changes. Independently verify each finding before repair. Fix only verified defects that do not require changing the approved scope; add regression tests for security/correctness fixes. Provide an audit table with evidence and unresolved items.

## Non-negotiable safety and implementation rules

- Inspect repository files, current `git status`, and existing conventions before changing anything. Preserve unrelated and prior-stage work; reuse existing code; make the smallest complete change.
- Use only the actual architecture in the research docs. The real runtime model is `superb/wav2vec2-base-superb-er`; Gemini is the coding model, never the app classifier. Never use hardcoded/random/heuristic/LLM predictions as successful SER.
- The model's only documented labels are angry, happy, neutral, sad. Call them estimated vocal-expression labels. Never infer fear, distress, nervousness, emotion truth, deception, intent, credibility, guilt, or urgency. No person ranking, automated investigative action, identity recognition, or speaker identification.
- Show uncalibrated scores as uncalibrated model outputs, never as truth probabilities. Unknown/error is valid. Don't invent a confidence threshold or calibration result.
- Do not send audio to an external provider. Do not use real personal/confidential calls as development fixtures. Audio stays in bounded local memory; no unnecessary retention, filename/path logging, or cloud services.
- Do not depend on subagents. Keep changes reviewable. Run relevant discovered tests/build commands; report failures honestly.


## Boundaries

Do not automatically accept Ponytail suggestions; do not broaden into deployment, database, auth, transcription, person ranking, urgency or live analysis. Do not remove tests/security for simplicity. No real private audio or external audio API.

## Acceptance criteria

All high-severity product/security violations are fixed or explicitly block the prototype claim; test/model/E2E results are accurately separated; every unresolved issue has severity, evidence, and next action; no misleading output label or fake inference path remains.

## Verification

Run actual discovered full test/lint/build commands. Run genuine model and browser E2E only if model/browser are available, and report their actual statuses. Run Ponytail's audit/review using OMP's `/skill:` command only if present in `omp skill list`; otherwise perform the documented manual checklist. Never say “all tests passed” if any are skipped or failed.
Discover the actual project commands first (`pyproject.toml`, `README.md`, CI config, Makefile, existing tests). Do not invent a command. Run the smallest relevant existing checks and any explicitly required real-model check. Distinguish automated checks from manual browser checks.

## Failure handling

If an issue requires legal interpretation, unavailable data access, unsupported provider entitlement, or a model change, record it as unresolved and preserve the safe failure mode. Do not choose a new model or edit global configuration without updating the decision documents.

## Definition of done

The repo has a concise, evidence-backed final audit and any safe verified fixes, with no unsupported suitability claim.

## Completion report

Return: files changed; commands actually run and their exit status; tests/builds passed, failed, or not run; whether a real model was used; privacy/security observations; limitations and unresolved issues; and the exact next prompt filename. Never report an unrun test or simulated result as success.
