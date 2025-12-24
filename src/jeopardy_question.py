from typing import Optional


class JeopardyQuestion:
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
