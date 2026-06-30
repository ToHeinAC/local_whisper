"""Standalone diagnostic: record a few seconds, report mic level, transcribe.

Run:                 uv run python scripts/diagnose.py
List input devices:  uv run python scripts/diagnose.py --list
Test a device index: uv run python scripts/diagnose.py 3
Speak during the 4-second recording window.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import sounddevice as sd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import load_settings  # noqa: E402
from src.transcriber import Transcriber  # noqa: E402

DURATION = 4


def list_devices() -> None:
    print("Input devices (index: name  [max input channels]):")
    for idx, dev in enumerate(sd.query_devices()):
        if dev["max_input_channels"] > 0:
            print(f"  {idx}: {dev['name']}  [{dev['max_input_channels']} ch]")
    print("\nTest one with:  uv run python scripts/diagnose.py <index>")


def main() -> None:
    args = sys.argv[1:]
    if args and args[0] == "--list":
        list_devices()
        return

    device = int(args[0]) if args else None
    settings = load_settings()

    list_devices()
    print("\nUsing device:", "default" if device is None else device)

    print(f"\nRecording {DURATION}s — SPEAK NOW ...")
    audio = sd.rec(
        int(DURATION * settings.sample_rate),
        samplerate=settings.sample_rate,
        channels=1,
        dtype="float32",
        device=device,
    )
    sd.wait()
    audio = audio[:, 0]

    peak = float(np.max(np.abs(audio))) if audio.size else 0.0
    rms = float(np.sqrt(np.mean(audio**2))) if audio.size else 0.0
    print(f"\nCaptured {audio.size} samples | peak={peak:.4f} rms={rms:.4f}")
    if peak < 0.01:
        print(">> Mic level is essentially silent. Check Windows input device / permissions.")

    print(f"\nLoading model '{settings.model}' ...")
    t0 = time.time()
    transcriber = Transcriber(settings)
    print(f"Model loaded in {time.time() - t0:.1f}s")

    print("Transcribing ...")
    text = transcriber.transcribe(audio)
    print(f"\nTRANSCRIPT: {text!r}")


if __name__ == "__main__":
    main()
