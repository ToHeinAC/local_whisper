"""Application configuration loaded from environment / .env.

All paths resolve relative to the application root so the whole folder stays
portable: dependencies, models and logs live next to the code.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Application root = parent of this `src/` package.
APP_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = APP_ROOT / "models"
LOGS_DIR = APP_ROOT / "logs"


@dataclass(frozen=True)
class Settings:
    """Resolved runtime settings."""

    model: str
    language: str | None  # None means auto-detect
    device: str
    compute_type: str
    hotkey: str
    type_delay: float
    sample_rate: int
    models_dir: Path
    logs_dir: Path


def load_settings() -> Settings:
    """Read .env (if present) and the environment into a Settings object."""
    load_dotenv(APP_ROOT / ".env")

    language = os.getenv("WHISPER_LANGUAGE", "auto").strip().lower()

    return Settings(
        model=os.getenv("WHISPER_MODEL", "small").strip(),
        language=None if language in ("", "auto") else language,
        device=os.getenv("DEVICE", "cpu").strip(),
        compute_type=os.getenv("COMPUTE_TYPE", "int8").strip(),
        hotkey=os.getenv("HOTKEY", "ctrl+alt+space").strip(),
        type_delay=float(os.getenv("TYPE_DELAY", "0.0")),
        sample_rate=int(os.getenv("SAMPLE_RATE", "16000")),
        models_dir=MODELS_DIR,
        logs_dir=LOGS_DIR,
    )
