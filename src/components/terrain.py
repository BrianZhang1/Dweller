# File for general terrain handling

import pygame as pg
from ..components import map


# This class handles Terrain loading and generation, as well as background rendering.
class Terrain_Handler:
    def __init__(self, parent, resources, tile_size, tilemap, width):
        self.parent = parent
        self.resources = resources
        self.tile_size = tile_size

        self.bg_img = self.resources["bg.png"]

        # Constants
        self.bg_num = width  # how many backgrounds will be in the map

        self.bg_w = self.bg_num * self.bg_img.get_width() # total width of background

        self.map = map.Map(self.parent, self.resources, self.tile_size, tilemap, width)




    def draw(self, offsetx):
        self.draw_background(offsetx)
        self.map.draw(offsetx)


    def draw_background(self, offsetx):
        for i in range(self.bg_num):
            posx = i * self.bg_img.get_width() - offsetx
            self.parent.blit(self.bg_img, (posx, 0))

    
    # gets the index of the tile that pos is on
    def get_tile(self, pos):
        try:
            tile = self.map.tilemap[int(pos[0]/self.tile_size)][int(pos[1]/self.tile_size)] # index of closest tile to pos
        except IndexError:
            print("Tile out of tilemap range.")
            tile = None
        return tile
    

    # returns a list of all nearby tiles
    # pos is the position to find tiles nearby
    # radius is how many tiles the search should be
    def get_nearby_tiles(self, pos, radius=2):
        nearby_tiles = []
        tile_index = self.get_tile(pos).list_pos
        # next, search around the tile
        t = (tile_index[0]-radius+1, tile_index[1]-radius+1) # top left tile in search radius
        for i in range(2*radius-1):
            for k in range(2*radius-1):
                try:
                  nearby_tiles.append(self.map.tilemap[t[0]+i][t[1]+k])
                except IndexError:
                  pass
        
        return nearby_tiles



