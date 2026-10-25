# 06 — Live analysis feasibility gate

## Purpose

Assess whether true live processing is supported by measured local performance; otherwise finish the recorded-only UX honestly.

## Required context

Read these files before editing:
- `docs/research/01-executive-summary.md`
- `docs/research/03-model-comparison.md`
- `docs/research/05-legal-privacy-and-responsible-use.md`
- `docs/research/06-threat-model-and-security.md`
- `docs/research/07-product-requirements.md`
- `docs/research/08-system-architecture.md`
- `docs/research/09-evaluation-and-test-plan.md`
- current real inference path and measured results
Also inspect `AGENTS.md`, `README.md`, `pyproject.toml`, and the nearest relevant source/tests if they exist. If a named research file is missing, stop and report the missing prerequisite; do not guess.

## Starting conditions

Stages 02–05 are complete. Do not assume microphone permission, MPS performance, incremental model support, or a latency result. The intended default is recorded-file only until evidence exists.

## Task instructions

First inspect actual benchmarks and determine whether the model/API can process incremental audio with stable windows and acceptable end-to-end latency without sending audio externally. If there is no measured evidence, do not add capture/streaming code; ensure UI clearly states “Recorded-file analysis only; live mode is not validated.” If evidence exists, propose a bounded local design and implement only if it preserves all privacy and uncertainty requirements; measure capture-to-visible-output latency on the actual machine, with explicit microphone start/stop and no recording persistence.

## Non-negotiable safety and implementation rules

- Inspect repository files, current `git status`, and existing conventions before changing anything. Preserve unrelated and prior-stage work; reuse existing code; make the smallest complete change.
- Use only the actual architecture in the research docs. The real runtime model is `superb/wav2vec2-base-superb-er`; Gemini is the coding model, never the app classifier. Never use hardcoded/random/heuristic/LLM predictions as successful SER.
- The model's only documented labels are angry, happy, neutral, sad. Call them estimated vocal-expression labels. Never infer fear, distress, nervousness, emotion truth, deception, intent, credibility, guilt, or urgency. No person ranking, automated investigative action, identity recognition, or speaker identification.
- Show uncalibrated scores as uncalibrated model outputs, never as truth probabilities. Unknown/error is valid. Don't invent a confidence threshold or calibration result.
- Do not send audio to an external provider. Do not use real personal/confidential calls as development fixtures. Audio stays in bounded local memory; no unnecessary retention, filename/path logging, or cloud services.
- Do not depend on subagents. Keep changes reviewable. Run relevant discovered tests/build commands; report failures honestly.


## Boundaries

Never create a fake live animation or periodically reclassify a static sample. No external API, continuous background mic, hidden recording, automatic urgency, or unverified “real-time” claim. Do not add microphone permission solely to match the screenshot title.

## Acceptance criteria

Either: (A) recorded workflow works and no fake/live UI is present, with exact feasibility gap documented; or (B) a true local mic path starts/stops visibly, runs the actual model on live audio, reports measured latency and errors, and stores nothing. The user can revoke/stop capture immediately.

## Verification

Run discovered tests. If live mode is attempted, run an actual microphone/device test with explicit user action and no private call; record hardware/software and p50/p95 latency. If a benchmark is absent, do not treat model unit tests as live verification.
Discover the actual project commands first (`pyproject.toml`, `README.md`, CI config, Makefile, existing tests). Do not invent a command. Run the smallest relevant existing checks and any explicitly required real-model check. Distinguish automated checks from manual browser checks.

## Failure handling

If permission, audio backend, model incremental behavior, or latency is not supported, preserve the recording workflow and document the blocker. Do not install a third-party cloud service or invent a model substitute.

## Definition of done

Live capability is either verified end-to-end or explicitly deferred without a misleading UI.

## Completion report

Return: files changed; commands actually run and their exit status; tests/builds passed, failed, or not run; whether a real model was used; privacy/security observations; limitations and unresolved issues; and the exact next prompt filename. Never report an unrun test or simulated result as success.
