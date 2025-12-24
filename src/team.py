class Team:
    def __init__(self, name: str, members: list[str]) -> None:
        self.name: str = name
        self.members: list[str] = members
        self.points: int = 0

    def add_points(self, amount: int) -> None:
        self.points += amount

    def remove_points(self, amount: int) -> None:
        self.points -= amount

    def reset_points(self) -> None:
        self.points = 0
