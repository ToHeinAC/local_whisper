"""Small always-on-top status indicator.

Tkinter is not thread-safe, so widget changes happen only on the main thread:
other threads set a desired state and a periodic poll applies it. Run
`mainloop()` on the main thread; call `show()` / `hide()` from anywhere.
"""

from __future__ import annotations

import tkinter as tk


class Overlay:
    def __init__(self) -> None:
        self._desired: tuple[bool, str] = (False, "")
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.overrideredirect(True)  # borderless
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#202020")
        self._label = tk.Label(
            self.root,
            text="",
            fg="#ffffff",
            bg="#202020",
            font=("Segoe UI", 12),
            padx=16,
            pady=8,
        )
        self._label.pack()

    def show(self, text: str) -> None:
        self._desired = (True, text)

    def hide(self) -> None:
        self._desired = (False, "")

    def _position_bottom_center(self) -> None:
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"+{(sw - w) // 2}+{sh - h - 80}")

    def _poll(self) -> None:
        visible, text = self._desired
        if visible:
            if self._label.cget("text") != text:
                self._label.config(text=text)
            if self.root.state() == "withdrawn":
                self.root.deiconify()
            self._position_bottom_center()
        elif self.root.state() != "withdrawn":
            self.root.withdraw()
        self.root.after(50, self._poll)

    def mainloop(self) -> None:
        self.root.after(50, self._poll)
        self.root.mainloop()

    def stop(self) -> None:
        self.root.after(0, self.root.destroy)
