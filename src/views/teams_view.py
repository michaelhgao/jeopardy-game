import tkinter as tk

from src.misc.button_factory import create_button
from src.misc.themes import (
    BG_COLOUR,
    FONT,
    QUESTION_TEXT_COLOUR,
    SMALL_BUTTON_THEME,
    TITLE_TEXT_COLOUR,
)
from src.misc.types import Screen
from src.views.base_view import BaseView


class TeamsView(BaseView):
    def render(self, **kwargs) -> None:
        self.clear()

        self.root.configure(bg=BG_COLOUR)

        # Title
        tk.Label(
            self.root,
            text="Team Scores",
            font=(FONT, 36, "bold"),
            fg=TITLE_TEXT_COLOUR,
            bg=BG_COLOUR,
        ).pack(pady=20)

        # List each team and points
        for team in self.game_controller.get_teams():
            tk.Label(
                self.root,
                text=f"{team.name}: {team.points} points",
                font=(FONT, 24),
                fg=QUESTION_TEXT_COLOUR,
                bg=BG_COLOUR,
            ).pack(pady=10)

        # Back button
        create_button(
            self.root,
            "Back to Board",
            theme=SMALL_BUTTON_THEME,
            command=lambda: self.ui_controller.navigate(Screen.BOARD),
        ).pack(pady=20)
