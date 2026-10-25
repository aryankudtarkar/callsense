# System architecture decision

## Selected architecture

```text
Browser page (static HTML/CSS/vanilla JS)
  ├── local file picker + local audio preview + Clear Session
  └── POST raw WAV or MP3 bytes to same-origin loopback API
          ↓
Python 3.14 / FastAPI, bound to 127.0.0.1
  ├── bounded request-body reader; no multipart/temp-file spool
  ├── WAV validation or PyAV MP3 decode/resample (in-memory)
  ├── chronological, non-overlapping five-second windows
  └── PyTorch + Transformers → pinned SUPERB Wav2Vec2 ER model
          ↓
  JSON: time range, exact model label, uncalibrated class scores, safe state
```

The UI is plain HTML/CSS/JavaScript served by FastAPI, avoiding Node because Node is not installed and the UI does not need a build system. FastAPI is a single local process serving static files and one bounded analysis endpoint. No database, persistent audio directory, third-party API, transcript model, authentication platform, cloud deployment, or additional model is justified for this single-user demo.

## Model and segment contract

Model: `superb/wav2vec2-base-superb-er`, pinned by immutable Hub revision plus weight hashes. Load the model/feature extractor once, eval mode, `trust_remote_code=False`. Input is normalized float waveform at exactly 16 kHz, mono. The model card labels one utterance; app windows are five-second transport/review slices, not natural emotion boundaries. The final partial window is analyzed only if at least one second; exact digital silence is returned as unknown. Do not claim this simple silence check detects speech or noise. [R3, R4]

Response shape is narrow and typed: `model_id`, `model_revision`, `sample_rate`, `duration_seconds`, and ordered `segments[{start_seconds,end_seconds,status,label,scores}]`. `label` must be one of `ang`, `hap`, `neu`, `sad`, or `unknown`; scores are raw finite class scores with a UI label saying “uncalibrated.” No person ID, voiceprint, transcript, or guilt/urgency field exists. Do not expose stack traces or file system paths.

## Audio lifecycle

Browser retains selected `File` and `ObjectURL` only for preview until the user clears or leaves the page. The API receives raw WAV or MP3 bytes, bounded while streaming into memory; no user filename or multipart upload. Validate actual WAV fields, or decode MP3 bytes with PyAV and resample to mono PCM16 at 16 kHz in memory. Enforce byte/duration limits and release audio references after response. Return no stored session ID. The model weight cache may persist, but audio and results do not. RAM/swap/crash-dump erasure is not promised. [R14, R15]

## Local security boundary

Serve and bind to `127.0.0.1` only. Serve UI and API from one origin; do not enable wildcard CORS. Require expected local `Host` and `Origin` for analysis; reject cross-origin browser requests. Accept only `audio/wav` and `audio/mpeg`; enforce byte count on the actual streamed body, not only Content-Length. Never use client filenames as server paths or logged values. Limit one long inference request at a time. Error messages are generic and actionable. [R15]

## Device policy and known gaps

Ship CPU-safe inference first. At runtime, MPS may be offered only if PyTorch reports it available and the exact model passes a real classification smoke test; report CPU or MPS in benchmark metadata. Apple Silicon's MPS backend is documented, but supported kernels and actual latency need measurement. Do not promise real-time response. There is no browser microphone or continuous streaming mode until the actual end-to-end pipeline has a measured latency budget and privacy review. [R13]

## Stack and run contract

Use stable Python 3.14 (PyTorch's current macOS install guidance recommends Python 3.10–3.14), a project-local `.venv`, FastAPI, Uvicorn, PyTorch, Transformers, NumPy, pytest, HTTPX/TestClient, and Python Playwright only for optional browser E2E. Verify current wheel compatibility during scaffold; avoid invented version pins. Use `pyproject.toml` as dependency/command source. Canonical commands after scaffold: `.venv/bin/python -m pytest`; `.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000`; browser `http://127.0.0.1:8000`. First inference needs model weights; report failure if download or model loading fails. [R13, R25]
