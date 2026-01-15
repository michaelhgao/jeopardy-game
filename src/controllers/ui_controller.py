import tkinter as tk
from typing import Optional

from src.controllers.game_controller import GameController
from src.misc.types import Screen
from src.models.question import Question
from src.views.base_view import BaseView


class UiController:
    def __init__(self, root: tk.Tk, game_controller: GameController):
        self.root = root
        self.game_controller = game_controller
        self.current_view: Optional[BaseView] = None
        self.current_screen: Optional[Screen] = None
        self.current_question: Optional[Question] = None

        self.root.title("Jeopardy")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.navigate(Screen.MAIN_MENU)

    def navigate(self, screen: Screen, **kwargs):
        self.current_screen = screen

        if self.current_view:
            self.current_view.clear()

        if screen == Screen.MAIN_MENU:
            from src.views.main_menu_view import MainMenuView

            self.current_view = MainMenuView(
                self.main_frame, self.game_controller, self
            )
        elif screen == Screen.BOARD:
            from src.views.board_view import BoardView

            self.current_view = BoardView(self.main_frame, self.game_controller, self)

        if self.current_view:
            self.current_view.render(**kwargs)
