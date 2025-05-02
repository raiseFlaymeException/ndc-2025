import sprite
import pyxel


class Projectile(sprite.Sprite):
    def __init__(self, x, y, img, u, v, w, h, damage, vitesse, colorkey=None):
        super().__init__(x, y, img, u, v, w, h, colorkey)
        self.damage = damage
        self.vitesse = vitesse

    def update(self):
        self.y -= self.vitesse

    
class ProjectileHandler:
    def __init__(self):
        self.projectiles = []

    def spawn_projectile(self, x, y, img, u, v, w, h, damage, vitesse, colorkey=None):
        self.projectiles.append(Projectile(x, y, img, u, v, w, h, damage, vitesse, colorkey))

    def update(self):
        idx = 0
        while idx < len(self.projectiles):
            projectile = self.projectiles[idx]
            projectile.update()
            if not -projectile.h <= projectile.y <= pyxel.height:
                self.projectiles.pop(idx)
            else:
                idx += 1


    def draw(self):
        for projectile in self.projectiles:
            projectile.draw()
