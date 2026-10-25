# SER Prototype — Demo & Presentation Guide

This guide is designed for presenting the Speech Emotion Recognition (SER) local prototype to academic reviewers, instructors, and stakeholders.

## 1. Core Presentation Message

> **"This is an engineering prototype demonstrating local audio ingestion and classification using emotion2vec+. It is a review navigation aid, NOT a lie detector, guilt detector, or emotion truth system."**

### Critical Distinctions to State Upfront:
1. **Software Pipeline vs. Scientific Model Validity:**
   - The *software pipeline* accepts WAV and MP3 uploads in memory, converts MP3 locally to the model's input format, and uses chronological 5-second windows on the loopback-only service. Audio is not persisted.
   - The *model validity* is domain-limited: `iic/emotion2vec_plus_large` outputs are not validated here for telephone bandwidth, real emergency calls, Indian English, or regional languages.
2. **Output Semantics:**
   - The model predicts **angry, disgusted, fearful, happy, neutral, other, sad, surprised**; silence is shown as `unknown`.
   - These are **uncalibrated model scores**, not probabilities that a caller actually feels an emotion.
   - The system **never** predicts truth, deception, intent, urgency, credibility, or guilt.

---

## 2. Step-by-Step Live Demonstration Script

### Step 1: Environment & Health Verification
Show that the application is running strictly on local loopback:
```bash
# Terminal 1: Run local server
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# Terminal 2: Verify health endpoint
curl -s http://127.0.0.1:8000/health
# Response: {"status":"ok","app":"ser-prototype"}
```

### Step 2: Open Browser Interface
- Navigate to `http://127.0.0.1:8000`.
- Highlight the **Operating Mode badge**: *"Mode: Recorded-File Analysis Only (Live mode is not validated)"*.
- Highlight the **Responsible Use Notice**: Emphasize that audio stays in memory and model outputs are navigation aids, not legal evidence.

### Step 3: Run Synthetic Demo
- Generate or select the synthetic test recording:
  ```bash
  .venv/bin/python scripts/generate_demo_wav.py
  ```
- In the browser, click **Choose File** and select `demo_sample.wav`.
- The browser audio preview player will appear. Press Play to demonstrate local browser audio preview.
- Check the mandatory affirmation box: *"I confirm I am legally authorized to analyze this recording..."*.
- Click **Analyze recording**.

### Step 4: Review Chronological Timeline
- Observe the generated chronological review timeline:
  - Three distinct 5-second windows: `[0.00s - 5.00s]`, `[5.00s - 10.00s]`, and `[10.00s - 12.00s]`.
  - For each window, point out:
    - Estimated vocal-expression label (`happy`, `angry`, `neutral`, `sad`, or `unknown`).
    - Raw uncalibrated model scores grid.
    - Play button (`▶ Play from Xs`): click it to show how an investigator seeks directly to that segment in the original local audio without server roundtrip.
  - Show the model metadata footer: model ID, note that the upstream revision is not pinned, and execution device.

### Step 5: Test Clear Session
- Click **Clear session**.
- Demonstrate that all local UI state, audio preview object URL, and displayed segments are instantly revoked and reset.
- Explain that no session, temporary file, or audio data remains on the server.

---

## 3. Anticipated Reviewer Q&A

**Q: Can this detect if a scammer or victim is lying or nervous?**
> *Answer:* No. The model estimates one of its vocal-expression categories. It has no capability to measure truth, deception, nervousness, or intent. Claiming lie detection from audio classifiers is scientifically unfounded.

**Q: Why not use a cloud LLM like Gemini or Claude to analyze the audio?**
> *Answer:* Privacy and legal compliance. In call analysis, transmitting audio to external commercial APIs risks exposing personal identifiers and violating data protection boundaries (e.g., India's DPDP Act provisions). Our local architecture ensures audio never leaves bounded device memory.

**Q: How fast does it run? Is it real-time?**
> *Answer:* On Apple Silicon M5, inference takes ~52 ms per 5-second window on MPS (Real-Time Factor ~0.0104, ~96x faster than real-time), and ~148 ms on CPU (~34x faster). However, we deliberately defer live microphone mode because the model was trained on complete utterances, not streaming audio frames, and true live operation requires streaming VAD to avoid arbitrary boundary cutoffs.

**Q: Where can I get real speech samples for testing?**
> *Answer:* Under our research protocol, confidential police call recordings are strictly forbidden. Use only audio that is authorized for analysis, and evaluate against suitable permitted data with an explicitly documented label mapping and speaker-disjoint protocol.
