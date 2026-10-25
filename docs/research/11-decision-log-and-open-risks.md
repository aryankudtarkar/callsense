# Decision log and open risks

| ID | Decision | Alternatives considered | Reason / evidence | Remaining uncertainty |
|---|---|---|---|---|
| D1 | Use `superb/wav2vec2-base-superb-er` as the primary local runtime model | SpeechBrain IEMOCAP; audEERING dimensional model; emotion2vec+; feature/SVM | Simple standard Transformers class, Apache model-card license, explicit 16 kHz input, four documented labels, 378 MB, real inference support. | No independent call/telephone benchmark; model card's Transformers score is only 0.6258 on session1. Need exact revision pin and local integration. [R3, R4] |
| D2 | Narrow label set to angry/happy/neutral/sad | Screenshot categories fear/distress/nervousness; use more general LLM outputs | The selected model only has these four output classes. Relabeling would fabricate capabilities. | These labels remain dataset categories, not ground-truth feelings. [R3, R4] |
| D3 | Local-only inference, Python-only stack | Node/React UI, cloud model API, DB/auth | Empty repo, Node absent, M5/16 GB, runtime privacy, smallest single-user build. | PyTorch/Transformers install and MPS behavior must be verified with Python 3.14. [R13, R25] |
| D4 | WAV-only input: mono PCM16, 16 kHz | MP3, phone-law/G.711, arbitrary media conversion | Standard-library parser and exact model sample rate avoid a new codec pipeline and unverified FFmpeg requirement. | Narrow usability; 8 kHz call recordings rejected. Format conversion is out of MVP. [R4, R15] |
| D5 | Five-second chronological windows; no separate VAD or speaker diarization | Whole-call label; natural turn segmentation; diarization | Makes a navigable recorded demonstration without claiming speaker identity or using an unverified segmentation model. | Fixed windows may split speech, mix speakers, include silence, and differ from utterance training. Must be labeled as model windows. [R3, R12] |
| D6 | No live mic/streaming in initial prototype | WebRTC/MPS real-time inference | No local timing evidence, model is utterance-level, no live architecture selected. | Prompt 06 permits reconsideration only after real end-to-end latency and privacy evidence. |
| D7 | No saved calls, sessions, reports, or database | Case-management/export features | Sensitive audio and unvalidated labels; no evidence purpose; local in-memory flow suffices. | RAM/swap and operating-system artifacts cannot be erased by app UI. No evidentiary integrity. |
| D8 | Use RAVDESS as optional public evaluation/demo corpus | IEMOCAP training benchmark, CREMA-D, MSP-Podcast | RAVDESS has clearly stated CC BY attribution terms and actor metadata; manageable four-class external check. | Acted English, only 24 actors; map/exclude classes and split by speaker. [R8, R1] |
| D9 | Use Gemini 3.8 Flash only as OMP coding agent; use Ponytail only for coding guidance/review | Cloud SER, LLM label, external review service | Differentiate developer model from app model. OMP catalog lists the Gemini model; local Ponytail plugin is 5.3.2. | Authentication/entitlement not tested. OMP docs/skill command surface can change. [R23, R24, R26] |
| D10 | Treat legal status conservatively and date-stamp it | Assume DPDP Act fully operative; treat investigation exemption as blanket authority | Gazette commencement notifications are phased; section 17 is not yet operative on snapshot date. | Legal review required for any actual call source, agency, state, jurisdiction, or later deployment. [R20–R22] |

## Risks ranked

1. **Construct validity:** model label is not an observed internal emotion and is not evidence of truth, deception, intent, credibility, or guilt.
2. **Domain shift:** no evaluation on real Indian/telephone/cybercrime calls; selected training source and available evaluation corpora differ.
3. **Misuse/overreliance:** visual status or softmax output may appear more certain/actionable than it is.
4. **Privacy/legal:** call capture and lawful processing are context-specific; local processing does not create authorization.
5. **Technical:** model loading, CPU/MPS latency, Python wheel availability, WAV limitations, and fixed-window distortions are unmeasured.
6. **Data rights:** model weights and source corpus have separate terms; RAVDESS/IEMOCAP/CREMA-D/MSP terms cannot be conflated.
7. **Reproducibility:** immutable checkpoint hash, package lock, evaluation manifest, and downloaded dataset are not created yet.

## Open questions to settle during later build

- What exact immutable Hugging Face commit for the SUPERB model will be pinned, and do weight hashes match the official repository?
- Can current stable Python 3.14/PyTorch/Transformers wheels install cleanly on the user's M5/macOS 27 environment?
- Does CPU or MPS inference finish within an acceptable recorded-file workflow, and what is measured cold/warm performance?
- Can the student lawfully obtain and cite the selected RAVDESS speech subset, and what exact actor split will be recorded?
- Do any later changes justify a validated abstention threshold? If not, retain uncalibrated score wording and abstain only for explicit input/model failures.
- Does local browser/E2E tooling work without adding a Node-based build or a model stub to the accepted path?
