import tkinter as tk
from enum import Enum, auto
from tkinter import filedialog, simpledialog
from typing import Optional

from src.controllers.game_controller import GameController
from src.misc.types import (
    ANSWER_TEXT_COLOUR,
    BG_COLOUR,
    BTN_ACTIVE_COLOUR,
    BTN_COLOUR,
    BTN_TEXT_COLOUR,
    CATEGORY_TEXT_COLOUR,
    FONT,
    GRID_SIZE,
    QUESTION_ANSWERED_COLOUR,
    QUESTION_TEXT_COLOUR,
    TITLE_TEXT_COLOUR,
    Category,
    GameMode,
)
from src.models.jeopardy_question import JeopardyQuestion, QuestionEdit
from src.models.team import Team


class Screen(Enum):
    MAIN_MENU = auto()
    BOARD = auto()
    QUESTION = auto()
    ANSWER = auto()
    TEAMS = auto()


class JeopardyUi:
    def __init__(self, root: tk.Tk, controller: GameController) -> None:
        self.root: tk.Tk = root
        self.controller = controller
        self.root.title("Jeopardy")

        self.main_frame: tk.Frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.category_buttons: list[tk.Button] = []
        self.question_buttons: list[list[tk.Button]] = []

        self._images: list = []

        self.navigate(Screen.MAIN_MENU)

    def navigate(self, screen: Screen, question: Optional[JeopardyQuestion] = None):
        self.current_screen = screen
        self.current_question = question
        self._clear()
        self.main_frame.config(bg=BG_COLOUR)

        if screen == Screen.MAIN_MENU:
            self._render_main_menu()
        elif screen == Screen.BOARD:
            self._render_board()
        elif screen == Screen.QUESTION:
            if question is None:
                raise ValueError("Question must be provided for QUESTION screen")
            self._render_question(question)
        elif screen == Screen.ANSWER:
            if question is None:
                raise ValueError("Question must be provided for ANSWER screen")
            self._render_answer(question)
        elif screen == Screen.TEAMS:
            self._render_teams()

    def _render_main_menu(self) -> None:
        tk.Label(
            self.main_frame,
            text="JEOPARDY",
            font=(FONT, 72, "bold"),
            fg=TITLE_TEXT_COLOUR,
            bg=BG_COLOUR,
        ).pack(pady=40)

        tk.Button(
            self.main_frame,
            text="Play Mode",
            width=16,
            font=(FONT, 36, "bold"),
            fg=BTN_TEXT_COLOUR,
            bg=BTN_COLOUR,
            activebackground=BTN_ACTIVE_COLOUR,
            command=self._play_mode,
        ).pack(pady=10)

        tk.Button(
            self.main_frame,
            text="Edit Mode",
            width=16,
            font=(FONT, 36, "bold"),
            fg=BTN_TEXT_COLOUR,
            bg=BTN_COLOUR,
            activebackground=BTN_ACTIVE_COLOUR,
            command=self._edit_mode,
        ).pack(pady=10)

    def _render_board(self) -> None:
        self.controller.ensure_minimum_board()
        editable = self.controller.get_mode() == GameMode.EDIT

        categories = self.controller.get_categories()[:GRID_SIZE]

        # Grid layout
        for r in range(GRID_SIZE + 1):  # +1 for category row
            self.main_frame.grid_rowconfigure(r, weight=1)
        for c in range(GRID_SIZE):
            self.main_frame.grid_columnconfigure(c, weight=1, uniform="UNIFORM")

        # CATEGORY ROW
        for i, category in enumerate(categories):
            btn = tk.Button(
                self.main_frame,
                text=category.name,
                fg=CATEGORY_TEXT_COLOUR,
                bg=BTN_COLOUR,
                font=(FONT, 24, "bold"),
                command=lambda c=category: self._edit_category(c) if editable else None,
            )
            btn.grid(row=0, column=i, sticky="nsew", padx=2, pady=2)
            self.category_buttons.append(btn)

        # QUESTION GRID
        for row in range(GRID_SIZE):
            row_buttons: list[tk.Button] = []
            for col in range(GRID_SIZE):
                category = categories[col]
                q = category.questions[row]

                btn = tk.Button(
                    self.main_frame,
                    text=f"${q.value}",
                    fg=QUESTION_TEXT_COLOUR,
                    bg=BTN_COLOUR if not q.answered else QUESTION_ANSWERED_COLOUR,
                    font=(FONT, 24, "bold"),
                    command=lambda q=q, editable=editable: (
                        self._edit_question(q)
                        if editable
                        else self.navigate(Screen.QUESTION, q)
                    ),
                )
                btn.grid(row=row + 1, column=col, sticky="nsew", padx=2, pady=2)
                row_buttons.append(btn)
            self.question_buttons.append(row_buttons)

        # BOTTOM BUTTON BAR
        bottom_frame = tk.Frame(self.main_frame, bg=BG_COLOUR, height=50)
        bottom_frame.grid(
            row=GRID_SIZE + 1,
            column=0,
            columnspan=GRID_SIZE,
            sticky="nsew",
        )
        self.main_frame.grid_rowconfigure(GRID_SIZE + 1, weight=0)

        # Back button
        tk.Button(
            bottom_frame,
            text="Back",
            font=(FONT, 16, "bold"),
            height=1,
            bg=BTN_COLOUR,
            fg=BTN_TEXT_COLOUR,
            command=lambda: self.navigate(Screen.MAIN_MENU),
        ).pack(side=tk.LEFT, padx=5, pady=5)

        if not editable:
            # Teams / Points button
            tk.Button(
                bottom_frame,
                text="Teams / Points",
                font=(FONT, 16, "bold"),
                height=1,
                bg=BTN_COLOUR,
                fg=BTN_TEXT_COLOUR,
                command=lambda: self.navigate(Screen.TEAMS),
            ).pack(side=tk.LEFT, padx=5, pady=5)

    def _render_question(self, question: JeopardyQuestion) -> None:
        # Category and question value
        tk.Label(
            self.main_frame,
            text=f"${question.value}",
            font=(FONT, 36, "bold"),
            fg=QUESTION_TEXT_COLOUR,
            bg=BG_COLOUR,
        ).pack(pady=20)

        # Question text
        tk.Label(
            self.main_frame,
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
                from PIL import Image, ImageTk

                img = Image.open(question.image_path)
                img.thumbnail((800, 600))
                photo = ImageTk.PhotoImage(img)

                self._images.append(photo)

                tk.Label(self.main_frame, image=photo, bg=BG_COLOUR).pack(pady=10)
            except Exception as e:
                tk.Label(
                    self.main_frame,
                    text=f"Failed to load image: {e}",
                    fg="red",
                    bg=BG_COLOUR,
                ).pack()

        # Buttons
        tk.Button(
            self.main_frame,
            text="Show Answer",
            font=(FONT, 16, "bold"),
            fg=BTN_TEXT_COLOUR,
            bg=BTN_COLOUR,
            activebackground=BTN_ACTIVE_COLOUR,
            command=lambda: self.navigate(Screen.ANSWER, question),
        ).pack(pady=10)

        tk.Button(
            self.main_frame,
            text="Back to Board",
            font=(FONT, 16, "bold"),
            fg=BTN_TEXT_COLOUR,
            bg=BTN_COLOUR,
            activebackground=BTN_ACTIVE_COLOUR,
            command=lambda: self.navigate(Screen.BOARD),
        ).pack(pady=10)

    def _render_answer(self, question: JeopardyQuestion) -> None:
        if not question.answered:
            question.mark_answered()

        # Question value
        tk.Label(
            self.main_frame,
            text=f"${question.value}",
            font=(FONT, 32, "bold"),
            fg=QUESTION_TEXT_COLOUR,
            bg=BG_COLOUR,
        ).pack(pady=20)

        # Question text
        tk.Label(
            self.main_frame,
            text=question.question,
            font=(FONT, 20),
            fg=QUESTION_TEXT_COLOUR,
            bg=BG_COLOUR,
            wraplength=1000,
            justify="center",
        ).pack(pady=10)

        # Answer
        tk.Label(
            self.main_frame,
            text=f"Answer: {question.answer}",
            font=(FONT, 24, "bold"),
            fg=ANSWER_TEXT_COLOUR,
            bg=BG_COLOUR,
            wraplength=1000,
            justify="center",
        ).pack(pady=20)

        # Instruction
        tk.Label(
            self.main_frame,
            text="Assign points to a team:",
            font=(FONT, 18, "italic"),
            fg=BTN_TEXT_COLOUR,
            bg=BG_COLOUR,
        ).pack(pady=10)

        # Buttons for each team
        for team in self.controller.get_teams():
            tk.Button(
                self.main_frame,
                text=f"{team.name} +${question.value}",
                font=(FONT, 16, "bold"),
                fg=BTN_TEXT_COLOUR,
                bg=BTN_COLOUR,
                activebackground=BTN_ACTIVE_COLOUR,
                command=lambda t=team: self._assign_points(question, t),
            ).pack(pady=5)

        # Optional: Skip assigning points
        tk.Button(
            self.main_frame,
            text="Skip / Back to Board",
            font=(FONT, 16, "bold"),
            fg=BTN_TEXT_COLOUR,
            bg=BTN_COLOUR,
            activebackground=BTN_ACTIVE_COLOUR,
            command=lambda: self.navigate(Screen.BOARD),
        ).pack(pady=10)

    def _render_teams(self) -> None:
        # Title
        tk.Label(
            self.main_frame,
            text="Team Scores",
            font=(FONT, 36, "bold"),
            fg=TITLE_TEXT_COLOUR,
            bg=BG_COLOUR,
        ).pack(pady=20)

        # List each team and points
        for team in self.controller.get_teams():
            tk.Label(
                self.main_frame,
                text=f"{team.name}: {team.points} points",
                font=(FONT, 24),
                fg=QUESTION_TEXT_COLOUR,
                bg=BG_COLOUR,
            ).pack(pady=10)

        # Back button
        tk.Button(
            self.main_frame,
            text="Back to Board",
            font=(FONT, 16, "bold"),
            fg=BTN_TEXT_COLOUR,
            bg=BTN_COLOUR,
            activebackground=BTN_ACTIVE_COLOUR,
            command=lambda: self.navigate(Screen.BOARD),
        ).pack(pady=20)

    def _clear(self) -> None:
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self._images.clear()

    def _play_mode(self):
        self.controller.set_mode(GameMode.PLAY)
        self._setup_teams()

    def _edit_mode(self):
        self.controller.set_mode(GameMode.EDIT)
        self.navigate(Screen.BOARD)

    def _setup_teams(self) -> None:
        self.controller.clear_teams()

        num_teams: Optional[int] = simpledialog.askinteger(
            "Teams", "How many teams? (1-10)", minvalue=1, maxvalue=10
        )
        if not num_teams:
            return

        for i in range(num_teams):
            team_name: Optional[str] = simpledialog.askstring(
                "Team Name", f"Enter name for Team {i + 1}:"
            )
            if not team_name:
                team_name = f"Team {i + 1}"
            self.controller.add_team(team_name, [])

        self.navigate(Screen.BOARD)

    def _edit_category(self, category: Category) -> None:
        new_name: Optional[str] = simpledialog.askstring(
            "Edit Category", f"Rename '{category.name}':"
        )
        if new_name is None:
            return

        self.controller.edit_category(category.name, new_name)
        self.navigate(Screen.BOARD)

    def _edit_question(self, question: JeopardyQuestion) -> None:
        q_text: Optional[str] = simpledialog.askstring(
            "Question",
            "Question:",
            initialvalue=question.question,
        )
        if q_text is None:
            return

        a_text: Optional[str] = simpledialog.askstring(
            "Answer",
            "Answer:",
            initialvalue=question.answer,
        )
        if a_text is None:
            return

        value: Optional[int] = simpledialog.askinteger(
            "Value",
            "Point value:",
            initialvalue=question.value,
        )
        if value is None:
            return

        image_path: Optional[str] = filedialog.askopenfilename(
            title="Select image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")],
        )

        q_edit: QuestionEdit = QuestionEdit(q_text, a_text, value, image_path)

        self.controller.edit_question(question, q_edit)

        self.navigate(Screen.BOARD)

    def _assign_points(self, question: JeopardyQuestion, team: Team) -> None:
        self.controller.assign_question_points(team, question)
        self.navigate(Screen.BOARD)
