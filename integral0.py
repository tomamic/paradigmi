#!/usr/bin/env python3
'''
@author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
'''
import math

def some_func(x: float) -> float:
    return x * x + x

def integral(a: float, b: float, n: int) -> float:
    """
    Estimate the area beneath the curve py_f, between the
    abscissas a and b; the region is approximated as n rectangles.
    """
    ## add a new param f: "types.Callable[[float], float]"
    total = 0.0
    dx = (b - a) / n
    for i in range(n):
        total += dx * some_func(a + dx * i)
    return total

def main():
    area = integral(1, 10, 1_000_000)
    print(area)

if __name__ == "__main__":
    main()
