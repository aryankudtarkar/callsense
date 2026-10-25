# 08 — Testing and evaluation

## Purpose

Verify software behavior, the true end-to-end UI/API/model path, model transfer performance, runtime timing, and responsible-use controls as separate results.

## Required context

Read these files before editing:
- `docs/research/03-model-comparison.md`
- `docs/research/04-datasets-and-benchmarks.md`
- `docs/research/05-legal-privacy-and-responsible-use.md`
- `docs/research/06-threat-model-and-security.md`
- `docs/research/08-system-architecture.md`
- `docs/research/09-evaluation-and-test-plan.md`
- `docs/research/11-decision-log-and-open-risks.md`
- all current tests, dependency metadata, model endpoint, and UI
Also inspect `AGENTS.md`, `README.md`, `pyproject.toml`, and the nearest relevant source/tests if they exist. If a named research file is missing, stop and report the missing prerequisite; do not guess.

## Starting conditions

Stages 02–07 are complete. Re-discover test commands and model revision. Confirm all demo data is synthetic or licensed and not a private call.

## Task instructions

Complete unit tests for file validation, segmentation, output handling, safe failures and clear session; backend integration through the real pinned model; and browser E2E showing UI selection calls the backend and displays its actual result. If a Playwright test framework is not yet present, use Python Playwright only if compatible and proportionate; document browser install. Run a real model smoke with weights, then (if authorized) an external RAVDESS speaker-disjoint evaluation with exact split manifest. Measure cold load and warm inference separately on CPU and optionally MPS. Report software correctness, model metrics, runtime latency, and security/responsible-use results in separate sections.

## Non-negotiable safety and implementation rules

- Inspect repository files, current `git status`, and existing conventions before changing anything. Preserve unrelated and prior-stage work; reuse existing code; make the smallest complete change.
- Use only the actual architecture in the research docs. The real runtime model is `superb/wav2vec2-base-superb-er`; Gemini is the coding model, never the app classifier. Never use hardcoded/random/heuristic/LLM predictions as successful SER.
- The model's only documented labels are angry, happy, neutral, sad. Call them estimated vocal-expression labels. Never infer fear, distress, nervousness, emotion truth, deception, intent, credibility, guilt, or urgency. No person ranking, automated investigative action, identity recognition, or speaker identification.
- Show uncalibrated scores as uncalibrated model outputs, never as truth probabilities. Unknown/error is valid. Don't invent a confidence threshold or calibration result.
- Do not send audio to an external provider. Do not use real personal/confidential calls as development fixtures. Audio stays in bounded local memory; no unnecessary retention, filename/path logging, or cloud services.
- Do not depend on subagents. Keep changes reviewable. Run relevant discovered tests/build commands; report failures honestly.


## Boundaries

A stub, random output, synthetic tone, model-card score, or one successful API call is not model validation. Never tune on final test actors. Do not infer phone/cybercrime/India performance. Do not fabricate or omit failed metrics.

## Acceptance criteria

Automated UI/API/model integration proves the actual frontend route reaches the actual local model; separate report contains dataset, classes, speakers/splits, model revision, metrics/counts, timing conditions/device, failures, and limitations. Real-model integration failure blocks claiming the app works.

## Verification

Use commands discovered from `pyproject.toml`/README; normally the local test command will be `.venv/bin/python -m pytest`, but verify before use. Run documented real-model and E2E commands. Run a benchmark script only if the repository provides one; record wall-clock durations and machine metadata. If external dataset access is unavailable, report the model-performance track as not run while still completing software checks.
Discover the actual project commands first (`pyproject.toml`, `README.md`, CI config, Makefile, existing tests). Do not invent a command. Run the smallest relevant existing checks and any explicitly required real-model check. Distinguish automated checks from manual browser checks.

## Failure handling

If model weights, browser runtime, or dataset are unavailable, do not replace with fakes or silently skip acceptance. Separate passed software checks from blocked/not-run real-model, E2E, or quality checks; provide exact next setup command based on verified instructions.

## Definition of done

The evidence distinguishes functioning software from scientific validation and contains no fabricated benchmark, fairness claim, or real-time claim.

## Completion report

Return: files changed; commands actually run and their exit status; tests/builds passed, failed, or not run; whether a real model was used; privacy/security observations; limitations and unresolved issues; and the exact next prompt filename. Never report an unrun test or simulated result as success.
