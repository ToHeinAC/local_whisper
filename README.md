# local_whisper

Portable Windows 11 push-to-talk dictation powered by local
[faster-whisper](https://github.com/SYSTRAN/faster-whisper). Hold a hotkey,
speak, release — the transcribed text is typed at the cursor. Fully offline;
everything lives in the app folder.

## Quick start

```bat
install.bat   :: one-time: bootstrap uv + sync deps + download model + shortcut
run.bat       :: launch (or double-click the desktop shortcut)
```

No admin rights, pre-installed tools, or **system Python** needed — `install.bat`
vendors a portable `uv` and a managed Python into `tools\`. One-time network
access required; after that it runs fully offline.

Hold **Ctrl+Shift**, speak, release. Configure via `.env` (see `.env.example`).

## Documentation

- [IMPLEMENTATION.md](IMPLEMENTATION.md) — current implementation state
- [docs/](docs/) — component-level detail

## License

Apache-2.0.
