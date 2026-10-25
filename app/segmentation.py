"""Windowing and chronological segmentation for local SER review."""

from dataclasses import asdict, dataclass
from typing import Any, Dict, List
import numpy as np

from app.classifier import ClassificationResult, EmotionClassifier, LABEL_MAPPING

WINDOW_DURATION_SECONDS = 5.0
MIN_WINDOW_DURATION_SECONDS = 1.0


@dataclass
class SegmentResult:
    start_seconds: float
    end_seconds: float
    status: str  # "classified", "silent", "too_short"
    label: str
    dataset_label: str
    scores: Dict[str, float]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def process_audio_segments(
    waveform: np.ndarray,
    sample_rate: int,
    classifier: EmotionClassifier,
) -> List[SegmentResult]:
    """Segment a waveform into chronological 5-second windows and classify each.

    Invariants:
    - Windows are strictly chronological and non-overlapping.
    - Full 5-second windows are classified using the real SER model.
    - A final partial window is classified if its duration >= 1.0s.
    - A final partial window < 1.0s is marked 'too_short' with label 'unknown'.
    - Exact digital silence returns 'silent' status with label 'unknown'.
    """
    total_samples = len(waveform)
    window_samples = int(WINDOW_DURATION_SECONDS * sample_rate)
    min_samples = int(MIN_WINDOW_DURATION_SECONDS * sample_rate)

    segments: List[SegmentResult] = []
    start_sample = 0

    while start_sample < total_samples:
        end_sample = min(start_sample + window_samples, total_samples)
        chunk = waveform[start_sample:end_sample]
        start_t = round(start_sample / float(sample_rate), 2)
        end_t = round(end_sample / float(sample_rate), 2)

        if len(chunk) < min_samples:
            segments.append(
                SegmentResult(
                    start_seconds=start_t,
                    end_seconds=end_t,
                    status="too_short",
                    label="unknown",
                    dataset_label="unknown",
                    scores={v: 0.0 for v in LABEL_MAPPING.values()},
                )
            )
            break

        max_amp = float(np.max(np.abs(chunk)))
        if max_amp == 0.0:
            segments.append(
                SegmentResult(
                    start_seconds=start_t,
                    end_seconds=end_t,
                    status="silent",
                    label="unknown",
                    dataset_label="unknown",
                    scores={v: 0.0 for v in LABEL_MAPPING.values()},
                )
            )
        else:
            res: ClassificationResult = classifier.classify_waveform(
                chunk,
                sample_rate=sample_rate,
            )
            segments.append(
                SegmentResult(
                    start_seconds=start_t,
                    end_seconds=end_t,
                    status="classified",
                    label=res.predicted_label,
                    dataset_label=res.predicted_dataset_label,
                    scores=res.scores,
                )
            )

        start_sample += window_samples

    return segments
