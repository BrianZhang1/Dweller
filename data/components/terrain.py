# File for general terrain handling

import pygame as pg
from ..components import map


# This class handles Terrain loading and generation, as well as background rendering.
class Terrain_Handler:
    def __init__(self, parent, resources, tilemap=None):
        self.parent = parent
        self.resources = resources

        self.bg_img = self.resources["bg.png"]

        # Constants
        self.bg_num = 2  # how many backgrounds will be in the map
        self.tile_size = 32 # length of a single tile

        self.bg_w = self.bg_num * self.bg_img.get_width() # total width of background

        self.map = map.Map(self.resources, self.tile_size)
        if tilemap:
            self.map.load_tilemap(tilemap)
        else:
            # 0 = empty space
            # 1 = block
            screen = pg.display.get_surface()
            cols = int(self.bg_w/self.tile_size) + 1
            rows = int(screen.get_height()/self.tile_size) + 1
            sample_tilemap = []

            for i in range(cols):
                col = []
                for k in range(rows):
                    if k == rows-1:
                        col.append(1)
                    elif i == 1 and k == rows-4:
                        col.append(1)
                    elif (k == rows-4 or k == rows-3 or k == rows-2) and i in [6, 7, 8]:
                        col.append(1)
                    elif k == rows-5 and i in [12, 13, 14, 15]:
                        col.append(1)
                    else:
                        col.append(0)
                sample_tilemap.append(col)
            
            self.map.load_tilemap(sample_tilemap)




    def draw(self, offsetx):
        self.draw_background(offsetx)
        self.draw_tiles(offsetx)


    def draw_background(self, offsetx):
        for i in range(self.bg_num):
            posx = i * self.bg_img.get_width() - offsetx
            self.parent.blit(self.bg_img, (posx, 0))

    
    # draw the tilemap onto the screen
    def draw_tiles(self, offsetx):
        for col in self.map.tilemap:
            for tile in col:
                tile.draw(self.parent, offsetx)
    

    # returns a list of all nearby tiles
    # pos is the position to find tiles nearby
    # radius is how many tiles the search should be
    def get_nearby_tiles(self, pos, radius=2):
        nearby_tiles = []
        tile_index = (int(pos[0]/self.tile_size), int(pos[1]/self.tile_size)) # index of closest tile to pos
        # next, search around the tile
        t = (tile_index[0]-radius+1, tile_index[1]-radius+1) # top left tile in search radius
        for i in range(2*radius-1):
            for k in range(2*radius-1):
                try:
                  nearby_tiles.append(self.map.tilemap[t[0]+i][t[1]+k])
                except IndexError:
                  pass
        
        return nearby_tiles



