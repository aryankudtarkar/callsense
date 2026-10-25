"""Tests for chronological 5-second window segmentation and results."""

import io
import math
import wave
import numpy as np
import pytest
from starlette.testclient import TestClient

from app.classifier import get_classifier
from app.main import app
from app.segmentation import (
    WINDOW_DURATION_SECONDS,
    process_audio_segments,
)

client = TestClient(app)


def make_tone_wav(duration_s: float = 6.0, freq: float = 440.0) -> bytes:
    """Synthesize multi-second WAV."""
    sample_rate = 16000
    n_samples = int(sample_rate * duration_s)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        frames = bytearray()
        for i in range(n_samples):
            val = int(16000 * math.sin(2 * math.pi * freq * (i / sample_rate)))
            frames.extend(val.to_bytes(2, byteorder="little", signed=True))
        w.writeframes(bytes(frames))
    return buf.getvalue()


def test_segmentation_12s_audio():
    """12.0s audio yields two 5s windows and one 2s classified partial window."""
    classifier = get_classifier()
    t = np.linspace(0, 12.0, 12 * 16000, endpoint=False, dtype=np.float32)
    waveform = 0.5 * np.sin(2 * np.pi * 440.0 * t)

    segments = process_audio_segments(waveform, sample_rate=16000, classifier=classifier)
    assert len(segments) == 3

    assert segments[0].start_seconds == 0.0
    assert segments[0].end_seconds == 5.0
    assert segments[0].status == "classified"
    assert segments[0].label in ("neutral", "happy", "angry", "sad")

    assert segments[1].start_seconds == 5.0
    assert segments[1].end_seconds == 10.0
    assert segments[1].status == "classified"

    assert segments[2].start_seconds == 10.0
    assert segments[2].end_seconds == 12.0
    assert segments[2].status == "classified"


def test_segmentation_too_short_tail():
    """5.5s audio yields one 5s classified window and one 0.5s too-short window."""
    classifier = get_classifier()
    t = np.linspace(0, 5.5, int(5.5 * 16000), endpoint=False, dtype=np.float32)
    waveform = 0.5 * np.sin(2 * np.pi * 440.0 * t)

    segments = process_audio_segments(waveform, sample_rate=16000, classifier=classifier)
    assert len(segments) == 2

    assert segments[0].start_seconds == 0.0
    assert segments[0].end_seconds == 5.0
    assert segments[0].status == "classified"

    assert segments[1].start_seconds == 5.0
    assert segments[1].end_seconds == 5.5
    assert segments[1].status == "too_short"
    assert segments[1].label == "unknown"


def test_segmentation_exact_silence():
    """5.0s digital silence yields one silent window with unknown label."""
    classifier = get_classifier()
    waveform = np.zeros(5 * 16000, dtype=np.float32)

    segments = process_audio_segments(waveform, sample_rate=16000, classifier=classifier)
    assert len(segments) == 1
    assert segments[0].status == "silent"
    assert segments[0].label == "unknown"


def test_analyze_endpoint_returns_segmented_timeline():
    """POST /analyze returns chronological timeline of windows."""
    raw = make_tone_wav(duration_s=7.0)
    response = client.post(
        "/analyze",
        content=raw,
        headers={"content-type": "audio/wav"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "segments" in data
    assert data["window_duration_seconds"] == WINDOW_DURATION_SECONDS
    assert len(data["segments"]) == 2
    assert data["segments"][0]["start_seconds"] == 0.0
    assert data["segments"][0]["end_seconds"] == 5.0
    assert data["segments"][1]["start_seconds"] == 5.0
    assert data["segments"][1]["end_seconds"] == 7.0
