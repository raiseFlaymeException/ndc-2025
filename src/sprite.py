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
        return self.colide_with_rect(other.x, other.y, other.w, other.h)

    def colide_with_rect(self, x, y, w, h):
        return self.x - w < x < self.x + self.w and self.y - h < y < self.y + self.h
