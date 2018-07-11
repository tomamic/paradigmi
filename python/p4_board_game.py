#!/usr/bin/env python3
'''
@author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
'''

class BoardGame:
    
    def play_at(self, x: int, y: int):
        raise NotImplementedError("Abstract method")
    
    def get_val(self, x: int, y: int) -> str:
        raise NotImplementedError("Abstract method")
    
    def cols(self) -> int:
        raise NotImplementedError("Abstract method")
    
    def rows(self) -> int:
        raise NotImplementedError("Abstract method")
    
    def finished(self) -> bool:
        raise NotImplementedError("Abstract method")
    
    def message(self) -> str:
        raise NotImplementedError("Abstract method")
    

class Knights(BoardGame):
    '''Knights domination game: knights have to cover all cells'''
    
    def __init__(self, side: int):
        solutions = (0, 1, 4, 4, 4, 5, 8, 10, 12, 14, 16, 21,
                     24, 28, 32, 36, 40, 46, 52, 57, 62)

        self._cols = side
        self._rows = side
        self._n = solutions[side]
        self._dirs = ((-1, -2), (+1, -2), (+2, -1), (+2, +1),
                      (+1, +2), (-1, +2), (-2, +1), (-2, -1))  # dx, dy
        self._board = [[False for x in range(side)] for y in range(side)]

    def cols(self) -> int:
        '''Get the number of columns'''
        return self._cols

    def rows(self) -> int:
        '''Get the number of rows'''
        return self._rows

    def _covered(self, x: int, y: int) -> bool:
        '''Is cell (x, y) covered by a knight?'''
        for dx, dy in self._dirs:
            if (0 <= x + dx < self._cols and
                0 <= y + dy < self._rows and
                self._board[y + dy][x + dx]):
                return True
        return False

    def finished(self) -> bool:
        '''Game solved?'''
        knights = 0
        for y in range(self._rows):
            for x in range(self._cols):
                if self._board[y][x]:
                    knights += 1
                elif not self._covered(x, y):
                    return False
        return self._n == knights

    def play_at(self, x: int, y: int):
        '''Place (or remove) a knight at cell (x, y)'''
        if 0 <= x < self._cols and 0 <= y < self._rows:
            self._board[y][x] = not self._board[y][x]

    def get_val(self, x: int, y: int) -> str:
        if (0 <= x < self._cols and
            0 <= y < self._rows and
            self._board[y][x]):
            return '♞'
        return '-'

    def message(self) -> str:
        '''Message to show when the game is solved'''
        return "Knights dominate the board!"


def print_game(game: BoardGame):
    for y in range(game.rows()):
        for x in range(game.cols()):
            print('{:3}'.format(game.get_val(x, y)), end='')
        print()

def console_play(game: BoardGame):
    print_game(game)
    
    while not game.finished():
        x, y = input().split()
        game.play_at(int(x), int(y))
        print_game(game)
        
    print(game.message())

def main():
    game = Knights(6)
    console_play(game)

if __name__ == '__main__':
    main()
