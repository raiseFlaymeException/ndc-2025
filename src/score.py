import pyxel

class Score:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0

    def draw(self):
        pyxel.text(self.x, self.y, f"score: {self.score}", 1)

    def update(self):
        self.score += 1