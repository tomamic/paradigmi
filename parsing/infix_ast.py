#!/usr/bin/env python3
"""
@author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
"""

from infix_eval import parse_expr
from math import isclose
from operator import add, sub, mul, truediv, neg

ops = {"+": add, "-": sub, "*": mul, "/": truediv, "~": neg}

class Expression:
    def to_prefix(self) -> str:
        raise NotImplementedError("Abstract method")

    def eval(self, context: dict[str, float]) -> float:
        raise NotImplementedError("Abstract method")

class BinaryOp(Expression):
    def __init__(self, op, x, y):
        self._op, self._x, self._y = op, x, y

    def to_prefix(self):
        x = self._x.to_prefix()
        y = self._y.to_prefix()
        return f"{self._op} {x} {y}"

    def eval(self, ctx):
        x = self._x.eval(ctx)
        y = self._y.eval(ctx)
        op = ops[self._op]
        return op(x, y)


class UnaryOp(Expression):
    def __init__(self, op, x):
        self._op, self._x = op, x

    def to_prefix(self):
        x = self._x.to_prefix()
        return f"{self._op}{x}"

    def eval(self, ctx):
        x = self._x.eval(ctx)
        op = ops[self._op]
        return op(x)

class Var(Expression):
    def __init__(self, name):
        self._name = name

    def to_prefix(self):
        return f"{self._name}"

    def eval(self, ctx):
        return ctx.get(self._name, 0)

class Num(Expression):
    def __init__(self, val):
        self._val = val

    def to_prefix(self):
        return f"{self._val}"

    def eval(self, ctx):
        return self._val


class Action:
    def add(self, x, y): return BinaryOp("+", x, y)
    def sub(self, x, y): return BinaryOp("-", x, y)
    def mul(self, x, y): return BinaryOp("*", x, y)
    def div(self, x, y): return BinaryOp("/", x, y)
    def neg(self, x): return UnaryOp("~", x)
    def num(self, x): return Num(float(x))
    def var(self, x): return Var(x)


# Tests
def main():
    ctx = {"w": 0.0, "x": 1.0, "y": 1.5, "z": 0.5}

    tests = [("(((1.5)))", "1.5", 1.5),
             ("w * -z", "* w ~z", 0.0),
             ("x / z * -y", "* / x z ~y", -3.0),
             ("x / 0.5 * --y", "* / x 0.5 ~~y", 3.0),
             ("w", "w", 0.0),
             ("(x + w) * (x + y)", "* + x w + x y", 2.5)]

    act = Action()
    for infix, prefix, val in tests:
        expr = parse_expr(infix, act)
        assert expr.to_prefix() == prefix
        assert isclose(expr.eval(ctx), val)

if __name__ == "__main__":
    main()
