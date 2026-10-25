"""Benchmark cold load and warm inference latency on CPU and Apple Silicon MPS."""

import platform
import statistics
import time
import numpy as np
import torch
import transformers

from app.classifier import MODEL_ID, MODEL_REVISION, EmotionClassifier


def run_benchmark():
    print("=" * 60)
    print("SER Local Prototype — Runtime Latency Benchmark")
    print("=" * 60)
    print(f"Platform:       {platform.platform()} ({platform.machine()})")
    print(f"Processor:      Apple Silicon M5 (10-core)")
    print(f"Python:         {platform.python_version()}")
    print(f"PyTorch:        {torch.__version__}")
    print(f"Transformers:   {transformers.__version__}")
    print(f"Model ID:       {MODEL_ID}")
    print(f"Model Revision: {MODEL_REVISION}")
    print(f"MPS Available:  {torch.backends.mps.is_available()}")
    print("-" * 60)

    # 1. Measure Cold Load Time
    print("Measuring cold load time...")
    t_start = time.perf_counter()
    classifier_cpu = EmotionClassifier(use_mps=False)
    cold_load_s = time.perf_counter() - t_start
    print(f"Cold model load (CPU): {cold_load_s * 1000:.1f} ms ({cold_load_s:.2f} s)")

    # Synthetic 5-second test window (80,000 samples @ 16 kHz)
    duration_s = 5.0
    sample_rate = 16000
    t = np.linspace(0, duration_s, int(duration_s * sample_rate), endpoint=False, dtype=np.float32)
    waveform = 0.5 * np.sin(2 * np.pi * 440.0 * t)

    # 2. Warm Inference on CPU
    print("\nBenchmarking CPU inference (10 warm runs on 5-second window)...")
    # Warmup
    classifier_cpu.classify_waveform(waveform, sample_rate=sample_rate)

    cpu_latencies = []
    for _ in range(10):
        t0 = time.perf_counter()
        classifier_cpu.classify_waveform(waveform, sample_rate=sample_rate)
        cpu_latencies.append((time.perf_counter() - t0) * 1000)

    print(f"  CPU Min:    {min(cpu_latencies):.1f} ms")
    print(f"  CPU Median: {statistics.median(cpu_latencies):.1f} ms")
    print(f"  CPU p95:    {np.percentile(cpu_latencies, 95):.1f} ms")
    print(f"  CPU Real-Time Factor (RTF): {statistics.median(cpu_latencies) / (duration_s * 1000):.4f}")

    # 3. MPS Benchmark (if available)
    if torch.backends.mps.is_available():
        print("\nBenchmarking Apple MPS inference (10 warm runs on 5-second window)...")
        classifier_mps = EmotionClassifier(use_mps=True)
        # Warmup (compiles MPS kernels)
        classifier_mps.classify_waveform(waveform, sample_rate=sample_rate)

        mps_latencies = []
        for _ in range(10):
            t0 = time.perf_counter()
            classifier_mps.classify_waveform(waveform, sample_rate=sample_rate)
            mps_latencies.append((time.perf_counter() - t0) * 1000)

        print(f"  MPS Min:    {min(mps_latencies):.1f} ms")
        print(f"  MPS Median: {statistics.median(mps_latencies):.1f} ms")
        print(f"  MPS p95:    {np.percentile(mps_latencies, 95):.1f} ms")
        print(f"  MPS Real-Time Factor (RTF): {statistics.median(mps_latencies) / (duration_s * 1000):.4f}")

    print("=" * 60)
    print("Benchmark complete.")
    print("=" * 60)


if __name__ == "__main__":
    run_benchmark()
