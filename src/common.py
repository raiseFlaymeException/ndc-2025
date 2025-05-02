import pyxel

def clamp(x, lower, upper):
    return min(max(x, lower), upper)


def printGameOver(x, y):
    pyxel.blt(x, y, 0, 0, 144, 8, 8, 1) # G
    pyxel.blt(x+9, y, 0, 8, 144, 8, 8, 1) # A
    pyxel.blt(x+18, y, 0, 0, 144+8, 8, 8, 1) # M
    pyxel.blt(x+27, y, 0, 8, 144+8, 8, 8, 1) # E
    
    pyxel.blt(x+44, y, 0, 16, 144, 8, 8, 1) # 0
    pyxel.blt(x+53, y, 0, 24, 144, 8, 8, 1) # V
    pyxel.blt(x+62, y, 0, 8, 144+8, 8, 8, 1) # E
    pyxel.blt(x+71, y, 0, 16, 144+8, 8, 8, 1) # R
