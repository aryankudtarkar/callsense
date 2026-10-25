# 01 — Repository audit and plan

## Purpose

Inspect the current repository and turn the approved architecture into a brief, repository-specific implementation plan. Do not scaffold or change code.

## Required context

Read these files before editing:
- `docs/research/01-executive-summary.md`
- `docs/research/03-model-comparison.md`
- `docs/research/05-legal-privacy-and-responsible-use.md`
- `docs/research/06-threat-model-and-security.md`
- `docs/research/07-product-requirements.md`
- `docs/research/08-system-architecture.md`
- `docs/research/09-evaluation-and-test-plan.md`
- `docs/research/10-environment-and-tooling-audit.md`
- `docs/research/11-decision-log-and-open-risks.md`
Also inspect `AGENTS.md`, `README.md`, `pyproject.toml`, and the nearest relevant source/tests if they exist. If a named research file is missing, stop and report the missing prerequisite; do not guess.

## Starting conditions

The repo may be empty or may contain work from earlier stages. Do not assume either. Preserve uncommitted files and inspect their purpose.

## Task instructions

Inspect current status, existing source/manifests/tests/instructions, installed Python executables, and whether stable Python 3.14 is available. Produce a short plan with existing files to reuse, files likely needed, actual test/build commands found (or to establish in stage 02), model-cache/first-download needs, and unresolved compatibility questions. Explicitly keep this at planning only.

## Non-negotiable safety and implementation rules

- Inspect repository files, current `git status`, and existing conventions before changing anything. Preserve unrelated and prior-stage work; reuse existing code; make the smallest complete change.
- Use only the actual architecture in the research docs. The real runtime model is `superb/wav2vec2-base-superb-er`; Gemini is the coding model, never the app classifier. Never use hardcoded/random/heuristic/LLM predictions as successful SER.
- The model's only documented labels are angry, happy, neutral, sad. Call them estimated vocal-expression labels. Never infer fear, distress, nervousness, emotion truth, deception, intent, credibility, guilt, or urgency. No person ranking, automated investigative action, identity recognition, or speaker identification.
- Show uncalibrated scores as uncalibrated model outputs, never as truth probabilities. Unknown/error is valid. Don't invent a confidence threshold or calibration result.
- Do not send audio to an external provider. Do not use real personal/confidential calls as development fixtures. Audio stays in bounded local memory; no unnecessary retention, filename/path logging, or cloud services.
- Do not depend on subagents. Keep changes reviewable. Run relevant discovered tests/build commands; report failures honestly.


## Boundaries

No app implementation, dependency installation, model download, or global configuration edit. Do not replace working code because it differs from the empty-repo hypothesis. Do not add features beyond the product spec.

## Acceptance criteria

Plan identifies the actual framework/conventions if present; names concrete smallest changes and checkpoints; records no unsupported command or model assumption; no source files changed.

## Verification

Use read-only discovery such as `pwd`, `git status --short --branch`, `rg --files --hidden -g '!.git'`, and inspection of manifests/CI. Do not run tests unless existing test instructions specifically make a read-only check useful; report actual commands available.
Discover the actual project commands first (`pyproject.toml`, `README.md`, CI config, Makefile, existing tests). Do not invent a command. Run the smallest relevant existing checks and any explicitly required real-model check. Distinguish automated checks from manual browser checks.

## Failure handling

If repository contents conflict with the selected model or privacy design, stop and document the conflict and minimal decision needed; don't silently rewrite the architecture. If Python 3.14 is absent, note stage 02 prerequisite rather than using Python 3.16.0a1.

## Definition of done

A concise, repository-specific plan and accurate file/runtime audit exist, with no code changes.

## Completion report

Return: files changed; commands actually run and their exit status; tests/builds passed, failed, or not run; whether a real model was used; privacy/security observations; limitations and unresolved issues; and the exact next prompt filename. Never report an unrun test or simulated result as success.
