import tkinter as tk

from src.controllers.game_controller import GameController
from src.models.jeopardy_game import JeopardyGame
from src.views.jeopardy_ui import JeopardyUi


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
    controller = GameController(game)

    # Launch the UI with the controller
    JeopardyUi(root, controller)

    # Start the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
