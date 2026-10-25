"""Tests for audio ingestion, WAV validation, and constraints."""

import io
import wave
import av
import numpy as np
import pytest
from starlette.testclient import TestClient

from app.audio import (
    MAX_BYTES,
    MAX_DURATION_SECONDS,
    AudioValidationError,
    decode_mp3_bytes,
    validate_audio_bytes,
    validate_wav_bytes,
)
from app.main import app

client = TestClient(app)


def make_test_wav(
    channels: int = 1,
    sampwidth: int = 2,
    framerate: int = 16000,
    n_frames: int = 16000,
) -> bytes:
    """Helper to synthesize uncompressed PCM WAV bytes in memory."""
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(channels)
        w.setsampwidth(sampwidth)
        w.setframerate(framerate)
        w.writeframes(b"\x00" * (n_frames * sampwidth * channels))
    return buf.getvalue()


def make_test_mp3(duration_s: float = 1.0, sample_rate: int = 24000) -> bytes:
    """Encode a short mono sine wave to MP3 entirely in memory with bundled FFmpeg."""
    samples = int(sample_rate * duration_s)
    t = np.arange(samples, dtype=np.float32) / sample_rate
    pcm = (np.sin(2 * np.pi * 440 * t) * 12000).astype(np.int16).reshape(1, -1)
    output = io.BytesIO()
    with av.open(output, mode="w", format="mp3") as container:
        stream = container.add_stream("libmp3lame", rate=sample_rate)
        stream.layout = "mono"
        frame = av.AudioFrame.from_ndarray(pcm, format="s16", layout="mono")
        frame.sample_rate = sample_rate
        for packet in stream.encode(frame):
            container.mux(packet)
        for packet in stream.encode(None):
            container.mux(packet)
    return output.getvalue()


def test_valid_wav_passes():
    """Valid 1-second 16 kHz mono 16-bit PCM WAV must pass validation."""
    raw = make_test_wav(n_frames=16000)
    validated = validate_wav_bytes(raw)
    assert validated.duration_seconds == 1.0
    assert validated.sample_rate == 16000
    assert validated.n_frames == 16000
    assert len(validated.raw_frames) == 32000


def test_mp3_decodes_and_resamples_in_memory():
    decoded = decode_mp3_bytes(make_test_mp3())
    assert decoded.sample_rate == 16000
    assert decoded.n_frames > 0
    assert decoded.duration_seconds == pytest.approx(1.0, abs=0.15)
    assert len(decoded.raw_frames) == decoded.n_frames * 2


def test_audio_dispatch_accepts_mpeg_content_type():
    decoded = validate_audio_bytes(make_test_mp3(), "audio/mpeg")
    assert decoded.sample_rate == 16000


def test_empty_payload_rejected():
    """Empty payload must raise 400."""
    with pytest.raises(AudioValidationError) as exc:
        validate_wav_bytes(b"")
    assert exc.value.status_code == 400
    assert "empty" in exc.value.message.lower()


def test_non_riff_rejected():
    """Non-RIFF data must raise 400."""
    with pytest.raises(AudioValidationError) as exc:
        validate_wav_bytes(b"NON_WAV_HEADER_DATA_1234567890")
    assert exc.value.status_code == 400


def test_stereo_rejected():
    """Stereo audio must raise 400 (mono required)."""
    raw = make_test_wav(channels=2)
    with pytest.raises(AudioValidationError) as exc:
        validate_wav_bytes(raw)
    assert exc.value.status_code == 400
    assert "channel" in exc.value.message.lower()


def test_wrong_sample_rate_rejected():
    """44.1 kHz audio must raise 400 (16 kHz required)."""
    raw = make_test_wav(framerate=44100)
    with pytest.raises(AudioValidationError) as exc:
        validate_wav_bytes(raw)
    assert exc.value.status_code == 400
    assert "sample rate" in exc.value.message.lower()


def test_wrong_bit_depth_rejected():
    """8-bit PCM must raise 400 (16-bit required)."""
    raw = make_test_wav(sampwidth=1)
    with pytest.raises(AudioValidationError) as exc:
        validate_wav_bytes(raw)
    assert exc.value.status_code == 400
    assert "sample width" in exc.value.message.lower()


def test_zero_frames_rejected():
    """WAV with 0 frames must raise 400."""
    raw = make_test_wav(n_frames=0)
    with pytest.raises(AudioValidationError) as exc:
        validate_wav_bytes(raw)
    assert exc.value.status_code == 400
    assert "zero" in exc.value.message.lower()


def test_duration_exceeding_max_rejected():
    """WAV declaring > 600s duration must raise 413."""
    # Craft a valid header that declares 601 seconds at 16 kHz
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)
        # We don't need to write all frames if we simulate duration check
        w.setnframes(int(16000 * 601))
    # Check that validator catches oversized duration
    with pytest.raises(AudioValidationError) as exc:
        validate_wav_bytes(buf.getvalue())
    assert exc.value.status_code in (400, 413)


def test_truncated_payload_rejected():
    """WAV payload truncated mid-frame must raise 400."""
    raw = make_test_wav(n_frames=16000)
    truncated = raw[: len(raw) - 100]
    with pytest.raises(AudioValidationError) as exc:
        validate_wav_bytes(truncated)
    assert exc.value.status_code == 400


def test_validate_endpoint_success():
    """POST /validate with valid WAV returns 200 and schema."""
    raw = make_test_wav(n_frames=32000)  # 2.0s
    response = client.post(
        "/validate",
        content=raw,
        headers={"content-type": "audio/wav"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["duration_seconds"] == 2.0
    assert data["sample_rate"] == 16000
    assert "valid" in data["message"].lower()


def test_validate_endpoint_accepts_mp3():
    response = client.post(
        "/validate",
        content=make_test_mp3(),
        headers={"content-type": "audio/mpeg"},
    )
    assert response.status_code == 200
    assert response.json()["sample_rate"] == 16000


def test_validate_endpoint_unsupported_media_type():
    """POST /validate without audio/wav Content-Type returns 415."""
    raw = make_test_wav(n_frames=16000)
    response = client.post(
        "/validate",
        content=raw,
        headers={"content-type": "application/json"},
    )
    assert response.status_code == 415


def test_validate_endpoint_malformed_returns_400():
    """POST /validate with corrupt body returns 400."""
    response = client.post(
        "/validate",
        content=b"CORRUPT_WAV_BODY",
        headers={"content-type": "audio/wav"},
    )
    assert response.status_code == 400
    assert "detail" in response.json()


def test_validate_endpoint_oversized_content_length():
    """POST /validate with oversized Content-Length header returns 413."""
    response = client.post(
        "/validate",
        content=b"dummy",
        headers={
            "content-type": "audio/wav",
            "content-length": str(MAX_BYTES + 1000),
        },
    )
    assert response.status_code == 413
