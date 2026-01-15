import tkinter as tk

from src.misc.button_factory import create_button
from src.misc.themes import (
    BG_COLOUR,
    BTN_COLOUR,
    CATEGORY_BUTTON_THEME,
    QUESTION_ANSWERED_COLOUR,
    QUESTION_BUTTON_THEME,
    SMALL_BUTTON_THEME,
)
from src.misc.types import GRID_SIZE, Category, GameMode, Screen
from src.models.question import Question
from src.views.base_view import BaseView


class BoardView(BaseView):
    def __init__(self, root, game_controller, ui_controller):
        super().__init__(root, game_controller, ui_controller)
        self.category_buttons: list[tk.Button] = []
        self.question_buttons: list[list[tk.Button]] = []

    def render(self, **kwargs) -> None:
        self.clear()

        self.category_buttons.clear()
        self.question_buttons.clear()

        self.game_controller.ensure_minimum_board()
        editable = self.game_controller.get_mode() == GameMode.EDIT
        categories = self.game_controller.get_categories()[:GRID_SIZE]

        for r in range(GRID_SIZE + 1):  # +1 for category row
            self.root.grid_rowconfigure(r, weight=1)
        for c in range(GRID_SIZE):
            self.root.grid_columnconfigure(c, weight=1, uniform="UNIFORM")

        for i, category in enumerate(categories):
            btn = create_button(
                self.root,
                text=category.name,
                theme=CATEGORY_BUTTON_THEME,
                command=(
                    lambda c=category: self._edit_category(c) if editable else None
                ),
            )
            btn.grid(row=0, column=i, sticky="nsew", padx=2, pady=2)
            self.category_buttons.append(btn)

        for row in range(GRID_SIZE):
            row_buttons: list[tk.Button] = []
            for col in range(GRID_SIZE):
                category = categories[col]
                q = category.questions[row]

                btn_bg = BTN_COLOUR if not q.answered else QUESTION_ANSWERED_COLOUR
                btn = create_button(
                    self.root,
                    text=f"${q.value}",
                    theme=QUESTION_BUTTON_THEME,
                    command=lambda q=q, editable=editable: self._on_question_click(
                        q, editable
                    ),
                    bg=btn_bg,
                    activebackground=btn_bg,
                )
                btn.grid(row=row + 1, column=col, sticky="nsew", padx=2, pady=2)
                row_buttons.append(btn)
            self.question_buttons.append(row_buttons)

        bottom_frame = tk.Frame(self.root, bg=BG_COLOUR, height=50)
        bottom_frame.grid(
            row=GRID_SIZE + 1,
            column=0,
            columnspan=GRID_SIZE,
            sticky="nsew",
        )
        self.root.grid_rowconfigure(GRID_SIZE + 1, weight=0)

        create_button(
            bottom_frame,
            text="Back",
            theme=SMALL_BUTTON_THEME,
            command=lambda: self.ui_controller.navigate(Screen.MAIN_MENU),
        ).pack(side=tk.LEFT, padx=5, pady=5)

        if not editable:
            create_button(
                bottom_frame,
                text="Teams / Points",
                theme=SMALL_BUTTON_THEME,
                command=lambda: self.ui_controller.navigate(Screen.TEAMS),
            ).pack(side=tk.LEFT, padx=5, pady=5)

    def _on_question_click(self, question: Question, editable: bool) -> None:
        if editable:
            self._edit_question(question)
        else:
            self.ui_controller.navigate(Screen.QUESTION, question=question)

    def _edit_category(self, category: Category) -> None:
        self.ui_controller.navigate(
            Screen.EDIT_CATEGORY,
            category=category,
        )

    def _edit_question(self, question: Question) -> None:
        self.ui_controller.navigate(
            Screen.EDIT_QUESTION,
            question=question,
        )
