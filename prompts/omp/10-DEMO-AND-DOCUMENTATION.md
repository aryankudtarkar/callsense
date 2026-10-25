# 10 — Demo and documentation

## Purpose

Finish verified setup/run instructions, a repeatable authorized demonstration, and a concise presentation guide that states limitations accurately.

## Required context

Read these files before editing:
- `docs/research/01-executive-summary.md`
- `docs/research/04-datasets-and-benchmarks.md`
- `docs/research/05-legal-privacy-and-responsible-use.md`
- `docs/research/07-product-requirements.md`
- `docs/research/08-system-architecture.md`
- `docs/research/09-evaluation-and-test-plan.md`
- `docs/research/10-environment-and-tooling-audit.md`
- current README, package metadata, and actual application behavior
Also inspect `AGENTS.md`, `README.md`, `pyproject.toml`, and the nearest relevant source/tests if they exist. If a named research file is missing, stop and report the missing prerequisite; do not guess.

## Starting conditions

The app has a real model route and tests. Recheck every command against actual metadata and current local files. Model weights may need a first-run download.

## Task instructions

Document stable Python 3.14 install/venv setup using the verified Homebrew command if applicable; dependency installation from project metadata; exact startup URL/command; model first-download, pinned revision/cache, and offline limitations; exact test commands; supported 16 kHz mono PCM WAV format and caps; how to run the UI demo; and how to clear a session. Provide an attribution-compliant public RAVDESS sample acquisition/use note or synthetic parser fixture, not bundled unlicensed audio. Write a brief project-review/presentation guide distinguishing pipeline demo from model validation.

## Non-negotiable safety and implementation rules

- Inspect repository files, current `git status`, and existing conventions before changing anything. Preserve unrelated and prior-stage work; reuse existing code; make the smallest complete change.
- Use only the actual architecture in the research docs. The real runtime model is `superb/wav2vec2-base-superb-er`; Gemini is the coding model, never the app classifier. Never use hardcoded/random/heuristic/LLM predictions as successful SER.
- The model's only documented labels are angry, happy, neutral, sad. Call them estimated vocal-expression labels. Never infer fear, distress, nervousness, emotion truth, deception, intent, credibility, guilt, or urgency. No person ranking, automated investigative action, identity recognition, or speaker identification.
- Show uncalibrated scores as uncalibrated model outputs, never as truth probabilities. Unknown/error is valid. Don't invent a confidence threshold or calibration result.
- Do not send audio to an external provider. Do not use real personal/confidential calls as development fixtures. Audio stays in bounded local memory; no unnecessary retention, filename/path logging, or cloud services.
- Do not depend on subagents. Keep changes reviewable. Run relevant discovered tests/build commands; report failures honestly.


## Boundaries

No false run/test/latency/accuracy claims, no credentials in docs, no real call sample, no secrets, no broad law-enforcement suitability claim, no fake output mode presented as real. Do not add external deployment or case export.

## Acceptance criteria

A beginner can set up, start, test, run a permitted sample, observe real model output, clear it, and understand what remains unvalidated. Every command succeeds as documented or is explicitly marked unverified with evidence.

## Verification

Execute the documented setup/test/start commands only when dependencies and weights are available. Verify each command from actual repo scripts/metadata. Check README links, attribution, no secrets, and that demo language matches the live UI. Do not claim success for an unrun step.
Discover the actual project commands first (`pyproject.toml`, `README.md`, CI config, Makefile, existing tests). Do not invent a command. Run the smallest relevant existing checks and any explicitly required real-model check. Distinguish automated checks from manual browser checks.

## Failure handling

If the intended command requires absent stable Python or model download, state the exact prerequisite and do not use Python 3.16 alpha or fake model output to create a successful demo.

## Definition of done

The documentation matches actual behavior and includes a repeatable, privacy-respecting demonstration path plus explicit limits.

## Completion report

Return: files changed; commands actually run and their exit status; tests/builds passed, failed, or not run; whether a real model was used; privacy/security observations; limitations and unresolved issues; and the exact next prompt filename. Never report an unrun test or simulated result as success.
