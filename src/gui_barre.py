import pyxel


class BarreGui:
    def __init__(self, x, y, w, h, max):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.max = max
        self.val = max

    def draw(self):
        for i in range(self.max*self.w):
            pyxel.rect(self.x + self.max*self.w - i, self.y, 1, self.h, 8 if self.val + i/self.w < self.max else 11)

    def update_val(self, val):
        self.val = val
