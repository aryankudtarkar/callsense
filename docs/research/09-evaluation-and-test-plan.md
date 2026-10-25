# Evaluation and verification plan

These are four distinct evidence tracks. Passing software tests means the pipeline works; it does not validate the emotion construct or call use.

## A. Software correctness and security

**Unit tests:** PCM WAV parser (valid header, malformed/truncated, wrong codec/bit depth/channel/rate); maximum byte and duration enforcement; window boundaries and final partial interval; digital silence to `unknown`; model output schema and non-finite values; error-to-safe-message mapping; clear-session state and object-URL cleanup. Never commit private voice fixtures.

**Backend integration:** Load the exact pinned model and call the real FastAPI endpoint with a permitted public sample or a synthetic test waveform. Verify actual model code ran, response labels are from the model's documented four classes, scores are finite, and no local file was written. Model cache missing is a setup failure; do not skip the real-model check or substitute a fake and call it passed.

**UI integration/E2E:** A Python Playwright test (if supported by the selected stable dependency versions) launches the local app, selects a generated WAV fixture, confirms the browser sends one request to the API and displays its response, checks invalid/clear states, and does not send a filename. A second manually observed E2E with a permitted RAVDESS file confirms the working demonstration. The synthetic waveform is a wiring test, not an emotion-quality test.

**Security cases:** too large, too long, malformed RIFF chunks, spoofed MIME/extension, missing/truncated body, digital silence, repeated request, concurrent request, model load failure, unexpected `Origin`/`Host`, and a cross-origin browser attempt. Confirm logs and temporary directories do not contain audio, filenames, transcripts, or prediction-linked identity.

## B. Model performance

Use the documented model and class IDs. For RAVDESS, map only angry/happy/neutral/sad, preserve the original four labels, and disclose that other RAVDESS categories are excluded. Split by actor, not random clips. Use development actors only for any temperature scaling or abstention threshold; do not inspect held-out test labels when selecting a threshold. Report accuracy, macro-F1, per-class precision/recall, confusion matrix, class counts, coverage/abstention, and (if meaningful) Brier score and expected calibration error. State whether the public test set is speaker-disjoint and whether the model was trained on a different corpus. Avoid race/accent/demographic performance claims from RAVDESS. [R1, R3, R8]

A fixed five-second app window may cross phrase boundaries and differs from a labeled acted utterance. Report benchmark evaluation at the dataset utterance level separately from app window behavior. Do not call a RAVDESS score an “emergency-call accuracy.” Do not reproduce the model-card IEMOCAP score unless the authorized dataset, fold protocol, preprocessing, and exact model are available and followed. [R3, R10]

## C. Runtime performance

Measure cold model initialization separately from warm inference. Report exact device (CPU/MPS), machine/chip/RAM, macOS, Python, PyTorch/Transformers versions, model revision, audio sample rate, number/duration of windows, median and p95 per-window inference, full-file wall time, and peak memory if available. State concurrency as one request. Do not infer “real-time” from a short sample; compare measured processing time with audio duration and intended interaction. No benchmark has been run in this research step.

## D. Responsible-use checks

Verify the interface uses “estimated vocal-expression pattern,” identifies the model, distinguishes raw uncalibrated score from probability, and visibly disclaims claims about truth, deception, intent, credibility, and guilt. There must be no automated urgency, suspicion, arrest, interrogation, or response decision. Confirm limitations are next to the result, not documentation-only. Test empty, silent, unsupported, corrupt, low-score/ambiguous-if-validated, model/network error, and clearing. Confirm only permitted demo audio is used. [R16, R17, R21]

## Reporting template

For each run: purpose; commit; model ID and immutable revision; dataset/version and license; speaker split manifest; included and omitted classes; exact preprocessing; machine/software; raw commands; metrics and counts; missing data; failure; calibration/threshold method; latency; privacy/security result; and limitations. Never manufacture a metric when the run cannot complete. Mark “not measured” explicitly.
