import pyxel

import score
import gui_barre
import explosions
import map
import projectile
import vaisseau
import monstre
import common

class Game:
    def __init__(self):
        pyxel.init(128, 128, title="Nuit du c0de", fps=30)
        pyxel.load("ressource.pyxres")

        self.reset()

        pyxel.run(self.update, self.draw)

    def reset(self):
        self.tick = 0
        self.game_over = False

        pyxel.play(0, 8)
        self.score = score.Score(10, 2)
        self.barre_gui = gui_barre.BarreGui(6, 10, 4, 4, 10)

        self.explosionHandler = explosions.ExplosionHandler()
        self.map = map.Map()
        self.projectile_handler = projectile.ProjectileHandler()
        self.joueur = vaisseau.Vaisseau(56, 96, 6, 10, 3, self.projectile_handler, self.barre_gui, self.explosionHandler, colorkey=1)
        self.monstre_handler = monstre.MonstreHandler(self.projectile_handler, self.joueur, self.explosionHandler, self.score)


    # =====================================================
    # == UPDATE
    # =====================================================
    def update(self):
        if self.game_over:
            if pyxel.btn(pyxel.KEY_R):
                self.reset()
        else:
            self.projectile_handler.update()
            if self.joueur.update(pyxel.btn(pyxel.KEY_RIGHT), pyxel.btn(pyxel.KEY_LEFT), pyxel.btn(pyxel.KEY_SPACE)):
                self.game_over = True
            if self.monstre_handler.update(self.tick):
                self.game_over = True
            self.map.update(self.tick)
            self.explosionHandler.update()
            self.score.update()
            self.tick = (self.tick + 1) % 30

    # =====================================================
    # == DRAW
    # =====================================================
    def draw(self):
        if self.game_over:
            self.map.draw()

            self.projectile_handler.draw()
            self.monstre_handler.draw()

            self.barre_gui.draw()
            common.printGameOver(28, 44)
            pyxel.text(46, 56, f"score: {self.score.score}", 1)
            pyxel.text(25, 64, "touche \"R\" pour reset", 1)
        else:
            self.map.draw()

            self.projectile_handler.draw()
            self.joueur.draw()
            self.monstre_handler.draw()
            self.explosionHandler.draw()

            self.barre_gui.draw()
            self.score.draw()


Game()
