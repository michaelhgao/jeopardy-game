import tkinter as tk
from tkinter import filedialog, messagebox

from src.misc.button_factory import create_button
from src.misc.themes import (
    BG_COLOUR,
    BTN_TEXT_COLOUR,
    FONT,
    SMALL_BUTTON_THEME,
    TITLE_TEXT_COLOUR,
)
from src.misc.types import Screen
from src.views.base_view import BaseView


class LoadBoardView(BaseView):
    def render(self, **kwargs) -> None:
        self.clear()
        self.root.configure(bg=BG_COLOUR)

        tk.Label(
            self.root,
            text="Load Board",
            font=(FONT, 36, "bold"),
            fg=TITLE_TEXT_COLOUR,
            bg=BG_COLOUR,
        ).pack(pady=40)

        tk.Label(
            self.root,
            text="Select a JSON file to load a board:",
            font=(FONT, 18),
            fg=BTN_TEXT_COLOUR,
            bg=BG_COLOUR,
        ).pack(pady=20)

        create_button(
            self.root,
            "Select File and Load",
            self._load_board_from_file,
            SMALL_BUTTON_THEME,
        ).pack(pady=10)

        create_button(
            self.root,
            "Back to Main Menu",
            theme=SMALL_BUTTON_THEME,
            command=lambda: self.ui_controller.navigate(Screen.MAIN_MENU),
        ).pack(pady=20)

    def _load_board_from_file(self):
        file_path = filedialog.askopenfilename(
            title="Load Board",
            filetypes=[("JSON Files", "*.json")],
        )

        if file_path:
            try:
                self.game_controller.import_json(file_path)
                messagebox.showinfo("Loaded", f"Board loaded from {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load board: {e}")

        self.ui_controller.navigate(Screen.MAIN_MENU)
