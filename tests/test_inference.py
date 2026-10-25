"""Integration tests for real emotion2vec+ SER model inference."""

import io
import math
import wave
import numpy as np
import pytest
import av
from starlette.testclient import TestClient

from app.classifier import (
    MODEL_ID,
    MODEL_REVISION,
    ClassificationResult,
    get_classifier,
)
from app.main import app

client = TestClient(app)


def make_tone_wav(duration_s: float = 1.0, freq: float = 440.0) -> bytes:
    """Synthesize a pure sine wave PCM16 mono WAV."""
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


def make_tone_mp3(duration_s: float = 1.0, freq: float = 440.0) -> bytes:
    """Synthesize and encode a mono MP3 entirely in memory."""
    sample_rate = 24000
    t = np.arange(int(sample_rate * duration_s), dtype=np.float32) / sample_rate
    pcm = (np.sin(2 * np.pi * freq * t) * 12000).astype(np.int16).reshape(1, -1)
    buf = io.BytesIO()
    with av.open(buf, mode="w", format="mp3") as container:
        stream = container.add_stream("libmp3lame", rate=sample_rate)
        stream.layout = "mono"
        frame = av.AudioFrame.from_ndarray(pcm, format="s16", layout="mono")
        frame.sample_rate = sample_rate
        for packet in stream.encode(frame):
            container.mux(packet)
        for packet in stream.encode(None):
            container.mux(packet)
    return buf.getvalue()


def test_classifier_loads_and_infers():
    """Verify that the real model loads and produces finite scores for an input."""
    classifier = get_classifier()
    t = np.linspace(0, 1.0, 16000, endpoint=False, dtype=np.float32)
    waveform = 0.5 * np.sin(2 * np.pi * 440.0 * t)

    result = classifier.classify_waveform(waveform, sample_rate=16000)
    assert isinstance(result, ClassificationResult)
    assert result.model_id == MODEL_ID
    assert result.model_revision == MODEL_REVISION
    expected_labels = {
        "angry", "disgusted", "fearful", "happy", "neutral",
        "other", "sad", "surprised", "unknown",
    }
    assert result.predicted_label in expected_labels
    assert result.predicted_dataset_label in expected_labels
    assert set(result.scores.keys()) == expected_labels
    for label, score in result.scores.items():
        assert math.isfinite(score)


def test_classifier_digital_silence_returns_unknown():
    """Exact digital silence must yield unknown label without error."""
    classifier = get_classifier()
    silent_waveform = np.zeros(16000, dtype=np.float32)
    result = classifier.classify_waveform(silent_waveform, sample_rate=16000)
    assert result.predicted_label == "unknown"
    assert result.predicted_dataset_label == "unknown"


def test_analyze_endpoint_real_inference():
    """POST /analyze must perform genuine inference and return expected response."""
    wav_bytes = make_tone_wav(duration_s=1.0)
    response = client.post(
        "/analyze",
        content=wav_bytes,
        headers={"content-type": "audio/wav"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["model_id"] == MODEL_ID
    assert data["model_revision"] == MODEL_REVISION
    assert len(data["segments"]) == 1
    seg = data["segments"][0]
    assert seg["label"] in {
        "angry", "disgusted", "fearful", "happy", "neutral",
        "other", "sad", "surprised", "unknown",
    }
    assert data["scores_label"] == "uncalibrated model scores"
    assert set(seg["scores"]) == {
        "angry", "disgusted", "fearful", "happy", "neutral",
        "other", "sad", "surprised", "unknown",
    }
    assert "notice" in data


def test_analyze_endpoint_real_mp3_inference():
    """MP3 upload must be decoded locally and reach the real emotion2vec+ model."""
    response = client.post(
        "/analyze",
        content=make_tone_mp3(),
        headers={"content-type": "audio/mpeg"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["model_id"] == MODEL_ID
    assert data["sample_rate"] == 16000
    assert len(data["segments"]) == 1
    assert data["segments"][0]["status"] == "classified"
    assert "fearful" in data["segments"][0]["scores"]


def test_analyze_endpoint_unsupported_media_type():
    """POST /analyze with wrong media type must return 415."""
    response = client.post(
        "/analyze",
        content=b"dummy",
        headers={"content-type": "text/plain"},
    )
    assert response.status_code == 415


def test_analyze_endpoint_malformed_returns_400():
    """POST /analyze with corrupted bytes must return 400."""
    response = client.post(
        "/analyze",
        content=b"NOT_A_VALID_WAV",
        headers={"content-type": "audio/wav"},
    )
    assert response.status_code == 400
