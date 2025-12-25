import json
from typing import Optional

from src.misc.types import GRID_SIZE, Category, GameMode
from src.models.jeopardy_game import JeopardyGame
from src.models.question import Question, QuestionEdit
from src.models.team import Team


class GameController:
    def __init__(self, game: JeopardyGame) -> None:
        self.game = game
        self.mode: GameMode = GameMode.PLAY
        self.current_category: Optional[Category] = None
        self.current_question: Optional[Question] = None

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

    def add_question(self, category: Category, question: Question) -> None:
        self.game.add_question(category, question)

    def edit_question(self, question: Question, edit: QuestionEdit) -> None:
        self.game.edit_question(question, edit)

    def set_current_question(self, category: Category, question_index: int) -> None:
        if question_index < 0 or question_index >= len(category.questions):
            raise IndexError("Question index out of bounds")
        self.current_category = category
        self.current_question = category.questions[question_index]

    def get_current_question(self) -> Optional[Question]:
        return self.current_question

    def add_team(self, name: str, members: list[str]) -> Team:
        return self.game.add_team(name, members)

    def get_team(self, name: str) -> Team:
        return self.game.get_team(name)

    def clear_teams(self) -> None:
        self.game.clear_teams()

    def get_teams(self) -> list[Team]:
        return self.game.teams

    def mark_question_answered(self, question: Optional[Question]) -> None:
        if question is None:
            if self.current_question is None:
                raise ValueError("No question selected")
            question = self.current_question

        question.mark_answered()

    def assign_question_points(
        self, team: Optional[Team], question: Optional[Question] = None
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
                    Question(
                        question="New Question",
                        answer="Answer",
                        value=(len(category.questions) + 1) * 100,
                    )
                )

    def export_json(self, file_path: str) -> None:
        data = {"categories": []}
        for category in self.game.categories:
            cat_data = {
                "name": category.name,
                "questions": [
                    {
                        "question": q.question,
                        "answer": q.answer,
                        "value": q.value,
                        "image_path": q.image_path,
                    }
                    for q in category.questions
                ],
            }
            data["categories"].append(cat_data)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def import_json(self, file_path: str) -> None:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.game.categories.clear()

        for cat_data in data.get("categories", []):
            category = self.game.add_category(cat_data["name"])
            for q_data in cat_data.get("questions", []):
                category.questions.append(
                    Question(
                        question=q_data["question"],
                        answer=q_data["answer"],
                        value=q_data["value"],
                        image_path=q_data.get("image_path"),
                    )
                )
