# Threat model and security controls

**System boundary:** one user's browser, a loopback FastAPI service, an in-memory audio parser, locally cached model weights, and a locally loaded PyTorch classifier. No database, authentication service, transcription, external inference, deployment server, or cloud storage is in scope.

## Assets and trust boundaries

| Asset | Why it matters | Main boundary |
|---|---|---|
| Uploaded audio | May include identifiable, confidential or legally sensitive voices and conversation content | Browser → local HTTP API → parser/model |
| Results and metadata | Can be misused or mistaken for evidence; filenames/timestamps may identify a case | Backend → page/log/export |
| Model weights and Python packages | Executed parser/model code and supply-chain risk | Public model/package registries → local environment |
| Local service | Can be reached by other local processes and potentially cross-origin browser requests | Browser origin / local network / loopback port |
| Browser audio object URL | Keeps selected audio available in page memory | File picker → page state |

## Threats and mitigations

| Threat | Example | Required mitigation / acceptance check |
|---|---|---|
| Audio disclosure | Uploaded bytes enter logs, temp files, telemetry, or a third-party endpoint | Raw bounded `audio/wav` request body, in-memory parser, no multipart spool, no filename sent, no external inference/analytics, no audio logging. Verify temporary directories and logs remain free of uploaded content. |
| Unauthorized recording/use | A private call is uploaded without an authorized basis | Clear pre-analysis notice and user affirmation; public/synthetic samples only in project docs/tests; technical UI does not claim that checkbox establishes authority. |
| Malformed or oversized file | Crafted RIFF/WAV headers, truncated payload, huge declared frame count, unsupported codec | Enforce content-length and streamed byte cap; verify RIFF/WAVE and actual header fields; allow only PCM16 mono 16 kHz; reject invalid duration/size before model call; return generic safe errors. Do not trust extension or content-type alone. [R15] |
| Resource exhaustion | Many long requests or repeated expensive inference | Max 20 MiB and 10 minutes; one analysis at a time; no request queue/concurrency promise; graceful progress/error; never set an unbounded upload/body parser. Measure exact local pipeline. |
| Local cross-origin access | A malicious website tries to make a browser send audio to localhost | Bind `127.0.0.1`; same-origin UI; no wildcard CORS; reject unexpected `Origin`/`Host`; require non-simple `audio/wav` request; verify with a negative browser request. Do not rely on loopback as an authentication system. |
| Path traversal / filename abuse | A filename overwrites data or appears as HTML | Do not use client filename on the server or in a file path; show escaped local name only if needed; no user-controlled audio downloads. |
| Unsafe model/repository code | A checkpoint enables remote Python code or changes unnoticed | Pin exact model revision and record hashes; use official model ID; keep `trust_remote_code=False`; review any required custom code; separate weight cache from project; no unrestricted model ID input. |
| Sensitive logging | Exceptions include stack, filename, or audio bytes | Do not log request bodies, filename, transcripts, model outputs tied to an identity, or raw exceptions to UI; map known errors to generic codes; keep minimal development logs and document any retained metadata. |
| Malicious content/prompt injection | A future ASR transcript contains instructions to the summarizer | No transcript/LLM in MVP. If later added, mark transcript as untrusted data; do not execute or follow embedded instructions; keep audio/model result types separate from instructions. |
| Prediction misuse | A user interprets anger score as guilt or urgency | Put limitations next to every result; no red emergency colors, auto-alert, people/case ranking, deception labels, or automated action; include a reviewer listen control and human-only decision statement. |
| Bias and overconfidence | System overstates reliability for a population or codec absent from benchmark | Report external speaker-disjoint results and limitations; model scores remain uncalibrated unless measured; abstain only at a documented threshold; no demographic/generalization claims from tiny acted data. [R1, R17] |

## Threat assumptions and non-goals

This local prototype is not multi-user, hardened for hostile local users, or a production police system. The machine owner can inspect process memory, model cache, browser storage, and logs. No cryptographic deletion or evidentiary chain of custody is promised. If remote access, account roles, case exports, or production deployment are later proposed, treat them as a new architecture/security/legal review, not a small extension.

## Verification evidence for the later build

Record a code review and tests for: invalid WAVs, byte cap, duration cap, all-zero audio, model load failure, no network call during inference after model cache is warm, no audio temp file, browser Clear Session behavior, Origin rejection, and generic error handling. Keep this evidence separate from emotion-model accuracy results. OWASP's upload guidance emphasizes allowlisting required file types, content validation, filename safety, and size limits. NIST AI RMF provides a lifecycle structure to map, measure, govern, and manage AI risk; it is guidance, not an India legal standard. [R15, R16, R17]
