# 03 — Audio ingestion and controls

## Purpose

Implement safe local file selection, preview, strict WAV validation, and clear-session controls without adding emotion output yet.

## Required context

Read these files before editing:
- `docs/research/05-legal-privacy-and-responsible-use.md`
- `docs/research/06-threat-model-and-security.md`
- `docs/research/07-product-requirements.md`
- `docs/research/08-system-architecture.md`
- `docs/research/09-evaluation-and-test-plan.md`
- current `README.md`, API entry point, UI files, and stage-02 report
Also inspect `AGENTS.md`, `README.md`, `pyproject.toml`, and the nearest relevant source/tests if they exist. If a named research file is missing, stop and report the missing prerequisite; do not guess.

## Starting conditions

Stage 02 exists. Inspect the actual app and tests. Model integration may not exist yet; do not fabricate a prediction to complete the page.

## Task instructions

Add file picker and local browser audio preview. Accept only mono 16-bit PCM WAV at 16 kHz; cap at 20 MiB and 10 minutes, enforced in backend on streamed bytes and decoded header/frame count. The browser may send raw file bytes with `audio/wav`; do not send its name. Parse/validate from bounded memory using the standard library where supported. Show clear unsupported, malformed, oversized, too-long, and empty states. Implement Clear Session to revoke object URL and clear browser file/results/errors. If an analysis button exists before model integration, it must clearly say analysis is not available yet or call a validation endpoint only.

## Non-negotiable safety and implementation rules

- Inspect repository files, current `git status`, and existing conventions before changing anything. Preserve unrelated and prior-stage work; reuse existing code; make the smallest complete change.
- Use only the actual architecture in the research docs. The real runtime model is `superb/wav2vec2-base-superb-er`; Gemini is the coding model, never the app classifier. Never use hardcoded/random/heuristic/LLM predictions as successful SER.
- The model's only documented labels are angry, happy, neutral, sad. Call them estimated vocal-expression labels. Never infer fear, distress, nervousness, emotion truth, deception, intent, credibility, guilt, or urgency. No person ranking, automated investigative action, identity recognition, or speaker identification.
- Show uncalibrated scores as uncalibrated model outputs, never as truth probabilities. Unknown/error is valid. Don't invent a confidence threshold or calibration result.
- Do not send audio to an external provider. Do not use real personal/confidential calls as development fixtures. Audio stays in bounded local memory; no unnecessary retention, filename/path logging, or cloud services.
- Do not depend on subagents. Keep changes reviewable. Run relevant discovered tests/build commands; report failures honestly.


## Boundaries

No multipart temp-file spool, arbitrary media decoder, upload folder, server-side filename use, audio logs, file caching, microphone, cloud request, transcription, or model-like fake result. Browser MIME/extension checks are not server validation.

## Acceptance criteria

Valid supported WAV passes validation; invalid format/header/size/duration and missing audio receive safe visible errors; uploaded bytes are not written to disk; UI Clear Session releases local references; no emotion prediction is shown.

## Verification

Discover project test/build commands. Run unit tests for parser/header/size/duration/error paths and UI checks available. Inspect changed request path to confirm body limits apply to actual streamed bytes and no temp file is created. Use synthetic WAV bytes only; do not download or use personal audio.
Discover the actual project commands first (`pyproject.toml`, `README.md`, CI config, Makefile, existing tests). Do not invent a command. Run the smallest relevant existing checks and any explicitly required real-model check. Distinguish automated checks from manual browser checks.

## Failure handling

If the installed Python `wave` behavior cannot decode a required header, reject that header explicitly and document it rather than enabling unsafe remote parsing. If request framework spools multipart, switch to the documented raw-body design. Never relax caps to make a fixture pass.

## Definition of done

Safe supported file controls and backend validation work with no persistent audio and no SER prediction.

## Completion report

Return: files changed; commands actually run and their exit status; tests/builds passed, failed, or not run; whether a real model was used; privacy/security observations; limitations and unresolved issues; and the exact next prompt filename. Never report an unrun test or simulated result as success.
