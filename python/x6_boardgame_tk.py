#!/usr/bin/env python3

from tkinter import Tk, Button, messagebox
from boardgame import BoardGame

class BoardGameTk(Tk):
    def __init__(self, g: BoardGame):
        Tk.__init__(self)
        self._game = g

        for y in range(g.rows()):
            for x in range(g.cols()):
                b = Button(self, width=3, height=2, font=("", 16))
                b["command"] = lambda x=x, y=y: self.handle_click(x, y)
                b.grid(column=x, row=y)
        self.resizable(0, 0)
        self.handle_click(-1, -1)

    def handle_click(self, bx=-1, by=-1):
        g = self._game
        if bx >= 0 and by >= 0:
            g.play(bx, by, "")
        for y in range(g.rows()):
            for x in range(g.cols()):
                b = self.grid_slaves(row=y, column=x)[0]
                b["text"] = g.read(x, y)
        if g.finished():
            messagebox.showinfo("Game finished", g.status())
            self.destroy()

if __name__ == "__main__":
    # import sys; sys.path.append("../../fondinfo")
    from c09_fifteen import Fifteen
    game = Fifteen(4, 4)
    gui = BoardGameTk(game)
    gui.mainloop()
