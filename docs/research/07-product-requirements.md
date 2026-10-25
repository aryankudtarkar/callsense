# Product specification and acceptance requirements

## Purpose and user

A single student/reviewer locally inspects a permitted recording and uses a chronological list of model-estimated vocal-expression labels as a navigation aid. The model does not decide who needs help, who is suspicious, or what an investigator should do. This prototype does not improve police outcomes by evidence; no such claim is made.

## Minimum user journey

1. Open the app on the same machine. A visible notice states: local prototype; upload only audio the user is legally authorized to process; no real confidential calls for demos; model outputs are not evidence about emotion, intent, honesty, deception, credibility, or guilt.
2. Select a mono 16 kHz, 16-bit PCM WAV recording. Show supported type and maximum limits (20 MiB and 10 minutes). Play it locally in the browser before analysis if desired.
3. Affirm permitted use and choose **Analyze recording**. The browser sends only raw audio bytes to the loopback backend; it does not send the filename.
4. Show loading/progress and then a chronological timeline of fixed five-second windows. Each window may be played from the browser's original local audio. Label outputs as estimates from the named model; scores are uncalibrated. Do not call windows speaker turns or natural emotion episodes.
5. Provide **Clear session** that removes the file reference, audio object URL, player, results, and errors. Backend holds no session/database/file.

## Required outputs and abstention

The real model's documented categories are only angry, happy, neutral, and sad. Map the exact labels; unknown labels or model failure must be an explicit error/unknown outcome, never silently remapped. Show raw per-class scores only as “uncalibrated model scores,” not truth probabilities. No arbitrary cutoff is allowed. A future ambiguous/abstain threshold is permitted only after a documented development split and must be evaluated on untouched actors. Exact digital silence and too-short input may return “no usable audio for this window”; do not pretend a speech detector is present. [R3, R4]

## Input and privacy contract

- Accept only uncompressed PCM16 mono 16 kHz WAV in MVP. Validate the actual file header; browser `accept` attribute is convenience, not validation.
- Maximum: 20 MiB and 10 minutes; reject before expensive inference. No uploaded content is written to disk, a cache, a database, or a session log.
- Model weights may be cached persistently after first download. The model cache is not audio storage. Pin the model commit and document that first-run model retrieval uses a network connection.
- Bind the service to loopback only; page and API same-origin; no wildcard CORS, analytics, transcript, cloud inference, login, database, or cloud deployment.
- No microphone/live capture in MVP. Recorded-file analysis must work first. Do not add a fake real-time view.

## User-visible states

Implement distinct empty, invalid file, unsupported format, too large/long, silent/too-short window, loading, success, model unavailable, inference failure, and clear-session states. Errors should say what the user can correct without showing paths, stack traces, or uploaded contents. Show model name/revision, category definitions, sampling format, and limitations next to results.

## Explicit non-goals

No transcription, translation, speaker identity or diarization, deception/credibility/intent inference, emotional profiling, case database, multi-user accounts, cloud storage, alerting, urgency score, person ranking, investigative recommendation, or evidentiary export. Do not claim reliability across language, accent, demographics, emergency calls, telephone compression, or law-enforcement use.

## Acceptance evidence

- Browser upload sends a real WAV to a backend endpoint and returns model-generated output.
- The backend smoke/integration test loads the pinned model and executes genuine Wav2Vec2 inference; stubs are allowed only in isolated unit tests.
- A local browser E2E path uploads a synthetic/test audio fixture through the UI and observes the backend response. A permitted RAVDESS sample provides the human-audible demo; it is not bundled unless its terms and attribution are met.
- Limits, malformed headers, silence, backend errors, clear/delete, Origin policy, and no-disk/no-log behavior are verified.
- Product copy prevents interpreting the estimate as a fact or action instruction. [R1, R3, R17]
