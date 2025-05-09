import sprite
import pyxel

STATE_MONSTRE_RIEN = 0
STATE_MONSTRE_JE_SUIS_MORT = 1
STATE_MONSTRE_JOUEUR_MORT = 2

class Monstre(sprite.Sprite):
    def __init__(self, x, y, img, u, v, w, h, pv, damage, vitesse, point, monstre_handler, colorkey=None):
        super().__init__(x, y, img, u, v, w, h, colorkey)
        self.pv = pv
        self.damage = damage
        self.vitesse = vitesse
        self.point = point
        # mstrh = monstre_handler
        self.mstrh = monstre_handler

    def update(self):
        idx = 0
        while idx < len(self.mstrh.projectile_handler.projectiles):
            projectile = self.mstrh.projectile_handler.projectiles[idx]
            if projectile.colide_with(self):
                self.pv -= projectile.damage
                self.mstrh.projectile_handler.projectiles.pop(idx)
                break
            idx += 1
        if self.pv <= 0:
            self.mstrh.score.score += self.point
            self.mstrh.explosionHandler.new_explosion([self.x, self.y])
            return STATE_MONSTRE_JE_SUIS_MORT
        elif self.colide_with(self.mstrh.joueur):
            self.mstrh.explosionHandler.new_explosion([self.x, self.y])
            self.mstrh.joueur.pv -= self.damage
            if self.mstrh.joueur.pv <= 0:
                return STATE_MONSTRE_JOUEUR_MORT
            return STATE_MONSTRE_JE_SUIS_MORT
        elif not -self.h <= self.y <= pyxel.height:
            return STATE_MONSTRE_JE_SUIS_MORT
        return STATE_MONSTRE_RIEN


class Monstre1(Monstre):
    def __init__(self, x, y, monstre_handler):
        super().__init__(x, y, 0, 0, 48, 16, 16, 3, 4, 1.5, 150, monstre_handler, colorkey=1)

    def update(self):
        state = super().update()
        self.y += self.vitesse
        return state

class Monstre2(Monstre):
    def __init__(self, x, y, monstre_handler):
        super().__init__(x, y, 0, 16, 48, 16, 16, 2, 1, 2, 0, monstre_handler, colorkey=1)

class Monstre3(Monstre):
    def __init__(self, x, y, monstre_handler):
        super().__init__(x, y, 0, 32, 48, 16, 16, 2, 1, 2, 200, monstre_handler, colorkey=1)
        self.cooldown = 0

    def update(self):
        state = super().update()
        self.y += self.vitesse

        if self.cooldown == 0:
            self.mstrh.projectile_handler.spawn_projectile(self.x + self.w/2 - 4, self.y - 10, 0, 0, 72, 8, 8, 1, -1, colorkey=1)
            self.cooldown = 20
        else:
            self.cooldown -= 1
        return state


class Monstre4(Monstre):
    def __init__(self, x, y, monstre_handler):
        super().__init__(x, y, 0, 48, 48, 16, 16, 1, 2, 5, 50, monstre_handler, colorkey=1)
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
    MAX_LASER_COOLDOWN = 70
    MAX_LASER_TIME = 20
    
    LASER_W = 2

    def __init__(self, x, y, monstre_handler):
        super().__init__(x, y, 0, 64, 48, 16, 16, 2, 1, 1, 250, monstre_handler, colorkey=1)
        self.laser_cooldown = self.MAX_LASER_COOLDOWN
        self.laser_time = self.MAX_LASER_TIME
        self.dir = 1 if pyxel.rndi(0, 1) == 0 else -1
        self.target_min_y = pyxel.height

    def laser_colide_with(self, other):
        return other.colide_with_rect(self.x + self.w / 2 - self.LASER_W / 2, self.y + self.h, self.LASER_W, self.target_min_y - self.y)

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
            self.target_min_y = pyxel.height
            monstre_min_y = None
            for monstre in self.mstrh.monstres:
                if monstre is self:
                    continue
                if self.laser_colide_with(monstre):
                    if monstre.y < self.target_min_y:
                        self.target_min_y = monstre.y
                        monstre_min_y = monstre

            if self.laser_colide_with(self.mstrh.joueur):
                if self.mstrh.joueur.y < self.target_min_y:
                    self.target_min_y = self.mstrh.joueur.y
                    if int(self.mstrh.joueur.pv - LASER_DAMAGE) < int(self.mstrh.joueur.pv):
                        self.mstrh.explosionHandler.new_explosion([self.x + self.w / 2 - self.LASER_W / 2, self.target_min_y])
                    self.mstrh.joueur.pv -= LASER_DAMAGE
                    if self.mstrh.joueur.pv <= 0:
                        return STATE_MONSTRE_JOUEUR_MORT
            else:
                if monstre_min_y is None:
                    return state
                monstre_min_y.pv -= LASER_DAMAGE
                if monstre_min_y.pv <= 0:
                    self.mstrh.explosionHandler.new_explosion([self.x + self.w / 2 - self.LASER_W / 2, self.target_min_y])

        return state


    def draw(self):
        super().draw()
        if self.laser_cooldown == 0:
            pyxel.rect(self.x + self.w / 2 - self.LASER_W / 2, self.y + self.h, self.LASER_W, self.target_min_y - self.y, pyxel.COLOR_RED)


class MonstreHandler:
    def __init__(self, projectile_handler, joueur, explosionHandler, score):
        self.monstres = []
        self.projectile_handler = projectile_handler
        self.joueur = joueur
        self.explosionHandler = explosionHandler
        self.score = score

    def spawn_monstre(self, x, y, idx):
        MONSTRES_CLASS = Monstre1, Monstre2, Monstre3, Monstre4, Monstre5
        self.monstres.append(MONSTRES_CLASS[idx](x, y, self))

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
