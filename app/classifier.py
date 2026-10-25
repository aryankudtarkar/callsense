"""Local emotion2vec+ speech emotion recognition through FunASR."""

from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np
import torch
from funasr import AutoModel

MODEL_ID = "iic/emotion2vec_plus_large"
MODEL_SOURCE = MODEL_ID
MODEL_REVISION = "master (upstream default; unpinned)"
MODEL_LICENSE = "FunASR Model Open Source License Agreement v1.1 (custom terms)"
MODEL_LICENSE_URL = "https://github.com/modelscope/FunASR/blob/main/MODEL_LICENSE"
MODEL_CARD_URL = "https://huggingface.co/emotion2vec/emotion2vec_plus_large"
LABEL_MAPPING = {
    "angry": "angry",
    "disgusted": "disgusted",
    "fearful": "fearful",
    "happy": "happy",
    "neutral": "neutral",
    "other": "other",
    "sad": "sad",
    "surprised": "surprised",
    "unknown": "unknown",
}


@dataclass
class ClassificationResult:
    predicted_label: str
    predicted_dataset_label: str
    scores: Dict[str, float]  # upstream softmax scores; not calibrated probabilities
    device: str
    model_id: str
    model_revision: str


class EmotionClassifier:
    """Run the official emotion2vec+ classifier locally with FunASR."""

    def __init__(self, use_mps: bool = False):
        # CPU is the predictable backend for FunASR's emotion2vec implementation.
        self.device = "mps" if use_mps and torch.backends.mps.is_available() else "cpu"
        self.model = AutoModel(
            model=MODEL_SOURCE,
            device=self.device,
            hub="ms",
            disable_update=True,
            disable_pbar=True,
        )

    def classify_waveform(self, waveform: np.ndarray, sample_rate: int = 16000) -> ClassificationResult:
        """Classify one 1D float32 waveform at 16 kHz without writing it to disk."""
        if sample_rate != 16000:
            raise ValueError(f"Sample rate must be 16000 Hz, got {sample_rate}")
        if waveform.ndim != 1 or len(waveform) == 0:
            raise ValueError("Waveform must be a non-empty 1D array")

        if float(np.max(np.abs(waveform))) == 0.0:
            return ClassificationResult(
                predicted_label="unknown",
                predicted_dataset_label="unknown",
                scores={label: 0.0 for label in LABEL_MAPPING},
                device=self.device,
                model_id=MODEL_ID,
                model_revision=MODEL_REVISION,
            )

        output = self.model.generate(
            input=np.asarray(waveform, dtype=np.float32),
            fs=sample_rate,
            granularity="utterance",
            extract_embedding=False,
        )
        if not output or not isinstance(output[0], dict):
            raise RuntimeError("emotion2vec+ returned an unexpected output")

        raw_labels = output[0].get("labels", [])
        raw_scores = output[0].get("scores", [])
        if len(raw_labels) != len(raw_scores) or not raw_labels:
            raise RuntimeError("emotion2vec+ returned no class scores")

        scores: Dict[str, float] = {}
        for label, score in zip(raw_labels, raw_scores):
            clean_label = str(label).strip().lower()
            # FunASR's tokenizer commonly returns bilingual names such as
            # "生气/angry", and the ninth class may be "<unk>" or empty.
            if "/" in clean_label:
                clean_label = clean_label.rsplit("/", 1)[-1]
            if clean_label in {"<unk>", "", "<|unk|>"}:
                clean_label = "unknown"
            user_label = LABEL_MAPPING.get(clean_label, "other")
            numeric_score = float(score)
            if not np.isfinite(numeric_score):
                raise RuntimeError("emotion2vec+ returned a non-finite score")
            scores[user_label] = round(numeric_score, 6)

        best_label = max(scores, key=scores.get)
        return ClassificationResult(
            predicted_label=best_label,
            predicted_dataset_label=best_label,
            scores=scores,
            device=self.device,
            model_id=MODEL_ID,
            model_revision=MODEL_REVISION,
        )


_global_classifier: Optional[EmotionClassifier] = None


def get_classifier(use_mps: bool = False) -> EmotionClassifier:
    """Retrieve or initialize the singleton classifier."""
    global _global_classifier
    if _global_classifier is None:
        _global_classifier = EmotionClassifier(use_mps=use_mps)
    return _global_classifier
