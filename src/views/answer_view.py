import tkinter as tk

from src.misc.button_factory import create_button
from src.misc.themes import (
    ANSWER_TEXT_COLOUR,
    BG_COLOUR,
    BTN_TEXT_COLOUR,
    FONT,
    QUESTION_TEXT_COLOUR,
    SMALL_BUTTON_THEME,
)
from src.misc.types import Screen
from src.models.question import Question
from src.models.team import Team
from src.views.base_view import BaseView


class AnswerView(BaseView):
    def render(self, **kwargs) -> None:
        self.clear()

        question: Question = kwargs["question"]

        if not question.answered:
            question.mark_answered()

        self.root.configure(bg=BG_COLOUR)

        # Value
        tk.Label(
            self.root,
            text=f"${question.value}",
            font=(FONT, 32, "bold"),
            fg=QUESTION_TEXT_COLOUR,
            bg=BG_COLOUR,
        ).pack(pady=20)

        # Question text
        tk.Label(
            self.root,
            text=question.question,
            font=(FONT, 20),
            fg=QUESTION_TEXT_COLOUR,
            bg=BG_COLOUR,
            wraplength=1000,
            justify="center",
        ).pack(pady=10)

        # Answer
        tk.Label(
            self.root,
            text=f"Answer: {question.answer}",
            font=(FONT, 24, "bold"),
            fg=ANSWER_TEXT_COLOUR,
            bg=BG_COLOUR,
            wraplength=1000,
            justify="center",
        ).pack(pady=20)

        # Instruction
        tk.Label(
            self.root,
            text="Assign points to a team:",
            font=(FONT, 18, "italic"),
            fg=BTN_TEXT_COLOUR,
            bg=BG_COLOUR,
        ).pack(pady=10)

        # Team buttons
        for team in self.game_controller.get_teams():
            create_button(
                self.root,
                text=f"{team.name} +${question.value}",
                theme=SMALL_BUTTON_THEME,
                command=lambda t=team: self._assign_points(question, t),
            ).pack(pady=5)

        # Skip
        create_button(
            self.root,
            text="Skip / Back to Board",
            theme=SMALL_BUTTON_THEME,
            command=lambda: self.ui_controller.navigate(Screen.BOARD),
        ).pack(pady=10)

    def _assign_points(self, question: Question, team: Team):
        team.add_points(question.value)
        self.ui_controller.navigate(Screen.BOARD)
