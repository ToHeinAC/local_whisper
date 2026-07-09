# Deployment

The app deploys as a self-contained folder: code, the uv-managed virtual
environment, the model files, and logs all live together.

## Prerequisites

- Windows 11
- Network access **for the one-time install only**

No admin rights and no pre-installed tooling are required. `install.bat`
bootstraps its own portable [uv](https://docs.astral.sh/uv/) into `tools\uv.exe`
(a single static binary, ~75 MB, no installer/registry). `uv` in turn fetches a
managed Python if the machine has none, so the target needs no system Python.

## Install (once)

```bat
install.bat
```

This will:
1. create `.env` from `.env.example` (if missing),
2. **bootstrap `uv`** — `scripts\bootstrap_uv.ps1` downloads the portable
   `uv.exe` into `tools\` (reuses a PATH `uv` if one exists; no-op if already
   vendored),
3. `uv sync` — create `.venv/` and install dependencies (pulling a managed
   Python if needed),
4. download the configured whisper model into `models/`,
5. create a **desktop shortcut** (`local_whisper.lnk`, launches minimized).

Both `install.bat` and `run.bat` resolve `uv` from `tools\uv.exe` first, falling
back to a `uv` on PATH. `run.bat` never downloads anything; if `uv` is missing it
tells you to run `install.bat`.

## Run

- Double-click the desktop shortcut, or run `run.bat`.
- Hold the hotkey (`ctrl+alt+space`), speak, release — text appears at the cursor.
- Quit from the tray icon (red dot) → **Quit**.

> **Windows 11 tray:** new tray icons are hidden in the overflow flyout by
> default. Click the `^` chevron next to the clock to find the red dot, or pin it
> via Settings → Personalization → Taskbar → Other system tray icons.

If global hotkeys don't fire, run `run.bat` as administrator (see
[architecture.md](architecture.md) on the `keyboard` hook).

## Moving to another machine

Copy the whole folder. With `models/` and `.venv/` present it runs offline; if you
copy without `.venv/`, run `install.bat` again on the target machine.

## Logs

`logs/sessions.jsonl` — one JSON object per dictation:

```json
{"user":"he","start":"2026-06-30T12:00:00","end":"2026-06-30T12:00:05","duration_s":5.0,"chars":42}
```
