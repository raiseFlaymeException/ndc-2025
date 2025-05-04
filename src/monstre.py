import sprite
import pyxel

STATE_MONSTRE_RIEN = 0
STATE_MONSTRE_JE_SUIS_MORT = 1
STATE_MONSTRE_JOUEUR_MORT = 2

class Monstre(sprite.Sprite):
    def __init__(self, x, y, img, u, v, w, h, pv, damage, vitesse, point, projectile_handler, joueur, explosionHandler, score, colorkey=None):
        super().__init__(x, y, img, u, v, w, h, colorkey)
        self.pv = pv
        self.damage = damage
        self.vitesse = vitesse
        self.point = point
        self.projectile_handler = projectile_handler
        self.joueur = joueur
        self.explosionHandler = explosionHandler
        self.score = score

    def update(self):
        idx_projectile = 0
        while idx_projectile < len(self.projectile_handler.projectiles):
            projectile = self.projectile_handler.projectiles[idx_projectile]
            if projectile.colide_with(self):
                self.pv -= projectile.damage
                self.projectile_handler.projectiles.pop(idx_projectile)
                break
            idx_projectile += 1
        if self.pv <= 0:
            self.score.score += self.point
            self.explosionHandler.new_explosion([self.x, self.y])
            return STATE_MONSTRE_JE_SUIS_MORT
        elif self.colide_with(self.joueur):
            self.explosionHandler.new_explosion([self.x, self.y])
            self.joueur.pv -= self.damage
            if self.joueur.pv <= 0:
                return STATE_MONSTRE_JOUEUR_MORT
            return STATE_MONSTRE_JE_SUIS_MORT
        elif not -self.h <= self.y <= pyxel.height:
            return STATE_MONSTRE_JE_SUIS_MORT
        return STATE_MONSTRE_RIEN


class Monstre1(Monstre):
    def __init__(self, x, y, projectile_handler, joueur, explosionHandler, score):
        super().__init__(x, y, 0, 0, 48, 16, 16, 3, 4, 1.5, 150, projectile_handler, joueur, explosionHandler, score, colorkey=1)

    def update(self):
        state = super().update()
        self.y += self.vitesse
        return state

class Monstre2(Monstre):
    def __init__(self, x, y, projectile_handler, joueur, explosionHandler, score):
        super().__init__(x, y, 0, 16, 48, 16, 16, 2, 1, 2, 0, projectile_handler, joueur, explosionHandler, score, colorkey=1)

class Monstre3(Monstre):
    def __init__(self, x, y, projectile_handler, joueur, explosionHandler, score):
        super().__init__(x, y, 0, 32, 48, 16, 16, 2, 1, 2, 200, projectile_handler, joueur, explosionHandler, score, colorkey=1)
        self.cooldown = 0

    def update(self):
        state = super().update()
        self.y += self.vitesse

        if self.cooldown == 0:
            self.projectile_handler.spawn_projectile(self.x + self.w/2 - 4, self.y - 10, 0, 0, 72, 8, 8, 1, -1, colorkey=1)
            self.cooldown = 20
        else:
            self.cooldown -= 1
        return state


class Monstre4(Monstre):
    def __init__(self, x, y, projectile_handler, joueur, explosionHandler, score):
        super().__init__(x, y, 0, 48, 48, 16, 16, 1, 2, 5, 50, projectile_handler, joueur, explosionHandler, score, colorkey=1)
        self.dir = 1 if pyxel.rndi(0, 1) == 0 else -1

    def update(self):
        state = super().update()
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
        return state
        

class Monstre5(Monstre):
    MAX_LASER_COOLDOWN = 30
    MAX_LASER_TIME = 10
    
    LASER_W = 2

    def __init__(self, x, y, projectile_handler, joueur, explosionHandler, score):
        super().__init__(x, y, 0, 64, 48, 16, 16, 2, 1, 1, 250, projectile_handler, joueur, explosionHandler, score, colorkey=1)
        self.laser_cooldown = self.MAX_LASER_COOLDOWN
        self.laser_time = self.MAX_LASER_TIME
        self.dir = 1 if pyxel.rndi(0, 1) == 0 else -1

    def update(self):
        Y_FACTEUR = 1/5
        LASER_DAMAGE = 5e-2

        state = super().update()
        if state == STATE_MONSTRE_JOUEUR_MORT:
            return STATE_MONSTRE_JOUEUR_MORT

        self.y += self.vitesse * Y_FACTEUR
        self.x += self.dir*self.vitesse
        if self.x < 0:
            self.x = 0
            self.dir = -self.dir
        elif self.x > pyxel.width - self.w:
            self.x = pyxel.width - self.w
            self.dir = -self.dir

        if self.laser_cooldown == 0:
            if self.laser_time == 0:
                self.laser_time = self.MAX_LASER_TIME
                self.laser_cooldown = self.MAX_LASER_COOLDOWN
            else:
                self.laser_time -= 1
        else:
            self.laser_cooldown -= 1

        if self.laser_cooldown == 0:
            if self.joueur.colide_with_rect(self.x + self.w / 2 - self.LASER_W / 2, self.y + self.h, self.LASER_W, pyxel.height - self.y):
                self.explosionHandler.new_explosion([self.x + self.w / 2 - self.LASER_W / 2, self.joueur.y])
                self.joueur.pv -= LASER_DAMAGE
                if self.joueur.pv <= 0:
                    return STATE_MONSTRE_JOUEUR_MORT
        return state


    def draw(self):
        super().draw()
        if self.laser_cooldown == 0:
            pyxel.rect(self.x + self.w / 2 - self.LASER_W / 2, self.y + self.h, self.LASER_W, pyxel.height - self.y, pyxel.COLOR_RED)


class MonstreHandler:
    def __init__(self, projectile_handler, joueur, explosionHandler, score):
        self.monstres = []
        self.projectile_handler = projectile_handler
        self.joueur = joueur
        self.explosionHandler = explosionHandler
        self.score = score

    def spawn_monstre(self, x, y, idx):
        MONSTRES_CLASS = Monstre1, Monstre2, Monstre3, Monstre4, Monstre5
        self.monstres.append(MONSTRES_CLASS[idx](x, y, self.projectile_handler, self.joueur, self.explosionHandler, self.score))

    def update(self, tick):
        idx_monstre = 0
        while idx_monstre < len(self.monstres):
            monstre = self.monstres[idx_monstre]

            state = monstre.update()
            if state == STATE_MONSTRE_RIEN:
                idx_monstre += 1
            elif state == STATE_MONSTRE_JE_SUIS_MORT:
                self.monstres.pop(idx_monstre)
            elif state == STATE_MONSTRE_JOUEUR_MORT:
                return True
            else:
                raise ValueError(f"state a une valeur impossible: {state=}")
        if tick % 60 == 0:
            self.spawn_monstre(pyxel.rndi(0, pyxel.width-16), -16, (0, 2, 3, 4)[pyxel.rndi(0, 3)])

    def draw(self):
        for monstre in self.monstres:
            monstre.draw()
