# Minimal implementation guardrails

Use this alongside the numbered OMP task currently being executed. The OMP prompt is the implementation task; this file constrains how to make the requested change small without weakening it.

## Read first

Read the current stage prompt and the cited research files before editing. Inspect the repository tree, current diff, neighboring code, dependency manifest, and existing tests. Preserve user changes and established conventions. The environment was initially empty, but later stages may already have created working code.

## Keep the implementation narrow

- Implement only the current stage's observable acceptance criteria.
- Reuse suitable installed dependencies and platform/browser capabilities. Do not add a framework, abstraction layer, service, database, or runtime dependency without a concrete need.
- Keep the project Python-only: FastAPI plus static HTML, CSS, and browser JavaScript. Do not add a Node build step.
- Keep recorded WAV upload as the MVP. Do not add transcription, diarization, identity recognition, live microphone analysis, cloud inference, account/case management, or export unless a research decision explicitly changes the scope.
- The application classifier is the real local `superb/wav2vec2-base-superb-er` checkpoint, with a reviewed immutable revision and weight hashes. Gemini through OMP is only the coding agent.
- Make model loading explicit and fail safely if the approved model cannot load. Never replace it with fixed values, random output, an audio heuristic, sentiment, or an LLM answer.

## Preserve mandatory controls

- Accept only the documented input contract: mono PCM16 WAV at 16 kHz, with bounded bytes and duration. Validate the actual RIFF/WAVE format and payload; do not trust extension or browser metadata.
- Keep audio request bytes in bounded process memory. Do not persist audio, filenames, or analysis output. Do not log request bodies or sensitive identifiers. Do not promise secure erasure from RAM, swap, or crash dumps.
- Bind to loopback and keep UI/API same-origin. No wildcard CORS, remote audio provider, analytics, or telemetry.
- Present only the four model classes: angry, happy, neutral, and sad. Describe them as model-estimated vocal-expression labels. Scores are uncalibrated model outputs unless calibration is actually measured.
- Treat empty, silent, malformed, too-short, unsupported, unknown, and model-error inputs honestly. Do not invent a confidence cutoff or recast an output as fear, distress, nervousness, urgency, deception, credibility, intent, or guilt.
- Keep limitations visible near results. Maintain keyboard access, clear labels, visible focus, and understandable error states.

## Use evidence to decide what to simplify

Before accepting a simplification, trace the affected behavior from UI to request validation, preprocessing, real model call, response, and cleanup. Check existing tests and add a focused test for a new boundary or security-sensitive branch. Prefer deleting demonstrably unused code over deleting a required safety check. Record any out-of-scope work rather than smuggling it into the current stage.

## Completion evidence

Report changed files, relevant commands and their results, failures, skipped checks, whether the real model was actually loaded and invoked, and remaining limitations. A successful parser test or synthetic fixture proves software behavior only; it does not prove model quality or real-time performance.
