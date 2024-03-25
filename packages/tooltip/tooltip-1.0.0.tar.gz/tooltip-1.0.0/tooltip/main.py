import tkinter as tk
import textwrap


class ToolTip(object):
    def __init__(self, widget, text='Widget info', justify='left', width=None, background=None, foreground=None):
        if justify not in ['left', 'right', 'center']:
            raise ValueError("justify must be 'left', 'right', or 'center'")
        self.widget = widget
        self.text = textwrap.fill(text, width) if width else text
        self.justify = justify
        self.width = width
        self.background = background
        self.foreground = foreground
        self.tw = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)

    def enter(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f"+{x}+{y}")
        self.tw.attributes('-topmost', True)
        label_options = {
            "text": self.text,
            "relief": 'solid',
            "borderwidth": 1,
            "font": ("arial", "10", "normal"),
            "justify": self.justify
        }
        if self.background is not None:
            label_options["background"] = self.background
        if self.foreground is not None:
            label_options["foreground"] = self.foreground
        label = tk.Label(self.tw, **label_options)
        label.pack()

    def close(self, event=None):
        if self.tw:
            self.tw.destroy()
            self.tw = None