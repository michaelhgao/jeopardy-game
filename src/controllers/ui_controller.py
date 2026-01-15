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
        elif screen == Screen.QUESTION:
            from src.views.question_view import QuestionView

            self.current_view = QuestionView(
                self.main_frame,
                self.game_controller,
                self,
            )
        elif screen == Screen.ANSWER:
            from src.views.answer_view import AnswerView

            self.current_view = AnswerView(
                self.main_frame,
                self.game_controller,
                self,
            )
        elif screen == Screen.SETUP_TEAMS:
            from src.views.setup_teams_view import SetupTeamsView

            self.current_view = SetupTeamsView(
                self.main_frame,
                self.game_controller,
                self,
            )
        elif screen == Screen.TEAMS:
            from src.views.teams_view import TeamsView

            self.current_view = TeamsView(
                self.main_frame,
                self.game_controller,
                self,
            )
        elif screen == Screen.SAVE:
            from src.views.save_board_view import SaveBoardView

            self.current_view = SaveBoardView(
                self.main_frame,
                self.game_controller,
                self,
            )
        elif screen == Screen.LOAD:
            from src.views.load_board_view import LoadBoardView

            self.current_view = LoadBoardView(
                self.main_frame,
                self.game_controller,
                self,
            )
        elif screen == Screen.EDIT_QUESTION:
            from src.views.edit_question_view import EditQuestionView

            self.current_view = EditQuestionView(
                self.main_frame, self.game_controller, self
            )
        elif screen == Screen.EDIT_CATEGORY:
            from src.views.edit_category_view import EditCategoryView

            self.current_view = EditCategoryView(
                self.main_frame, self.game_controller, self
            )

        if self.current_view:
            self.current_view.render(**kwargs)