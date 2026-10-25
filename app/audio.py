"""In-memory WAV validation for bounded 16 kHz mono PCM16 audio."""

import io
import wave
from dataclasses import dataclass

import av
import numpy as np

MAX_BYTES = 20 * 1024 * 1024       # 20 MiB
MAX_DURATION_SECONDS = 600.0        # 10 minutes (600.0s)
REQUIRED_SAMPLE_RATE = 16000
REQUIRED_CHANNELS = 1
REQUIRED_SAMPLE_WIDTH = 2           # 16-bit PCM (2 bytes)


class AudioValidationError(Exception):
    """Raised when audio payload does not satisfy the input contract."""
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


@dataclass
class ValidatedAudio:
    duration_seconds: float
    sample_rate: int
    n_frames: int
    raw_frames: bytes


def validate_wav_bytes(payload: bytes) -> ValidatedAudio:
    """Validate raw WAV bytes strictly in-memory.

    Rejects:
    - Empty payload (400)
    - Oversized payload (> 20 MiB) (413)
    - Non-RIFF / malformed header (400)
    - Unsupported compression (non-PCM) (400)
    - Wrong channel count (not mono) (400)
    - Wrong sample width (not 16-bit) (400)
    - Wrong sample rate (not 16000 Hz) (400)
    - Zero frame count (400)
    - Duration exceeding 10 minutes (413)
    - Truncated frame data (400)
    """
    if not payload:
        raise AudioValidationError("Audio payload is empty.", status_code=400)

    if len(payload) > MAX_BYTES:
        raise AudioValidationError(
            f"Audio payload exceeds maximum size of 20 MiB ({len(payload)} bytes).",
            status_code=413,
        )

    try:
        with wave.open(io.BytesIO(payload), "rb") as w:
            channels = w.getnchannels()
            sampwidth = w.getsampwidth()
            framerate = w.getframerate()
            n_frames = w.getnframes()
            comptype = w.getcomptype()

            if comptype != "NONE":
                raise AudioValidationError(
                    f"Unsupported audio compression '{comptype}'. Only uncompressed PCM is supported.",
                    status_code=400,
                )

            if channels != REQUIRED_CHANNELS:
                raise AudioValidationError(
                    f"Invalid channel count ({channels}). Only mono audio is supported.",
                    status_code=400,
                )

            if sampwidth != REQUIRED_SAMPLE_WIDTH:
                raise AudioValidationError(
                    f"Invalid sample width ({sampwidth * 8}-bit). Only 16-bit PCM is supported.",
                    status_code=400,
                )

            if framerate != REQUIRED_SAMPLE_RATE:
                raise AudioValidationError(
                    f"Invalid sample rate ({framerate} Hz). Exactly 16000 Hz is required.",
                    status_code=400,
                )

            if n_frames <= 0:
                raise AudioValidationError("Audio contains zero audio frames.", status_code=400)

            duration = n_frames / float(framerate)
            if duration > MAX_DURATION_SECONDS:
                raise AudioValidationError(
                    f"Audio duration ({duration:.2f}s) exceeds maximum allowed duration of {MAX_DURATION_SECONDS}s.",
                    status_code=413,
                )

            expected_bytes = n_frames * sampwidth * channels
            raw_frames = w.readframes(n_frames)
            if len(raw_frames) != expected_bytes:
                raise AudioValidationError(
                    f"Audio payload truncated: expected {expected_bytes} frame bytes, found {len(raw_frames)}.",
                    status_code=400,
                )

            return ValidatedAudio(
                duration_seconds=round(duration, 4),
                sample_rate=framerate,
                n_frames=n_frames,
                raw_frames=raw_frames,
            )
    except wave.Error as e:
        raise AudioValidationError(
            f"Malformed or unsupported WAV header: {str(e)}",
            status_code=400,
        ) from e


def decode_mp3_bytes(payload: bytes) -> ValidatedAudio:
    """Decode an MP3 in memory and resample it to the model's mono PCM contract."""
    if not payload:
        raise AudioValidationError("Audio payload is empty.", status_code=400)
    if len(payload) > MAX_BYTES:
        raise AudioValidationError(
            f"Audio payload exceeds maximum size of 20 MiB ({len(payload)} bytes).",
            status_code=413,
        )

    converted_frames = []
    decoded_duration = 0.0
    try:
        with av.open(io.BytesIO(payload), mode="r", format="mp3") as container:
            stream = next((s for s in container.streams if s.type == "audio"), None)
            if stream is None:
                raise AudioValidationError("MP3 contains no audio stream.", status_code=400)

            resampler = av.AudioResampler(format="s16", layout="mono", rate=REQUIRED_SAMPLE_RATE)
            for frame in container.decode(stream):
                source_rate = frame.sample_rate or stream.codec_context.sample_rate
                if not source_rate:
                    raise AudioValidationError("MP3 has no valid sample rate.", status_code=400)
                decoded_duration += frame.samples / float(source_rate)
                if decoded_duration > MAX_DURATION_SECONDS:
                    raise AudioValidationError(
                        "Audio duration exceeds maximum allowed duration of 600 seconds.",
                        status_code=413,
                    )
                converted_frames.extend(resampler.resample(frame))
            converted_frames.extend(resampler.resample(None))
    except AudioValidationError:
        raise
    except (av.error.FFmpegError, ValueError, OSError) as exc:
        raise AudioValidationError("Malformed or unsupported MP3 audio.", status_code=400) from exc

    if not converted_frames:
        raise AudioValidationError("MP3 contains zero decodable audio frames.", status_code=400)

    raw_frames = b"".join(frame.to_ndarray().reshape(-1).astype(np.int16, copy=False).tobytes()
                           for frame in converted_frames)
    n_frames = len(raw_frames) // REQUIRED_SAMPLE_WIDTH
    if n_frames <= 0:
        raise AudioValidationError("MP3 contains zero decodable audio frames.", status_code=400)
    duration = n_frames / float(REQUIRED_SAMPLE_RATE)
    return ValidatedAudio(
        duration_seconds=round(duration, 4),
        sample_rate=REQUIRED_SAMPLE_RATE,
        n_frames=n_frames,
        raw_frames=raw_frames,
    )


def validate_audio_bytes(payload: bytes, content_type: str) -> ValidatedAudio:
    """Validate/decode the supported upload type using its declared media type."""
    if content_type in ("audio/wav", "audio/x-wav"):
        return validate_wav_bytes(payload)
    if content_type in ("audio/mpeg", "audio/mp3", "audio/x-mp3"):
        return decode_mp3_bytes(payload)
    raise AudioValidationError(
        f"Unsupported Content-Type '{content_type}'. Use WAV or MP3 audio.",
        status_code=415,
    )
