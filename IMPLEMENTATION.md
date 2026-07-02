# IMPLEMENTATION.md

Current implementation state of **local_whisper**. See [PRD.md](PRD.md) for the
original goals and [docs/](docs/) for component detail.

> Note: the CLAUDE.md tech section mentions `streamlit` and an LLM `prompts.py`.
> Those are template boilerplate and do **not** apply here — this is a background
> tray app with no web UI and no LLM prompting. No `src/prompts.py` exists.

## What it does

Hold a global hotkey (`ctrl+alt+space` by default) → record the microphone →
transcribe locally with faster-whisper → type the text at the cursor → release
hides the indicator and logs the session. Fully offline; model files live in
`models/`.

**Voice formatting commands** (recognised in the transcript by `commands.py`):
`new line` / `next line` → Enter, `new paragraph` → Enter×2, `tab` → Tab. The
match eats whitespace/punctuation Whisper puts around the spoken command, so a
punctuation mark dictated right next to a command word may be swallowed.

## Components (`src/`)

| Module | Responsibility |
|--------|----------------|
| `config.py` | Load `.env` into a `Settings` dataclass; resolve app-relative paths |
| `recorder.py` | `AudioRecorder` — mic capture (sounddevice) → mono float32 numpy |
| `transcriber.py` | `Transcriber` — faster-whisper wrapper, model under `models/` |
| `commands.py` | `parse()` — split transcript into text + special-key actions (voice formatting) |
| `injector.py` | `TextInjector` — type text (`inject`) and press keys (`press`) at cursor via Win32 `SendInput` |
| `overlay.py` | `Overlay` — status indicator: animated mic-level waveform while recording, text while transcribing (tkinter) |
| `tray.py` | system-tray icon with Quit (pystray) |
| `session_log.py` | `SessionLogger` — append JSONL session records |
| `hotkey.py` | `PushToTalk` — global press/release listener |
| `controller.py` | `Controller` — record→transcribe→inject→log state machine |
| `main.py` | wiring + threading + run loop |
| `download_model.py` | one-time model pre-download for offline use |

## Threading model

- Main thread: Tk overlay `mainloop`.
- Tray icon: own thread via `run_detached`.
- Keyboard hooks: keyboard library thread; the release handler offloads
  transcription to a worker thread so the hook returns immediately.
- Overlay is updated thread-safely (other threads set desired state; a 50 ms
  poll on the main thread applies it).

See [docs/architecture.md](docs/architecture.md).

## Configuration

All settings come from `.env` (see `.env.example`). Details in
[docs/configuration.md](docs/configuration.md).

## Run & deploy

`install.bat` (sync deps + download model + desktop shortcut), then `run.bat`.
Details in [docs/deployment.md](docs/deployment.md).

## Tests

`uv run pytest -m "not slow"` — fast unit tests (hardware mocked).
`uv run pytest -m slow` — integration test that loads a real model.

| Area | Test file |
|------|-----------|
| config / recorder buffer | `tests/test_recorder.py` |
| transcriber (empty + real) | `tests/test_transcriber.py` |
| text injection | `tests/test_injector.py` |
| session logging | `tests/test_session_log.py` |
| controller state machine | `tests/test_controller.py` |

## Known constraints / open items

- The `keyboard` library global hook may require running as **administrator** on
  Windows 11. Fallback option: `pynput` (no admin). See docs/architecture.md.
- GPU is opt-in via `.env` (`DEVICE=cuda`, `COMPUTE_TYPE=float16`); default is CPU
  `int8` for portability.
- Manual verification still pending: real hold-to-talk typing into Notepad/Word,
  umlaut fidelity, tray + overlay behavior on the live desktop.
