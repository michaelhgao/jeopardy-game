from typing import Optional

from src.misc.types import GRID_SIZE, Category, GameMode
from src.models.jeopardy_game import JeopardyGame
from src.models.jeopardy_question import JeopardyQuestion, QuestionEdit
from src.models.team import Team


class GameController:
    def __init__(self, game: JeopardyGame) -> None:
        self.game = game
        self.mode: GameMode = GameMode.PLAY
        self.current_category: Optional[Category] = None
        self.current_question: Optional[JeopardyQuestion] = None

    def set_mode(self, mode: GameMode) -> None:
        self.mode = mode

    def get_mode(self) -> GameMode:
        return self.mode

    def add_category(self, name: str) -> Category:
        return self.game.add_category(name)

    def remove_category(self, name: str) -> None:
        self.game.remove_category(name)

    def edit_category(self, old_name: str, new_name: str) -> None:
        self.game.edit_category(old_name, new_name)

    def get_categories(self) -> list[Category]:
        return self.game.categories

    def add_question(self, category: Category, question: JeopardyQuestion) -> None:
        self.game.add_question(category, question)

    def edit_question(self, question: JeopardyQuestion, edit: QuestionEdit) -> None:
        self.game.edit_question(question, edit)

    def set_current_question(self, category: Category, question_index: int) -> None:
        if question_index < 0 or question_index >= len(category.questions):
            raise IndexError("Question index out of bounds")
        self.current_category = category
        self.current_question = category.questions[question_index]

    def get_current_question(self) -> Optional[JeopardyQuestion]:
        return self.current_question

    def add_team(self, name: str, members: list[str]) -> Team:
        return self.game.add_team(name, members)

    def get_team(self, name: str) -> Team:
        return self.game.get_team(name)

    def clear_teams(self) -> None:
        self.game.clear_teams()

    def get_teams(self) -> list[Team]:
        return self.game.teams

    def mark_question_answered(self, question: Optional[JeopardyQuestion]) -> None:
        if question is None:
            if self.current_question is None:
                raise ValueError("No question selected")
            question = self.current_question

        question.mark_answered()

    def assign_question_points(
        self, team: Optional[Team], question: Optional[JeopardyQuestion] = None
    ) -> None:
        if question is None:
            if self.current_question is None:
                raise ValueError("No question selected")
            question = self.current_question

        self.game.assign_question_points(team, question)

        self.current_question = None
        self.current_category = None

    def reset_game(self) -> None:
        for category in self.game.categories:
            for question in category.questions:
                question.answered = False
        for team in self.game.teams:
            team.reset_points()
        self.current_question = None
        self.current_category = None

    def ensure_minimum_board(self) -> None:
        while len(self.game.categories) < GRID_SIZE:
            self.add_category(f"Category {len(self.game.categories) + 1}")

        for category in self.game.categories[:GRID_SIZE]:
            while len(category.questions) < GRID_SIZE:
                category.questions.append(
                    JeopardyQuestion(
                        question="New Question",
                        answer="Answer",
                        value=(len(category.questions) + 1) * 100,
                    )
                )
