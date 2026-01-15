import tkinter as tk

from src.controllers.game_controller import GameController
from src.controllers.ui_controller import UiController
from src.misc.types import Screen
from src.models.jeopardy_game import JeopardyGame


def main() -> None:
    # Create the root window
    root = tk.Tk()

    # Launch maximized
    try:
        root.state("zoomed")
    except tk.TclError:
        root.attributes("-zoomed", True)

    # Initialize the game and controller
    game = JeopardyGame()
    game_controller = GameController(game)
    ui_controller = UiController(root, game_controller)

    # Launch the UI with the controller
    ui_controller.navigate(Screen.MAIN_MENU)

    # Start the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
