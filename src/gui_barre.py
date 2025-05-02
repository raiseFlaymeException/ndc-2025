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
        for i in range(self.max):
            pyxel.rect(self.x + self.w * self.max - self.w * i, self.y, self.w, self.h, 8 if self.val + i < self.max else 11)

    def update_val(self, val):
        self.val = val