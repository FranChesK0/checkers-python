from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage

from checkers import X_SIZE, Y_SIZE, CELL_SIZE, Game


def main() -> None:
    window = Tk()
    window.title("Checkers")
    window.resizable(False, False)
    window.iconphoto(False, PhotoImage(file=Path("assets", "icon.png")))

    canvas = Canvas(window, width=CELL_SIZE * X_SIZE, height=CELL_SIZE * Y_SIZE)
    canvas.pack()

    game = Game(canvas, X_SIZE, Y_SIZE)

    canvas.bind("<Motion>", game.mouse_move)
    canvas.bind("<Button-1>", game.mouse_down)

    window.mainloop()


if __name__ == "__main__":
    main()
