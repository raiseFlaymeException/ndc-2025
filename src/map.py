import pyxel

class Map:
    def __init__(self):
        self.map = [(0, 128),(0, 0), (128, 0), (128, 128), (0, 256), (0, 48*8)]
        self.map1_rendered = 0
        self.map2_rendered = 1
        self.map_position = 0
        self.map_loop_1_index = 2
    def update(self, tick):
        self.map_position += 1
        if self.map_position == 128:
            self.map1_rendered = self.map2_rendered
            self.map2_rendered += 1
            if self.map2_rendered == len(self.map):
                self.map2_rendered = self.map_loop_1_index = 2
            elif self.map1_rendered == len(self.map):
                self.map1_rendered = self.map_loop_1_index = 2
            
            self.map_position = 0
            
    def draw(self):
        pyxel.bltm(0, self.map_position, 0, self.map[self.map1_rendered][0], self.map[self.map1_rendered][1], 128, 128, 1)
        pyxel.bltm(0, self.map_position-128, 0, self.map[self.map2_rendered][0], self.map[self.map2_rendered][1], 128, 128, 1)
