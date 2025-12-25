import tkinter as tk
from enum import Enum, auto
from tkinter import filedialog, simpledialog
from typing import Optional

from src.jeopardy_game import JeopardyGame
from src.jeopardy_question import JeopardyQuestion
from src.team import Team
from src.types import (
    BG_COLOUR,
    BTN_ACTIVE_COLOUR,
    BTN_COLOUR,
    BTN_TEXT_COLOUR,
    CATEGORY_TEXT_COLOUR,
    FONT,
    QUESTION_ANSWERED_COLOUR,
    QUESTION_TEXT_COLOUR,
    TITLE_TEXT_COLOUR,
    GameMode,
)


class Screen(Enum):
    MAIN_MENU = auto()
    BOARD = auto()
    QUESTION = auto()
    ANSWER = auto()
    TEAMS = auto()


class JeopardyUi:
    GRID_SIZE = 5

    def __init__(self, root: tk.Tk, game: JeopardyGame) -> None:
        self.root: tk.Tk = root
        self.game: JeopardyGame = game
        self.root.title("Jeopardy")

        self.main_frame: tk.Frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.category_buttons: list[tk.Button] = []
        self.question_buttons: list[list[tk.Button]] = []

        self._build_main_menu()

    def _clear(self) -> None:
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def _build_main_menu(self) -> None:
        self._clear()

        # Set background color
        self.main_frame.config(bg=BG_COLOUR)

        # Title
        tk.Label(
            self.main_frame,
            text="JEOPARDY",
            font=(FONT, 72, "bold"),
            fg=TITLE_TEXT_COLOUR,
            bg=BG_COLOUR,
        ).pack(pady=40)

        # Play Mode button
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

        # Edit Mode button
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

    def _play_mode(self) -> None:
        self.game.set_mode(GameMode.PLAY)
        self._setup_teams()

    def _edit_mode(self) -> None:
        self.game.set_mode(GameMode.EDIT)
        self._build_board(editable=True)

    def _build_board(self, editable: bool) -> None:
        self._clear()
        self.category_buttons.clear()
        self.question_buttons.clear()

        # Set background
        self.main_frame.config(bg=BG_COLOUR)

        # Ensure at least 5 categories exist
        while len(self.game.category_order) < self.GRID_SIZE:
            cat_name = f"Category {len(self.game.category_order) + 1}"
            self.game.add_category(cat_name)

        categories = self.game.category_order[: self.GRID_SIZE]

        # Grid layout
        for r in range(self.GRID_SIZE + 1):  # +1 for category row
            self.main_frame.grid_rowconfigure(r, weight=1)
        for c in range(self.GRID_SIZE):
            self.main_frame.grid_columnconfigure(c, weight=1, uniform="UNIFORM")

        # CATEGORY ROW
        for i, cat_name in enumerate(categories):
            btn = tk.Button(
                self.main_frame,
                text=cat_name,
                fg=CATEGORY_TEXT_COLOUR,
                bg=BTN_COLOUR,
                font=(FONT, 24, "bold"),
                command=lambda i=i: self._edit_category(i) if editable else None,
            )
            btn.grid(row=0, column=i, sticky="nsew", padx=2, pady=2)
            self.category_buttons.append(btn)

        # QUESTION GRID
        for row in range(self.GRID_SIZE):
            row_buttons: list[tk.Button] = []
            for col in range(self.GRID_SIZE):
                category = categories[col]
                while len(self.game.questions[category]) <= row:
                    self.game.add_question(
                        category,
                        JeopardyQuestion("New Question", "Answer", (row + 1) * 100),
                    )
                q = self.game.questions[category][row]

                btn_text = f"${q.value}"
                btn = tk.Button(
                    self.main_frame,
                    text=btn_text,
                    fg=QUESTION_TEXT_COLOUR,
                    bg=BTN_COLOUR if not q.answered else QUESTION_ANSWERED_COLOUR,
                    font=(FONT, 24, "bold"),
                    command=lambda q=q, editable=editable: (
                        self._edit_question(q) if editable else self._show_question(q)
                    ),
                )
                btn.grid(row=row + 1, column=col, sticky="nsew", padx=2, pady=2)
                row_buttons.append(btn)
            self.question_buttons.append(row_buttons)

        # BOTTOM BUTTON BAR
        bottom_frame = tk.Frame(self.main_frame, bg=BG_COLOUR, height=50)
        bottom_frame.grid(
            row=self.GRID_SIZE + 1,
            column=0,
            columnspan=self.GRID_SIZE,
            sticky="nsew",
        )
        self.main_frame.grid_rowconfigure(self.GRID_SIZE + 1, weight=0)

        # Back button
        tk.Button(
            bottom_frame,
            text="Back",
            font=(FONT, 16, "bold"),
            height=1,
            bg=BTN_COLOUR,
            fg=BTN_TEXT_COLOUR,
            command=self._build_main_menu,
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
                command=self._show_teams_points,
            ).pack(side=tk.LEFT, padx=5, pady=5)

    def _setup_teams(self) -> None:
        self.game.clear_teams()

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
            self.game.add_team(team_name, [])

        self._build_board(editable=False)

    def _edit_category(self, index: int) -> None:
        old_name = self.game.category_order[index]

        new_name: Optional[str] = simpledialog.askstring(
            "Edit Category", f"Rename '{old_name}':"
        )
        if new_name is None:
            return

        success: bool = self.game.edit_category(index, new_name)

        if success:
            self._build_board(editable=True)

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

        self.game.edit_question(
            question=question,
            new_question=q_text,
            new_answer=a_text,
            new_value=value,
            image_path=image_path,
        )

        self._build_board(editable=True)

    def _show_question(self, question: JeopardyQuestion) -> None:
        self._clear()

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

                if not hasattr(self, "_images"):
                    self._images: list[ImageTk.PhotoImage] = []
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
            command=lambda q=question: self._show_answer(q),
        ).pack(pady=10)

        tk.Button(
            self.main_frame,
            text="Back to Board",
            font=(FONT, 16, "bold"),
            fg=BTN_TEXT_COLOUR,
            bg=BTN_COLOUR,
            activebackground=BTN_ACTIVE_COLOUR,
            command=lambda: self._build_board(editable=False),
        ).pack(pady=10)

    def _show_answer(self, question: JeopardyQuestion) -> None:
        self._clear()

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
            fg="green",
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
        for team in self.game.teams:
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
            command=lambda: self._build_board(editable=False),
        ).pack(pady=10)

    def _assign_points(self, question: JeopardyQuestion, team: Team) -> None:
        self.game.add_points(team, question)
        self._build_board(editable=False)

    def _show_teams_points(self) -> None:
        self._clear()

        # Title
        tk.Label(
            self.main_frame,
            text="Team Scores",
            font=(FONT, 36, "bold"),
            fg=TITLE_TEXT_COLOUR,
            bg=BG_COLOUR,
        ).pack(pady=20)

        # List each team and points
        for team in self.game.teams:
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
            command=lambda: self._build_board(editable=False),
        ).pack(pady=20)
