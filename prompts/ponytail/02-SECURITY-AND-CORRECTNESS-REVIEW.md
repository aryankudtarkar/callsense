# Security and correctness review checklist

Use this checklist with `/skill:ponytail-review` when available. Review source and synthetic test fixtures only; never provide private call audio to the coding agent. Record each check as **verified**, **failed**, or **not run**, with a file/test reference or reason.

## 1. Request and audio boundary

- Does the server accept only the intended raw WAV request and reject unsupported media types?
- Are the actual RIFF/WAVE header, codec, channel count, sample rate, sample width, frame count, truncation, byte count, and duration checked before inference?
- Is the body cap enforced while reading, including when `Content-Length` is absent or misleading?
- Can malformed headers or oversized input trigger an unbounded allocation, temporary file, crash, or parser exception exposed to the user?
- Are errors generic, useful, and free of file paths, filenames, stack traces, or audio content?
- Are zero/silent and too-short windows handled honestly without pretending to perform voice activity detection?

## 2. Local-only privacy and web controls

- Does the service bind only to `127.0.0.1` and serve UI/API from the same origin?
- Are unexpected `Host`/`Origin` requests rejected where required, with no wildcard CORS?
- Does any code send audio, transcript, predictions, or identifiers to an external service?
- Are audio, user filenames, and results absent from logs, databases, session files, and temp directories?
- Does the browser clear the selected file reference, preview URL, and displayed results when the user clears or leaves the session?
- Do notices explain local processing, model-weight download behavior, limitations, and the user's responsibility to use authorized material?

## 3. Model identity and output contract

- Is the real model ID, immutable revision, file hash, and license recorded? Is `trust_remote_code=False` explicit?
- Does code load the selected Transformers classifier and call it with mono floating-point audio at 16 kHz?
- Is the model initialized once and reused without accepting an arbitrary client-supplied model ID?
- Are class IDs mapped exactly to `ang`, `hap`, `neu`, and `sad`? Do unknown IDs or load failures stop or return an explicit unknown/error state?
- Are raw model values called uncalibrated scores rather than probabilities of what a person feels?
- Is there any fake-success fallback, hardcoded result, random output, keyword rule, transcription sentiment, or LLM label? If so, fail the review.
- Does the UI avoid unsupported labels and claims about distress, urgency, deception, credibility, intent, or guilt?

## 4. Correctness and tests

- Do tests cover valid WAV, wrong sample format, malformed/truncated data, byte/duration bounds, silent/short audio, model failure, and clear-session behavior?
- Is at least one integration check wired through the actual backend to the real classifier, with its availability and result reported separately from synthetic parser tests?
- Are security-sensitive regressions covered without requiring personal audio?
- Are automated tests distinguished from manual browser checks, dataset metrics, and runtime benchmarks?
- Do test results state skipped/unavailable checks honestly?

## 5. Findings and repair

For each finding, write: severity, concrete evidence, user impact, smallest safe repair, and verification. Confirm a finding in code before changing anything. Fix in-scope verified defects and add a regression test when appropriate. If a fix would change the model, legal scope, or user-approved architecture, preserve safe behavior and report the decision needed.

Do not remove validation, privacy safeguards, error handling, accessibility, real inference, or required tests in the name of simplicity. Do not describe this review checklist as a penetration test or legal review.
