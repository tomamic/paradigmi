#!/usr/bin/env python3
"""
@author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
"""

import re
from math import isclose

# expr = term {( "+" | "-" ) term}
# term = factor {( "*" | "/" ) factor}
# factor = "-" factor | "(" expr ")" | var | num
# var = "w" | "x" | "y" | "z"

# expr = term {( "+" | "-" ) term}
def expr(tok, act):
    x = term(tok, act)
    nxt = tok.peek()
    while nxt in ("+", "-"):
        tok.consume(nxt)
        y = term(tok, act)
        if nxt == "+": x = act.add(x, y)
        else: x = act.sub(x, y)
        nxt = tok.peek()
    return x

# term = factor {( "*" | "/" ) factor}
def term(tok, act):
    x = factor(tok, act)
    nxt = tok.peek()
    while nxt in ("*", "/"):
        tok.consume(nxt)
        y = factor(tok, act)
        if nxt == "*": x = act.mul(x, y)
        else: x = act.div(x, y)
        nxt = tok.peek()
    return x

# factor = "-" factor | "(" expr ")" | var | num
def factor(tok, act):
    nxt = tok.peek()
    if nxt == "-":
        tok.consume("-")
        x = factor(tok, act)
        return act.opp(x)
    elif nxt == "(":
        tok.consume("(")
        x = expr(tok, act)
        tok.consume(")")
        return x
    elif nxt.isalpha():
        tok.consume(nxt)
        x = act.var(nxt)
        return x
    else:
        tok.consume(nxt)
        x = act.num(nxt)
        return x


class Action:
    def __init__(self, ctx):
        self._ctx = ctx
    def add(self, x, y): return x + y
    def sub(self, x, y): return x - y
    def mul(self, x, y): return x * y
    def div(self, x, y): return x / y
    def opp(self, x): return -x
    def num(self, x): return float(x)
    def var(self, x): return self._ctx.get(x, 0)


class Tokenizer:
    def __init__(self, text, regex):
        self._text = text.rstrip()
        self._point = 0
        self._token_re = re.compile(regex)

    def peek(self):
        return self._token_re.match(self._text, self._point).group(1)

    def consume(self, x):
        m = self._token_re.match(self._text, self._point)
        if m.group(1) != x:
            raise SyntaxError("expected " + x)
        self._point = m.end()

    def end(self):
        if self._point < len(self._text):
            raise SyntaxError("Extra stuff after expression")


# Wrapper function
def parse_expr(text, act):
    regex = r"\s*([A-Za-z0-9\.]+|.?)"
    tok = Tokenizer(text, regex)
    result = expr(tok, act)
    tok.end()
    return result


# Tests
def main():
    ctx = {"w": 0.0, "x": 1.0, "y": 1.5, "z": 0.5}
    act = Action(ctx)

    tests = [("(((1.5)))", 1.5),
             ("w * -z", 0),
             ("x / z * -y", -3),
             ("x / 0.5 * --y", 3),
             ("w", 0),
             ("(x + w) * (x + y)", 2.5)]
    for infix, val in tests:
        assert isclose(parse_expr(infix, act), val)

if __name__ == "__main__":
    main()