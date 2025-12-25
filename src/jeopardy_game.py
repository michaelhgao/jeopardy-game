from typing import Optional

from src.jeopardy_question import JeopardyQuestion
from src.team import Team
from src.types import GameMode


class JeopardyGame:
    def __init__(self) -> None:
        self.questions: dict[str, list[JeopardyQuestion]] = {}
        self.category_order: list[str] = []
        self.teams: list[Team] = []
        self.mode: GameMode = GameMode.PLAY

    def set_mode(self, mode: GameMode) -> None:
        self.mode = mode

    def get_mode(self) -> GameMode:
        return self.mode

    def add_category(self, name: str) -> None:
        if name in self.questions:
            raise ValueError("Category already exists")
        self.questions[name] = []
        self.category_order.append(name)

    def remove_category(self, name: str) -> None:
        del self.questions[name]

    def edit_category(self, index: int, new_name: str) -> bool:
        if index < 0 or index >= len(self.category_order):
            return False
        old_name: str = self.category_order[index]
        if not new_name or new_name in self.questions:
            return False
        self.questions[new_name] = self.questions.pop(old_name)
        self.category_order[index] = new_name
        return True

    def add_question(self, category: str, question: JeopardyQuestion) -> None:
        self.questions[category].append(question)

    def get_question(self, category: str, index: int) -> JeopardyQuestion:
        return self.questions[category][index]

    def edit_question(
        self,
        question: JeopardyQuestion,
        new_question: str,
        new_answer: str,
        new_value: int,
        image_path: Optional[str] = None,
    ) -> None:
        question.question = new_question
        question.answer = new_answer
        question.value = new_value

        if image_path:
            question.image_path = image_path

    def add_team(self, name: str, members: list[str]) -> Team:
        team = Team(name, members)
        self.teams.append(team)
        return team

    def get_team(self, name: str) -> Team:
        for team in self.teams:
            if team.name == name:
                return team
        raise KeyError("Team not found")

    def clear_teams(self) -> None:
        self.teams.clear()

    def add_points(self, team: Team, question: JeopardyQuestion) -> None:
        team.add_points(question.value)
        question.mark_answered()

    def remove_points(self, team: Team, question: JeopardyQuestion) -> None:
        team.remove_points(question.value)
