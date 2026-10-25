# Speech emotion recognition: concepts and evidence

## What the model pipeline does

A microphone or audio file contains sampled pressure changes. A classifier first receives a waveform with a known sample rate and channel layout. A feature-based system may calculate pitch, loudness/energy, pauses, speaking rate, spectral shape, and prosody. A learned system such as Wav2Vec2 first transforms short waveform frames into learned representations, then a task-specific head maps a pooled representation to dataset categories. The chosen model is a Wav2Vec2-base sequence classifier: it produces one categorical result for one supplied audio segment. It does not identify where a natural emotion begins or ends. [R2, R3, R4]

The model's label is best read as “the input resembles examples tagged this way under this dataset and model,” not as direct access to a person's private mental state. An utterance can sound tense, loud, or quiet for reasons unrelated to a single emotion. The model card itself describes a task label and disclaims guaranteed performance on other datasets. Annotation is also affected by the choice of label set, speaker, elicitation, and annotator agreement. [R1, R3, R10]

## Related tasks are different

| Task | Input and output | In this MVP? |
|---|---|---|
| Speech emotion recognition (SER) | Audio patterns to learned vocal-expression categories | Yes; four classes only |
| Automatic speech recognition (ASR) | Audio to words and timestamps | No |
| Speaker identification | Voice to a person's identity | No |
| Speaker diarization | Audio to anonymous speaker-turn labels | No |
| Sentiment analysis | Usually words/text to positive/negative/neutral stance | No |
| Voice activity detection (VAD) | Audio intervals likely containing speech | No separate VAD model |
| Audio event detection | Audio to events such as alarms or impacts | No |

A transcription model or LLM-generated label is not a substitute for audio SER. The coding agent (Gemini through OMP) is separate from the application runtime: the app must call the documented local classifier and must never send call audio to Gemini or another cloud provider. [R3, R23, R24]

## Why the familiar acoustics are only cues

Fundamental frequency and its range, energy, tempo, pausing, voice quality, and spectral information can correlate with how speech was produced. Those measurements are affected by the words spoken, speaker anatomy and habitual style, language, accent, recording distance, microphone, compression, noise, overlap, and how the dataset elicited and labeled an expression. MFCCs and related spectral representations summarize parts of a sound spectrum; self-supervised encoders learn richer representations from large speech corpora. Neither representation makes a label equivalent to psychological truth. [R1, R2]

## Model-family trade-offs

- **Feature + classical ML (for example, acoustic features with SVM):** small model and useful teaching baseline. It requires training and careful speaker-independent splits; no ready checkpoint was selected for this project.
- **CNN/RNN on spectrogram/features:** can learn temporal patterns with moderate compute, but usually needs task-specific training data and a robust evaluation plan.
- **Self-supervised speech encoders (Wav2Vec2, HuBERT, WavLM) with a classifier head:** reuse speech representations and allow actual inference from a pretrained checkpoint. They are the practical fit for this prototype, but their evaluation still depends on the emotion corpus and target conditions. SUPERB demonstrates task-specialized heads on shared speech representations; it does not certify field use. [R2]
- **Emotion-specific pretrained classifiers:** convenient for a demo, but label set, training corpus, license, model-card detail, and inference dependencies must be checked individually. The selected SUPERB model has a particularly small, explicit task contract. [R3]
- **Cloud multimodal or generative models:** not selected. They introduce data disclosure, network dependence, and an unverified substitute for the documented SER task. The coding model is not the runtime model. [R23, R24]

## Segmentation, noise, and calls

SER model cards commonly define one label per utterance. A multi-minute call is not one utterance, so this plan uses fixed, chronological five-second windows for navigation. Each result must be labeled as a window-level model output; it is not a speaker turn, a moment of distress, or a natural emotional event. Overlapping people are mixed acoustically. The MVP does not separate channels, detect speakers, or treat a telephone-specific signal as validated. [R3, R4]

Noise, clipping, silence, sample-rate mismatch, and 8 kHz telephone bandwidth can make input unlike the selected model's 16 kHz training/evaluation audio. Resampling 8 kHz to 16 kHz does not recreate discarded high frequencies. MSP-Podcast v2 is a useful counterexample: it is a large naturalistic corpus, but the lab explicitly excludes voices recorded over 4 kHz telephone bandwidth from its data. [R12]

## Evaluation and epistemic limits

Randomly splitting adjacent clips can let a model exploit speaker or recording similarity. The cross-corpus benchmark recommends speaker-independent evaluation and finds generalization problems across corpora; it also reports that human recognition itself varies with speaker familiarity. Evaluate the pretrained model on an external acted corpus with speaker-disjoint partitions, report classwise metrics and coverage, and call this a limited transfer check—not a validation on Indian callers. [R1]

The model's softmax values are model scores, not calibrated frequencies or truth probabilities. A calibration metric such as expected calibration error or Brier score is only meaningful against an appropriately separated labeled evaluation set. If there is no adequate validation evidence, show the score distribution with an explicit “uncalibrated” label and avoid confidence language. No individual output can establish honesty, deception, intent, credibility, urgency, or guilt. [R1, R3, R17]
