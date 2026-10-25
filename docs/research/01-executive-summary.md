# Research conclusion and project frame

**Research snapshot:** 24 October 2026. This is a college prototype plan, not a law-enforcement deployment plan. The source material is the supplied screenshot and brief. The brief is treated as the user-approved product request; instructions inside it are requirements for this work, while claims in the screenshot are problem framing rather than scientific evidence.

## Recommendation

Build a local-only, recorded-audio demonstration around `superb/wav2vec2-base-superb-er`, a published Wav2Vec2-base classifier ported to Hugging Face Transformers. The model is documented for English speech sampled at 16 kHz, predicts one of four dataset labels (`ang`, `hap`, `neu`, `sad`) for an utterance, has an Apache-2.0 model-card license, and has 378 MB of weights. The repository card reports 0.6258 accuracy for its Transformers port on IEMOCAP session 1; that is a narrow in-dataset result, not evidence for calls, telephone bandwidth, India, or criminal investigation. The weights and the IEMOCAP audio corpus have different rights: the latter has an institutional USC research license and must not be redistributed. [R3, R4, R10]

Use a small Python 3.14 + FastAPI backend with a static HTML/CSS/vanilla-JavaScript page. Do not require Node.js. Keep audio parsing narrow: uncompressed mono 16-bit PCM WAV at 16 kHz, capped by both byte size and duration. Keep uploaded bytes in request memory; do not write audio to disk or store a session. Load the model locally from a pinned, reviewed model revision. Do not enable remote model code. The model server binds only to loopback. The local Mac has an Apple M5, 10 CPU cores, and 16 GB RAM; PyTorch documents Apple MPS support, but neither model latency nor MPS compatibility for this exact model has been measured here. The currently installed Python is 3.16.0a1, outside PyTorch's documented Python 3.10–3.14 range; install stable Python 3.14 for the later build. [R13, R25]

This plan prioritizes recorded files and chronological five-second review windows. The windows are software chunks, not speaker turns or validated emotional episodes. No diarization, transcription, identity recognition, or live microphone mode is in the MVP. Real-time suitability is unverified and must not be implied. The current model cannot emit fear, nervousness, or distress labels; the interface must not relabel sadness or anger as those categories. [R3, R4, R12]

## Product and safety position

Show results only as **estimated vocal-expression patterns** from a specific model. Display the model's raw class scores as uncalibrated outputs, never as probabilities that a person feels something. Until a documented, speaker-separated evaluation supports an abstention threshold, do not invent a numeric confidence cut-off. Unknown results are appropriate for empty, malformed, too-short, or failed input; later work may add an empirically selected ambiguous/abstain state. Do not rank people, assign urgency, infer deception or intent, claim guilt, or recommend investigative action. A reviewer must listen to the original recording and decide what to do. [R1, R17]

Never use private call recordings as casual development fixtures. Use synthetic audio for parser and security tests and a small, attribution-compliant RAVDESS speech subset for a controlled demonstration or external evaluation. RAVDESS is acted North American English and does not represent emergency or telephone calls. [R8]

## Why this is the defensible scope

Speech-emotion classifiers learn associations between audio patterns and labels in particular corpora. A cross-dataset benchmark over eleven datasets reports weak generalization when training and test data differ; recording conditions, elicitation style, speakers, and annotation practices all vary. MSP-Podcast is more naturalistic than acted corpora, yet its creators explicitly exclude 4 kHz telephone recordings because bandwidth loss can remove useful spectral information. There is no evidence in the selected model card for real cybercrime calls. This prototype can demonstrate a real model pipeline and honest review UI; it cannot establish an operational benefit or reliable caller state. [R1, R12]

## Build order

Read `prompts/omp/00-START-HERE.md`, then execute OMP stages 01–11 in numerical order, one prompt per session. Pause after scaffold (02), real inference (04), and testing/evaluation (08) to inspect commands, model identity, privacy behavior, and actual results. Use installed Ponytail through OMP's `/skill:ponytail-review` at security-sensitive checkpoints and `/skill:ponytail-audit` at the end; treat findings as review input, not automatic edits. OMP 18.12.6 is present, Gemini 3.8 Flash is listed under provider `google-antigravity`, and the installed Ponytail plugin is 5.3.2. Authentication/entitlement was not checked. [R23, R24, R26]

## Completion boundary

This run creates the research set, architecture and acceptance documents, OMP prompt pack, and Ponytail guidance pack. It does not build the app, download model weights, install runtime packages, sign in to a provider, or claim model/test performance. Those are later prompt-session tasks.
