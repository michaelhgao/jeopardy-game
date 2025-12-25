from typing import Optional

from src.misc.types import Category
from src.models.question import Question, QuestionEdit
from src.models.team import Team


class JeopardyGame:
    def __init__(self) -> None:
        self.categories: list[Category] = []
        self.teams: list[Team] = []

    def add_category(self, name: str) -> Category:
        if not name:
            raise ValueError("Category name cannot be empty")

        if any(c.name == name for c in self.categories):
            raise ValueError("Category already exists")

        category = Category(name=name, questions=[])
        self.categories.append(category)
        return category

    def remove_category(self, name: str) -> None:
        for i, category in enumerate(self.categories):
            if category.name == name:
                del self.categories[i]
                return
        raise KeyError(name)

    def edit_category(self, old_name: str, new_name: str) -> None:
        if not new_name:
            raise ValueError("Category name cannot be empty")

        if any(c.name == new_name for c in self.categories):
            raise ValueError("Category already exists")

        for category in self.categories:
            if category.name == old_name:
                category.name = new_name
                return

        raise KeyError(old_name)

    def add_question(self, category: Category, question: Question) -> None:
        category.questions.append(question)

    def get_question(self, category: Category, index: int) -> Question:
        return category.questions[index]

    def edit_question(
        self,
        question: Question,
        new: QuestionEdit,
        image_path: Optional[str] = None,
    ) -> None:
        question.question = new.question
        question.answer = new.answer
        question.value = new.value

        if image_path:
            question.image_path = image_path

    def add_team(self, name: str, members: list[str]) -> Team:
        if any(t.name == name for t in self.teams):
            raise ValueError("Team already exists")

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

    def assign_question_points(self, team: Optional[Team], question: Question) -> None:
        if team:
            team.add_points(question.value)
