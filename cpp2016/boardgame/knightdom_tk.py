#!/usr/bin/env python3
import sys
sys.path.append('../../examples/')

from knightdom import KnightDom
from boardgame_tk import BoardGameGui

def main():
    game = KnightDom(6)
    gui = BoardGameGui(game)
    gui.mainloop()
    
if __name__ == '__main__':
    main()
