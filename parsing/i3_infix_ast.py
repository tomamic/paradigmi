#!/usr/bin/env python3
"""
@author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
"""

from i3_infix_eval import parse_expr

class Expression:
    def print(self, indent):
        raise NotImplementedError("Abstract method")

class BinaryOp(Expression):
    def __init__(self, op, x, y):
        self._op, self._x, self._y = op, x, y

    def print(self, indent):
        print(indent, self._op)
        self._x.print(indent + "  ")
        self._y.print(indent + "  ")

class UnaryOp(Expression):
    def __init__(self, op, x):
        self._op, self._x = op, x

    def print(self, indent):
        print(indent, self._op)
        self._x.print(indent + "  ")

class Var(Expression):
    def __init__(self, name):
        self._name = name

    def print(self, indent):
        print(indent, self._name)

class Num(Expression):
    def __init__(self, val):
        self._val = val

    def print(self, indent):
        print(indent, self._val)

class Actions:
    def add(self, x, y): return BinaryOp("+", x, y)
    def sub(self, x, y): return BinaryOp("-", x, y)
    def mul(self, x, y): return BinaryOp("*", x, y)
    def div(self, x, y): return BinaryOp("/", x, y)
    def opp(self, x): return UnaryOp("~", x)
    def num(self, x): return Num(float(x))
    def var(self, x): return Var(x)


# Tests.
act = Actions()

if __name__ == "__main__":
    parse_expr("(((1.5)))", act).print("")
    parse_expr("w * -z", act).print("")
    parse_expr("x / z * -y", act).print("")
    parse_expr("x / 0.5 * --y", act).print("")
    parse_expr("w", act).print("")
    parse_expr("(x + w) * (x + y) * (y - z)", act).print("")
