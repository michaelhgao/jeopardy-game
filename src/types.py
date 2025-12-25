from enum import Enum, auto
from typing import Final


class GameMode(Enum):
    PLAY = auto()
    EDIT = auto()


# Background color
BG_COLOUR: Final[str] = "#060CE9"

# Buttons
BTN_COLOUR: Final[str] = "#003399"
BTN_ACTIVE_COLOUR: Final[str] = "#0055CC"
QUESTION_ANSWERED_COLOUR: Final[str] = "#001166"

# Text colors
TITLE_TEXT_COLOUR: Final[str] = "#FFFFFF"
BTN_TEXT_COLOUR: Final[str] = "#FFFFFF"
CATEGORY_TEXT_COLOUR: Final[str] = "#FFFFFF"
QUESTION_TEXT_COLOUR: Final[str] = "#FFCC00"

# Font
FONT: Final[str] = "Arial"
TITLE_FONT_SIZE: Final[int] = 72
TITLE_BUTTON_FONT_SIZE: Final[int] = 36
CATEGORY_FONT_SIZE: Final[int] = 36
BOARD_QUESTION_FONT_SIZE: Final[int] = 36
BTN_FONT_SIZE: Final[int] = 16
