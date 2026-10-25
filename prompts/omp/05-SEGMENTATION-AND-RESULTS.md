# 05 — Segmentation and results

## Purpose

Turn a validated recording into a chronological review timeline of clearly identified fixed-window model estimates.

## Required context

Read these files before editing:
- `docs/research/03-model-comparison.md`
- `docs/research/04-datasets-and-benchmarks.md`
- `docs/research/05-legal-privacy-and-responsible-use.md`
- `docs/research/07-product-requirements.md`
- `docs/research/08-system-architecture.md`
- `docs/research/09-evaluation-and-test-plan.md`
- real model inference endpoint and current UI
Also inspect `AGENTS.md`, `README.md`, `pyproject.toml`, and the nearest relevant source/tests if they exist. If a named research file is missing, stop and report the missing prerequisite; do not guess.

## Starting conditions

Stage 04 has genuine model inference. Inspect its actual model output, units, response schema, and tests before adding presentation logic.

## Task instructions

Analyze chronological, non-overlapping five-second windows. Keep timestamps tied to original waveform. Analyze a final partial window only if it is at least one second. Exact digital silence may return unknown; do not call this VAD. For each other window, invoke the real model and map only its four documented labels. Show a playable segment control that seeks the browser's original local file; display raw class scores as explicitly uncalibrated. If the model's labels/scores are missing or non-finite, show unknown/error, not a substitute. Show chronological results only, without severity ordering.

## Non-negotiable safety and implementation rules

- Inspect repository files, current `git status`, and existing conventions before changing anything. Preserve unrelated and prior-stage work; reuse existing code; make the smallest complete change.
- Use only the actual architecture in the research docs. The real runtime model is `superb/wav2vec2-base-superb-er`; Gemini is the coding model, never the app classifier. Never use hardcoded/random/heuristic/LLM predictions as successful SER.
- The model's only documented labels are angry, happy, neutral, sad. Call them estimated vocal-expression labels. Never infer fear, distress, nervousness, emotion truth, deception, intent, credibility, guilt, or urgency. No person ranking, automated investigative action, identity recognition, or speaker identification.
- Show uncalibrated scores as uncalibrated model outputs, never as truth probabilities. Unknown/error is valid. Don't invent a confidence threshold or calibration result.
- Do not send audio to an external provider. Do not use real personal/confidential calls as development fixtures. Audio stays in bounded local memory; no unnecessary retention, filename/path logging, or cloud services.
- Do not depend on subagents. Keep changes reviewable. Run relevant discovered tests/build commands; report failures honestly.


## Boundaries

These are fixed processing windows, not natural emotion events, speaker turns, or identified persons. No diarization, emotion mixing, fear/distress/nervousness, red alert colors, urgency ranking, confidence threshold, or decision action. Do not apply an arbitrary cutoff. Keep underlying file local and ephemeral.

## Acceptance criteria

Timeline timestamps cover the validated duration without overlap/gaps except a documented too-short tail; play controls seek to the correct time; all displayed labels come from the actual model; unknown/error states are visible; every score label says uncalibrated and every screen says the output is only an estimate.

## Verification

Run the project's discovered unit/integration tests. Add tests for window boundary cases, exact-silence abstention, model failure and time mapping. Use a real model integration fixture to check a result round-trip; a fake may test component states only and must not count for inference acceptance.
Discover the actual project commands first (`pyproject.toml`, `README.md`, CI config, Makefile, existing tests). Do not invent a command. Run the smallest relevant existing checks and any explicitly required real-model check. Distinguish automated checks from manual browser checks.

## Failure handling

If fixed windows cause excessive model load, do not silently lengthen them or create VAD/diarization. Benchmark and document the issue; keep a working recorded-file path or report a concrete limitation.

## Definition of done

Results view is useful for manual review while accurately describing fixed windows, four labels, uncalibrated scores, and human responsibility.

## Completion report

Return: files changed; commands actually run and their exit status; tests/builds passed, failed, or not run; whether a real model was used; privacy/security observations; limitations and unresolved issues; and the exact next prompt filename. Never report an unrun test or simulated result as success.
