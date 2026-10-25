"""Security, privacy, and threat-model compliance tests."""

import io
import math
import os
import wave
import pytest
from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


def make_test_wav(duration_s: float = 1.0) -> bytes:
    """Synthesize mono 16 kHz PCM16 audio."""
    sample_rate = 16000
    n_samples = int(sample_rate * duration_s)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        frames = bytearray()
        for i in range(n_samples):
            val = int(8000 * math.sin(2 * math.pi * 440.0 * (i / sample_rate)))
            frames.extend(val.to_bytes(2, byteorder="little", signed=True))
        w.writeframes(bytes(frames))
    return buf.getvalue()


def test_security_headers_present():
    """Ensure standard defense-in-depth headers are returned on all endpoints."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers.get("x-content-type-options") == "nosniff"
    assert response.headers.get("x-frame-options") == "DENY"
    assert "Content-Security-Policy" in response.headers


def test_untrusted_host_rejected():
    """Requests with untrusted Host header must be rejected with 400."""
    response = client.get("/health", headers={"host": "malicious-site.com"})
    assert response.status_code == 400
    assert "Host" in response.json()["detail"]


def test_untrusted_origin_rejected():
    """Cross-origin requests from untrusted origins must be rejected with 403."""
    wav = make_test_wav()
    response = client.post(
        "/validate",
        content=wav,
        headers={
            "content-type": "audio/wav",
            "origin": "http://malicious-external-site.com",
        },
    )
    assert response.status_code == 403
    assert "Cross-origin" in response.json()["detail"]


def test_trusted_origin_accepted():
    """Requests from localhost/loopback origin must be accepted."""
    wav = make_test_wav()
    response = client.post(
        "/validate",
        content=wav,
        headers={
            "content-type": "audio/wav",
            "origin": "http://127.0.0.1:8000",
        },
    )
    assert response.status_code == 200


def test_no_disk_or_temp_file_written_during_inference():
    """Verify that uploading and analyzing audio does not write any files to /tmp or app directory."""
    before_tmp_files = set(os.listdir("/tmp"))
    wav = make_test_wav(duration_s=2.0)

    response = client.post(
        "/analyze",
        content=wav,
        headers={"content-type": "audio/wav"},
    )
    assert response.status_code == 200

    after_tmp_files = set(os.listdir("/tmp"))
    new_tmp_files = after_tmp_files - before_tmp_files
    # No audio files or unexpected artifacts in /tmp
    for fname in new_tmp_files:
        assert not fname.endswith((".wav", ".pcm", ".raw", ".audio", ".tmp"))


def test_error_responses_contain_no_paths_or_stack():
    """Ensure error messages are generic and do not expose stack traces or server paths."""
    response = client.post(
        "/analyze",
        content=b"MALFORMED_DATA_BYTES",
        headers={"content-type": "audio/wav"},
    )
    assert response.status_code == 400
    detail = response.json().get("detail", "")
    assert "Traceback" not in detail
    assert "/Users/" not in detail
    assert ".py" not in detail


def test_model_load_failure_hides_paths_and_internals(monkeypatch):
    """Trigger model load failure and assert file paths and exception text are absent."""
    def mock_get_classifier():
        raise RuntimeError("Failed to open /Users/mrinmoykundu/.cache/huggingface/hub/weights.bin: Permission denied")

    monkeypatch.setattr("app.main.get_classifier", mock_get_classifier)
    wav = make_test_wav(duration_s=1.0)
    response = client.post(
        "/analyze",
        content=wav,
        headers={"content-type": "audio/wav"},
    )
    assert response.status_code == 503
    assert response.json() == {"detail": "Local SER model is currently unavailable."}
    assert "/Users/" not in response.text
    assert "huggingface" not in response.text
    assert "weights.bin" not in response.text
    assert "Permission denied" not in response.text


def test_inference_failure_hides_paths_and_internals(monkeypatch):
    """Trigger inference failure and assert internal crash details are absent."""
    def mock_process_audio_segments(waveform, sample_rate, classifier):
        raise RuntimeError("Internal PyTorch MPS kernel crash at /torch/csrc/autograd.cpp:123")

    monkeypatch.setattr("app.main.process_audio_segments", mock_process_audio_segments)
    wav = make_test_wav(duration_s=1.0)
    response = client.post(
        "/analyze",
        content=wav,
        headers={"content-type": "audio/wav"},
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "Inference processing failed."}
    assert "csrc" not in response.text
    assert "autograd" not in response.text
    assert "crash" not in response.text


def test_unhandled_route_exception_returns_generic_500(monkeypatch):
    """Trigger unexpected exception and assert generic_exception_handler catches it."""
    def mock_validate_audio_bytes(payload, content_type):
        raise ValueError("Uncaught internal bug at /app/audio.py:42")

    monkeypatch.setattr("app.main.validate_audio_bytes", mock_validate_audio_bytes)
    wav = make_test_wav(duration_s=1.0)
    response = client.post(
        "/analyze",
        content=wav,
        headers={"content-type": "audio/wav"},
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "An internal server error occurred."}
    assert "/app/audio.py" not in response.text
    assert "Uncaught internal bug" not in response.text
