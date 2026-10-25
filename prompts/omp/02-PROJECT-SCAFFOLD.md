# 02 — Project scaffold

## Purpose

Create the smallest runnable Python-only project skeleton, local UI shell, dependency metadata, and repeatable development commands.

## Required context

Read these files before editing:
- `docs/research/01-executive-summary.md`
- `docs/research/07-product-requirements.md`
- `docs/research/08-system-architecture.md`
- `docs/research/09-evaluation-and-test-plan.md`
- `docs/research/10-environment-and-tooling-audit.md`
- output from `prompts/omp/01-REPOSITORY-AUDIT-AND-PLAN.md` if available
Also inspect `AGENTS.md`, `README.md`, `pyproject.toml`, and the nearest relevant source/tests if they exist. If a named research file is missing, stop and report the missing prerequisite; do not guess.

## Starting conditions

Stage 01 is complete. Re-inspect the repository. Existing application files may have appeared; reuse them. Target stable Python 3.14, not the host's Python 3.16.0a1. Do not assume dependencies have been installed.

## Task instructions

Create or adapt `pyproject.toml`, a FastAPI application entry point, static HTML/CSS/vanilla-JS shell, a local health endpoint, project-local virtual-environment/setup instructions, `.gitignore`, and a small pytest skeleton. Keep the app bound to 127.0.0.1. Establish discoverable commands for app startup and tests. Keep model dependency/model loading for stage 04. Use no Node build, database, cloud, or framework unless existing code justifies it. Verify current package compatibility instead of inventing version pins.

## Non-negotiable safety and implementation rules

- Inspect repository files, current `git status`, and existing conventions before changing anything. Preserve unrelated and prior-stage work; reuse existing code; make the smallest complete change.
- Use only the actual architecture in the research docs. The real runtime model is `superb/wav2vec2-base-superb-er`; Gemini is the coding model, never the app classifier. Never use hardcoded/random/heuristic/LLM predictions as successful SER.
- The model's only documented labels are angry, happy, neutral, sad. Call them estimated vocal-expression labels. Never infer fear, distress, nervousness, emotion truth, deception, intent, credibility, guilt, or urgency. No person ranking, automated investigative action, identity recognition, or speaker identification.
- Show uncalibrated scores as uncalibrated model outputs, never as truth probabilities. Unknown/error is valid. Don't invent a confidence threshold or calibration result.
- Do not send audio to an external provider. Do not use real personal/confidential calls as development fixtures. Audio stays in bounded local memory; no unnecessary retention, filename/path logging, or cloud services.
- Do not depend on subagents. Keep changes reviewable. Run relevant discovered tests/build commands; report failures honestly.


## Boundaries

Do not add fake predictions, model stubs to the production route, audio persistence, telemetry, login, or network deployment. Do not use the alpha Python interpreter to claim a working dependency install. Preserve existing code and instructions.

## Acceptance criteria

A documented command starts the local app on loopback and renders a usable empty state; a documented test command runs a minimal passing scaffold test; dependencies are in project metadata; no audio is accepted/stored yet; no hardcoded prediction exists.

## Verification

If Python 3.14 is installed, create `.venv` with `python3.14 -m venv .venv`; then use `.venv/bin/python -m pip install -e '.[dev]'` only if that exact metadata is present. Run the discovered test command (expected `.venv/bin/python -m pytest`) and startup smoke (`.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000`) only if module path matches. Stop the server after checking. Do not invoke the Python 3.16 alpha. If dependency install is unavailable, keep the scaffold inspectable and report the exact blocker.
Discover the actual project commands first (`pyproject.toml`, `README.md`, CI config, Makefile, existing tests). Do not invent a command. Run the smallest relevant existing checks and any explicitly required real-model check. Distinguish automated checks from manual browser checks.

## Failure handling

If Python 3.14 or a package wheel is unavailable, do not substitute random libraries or switch to a Node app; report which tested-compatible version/runtime was found and leave install steps explicit. If repo has working tests, use their commands and preserve them.

## Definition of done

The smallest local app shell, setup instructions, and an honest repeatable test/start path exist; no SER success is claimed.

## Completion report

Return: files changed; commands actually run and their exit status; tests/builds passed, failed, or not run; whether a real model was used; privacy/security observations; limitations and unresolved issues; and the exact next prompt filename. Never report an unrun test or simulated result as success.
