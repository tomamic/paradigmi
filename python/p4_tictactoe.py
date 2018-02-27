#!/usr/bin/env python3
'''
@author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
'''

import sys

from p4_board_game import BoardGame, console_play

class TicTacToe(BoardGame):
    NONE = '.'
    PLR1 = 'X'
    PLR2 = 'O'
    DRAW = 'N'
    OUT = '!'

    def __init__(self, side=3):
        self._side = side
        self._matrix = [self.NONE] * (self._side * self._side)
        self._winner = self.NONE
        self.clear()

    def clear(self):
        for i in range(len(self._matrix)):
            self._matrix[i] = self.NONE
        self._turn = 0

    def play_at(self, x: int, y: int):
        if self.get_val(x, y) == self.NONE:
            i = y * self._side + x
            if self._turn % 2 == 0:
                self._matrix[i] = self.PLR1
            else:
                self._matrix[i] = self.PLR2
            self._turn += 1
            self._winner = self.winner()

    def get_val(self, x: int, y: int) -> str:
        if 0 <= x < self._side and 0 <= y < self._side:
            return self._matrix[y * self._side + x]
        else:
            return self.OUT

    def _check_line(self, x: int, y: int, dx: int, dy: int) -> bool:
        '''Check a single line, starting at (x, y) and
        advancing for `side` steps in direction (dx, dy).
        If a single player occupies all cells, he's won.'''
        player = self.get_val(x, y)
        if player == self.NONE:
            return False
        for i in range(self._side):
            if self.get_val(x + dx * i, y + dy * i) != player:
                return False
        return True

    def finished(self) -> bool:
        return self._winner != self.NONE
        
    def message(self) -> str:
        return "Winner: " + self._winner
        
    def winner(self) -> str:
        '''Check all rows, columns and diagonals.
        Otherwise, check if the game is tied.'''
        for x in range(self._side):
            if self._check_line(x, 0, 0, 1):
                return self.get_val(x, 0)
        for y in range(self._side):
            if self._check_line(0, y, 1, 0):
                return self.get_val(0, y)
        if self._check_line(0, 0, 1, 1):
            return self.get_val(0, 0)
        if self._check_line(self._side - 1, 0, -1, 1):
            return self.get_val(self._side - 1, 0)
        if self._turn == self._side * self._side:
            return self.DRAW
        return self.NONE

    def cols(self) -> int:
        return self._side

    def rows(self) -> int:
        return self._side

    def __str__(self):
        '''Get a string representation of the game'''
        result = []
        for y in range(self._side):
            for x in range(self._side):
                result.append(self.get_val(x, y))
            result.append('\n')
        return "".join(result)

def main():
    game = TicTacToe(3)
    console_play(game)    

if __name__ == '__main__':
    main()
