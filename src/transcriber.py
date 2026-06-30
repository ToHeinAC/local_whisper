"""faster-whisper wrapper.

The model is loaded once and reused. Model files are stored under the app's
`models/` folder so the whole application stays self-contained and offline.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from faster_whisper import WhisperModel

from .config import Settings


class Transcriber:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        settings.models_dir.mkdir(parents=True, exist_ok=True)
        self._model = WhisperModel(
            settings.model,
            device=settings.device,
            compute_type=settings.compute_type,
            download_root=str(settings.models_dir),
        )

    def transcribe(self, audio: np.ndarray) -> str:
        """Transcribe mono float32 audio into stripped text."""
        if audio.size == 0:
            return ""
        segments, _info = self._model.transcribe(
            audio,
            language=self._settings.language,
            beam_size=5,
            vad_filter=True,
        )
        return " ".join(segment.text.strip() for segment in segments).strip()
