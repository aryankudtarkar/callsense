# Speech Emotion Recognition (SER) Local Prototype

Academic prototype for local speech emotion recognition review using emotion2vec+ on recorded audio.

## Prerequisites

- macOS Apple Silicon (arm64) or compatible Unix environment
- Stable Python 3.14 (`brew install python@3.14`)

## Setup

```bash
python3.14 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
```

## Running Tests

```bash
.venv/bin/python -m pytest
```

## Running Benchmarks

```bash
.venv/bin/python scripts/benchmark.py
```

## Generating Demo Audio Fixture

```bash
.venv/bin/python scripts/generate_demo_wav.py
```
Creates `demo_sample.wav` (12-second synthetic audio) for local browser testing.

## Presentation & Review Guide

See [`docs/DEMO-AND-PRESENTATION-GUIDE.md`](docs/DEMO-AND-PRESENTATION-GUIDE.md) for a comprehensive reviewer walk-through, live demonstration steps, and handling academic questions.

## Running Application

```bash
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000` (or `http://127.0.0.1:8000/analyze` directly) in your web browser.

## Safety & Boundaries

- Single-user local application bound exclusively to loopback (`127.0.0.1`).
- No audio persistence, database storage, logging of audio bytes, or remote cloud inference.
- Displays emotion2vec+ model-estimated vocal-expression labels (`angry`, `disgusted`, `fearful`, `happy`, `neutral`, `other`, `sad`, `surprised`) and `unknown` for silence as uncalibrated model scores.
- Never infers truth, deception, intent, urgency, credibility, or guilt.

## Model Identity & Attribution

- **Model:** `iic/emotion2vec_plus_large` (emotion2vec+), loaded locally through FunASR `AutoModel`.
- **Revision:** The current FunASR/ModelScope loader downloads the upstream `master` default; this project does not pin an immutable model commit or weight hashes. Record the downloaded model revision before comparing runs.
- **Labels:** angry, disgusted, fearful, happy, neutral, other, sad, surprised, unknown. Exact digital silence is handled as `unknown` without model inference.
- **Attribution:** emotion2vec by Ziyang Ma, Zhisheng Zheng, Jiaxin Ye, Jinchao Li, Zhifu Gao, Shiliang Zhang, and Xie Chen; [model card](https://huggingface.co/emotion2vec/emotion2vec_plus_large); inference integration by [FunASR](https://github.com/modelscope/FunASR).
- **Model terms:** [FunASR Model Open Source License Agreement v1.1](https://github.com/modelscope/FunASR/blob/main/MODEL_LICENSE) (custom terms, not Apache/MIT). Preserve model name and source/author attribution. Review current terms for the intended deployment before use.
- The class scores are not calibrated probabilities and are not validated for actual distress, telephone calls, or investigative decisions.

## Live Analysis Feasibility Assessment

- **Operating Mode:** Recorded-file analysis only (`audio/wav` and `audio/mpeg`). MP3 is decoded and resampled locally in memory to mono 16 kHz PCM16 before analysis.
- **Live Streaming Status:** Not validated; explicitly deferred.
- **Feasibility Gap Analysis:**
  - The underlying classifier (`iic/emotion2vec_plus_large`) is run over fixed five-second windows; this prototype has not validated incremental streaming behavior.
  - Real-time incremental processing would require causal convolution / attention masks and robust streaming Voice Activity Detection (VAD) to avoid arbitrary boundary cutoffs.
  - Browser microphone capture introduces unnecessary permission and privacy surface without operational justification for a post-call review prototype.
  - No fake live animations or simulated streaming loops are permitted or implemented.

Made with love by Team Elysian. 
