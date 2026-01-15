import tkinter as tk
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from src.controllers.game_controller import GameController

if TYPE_CHECKING:
    from src.controllers.ui_controller import UiController


class BaseView(ABC):
    def __init__(
        self,
        root: tk.Frame,
        game_controller: GameController,
        ui_controller: "UiController",
    ):
        self.root = root
        self.game_controller = game_controller
        self.ui_controller = ui_controller
        self._images = []

    @abstractmethod
    def render(self, **kwargs):
        pass

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self._images.clear()

    def destroy(self):
        self.root.destroy()
