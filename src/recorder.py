"""Microphone capture into an in-memory buffer.

Recording is push-to-talk: `start()` opens the input stream, `stop()` closes it
and returns the captured audio as a mono float32 numpy array at the configured
sample rate (the format faster-whisper expects).
"""

from __future__ import annotations

import numpy as np
import sounddevice as sd


class AudioRecorder:
    def __init__(self, sample_rate: int = 16000) -> None:
        self.sample_rate = sample_rate
        self._chunks: list[np.ndarray] = []
        self._stream: sd.InputStream | None = None

    def _callback(self, indata, frames, time, status) -> None:  # noqa: ANN001
        # Copy: sounddevice reuses the buffer after the callback returns.
        self._chunks.append(indata[:, 0].copy())

    def start(self) -> None:
        """Open the microphone stream and begin accumulating audio."""
        self._chunks = []
        self._stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
            callback=self._callback,
        )
        self._stream.start()

    def stop(self) -> np.ndarray:
        """Stop the stream and return the captured mono float32 audio."""
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        return self._merge()

    def _merge(self) -> np.ndarray:
        if not self._chunks:
            return np.zeros(0, dtype=np.float32)
        return np.concatenate(self._chunks).astype(np.float32)
