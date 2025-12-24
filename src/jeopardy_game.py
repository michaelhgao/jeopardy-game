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

    def add_question(self, category: str, question: JeopardyQuestion) -> None:
        self.questions[category].append(question)

    def get_question(self, category: str, index: int) -> JeopardyQuestion:
        return self.questions[category][index]

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

    def add_points(self, team_name: str, question: JeopardyQuestion) -> None:
        team = self.get_team(team_name)
        team.add_points(question.value)
        question.mark_answered()

    def remove_points(self, team_name: str, question: JeopardyQuestion) -> None:
        team = self.get_team(team_name)
        team.remove_points(question.value)
