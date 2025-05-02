import sprite
import pyxel

class Monstre(sprite.Sprite):
    def __init__(self, x, y, img, u, v, w, h, pv, damage, vitesse, point, projectile_handler, colorkey=None):
        super().__init__(x, y, img, u, v, w, h, colorkey)
        self.pv = pv
        self.damage = damage
        self.vitesse = vitesse
        self.point = point
        self.projectile_handler = projectile_handler


class Monstre1(Monstre):
    def __init__(self, x, y, projectile_handler):
        super().__init__(x, y, 0, 0, 48, 16, 16, 3, 4, 1.5, 150, projectile_handler, colorkey=1)

    def update(self):
        self.y += self.vitesse

class Monstre2(Monstre):
    def __init__(self, x, y, projectile_handler):
        super().__init__(x, y, 0, 16, 48, 16, 16, 2, 1, 2, 0, projectile_handler, colorkey=1)

    def update(self):
        pass

class Monstre3(Monstre):
    def __init__(self, x, y, projectile_handler):
        super().__init__(x, y, 0, 32, 48, 16, 16, 2, 1, 2, 200, projectile_handler, colorkey=1)
        self.cooldown = 0

    def update(self):
        self.y += self.vitesse

        if self.cooldown == 0:
            self.projectile_handler.spawn_projectile(self.x + self.w/2 - 4, self.y - self.h / 2, 0, 0, 72, 8, 8, 1, -1, colorkey=1)
            self.cooldown = 20
        else:
            self.cooldown -= 1


class Monstre4(Monstre):
    def __init__(self, x, y, projectile_handler):
        super().__init__(x, y, 0, 48, 48, 16, 16, 1, 2, 5, 50, projectile_handler, colorkey=1)
        self.dir = 1 if pyxel.rndi(0, 1) == 0 else -1

    def update(self):
        Y_FACTEUR = 0.25
        CHANGE_DIR_CHANCE = 50
        self.x += self.dir*self.vitesse
        self.y += self.vitesse*Y_FACTEUR
        if self.x < 0:
            self.x = 0
            self.dir = -self.dir
        elif self.x > pyxel.width - self.w:
            self.x = pyxel.width - self.w
            self.dir = -self.dir
        elif pyxel.rndi(0, CHANGE_DIR_CHANCE) == 0:
            self.dir = -self.dir
        

class Monstre5(Monstre):
    def __init__(self, x, y, projectile_handler):
        super().__init__(x, y, 0, 64, 48, 16, 16, 2, 1, 2, 0, projectile_handler, colorkey=1)

    def update(self):
        pass


class MonstreHandler:
    def __init__(self, projectile_handler, joueur, explosionHandler, score):
        self.monstres = []
        self.projectile_handler = projectile_handler
        self.joueur = joueur
        self.explosionHandler = explosionHandler
        self.score = score

    def spawn_monstre(self, x, y, idx):
        MONSTRES_CLASS = Monstre1, Monstre2, Monstre3, Monstre4, Monstre5
        self.monstres.append(MONSTRES_CLASS[idx](x, y, self.projectile_handler))

    def update(self, tick):
        idx_monstre = 0
        while idx_monstre < len(self.monstres):
            monstre = self.monstres[idx_monstre]
            monstre.update()
            idx_projectile = 0
            while idx_projectile < len(self.projectile_handler.projectiles):
                projectile = self.projectile_handler.projectiles[idx_projectile]
                if projectile.colide_with(monstre):
                    monstre.pv -= projectile.damage
                    self.projectile_handler.projectiles.pop(idx_projectile)
                    break
                idx_projectile += 1
            if monstre.pv <= 0:
                self.score.score += monstre.point
                self.explosionHandler.new_explosion([monstre.x, monstre.y])
                self.monstres.pop(idx_monstre)
            elif monstre.colide_with(self.joueur):
                self.explosionHandler.new_explosion([monstre.x, monstre.y])
                self.joueur.pv -= monstre.damage
                if self.joueur.pv <= 0:
                    return True
                self.monstres.pop(idx_monstre)
            elif not -monstre.h <= monstre.y <= pyxel.height:
                self.monstres.pop(idx_monstre)
            else:
                idx_monstre += 1
        if tick % 60 == 0:
            self.spawn_monstre(pyxel.rndi(0, pyxel.width-16), -16, (0, 2, 3)[pyxel.rndi(0, 2)])

    def draw(self):
        for monstre in self.monstres:
            monstre.draw()
