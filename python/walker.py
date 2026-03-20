from random import choice

W, H = 320, 240
dirs = [(2,0), (0,2), (-2,0), (0,-2)]

class Walker:
    def __init__(self):
        self._x, self._y = W // 2, H // 2
        self._dx, self._dy = dirs[0]

    def move(self, command):
        if "t" in command:
            self._dx, self._dy = choice(dirs)
        self._x += self._dx
        self._y += self._dy

    def pos(self):
        return self._x, self._y


w = Walker()
print(w.pos())

commands = ["", "", "", "", "t", "", "", "", "t", "", "", ""]
for c in commands:
    w.move(c)
    print(w.pos())
