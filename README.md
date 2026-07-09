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

No admin rights or pre-installed tools needed — `install.bat` fetches a portable
`uv` into `tools\` (which then supplies Python too). One-time network access
required; after that it runs fully offline.

Hold **Ctrl+Alt+Space**, speak, release. Configure via `.env` (see `.env.example`).

## Documentation

- [PRD.md](PRD.md) — product requirements
- [IMPLEMENTATION.md](IMPLEMENTATION.md) — current implementation state
- [docs/](docs/) — component-level detail

## License

Apache-2.0.
