# Architecture

## Flow

```
hotkey DOWN ─▶ Controller.on_press ─▶ overlay.show("● Recording") ─▶ recorder.start()
hotkey UP   ─▶ (worker thread) Controller.on_release:
                 audio = recorder.stop()
                 overlay.show("… Transcribing")
                 text  = transcriber.transcribe(audio)
                 injector.inject(text)        # typed at cursor
                 logger.record(start, end, len(text))
                 overlay.hide()
```

`Controller` holds a `_busy` flag so a second press while recording, or a release
without a press, is ignored.

## Threads

| Thread | Runs | Why |
|--------|------|-----|
| main | Tk overlay `mainloop` | tkinter must own the main thread |
| tray | `pystray.Icon.run_detached` | `run()` blocks |
| keyboard | global hooks | provided by the `keyboard` library |
| worker | `Controller.on_release` | keep transcription off the hook thread |

The overlay is not mutated from worker/hook threads directly. They set a desired
`(visible, text)` tuple; a 50 ms `after` poll on the main thread applies it,
keeping all widget access single-threaded.

## Hotkey detection

`PushToTalk` registers `keyboard.add_hotkey(combo, on_press)` for the down edge
and `keyboard.on_release_key(trigger_key, on_release)` for the up edge, where
`trigger_key` is the last key of the combo (e.g. `space` in `ctrl+alt+space`).

**Admin rights:** the `keyboard` library installs a low-level global hook that on
some Windows 11 setups requires running as administrator. If avoiding admin is a
hard requirement, swap `hotkey.py` to `pynput` keyboard listeners (tracking the
modifier+key set manually); the `PushToTalk` interface can stay the same.

## Offline model storage

`Transcriber` passes `download_root=models/` to faster-whisper. `download_model.py`
pre-fetches the model during install so runtime needs no network.
