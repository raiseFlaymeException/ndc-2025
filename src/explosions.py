import pyxel


class ExplosionHandler:
    def __init__(self):
        self.explosions = []
    def new_explosion(self, coords):
        self.explosions.append(Explosion(coords))
    def update(self):
        i = 0
        while i < len(self.explosions):
            if self.explosions[i].update(i):
                self.explosions.pop(i)
            else:
                i += 1
    def draw(self):
        for explosion in self.explosions:
            explosion.draw()
class Explosion:
    def __init__(self, coords):
        pyxel.play(0, 7)
        self.coords = coords
        self.anim_frame = 0
        self.time_played = 0
    def update(self, animation_index):
        self.coords[1] += 1.5
        self.time_played += 1
        self.anim_frame = int(self.time_played/5)
        if self.anim_frame == 5:
            return True
        else:
            return False
    def draw(self):
        pyxel.blt(self.coords[0], self.coords[1], 0, 0+16*self.anim_frame, 80, 16, 16, 1)
        
