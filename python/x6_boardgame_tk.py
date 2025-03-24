#!/usr/bin/env python3

from tkinter import Tk, Button, messagebox
from boardgame import BoardGame

class BoardGameTk(Tk):
    def __init__(self, g: BoardGame):
        Tk.__init__(self)
        self._game = g
        
        for y in range(g.rows()):
            for x in range(g.cols()):
                b = Button(self, width=3, height=2, font=('', 16))
                b['command'] = (lambda x=x, y=y:
                                (self._game.play(x, y, ""),
                                 self.update_buttons()))
                b.grid(column=x, row=y)
        self.resizable(0, 0)
        self.update_buttons()

    def update_buttons(self):
        for y in range(self._game.rows()):
            for x in range(self._game.cols()):
                b = self.grid_slaves(row=y, column=x)[0]
                b['text'] = self._game.read(x, y)
        if self._game.finished():
            messagebox.showinfo('Game finished', self._game.status())
            self.destroy()

if __name__ == "__main__":
    from c09_fifteen import Fifteen 
    game = Fifteen(4, 4)
    gui = BoardGameTk(game)
    gui.mainloop()