import tkinter as tk

from src.misc.button_factory import create_button
from src.misc.themes import BG_COLOUR, FONT, SMALL_BUTTON_THEME
from src.misc.types import Category, Screen
from src.views.base_view import BaseView


class EditCategoryView(BaseView):
    def render(self, **kwargs) -> None:
        self.clear()

        category: Category = kwargs["category"]

        self.root.configure(bg=BG_COLOUR)

        tk.Label(
            self.root,
            text="Edit Category",
            font=(FONT, 32, "bold"),
            bg=BG_COLOUR,
        ).pack(pady=20)

        self.entry = tk.Entry(self.root, font=(FONT, 18))
        self.entry.insert(0, category.name)
        self.entry.pack(pady=10)

        create_button(
            self.root,
            text="Save",
            theme=SMALL_BUTTON_THEME,
            command=lambda: self._save(category),
        ).pack(pady=10)

        create_button(
            self.root,
            text="Cancel",
            theme=SMALL_BUTTON_THEME,
            command=lambda: self.ui_controller.navigate(Screen.BOARD),
        ).pack(pady=10)

    def _save(self, category: Category):
        new_name = self.entry.get().strip()
        if new_name:
            self.game_controller.edit_category(category.name, new_name)
        self.ui_controller.navigate(Screen.BOARD)
