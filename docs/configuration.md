# Configuration

All settings are read from `.env` (copy from `.env.example`). Loaded by
`src/config.py` into a frozen `Settings` dataclass.

| Variable | Default | Meaning |
|----------|---------|---------|
| `WHISPER_MODEL` | `small` | Model size: `tiny`/`base`/`small`/`medium`/`large-v3` |
| `WHISPER_LANGUAGE` | `auto` | Language code (`de`, `en`, ...) or `auto` to detect |
| `DEVICE` | `cpu` | `cpu` or `cuda` |
| `COMPUTE_TYPE` | `int8` | `int8` (CPU), `float16` / `int8_float16` (CUDA) |
| `HOTKEY` | `ctrl+alt+space` | Push-to-talk combo (`keyboard` library syntax) |
| `TYPE_DELAY` | `0.0` | Seconds between simulated keystrokes |
| `SAMPLE_RATE` | `16000` | Mic capture rate (Hz); whisper expects 16000 |

## Paths

Resolved relative to the application root (parent of `src/`), keeping the folder
portable:

- `models/` — downloaded whisper model files
- `logs/sessions.jsonl` — appended session records

## Model / accuracy trade-offs

- `small`: good balance, ~real-time on CPU.
- `medium`: better accuracy (esp. German), slower on CPU.
- Set `WHISPER_LANGUAGE=de` to skip auto-detect when you only dictate German.
- For GPU: `DEVICE=cuda` + `COMPUTE_TYPE=float16` (requires CUDA runtime).
