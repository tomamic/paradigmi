#!/usr/bin/env python3
'''
@author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
'''

def create_pow(exponent: float):
    def result(base: float):
        return base ** exponent
    return result

def main():
    root = create_pow(0.5)
    cube = create_pow(3)

    print(root(3))
    print(root(4))

    print(cube(3))
    print(cube(4))

main()
