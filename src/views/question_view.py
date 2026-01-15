import tkinter as tk

from PIL import Image, ImageTk

from src.misc.button_factory import create_button
from src.misc.themes import (
    BG_COLOUR,
    FONT,
    QUESTION_TEXT_COLOUR,
    SMALL_BUTTON_THEME,
)
from src.misc.types import Screen
from src.models.question import Question
from src.views.base_view import BaseView


class QuestionView(BaseView):
    def render(self, **kwargs) -> None:
        self.clear()

        question: Question = kwargs["question"]

        self.root.configure(bg=BG_COLOUR)

        # Value
        tk.Label(
            self.root,
            text=f"${question.value}",
            font=(FONT, 36, "bold"),
            fg=QUESTION_TEXT_COLOUR,
            bg=BG_COLOUR,
        ).pack(pady=20)

        # Question text
        tk.Label(
            self.root,
            text=question.question,
            font=(FONT, 24),
            fg=QUESTION_TEXT_COLOUR,
            bg=BG_COLOUR,
            wraplength=1000,
            justify="center",
        ).pack(pady=20)

        # Optional image
        if question.image_path:
            try:
                img = Image.open(question.image_path)
                img.thumbnail((800, 600))
                photo = ImageTk.PhotoImage(img)

                self._images.append(photo)

                tk.Label(self.root, image=photo, bg=BG_COLOUR).pack(pady=10)
            except Exception as e:
                tk.Label(
                    self.root,
                    text=f"Failed to load image: {e}",
                    fg="red",
                    bg=BG_COLOUR,
                ).pack()

        # Buttons
        create_button(
            self.root,
            text="Show Answer",
            theme=SMALL_BUTTON_THEME,
            command=lambda: self.ui_controller.navigate(
                Screen.ANSWER,
                question=question,
            ),
        ).pack(pady=10)

        create_button(
            self.root,
            text="Back to Board",
            theme=SMALL_BUTTON_THEME,
            command=lambda: self.ui_controller.navigate(Screen.BOARD),
        ).pack(pady=10)
