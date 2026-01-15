from dataclasses import dataclass
from enum import Enum, auto

from src.models.question import Question


class GameMode(Enum):
    PLAY = auto()
    EDIT = auto()


@dataclass
class Category:
    name: str
    questions: list[Question]


GRID_SIZE = 5


class Screen(Enum):
    MAIN_MENU = auto()
    BOARD = auto()
    QUESTION = auto()
    ANSWER = auto()
    SETUP_TEAMS = auto()
    TEAMS = auto()
    SAVE = auto()
    LOAD = auto()
    EDIT_QUESTION = auto()
    EDIT_CATEGORY = auto()
