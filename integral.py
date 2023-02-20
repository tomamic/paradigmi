#!/usr/bin/env python3
'''
@author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
'''
import math, typing

def some_func(x: float) -> float:
    return x * x + x

def some_integral(a: float, b: float, n: int) -> float:
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

def integral(f: typing.Callable[[float], float],
             a: float, b: float, n: int) -> float:
    """
    Estimate the area beneath the curve py_f, between the
    abscissas a and b; the region is approximated as n rectangles.
    """
    ## add a new param f: "types.Callable[[float], float]"
    total = 0.0
    dx = (b - a) / n
    for i in range(n):
        total += dx * f(a + dx * i)
    return total

def example():
    area_func = integral(some_func, 1, 10, 1_000_000)
    print(area_func)

    area_sin = integral(math.sin, 0, math.pi, 1_000_000)
    print(area_sin)
    
def cpp_vs_py():
    import subprocess, time

    subprocess.run(["g++", "-O3", "integral.cpp", "-o", "_integral"])

    t0 = time.time()
    result = subprocess.run(["./_integral", "1", "10", "100000000"],
                        capture_output=True, text=True)
    t_cpp = time.time() - t0
    #print(result.stdout)
    i = float(result.stdout.split()[1])
    print(f"C++\t{i:10.4f}\t{t_cpp:10.4f}")

    t0 = time.time()
    i = integral(some_func, 1, 10, 100_000_000)
    t_py = time.time() - t0
    print(f"Python\t{i:10.4f}\t{t_py:10.4f}")
    print(t_py / t_cpp)

if __name__ == "__main__":
    cpp_vs_py()
