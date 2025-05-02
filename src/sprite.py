import pyxel

class Sprite:
    def __init__(self, x, y, img, u, v, w, h, colorkey=None) -> None:
        self.x = x
        self.y = y
        self.img = img
        self.u = u
        self.v = v
        self.w = w 
        self.h = h
        self.colorkey = colorkey

    def draw(self):
        pyxel.blt(self.x, self.y, self.img, self.u, self.v, self.w, self.h, self.colorkey)
    
    def goto(self, x, y):
        self.x = x
        self.y = y

    def colide_with(self, other):
        return self.x - other.w < other.x < self.x + self.w and self.y - other.h < other.y < self.y + self.h