import pyxel
import sprite
import common

class Vaisseau(sprite.Sprite):
    def __init__(self, x, y, cooldown, pv, max_vitesse, projectile_handler, barre_gui, explosionHandler, colorkey=None):
        super().__init__(x, y, 0, 16, 16, 16, 16, colorkey)

        self.cur_cooldown = 0
        self.cooldown = cooldown
        self.__pv = pv
        self.max_vitesse = max_vitesse
        self.vx = 0 
        self.projectile_handler = projectile_handler
        self.barre_gui = barre_gui
        self.explosionHandler = explosionHandler

    def update(self, droite, gauche, tirer):
        FRICTION = 0.1
        ACCELERATION = 0.5
        SPEED_ANIM_FACTEUR = 2/3

        if droite:
            self.vx += ACCELERATION
            if self.vx > self.max_vitesse:
                self.vx = self.max_vitesse
        if gauche:
            self.vx -= ACCELERATION
            if self.vx < -self.max_vitesse:
                self.vx = -self.max_vitesse
        if not droite and not gauche:
            self.vx -= pyxel.sgn(self.vx) * FRICTION
            if abs(self.vx) <= FRICTION:
                self.vx = 0

        self.goto(common.clamp(self.x + self.vx, 0, pyxel.width-self.w), self.y)

        if self.cur_cooldown > 0:
            self.cur_cooldown -= 1
        else:
            if tirer:
                pyxel.play(0, 6)
                self.projectile_handler.spawn_projectile(self.x+self.w/2-4, self.y - 9, 0, 32, 64, 8, 8, 1, 4, colorkey=1)
                self.cur_cooldown = self.cooldown

        if abs(self.vx) <= self.max_vitesse*SPEED_ANIM_FACTEUR:
            self.u = 16
        elif self.vx > self.max_vitesse*SPEED_ANIM_FACTEUR:
            self.u = 64
        else:
            self.u = 48

        idx = 0
        while idx < len(self.projectile_handler.projectiles):
            projectile = self.projectile_handler.projectiles[idx]
            if projectile.colide_with(self):
                self.explosionHandler.new_explosion([self.x, self.y])
                self.pv -= projectile.damage
                if self.pv <= 0:
                    return True
                self.projectile_handler.projectiles.pop(idx)
            else:
                idx += 1
        return False

    @property
    def pv(self, pv):
        return self.__pv

    @pv.setter
    def pv(self, pv):
        self.__pv = pv
        self.barre_gui.update_val(self.__pv)

    @pv.getter
    def pv(self):
        return self.__pv
