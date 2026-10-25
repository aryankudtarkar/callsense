# 07 — Privacy and security controls

## Purpose

Harden local audio ingestion, loopback API, error handling, logging, and clear-session behavior against the threat model.

## Required context

Read these files before editing:
- `docs/research/05-legal-privacy-and-responsible-use.md`
- `docs/research/06-threat-model-and-security.md`
- `docs/research/07-product-requirements.md`
- `docs/research/08-system-architecture.md`
- `docs/research/09-evaluation-and-test-plan.md`
- all current backend upload/model code, app config, and log setup
Also inspect `AGENTS.md`, `README.md`, `pyproject.toml`, and the nearest relevant source/tests if they exist. If a named research file is missing, stop and report the missing prerequisite; do not guess.

## Starting conditions

Stages 02–06 are complete. Inspect the entire audio path, not just the upload function. Preserve functional model inference and existing tests.

## Task instructions

Verify loopback-only bind; same-origin UI/API; no wildcard CORS; expected Host/Origin checks; streamed body byte caps; WAV content parsing; no server filename/path use; no multipart temp spool; no audio or label-linked identity in logs; no database/cache for user data; safe generic errors; and browser Clear Session releasing object URLs and local result state. Verify package/model revision is pinned and remote code disabled. Add tests for security-sensitive branches.

## Non-negotiable safety and implementation rules

- Inspect repository files, current `git status`, and existing conventions before changing anything. Preserve unrelated and prior-stage work; reuse existing code; make the smallest complete change.
- Use only the actual architecture in the research docs. The real runtime model is `superb/wav2vec2-base-superb-er`; Gemini is the coding model, never the app classifier. Never use hardcoded/random/heuristic/LLM predictions as successful SER.
- The model's only documented labels are angry, happy, neutral, sad. Call them estimated vocal-expression labels. Never infer fear, distress, nervousness, emotion truth, deception, intent, credibility, guilt, or urgency. No person ranking, automated investigative action, identity recognition, or speaker identification.
- Show uncalibrated scores as uncalibrated model outputs, never as truth probabilities. Unknown/error is valid. Don't invent a confidence threshold or calibration result.
- Do not send audio to an external provider. Do not use real personal/confidential calls as development fixtures. Audio stays in bounded local memory; no unnecessary retention, filename/path logging, or cloud services.
- Do not depend on subagents. Keep changes reviewable. Run relevant discovered tests/build commands; report failures honestly.


## Boundaries

Do not remove tests or protections to reduce code size. Do not claim legal compliance or secure RAM erasure. Do not introduce auth/cloud/analytics as a workaround. No real calls in tests.

## Acceptance criteria

Unsupported/crafted/oversize input is rejected before model call; cross-origin attempts fail; a repeat request does not create user files; errors expose no stack/path/audio; clear action removes browser state; real model route still passes integration.

## Verification

Run discovered tests, including actual-model smoke if weights are available; run project formatting/type/lint commands if defined. Inspect filesystem/temp dirs and logs after synthetic upload. Record actual result and any tests not run. No private audio.
Discover the actual project commands first (`pyproject.toml`, `README.md`, CI config, Makefile, existing tests). Do not invent a command. Run the smallest relevant existing checks and any explicitly required real-model check. Distinguish automated checks from manual browser checks.

## Failure handling

If framework behavior causes disk spooling or Origin handling cannot be implemented safely, redesign the endpoint within the approved raw-body/loopback architecture and add a regression test. Do not accept a known leak as a deferred harmless detail.

## Definition of done

Threat-model controls are implemented, tested, and do not break the real model path.

## Completion report

Return: files changed; commands actually run and their exit status; tests/builds passed, failed, or not run; whether a real model was used; privacy/security observations; limitations and unresolved issues; and the exact next prompt filename. Never report an unrun test or simulated result as success.
