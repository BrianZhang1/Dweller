# This class handles Terrain loading and generation, as well as background rendering.

import pygame as pg

class Terrain_Handler:
    def __init__(self, parent, resources, tilemap=None):
        self.parent = parent
        self.resources = resources

        self.bg_img = self.resources["bg.png"]

        # Constants
        self.bg_num = 2  # how many backgrounds will be in the map
        self.tile_size = 32 # length of a single tile

        self.bg_w = self.bg_num * self.bg_img.get_width() # total width of background


        if tilemap == None:
            # 0 = empty space
            # 1 = block
            screen = pg.display.get_surface()
            rows = int(screen.get_height()/self.tile_size)
            cols = int(self.bg_w/self.tile_size)
            sample_tilemap = []

            for i in range(rows):
                row = []
                for k in range(cols):
                    if i == 0 or i == 2:
                        row.append(1)
                    else:
                        row.append(0)
                sample_tilemap.append(row)
            
            self.load_tilemap(sample_tilemap)



    # loads the tile map
    # the tile map is a 2d list of all the tiles that are in the level
    def load_tilemap(self, tilemap):
        self.tilemap = tilemap


    def draw(self, offsetx):
        self.draw_background(offsetx)
        self.draw_tiles(offsetx)


    def draw_background(self, offsetx):
        for i in range(self.bg_num):
            posx = i * self.bg_img.get_width() - offsetx
            self.parent.blit(self.bg_img, (posx, 0))

    
    def draw_tiles(self, offsetx):
        tile_img = self.resources["tile.png"]
        init_pos = [-1*offsetx, self.parent.get_height()-self.tile_size]
        pos = init_pos.copy()
        for row in self.tilemap:
            for col in row:
                if col == 1:
                    self.parent.blit(tile_img, pos)
                pos[0] += self.tile_size
            pos[0] = init_pos[0]
            pos[1] -= int(self.tile_size)

