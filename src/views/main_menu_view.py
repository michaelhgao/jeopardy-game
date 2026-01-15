import tkinter as tk

from src.misc.button_factory import create_button
from src.misc.themes import BG_COLOUR, FONT, MAIN_MENU_BUTTON_THEME, TITLE_TEXT_COLOUR
from src.misc.types import GameMode, Screen
from src.views.base_view import BaseView


class MainMenuView(BaseView):
    def render(self, **kwargs) -> None:
        self.clear()

        self.root.configure(bg=BG_COLOUR)

        tk.Label(
            self.root,
            text="JEOPARDY",
            font=(FONT, 72, "bold"),
            fg=TITLE_TEXT_COLOUR,
            bg=BG_COLOUR,
        ).pack(pady=40)

        create_button(
            self.root,
            text="Play Mode",
            command=self._play_mode,
            theme=MAIN_MENU_BUTTON_THEME,
        ).pack(pady=10)

        create_button(
            self.root,
            text="Edit Mode",
            command=self._edit_mode,
            theme=MAIN_MENU_BUTTON_THEME,
        ).pack(pady=10)

        create_button(
            self.root,
            text="Save Board",
            command=self._save_board,
            theme=MAIN_MENU_BUTTON_THEME,
        ).pack(pady=10)

        create_button(
            self.root,
            text="Load Board",
            command=self._load_board,
            theme=MAIN_MENU_BUTTON_THEME,
        ).pack(pady=10)

    def _play_mode(self):
        self.game_controller.set_mode(GameMode.PLAY)
        self.ui_controller.navigate(Screen.SETUP_TEAMS)

    def _edit_mode(self):
        self.game_controller.set_mode(GameMode.EDIT)
        self.ui_controller.navigate(Screen.BOARD)

    def _save_board(self):
        self.ui_controller.navigate(Screen.SAVE)

    def _load_board(self):
        self.ui_controller.navigate(Screen.LOAD)
