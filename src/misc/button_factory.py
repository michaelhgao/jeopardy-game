import tkinter as tk
from typing import Callable

from src.misc.themes import ButtonTheme


def create_button(
    parent: tk.Widget,
    text: str,
    command: Callable,
    theme: ButtonTheme,
    **kwargs,
) -> tk.Button:
    options = {
        "text": text,
        "command": command,
        "bg": theme.bg,
        "fg": theme.fg,
        "font": theme.font,
        "activebackground": theme.active_bg,
        "activeforeground": theme.active_fg,
        "borderwidth": theme.borderwidth,
        "width": theme.width,
        "height": theme.height,
    }
    options.update(kwargs)
    return tk.Button(parent, **options)
