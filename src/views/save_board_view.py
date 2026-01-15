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


class SaveBoardView(BaseView):
    def render(self, **kwargs) -> None:
        self.clear()
        self.root.configure(bg=BG_COLOUR)

        tk.Label(
            self.root,
            text="Save Board",
            font=(FONT, 36, "bold"),
            fg=TITLE_TEXT_COLOUR,
            bg=BG_COLOUR,
        ).pack(pady=40)

        tk.Label(
            self.root,
            text="Choose a file to save the board:",
            font=(FONT, 18),
            fg=BTN_TEXT_COLOUR,
            bg=BG_COLOUR,
        ).pack(pady=20)

        create_button(
            self.root,
            "Select File and Save",
            self._save_board_to_file,
            SMALL_BUTTON_THEME,
        ).pack(pady=10)

        create_button(
            self.root,
            "Back to Main Menu",
            theme=SMALL_BUTTON_THEME,
            command=lambda: self.ui_controller.navigate(Screen.MAIN_MENU),
        ).pack(pady=20)

    def _save_board_to_file(self):
        file_path = filedialog.asksaveasfilename(
            title="Save Board",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
        )

        if file_path:
            try:
                self.game_controller.export_json(file_path)
                messagebox.showinfo("Saved", f"Board saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save board: {e}")

        self.ui_controller.navigate(Screen.MAIN_MENU)
