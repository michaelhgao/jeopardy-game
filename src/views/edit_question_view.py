import tkinter as tk
from tkinter import filedialog

from src.misc.button_factory import create_button
from src.misc.themes import BG_COLOUR, FONT, SMALL_BUTTON_THEME
from src.misc.types import Screen
from src.models.question import Question, QuestionEdit
from src.views.base_view import BaseView


class EditQuestionView(BaseView):
    def render(self, **kwargs) -> None:
        self.clear()

        question: Question = kwargs["question"]

        self.root.configure(bg=BG_COLOUR)

        tk.Label(
            self.root,
            text="Edit Question",
            font=(FONT, 32, "bold"),
            bg=BG_COLOUR,
        ).pack(pady=20)

        self.q_entry = tk.Entry(self.root, font=(FONT, 16), width=80)
        self.q_entry.insert(0, question.question)
        self.q_entry.pack(pady=5)

        self.a_entry = tk.Entry(self.root, font=(FONT, 16), width=80)
        self.a_entry.insert(0, question.answer)
        self.a_entry.pack(pady=5)

        self.value_entry = tk.Entry(self.root, font=(FONT, 16), width=10)
        self.value_entry.insert(0, str(question.value))
        self.value_entry.pack(pady=5)

        self.image_path = question.image_path

        create_button(
            self.root,
            text="Select Image",
            theme=SMALL_BUTTON_THEME,
            command=self._select_image,
        ).pack(pady=5)

        create_button(
            self.root,
            text="Save",
            theme=SMALL_BUTTON_THEME,
            command=lambda: self._save(question),
        ).pack(pady=10)

        create_button(
            self.root,
            text="Cancel",
            theme=SMALL_BUTTON_THEME,
            command=lambda: self.ui_controller.navigate(Screen.BOARD),
        ).pack(pady=10)

    def _select_image(self):
        self.image_path = filedialog.askopenfilename(
            title="Select image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")],
        )

    def _save(self, question: Question):
        edit = QuestionEdit(
            self.q_entry.get(),
            self.a_entry.get(),
            int(self.value_entry.get()),
            self.image_path,
        )
        self.game_controller.edit_question(question, edit)
        self.ui_controller.navigate(Screen.BOARD)
