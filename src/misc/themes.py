from dataclasses import dataclass
from typing import Final, Tuple

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
ANSWER_TEXT_COLOUR: Final[str] = "#11AA11"

# Font
FONT: Final[str] = "Arial"
TITLE_FONT_SIZE: Final[int] = 72
TITLE_BUTTON_FONT_SIZE: Final[int] = 36
CATEGORY_FONT_SIZE: Final[int] = 36
BOARD_QUESTION_FONT_SIZE: Final[int] = 36
BTN_FONT_SIZE: Final[int] = 16


@dataclass
class ButtonTheme:
    bg: str
    fg: str
    font: Tuple[str, int, str]  # font name, font size, font weight
    active_bg: str
    active_fg: str
    borderwidth: int
    width: int
    height: int


MAIN_MENU_BUTTON_THEME = ButtonTheme(
    bg="#003399",
    fg="#FFFFFF",
    font=("Arial", 36, "bold"),
    active_bg="#0055CC",
    active_fg="#FFFFFF",
    borderwidth=2,
    width=16,
    height=1,
)

CATEGORY_BUTTON_THEME = ButtonTheme(
    bg="#003399",
    fg="#FFFFFF",
    font=("Arial", 24, "bold"),
    active_bg="#0055CC",
    active_fg="#FFFFFF",
    borderwidth=2,
    width=0,
    height=0,
)

QUESTION_BUTTON_THEME = ButtonTheme(
    bg="#003399",
    fg="#FFCC00",
    font=(FONT, 24, "bold"),
    active_bg="#003399",
    active_fg="#FFCC00",
    borderwidth=2,
    width=0,
    height=0,
)

SMALL_BUTTON_THEME = ButtonTheme(
    bg="#003399",
    fg="#FFFFFF",
    font=("Arial", 16, "bold"),
    active_bg="#0055CC",
    active_fg="#FFFFFF",
    borderwidth=2,
    width=0,
    height=0,
)
