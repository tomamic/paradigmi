#!/usr/bin/env python3
"""
@author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
"""

from infix_eval import parse_expr

class Action:
    def add(self, x, y): return f"+ {x} {y}"
    def sub(self, x, y): return f"- {x} {y}"
    def mul(self, x, y): return f"* {x} {y}"
    def div(self, x, y): return f"/ {x} {y}"
    def opp(self, x): return f"~{x}"
    def num(self, x): return x
    def var(self, x): return x


# Tests
def main():
    act = Action()

    tests = [("(((1.5)))", "1.5"),
             ("w * -z", "* w ~z"),
             ("x / z * -y", "* / x z ~y"),
             ("x / 0.5 * --y", "* / x 0.5 ~~y"),
             ("w", "w"),
             ("(x + w) * (x + y)", "* + x w + x y")]

    for infix, prefix in tests:
        assert parse_expr(infix, act) == prefix

if __name__ == "__main__":
    main()