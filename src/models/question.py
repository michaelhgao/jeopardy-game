from dataclasses import dataclass
from typing import Optional


class Question:
    def __init__(
        self, question: str, answer: str, value: int, image_path: Optional[str] = None
    ) -> None:
        self.question: str = question
        self.answer: str = answer
        self.value: int = value
        self.image_path: Optional[str] = image_path
        self.answered: bool = False

    def set_image(self, path: str) -> None:
        self.image_path = path

    def mark_answered(self) -> None:
        self.answered = True

    def reset(self) -> None:
        self.answered = False


@dataclass
class QuestionEdit:
    question: str
    answer: str
    value: int
    image_path: Optional[str] = None

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Question value cannot be negative")
        if not self.question.strip():
            raise ValueError("Question text cannot be empty")
        if not self.answer.strip():
            raise ValueError("Answer text cannot be empty")
