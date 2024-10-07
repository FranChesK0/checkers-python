from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage

from checkers import RENDER_PARAMS, Game


def main() -> None:
    window = Tk()
    window.title("Checkers")
    window.resizable(False, False)
    window.iconphoto(False, PhotoImage(file=Path("assets", "icon.png")))

    canvas = Canvas(
        window,
        width=RENDER_PARAMS.CELL_SIZE * RENDER_PARAMS.X_SIZE,
        height=RENDER_PARAMS.CELL_SIZE * RENDER_PARAMS.Y_SIZE,
    )
    canvas.pack()

    game = Game(canvas, RENDER_PARAMS.X_SIZE, RENDER_PARAMS.Y_SIZE)

    canvas.bind("<Motion>", game.mouse_move)
    canvas.bind("<Button-1>", game.mouse_down)

    window.mainloop()


if __name__ == "__main__":
    main()
