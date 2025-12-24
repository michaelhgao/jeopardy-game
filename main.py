import tkinter as tk

from src.jeopardy_game import JeopardyGame
from src.jeopardy_ui import JeopardyUi


def main() -> None:
    root = tk.Tk()

    # Launch maximized
    try:
        root.state("zoomed")
    except tk.TclError:
        root.attributes("-zoomed", True)

    game = JeopardyGame()
    JeopardyUi(root, game)

    root.mainloop()


if __name__ == "__main__":
    main()
