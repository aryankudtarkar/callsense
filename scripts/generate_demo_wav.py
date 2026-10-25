"""Generate an authorized synthetic test WAV file for demo and verification."""

import io
import math
import wave
from pathlib import Path


def generate_demo_wav(output_path: Path, duration_s: float = 12.0, sample_rate: int = 16000) -> None:
    """Generate a clean synthetic 12-second multi-frequency WAV file.

    Simulates speech-like harmonic frequencies across three 4-second blocks:
    - 0-4s:   220 Hz fundamental (simulated low pitch)
    - 4-8s:   440 Hz fundamental (simulated mid pitch)
    - 8-12s:  330 Hz fundamental (simulated neutral pitch)
    """
    n_samples = int(duration_s * sample_rate)
    frames = bytearray()

    for i in range(n_samples):
        t = i / float(sample_rate)
        if t < 4.0:
            freq = 220.0
        elif t < 8.0:
            freq = 440.0
        else:
            freq = 330.0

        # Primary harmonic + gentle overtone to approximate complex harmonic structure
        sample_val = 0.6 * math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(2 * math.pi * 2 * freq * t)
        int_sample = int(sample_val * 16000)
        # Clamp to 16-bit signed range
        int_sample = max(-32768, min(32767, int_sample))
        frames.extend(int_sample.to_bytes(2, byteorder="little", signed=True))

    with wave.open(str(output_path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(bytes(frames))

    print(f"Generated synthetic demo WAV: {output_path} ({duration_s}s, {sample_rate} Hz, mono PCM16)")


if __name__ == "__main__":
    out_file = Path("demo_sample.wav")
    generate_demo_wav(out_file)
