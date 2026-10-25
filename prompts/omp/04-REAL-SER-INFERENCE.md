# 04 — Real SER inference

## Purpose

Integrate the exact documented local classifier and prove the backend executes genuine audio inference.

## Required context

Read these files before editing:
- `docs/research/03-model-comparison.md`
- `docs/research/04-datasets-and-benchmarks.md`
- `docs/research/05-legal-privacy-and-responsible-use.md`
- `docs/research/06-threat-model-and-security.md`
- `docs/research/08-system-architecture.md`
- `docs/research/09-evaluation-and-test-plan.md`
- current audio validation code and package metadata
Also inspect `AGENTS.md`, `README.md`, `pyproject.toml`, and the nearest relevant source/tests if they exist. If a named research file is missing, stop and report the missing prerequisite; do not guess.

## Starting conditions

Stages 02 and 03 are complete and validated. Confirm stable Python 3.14 and inspect the existing audio endpoint. No weights may be present. The first model load needs a network download unless already cached.

## Task instructions

Integrate `superb/wav2vec2-base-superb-er` using standard Transformers/PyTorch classes. Before coding, inspect the current model card/config and choose an immutable Hub commit; record model ID, revision, license, and hashes in app documentation. Keep `trust_remote_code=False`. Load once in evaluation mode; use CPU baseline and optional MPS only after `torch.backends.mps.is_available()` and a real smoke pass. Convert only validated 16 kHz mono PCM16 to the model's expected waveform. Map only model labels to exact user-facing labels. Add an actual API path that returns real class scores and reports model unavailable/inference failure explicitly. Never fall back to a fake.

## Non-negotiable safety and implementation rules

- Inspect repository files, current `git status`, and existing conventions before changing anything. Preserve unrelated and prior-stage work; reuse existing code; make the smallest complete change.
- Use only the actual architecture in the research docs. The real runtime model is `superb/wav2vec2-base-superb-er`; Gemini is the coding model, never the app classifier. Never use hardcoded/random/heuristic/LLM predictions as successful SER.
- The model's only documented labels are angry, happy, neutral, sad. Call them estimated vocal-expression labels. Never infer fear, distress, nervousness, emotion truth, deception, intent, credibility, guilt, or urgency. No person ranking, automated investigative action, identity recognition, or speaker identification.
- Show uncalibrated scores as uncalibrated model outputs, never as truth probabilities. Unknown/error is valid. Don't invent a confidence threshold or calibration result.
- Do not send audio to an external provider. Do not use real personal/confidential calls as development fixtures. Audio stays in bounded local memory; no unnecessary retention, filename/path logging, or cloud services.
- Do not depend on subagents. Keep changes reviewable. Run relevant discovered tests/build commands; report failures honestly.


## Boundaries

Do not download IEMOCAP audio, retrain, substitute a cloud API, use SpeechBrain remote custom classes, send audio to Gemini, call its labels emotion truth, or expand labels beyond angry/happy/neutral/sad. Do not label model softmax as calibrated confidence/probability.

## Acceptance criteria

A documented real model load and inference run returns finite scores and one exact model label for a permitted test input through the actual backend. Model revision is immutable and recorded. Missing weights/network produces a clear unavailable state; no fake result. Input memory does not persist.

## Verification

Run discovered unit tests. Then run a genuine integration smoke against the backend using a synthetic test waveform or licensed public speech clip; record whether weights were downloaded, exact model revision, actual device, output schema, and command. Do not claim model performance from a single smoke. If model load/weights are unavailable, report failed/not-run; do not replace with a stub and count as acceptance.
Discover the actual project commands first (`pyproject.toml`, `README.md`, CI config, Makefile, existing tests). Do not invent a command. Run the smallest relevant existing checks and any explicitly required real-model check. Distinguish automated checks from manual browser checks.

## Failure handling

If the exact model fails with current stable Python/dependencies, first inspect the official model card and supported Transformers/PyTorch versions. Try at most the smallest compatible dependency correction. Do not enable remote code or switch models without updating research/model decision docs; stop with a documented blocker if unresolved.

## Definition of done

The backend's working path invokes the selected real checkpoint locally or explicitly reports that it cannot; no simulated predictions can reach success UI.

## Completion report

Return: files changed; commands actually run and their exit status; tests/builds passed, failed, or not run; whether a real model was used; privacy/security observations; limitations and unresolved issues; and the exact next prompt filename. Never report an unrun test or simulated result as success.
