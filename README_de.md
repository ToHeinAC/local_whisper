# local_whisper

Portable Windows 11 Push-to-Talk-Diktat, lokal, powered by 
[faster-whisper](https://github.com/SYSTRAN/faster-whisper). Halte eine Hotkey-Tastenkombination gedrückt,
sprich (idealerweise in ein Headset), lasse Hotkeys los — der transkribierte Text wird an der Cursorposition eingetippt. 

> Vollständig offline; alles befindet sich im App-Ordner auf deinem Rechner

## Schnellstart

Herunterladen des gesamten Ordners auf lokales Laufwerk, z.B. C:\Users\ #he\Desktop.

### Inbetriebnahme

Führe aus (vie Kommandozeile oder Doppelklick):
```bat
install.bat   :: einmalig: uv bootstrap + deps synchronisieren + Modell herunterladen + Verknüpfung
run.bat       :: starten (oder Desktop-Verknüpfung doppelklicken)
```

Keine **Admin-Rechte**, **vorinstallierte Tools** oder **systemweites Python** erforderlich — `install.bat`
bringt ein portables `uv` und ein verwaltetes Python in `tools\` ein. Einmaliger Netzwerkzugriff
erforderlich; danach läuft es vollständig offline.

Start der Anwendung über `run.bat` oder die Desktop-Verknüpfung.

### Verwendung

Halte **Ctrl+Shift**, sprich, lass los. Konfiguriere (optional; z.B. Sprache) über `.env` (siehe `.env.example`).

## Dokumentation

- [IMPLEMENTATION.md](IMPLEMENTATION.md) — aktueller Implementierungsstatus
- [docs/](docs/) — Details auf Komponentenebene

## Vereinbarungen

- Nur für **BRENK-dienstliche Zwecke**
- Weitergabe an Dritte nur nach **Rücksprache** mit Tobias Hein

## Lizenz

Apache-2.0.
