# 00 — Start here: execution and safety rules

## Purpose

Check the approved architecture, the OMP environment, and the prompt sequence before the implementation begins. Do not build the app in this stage.

## Required context

Read these files before editing:
- `docs/research/01-executive-summary.md`
- `docs/research/07-product-requirements.md`
- `docs/research/08-system-architecture.md`
- `docs/research/09-evaluation-and-test-plan.md`
- `docs/research/10-environment-and-tooling-audit.md`
- `docs/research/11-decision-log-and-open-risks.md`
- `prompts/ponytail/00-PONYTAIL-USAGE-AND-INTEGRATION.md`
Also inspect `AGENTS.md`, `README.md`, `pyproject.toml`, and the nearest relevant source/tests if they exist. If a named research file is missing, stop and report the missing prerequisite; do not guess.

## Starting conditions

This repository was empty when the pack was researched. It may have changed. Check current files and `git status` before assuming it is still empty. The app is not built by this stage.

## Task instructions

1. Confirm that all required research and prompt files exist and read them.
2. Inspect repository status, file tree, OMP version, model catalog and available skill names using read-only commands. Never print auth tokens or environment secrets.
3. Confirm `omp` can resolve `google-antigravity/gemini-3.8-flash` in `omp models`; this proves catalog visibility only, not account authorization.
4. Tell the user the build sequence, checkpoints, local Python prerequisite, and model/auth limitation. Make no source-code changes.

## Non-negotiable safety and implementation rules

- Inspect repository files, current `git status`, and existing conventions before changing anything. Preserve unrelated and prior-stage work; reuse existing code; make the smallest complete change.
- Use only the actual architecture in the research docs. The real runtime model is `superb/wav2vec2-base-superb-er`; Gemini is the coding model, never the app classifier. Never use hardcoded/random/heuristic/LLM predictions as successful SER.
- The model's only documented labels are angry, happy, neutral, sad. Call them estimated vocal-expression labels. Never infer fear, distress, nervousness, emotion truth, deception, intent, credibility, guilt, or urgency. No person ranking, automated investigative action, identity recognition, or speaker identification.
- Show uncalibrated scores as uncalibrated model outputs, never as truth probabilities. Unknown/error is valid. Don't invent a confidence threshold or calibration result.
- Do not send audio to an external provider. Do not use real personal/confidential calls as development fixtures. Audio stays in bounded local memory; no unnecessary retention, filename/path logging, or cloud services.
- Do not depend on subagents. Keep changes reviewable. Run relevant discovered tests/build commands; report failures honestly.


## Boundaries

Do not install software, download weights, edit global OMP settings, inspect credentials, call external providers with audio, or implement any application code. Do not use the screenshot as scientific validation.

## Acceptance criteria

All listed research/prompt files are present; current repo state and OMP catalog are reported accurately; no app code changed; exact sequence 01 through 11 and checkpoints after 02, 04, and 08 are stated.

## Verification

Use OMP local discovery only: `omp --version`, `omp --help`, `omp models find gemini-3.8-flash`, `omp plugin list`, `omp skill list`, and `omp config get skills.enableSkillCommands`. Do not run an inference request merely to test login. State that catalog visibility is not entitlement. No software tests apply because this stage makes no code changes.
Discover the actual project commands first (`pyproject.toml`, `README.md`, CI config, Makefile, existing tests). Do not invent a command. Run the smallest relevant existing checks and any explicitly required real-model check. Distinguish automated checks from manual browser checks.

## Failure handling

If a prompt/research file is missing, stop before implementation and report its exact path. If model or skill discovery differs, update the workflow recommendation using observed output and official OMP docs; do not change provider/auth settings.

## Definition of done

The user can start stage 01 with an accurate environment summary, safe execution rules, and no implementation changes.

## Completion report

Return: files changed; commands actually run and their exit status; tests/builds passed, failed, or not run; whether a real model was used; privacy/security observations; limitations and unresolved issues; and the exact next prompt filename. Never report an unrun test or simulated result as success.
