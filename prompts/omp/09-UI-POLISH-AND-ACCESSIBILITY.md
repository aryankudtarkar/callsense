# 09 — UI polish and accessibility

## Purpose

Improve clarity, keyboard access, screen-reader labeling, and responsive layout without changing model meaning or adding product scope.

## Required context

Read these files before editing:
- `docs/research/05-legal-privacy-and-responsible-use.md`
- `docs/research/07-product-requirements.md`
- `docs/research/08-system-architecture.md`
- current UI and accessibility/test setup
Also inspect `AGENTS.md`, `README.md`, `pyproject.toml`, and the nearest relevant source/tests if they exist. If a named research file is missing, stop and report the missing prerequisite; do not guess.

## Starting conditions

The real recorded-file workflow and result states exist. Inspect the page with a keyboard and screen reader-friendly markup before redesigning it. The screenshot supplies the project problem context, not UI requirements to copy literally.

## Task instructions

Make file selection, analyze, playback/seek, clear, errors, loading, and timeline controls keyboard accessible with clear labels and focus order. Use semantic HTML, visible focus, readable contrast, responsive layout, and non-color-only emotion/status cues. Keep privacy notice and model limitations adjacent to results. Avoid flashing or emergency-red urgency design. Preserve user controls and model outputs.

## Non-negotiable safety and implementation rules

- Inspect repository files, current `git status`, and existing conventions before changing anything. Preserve unrelated and prior-stage work; reuse existing code; make the smallest complete change.
- Use only the actual architecture in the research docs. The real runtime model is `superb/wav2vec2-base-superb-er`; Gemini is the coding model, never the app classifier. Never use hardcoded/random/heuristic/LLM predictions as successful SER.
- The model's only documented labels are angry, happy, neutral, sad. Call them estimated vocal-expression labels. Never infer fear, distress, nervousness, emotion truth, deception, intent, credibility, guilt, or urgency. No person ranking, automated investigative action, identity recognition, or speaker identification.
- Show uncalibrated scores as uncalibrated model outputs, never as truth probabilities. Unknown/error is valid. Don't invent a confidence threshold or calibration result.
- Do not send audio to an external provider. Do not use real personal/confidential calls as development fixtures. Audio stays in bounded local memory; no unnecessary retention, filename/path logging, or cloud services.
- Do not depend on subagents. Keep changes reviewable. Run relevant discovered tests/build commands; report failures honestly.


## Boundaries

Do not turn the page into an alarm dashboard or imply detection certainty; no urgency score or person ranking. Do not add a new frontend framework, charts dependency, animations that resemble live detection, or content not supported by the model.

## Acceptance criteria

A keyboard user can complete select/analyze/play/clear; status and errors are perceivable; layout remains usable at narrow viewport; output disclaimer is visible; no semantic or functional workflow regresses.

## Verification

Run discovered UI/unit/E2E checks and any existing accessibility checker. If no automated accessibility tooling exists, document a manual keyboard/zoom/contrast check and what was actually inspected. Run real model integration only if UI changes touch the inference flow.
Discover the actual project commands first (`pyproject.toml`, `README.md`, CI config, Makefile, existing tests). Do not invent a command. Run the smallest relevant existing checks and any explicitly required real-model check. Distinguish automated checks from manual browser checks.

## Failure handling

If a contrast or layout issue cannot be resolved without changing the stack, use native HTML/CSS and document the remaining issue; do not remove required controls or disclaimer.

## Definition of done

UI is clear, accessible in tested dimensions/input modes, and still presents only the qualified four-class model outputs.

## Completion report

Return: files changed; commands actually run and their exit status; tests/builds passed, failed, or not run; whether a real model was used; privacy/security observations; limitations and unresolved issues; and the exact next prompt filename. Never report an unrun test or simulated result as success.
