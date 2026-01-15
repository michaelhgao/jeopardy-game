import tkinter as tk

from src.misc.button_factory import create_button
from src.misc.themes import BG_COLOUR, FONT, SMALL_BUTTON_THEME
from src.misc.types import Screen
from src.views.base_view import BaseView


class SetupTeamsView(BaseView):
    def render(self, **kwargs) -> None:
        self.clear()

        self.root.configure(bg=BG_COLOUR)

        tk.Label(
            self.root,
            text="Setup Teams",
            font=(FONT, 32, "bold"),
            bg=BG_COLOUR,
        ).pack(pady=20)

        # Number of teams
        tk.Label(
            self.root,
            text="Number of teams (1–10):",
            bg=BG_COLOUR,
        ).pack()

        self.num_teams_var = tk.IntVar(value=2)
        tk.Spinbox(
            self.root,
            from_=1,
            to=10,
            textvariable=self.num_teams_var,
            width=5,
        ).pack(pady=5)

        create_button(
            self.root,
            text="Next",
            theme=SMALL_BUTTON_THEME,
            command=self._build_team_entries,
        ).pack(pady=10)

        create_button(
            self.root,
            text="Cancel",
            theme=SMALL_BUTTON_THEME,
            command=lambda: self.ui_controller.navigate(Screen.MAIN_MENU),
        ).pack(pady=10)

    def _build_team_entries(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.team_entries: list[tk.Entry] = []

        tk.Label(
            self.root,
            text="Enter Team Names",
            font=(FONT, 28, "bold"),
            bg=BG_COLOUR,
        ).pack(pady=20)

        for i in range(self.num_teams_var.get()):
            entry = tk.Entry(self.root, font=(FONT, 16))
            entry.insert(0, f"Team {i + 1}")
            entry.pack(pady=5)
            self.team_entries.append(entry)

        create_button(
            self.root,
            text="Start Game",
            theme=SMALL_BUTTON_THEME,
            command=self._save_teams,
        ).pack(pady=20)

        create_button(
            self.root,
            text="Back",
            theme=SMALL_BUTTON_THEME,
            command=lambda: self.ui_controller.navigate(Screen.MAIN_MENU),
        ).pack(pady=10)

    def _save_teams(self):
        self.game_controller.clear_teams()

        for entry in self.team_entries:
            name = entry.get().strip() or "Team"
            self.game_controller.add_team(name, [])

        self.ui_controller.navigate(Screen.BOARD)
