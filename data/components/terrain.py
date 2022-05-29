# File for general terrain handling

import pygame as pg

# class for an individual tile
class Tile:
    def __init__(self, resources, type):
        # top/right/bottom/left are boolean values that identify the tiles surrounding this tile
        # e.g., top = True means there is a tile above this one

        self.resources = resources
        self.type = type

        self.image = None

    
    
    # loads image for the tile depending on the tiles surrounding it
    def load_image(self, top, right, bottom, left):
        if self.type == 1:
            if top:
                self.image = self.resources["Tile_04.png"]
            elif bottom:
                if right:
                    if left:
                        self.image = self.resources["Tile_02.png"]
                    else:
                        self.image = self.resources["Tile_01.png"]
                else:
                    if left:
                        self.image = self.resources["Tile_03.png"]
                    else:
                        self.image = self.resources["Tile_05.png"]
            elif right:
                if left:
                    self.image = self.resources["Tile_07.png"]
                else:
                    self.image = self.resources["Tile_06.png"]
            elif left:
                self.image = self.resources["Tile_08.png"]
            else:
                print("An error has occured while loading a tile image.")


    # draws this tile
    def draw(self, parent, pos):
        if self.type != 0:
            parent.blit(self.image, pos)



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

        if tilemap:
            self.load_tilemap(tilemap)
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
                    else:
                        col.append(0)
                sample_tilemap.append(col)
            
            self.load_tilemap(sample_tilemap)



    # tilemap argument is a 2d array of tiles
    # it loads the data from the tilemap into Tile objects and creates a new tilemap
    def load_tilemap(self, tilemap):
        new_tilemap = []
        for i in range(len(tilemap)):
            col = []
            for k in range(len(tilemap[i])):
                # if the tile is empty, append an empty tile
                if tilemap[i][k] == 0:
                    col.append(Tile(self.resources, type=0))
                else:
                    # False = empty, True = filled
                    # e.g., top = False means there is no tile above this tile
                    top = False
                    right = False
                    bottom = False
                    left = False
                    if i != 0:
                        if tilemap[i-1][k] != 0:
                            left = True
                    if i != len(tilemap)-1:
                        if tilemap[i+1][k] != 0:
                            right = True
                    if k != 0:
                        if tilemap[i][k-1] != 0:
                            top = True
                    if k != len(tilemap[i])-1:
                        if tilemap[i][k+1] != 0:
                            bottom = True
                    tile = Tile(self.resources, type=1)
                    tile.load_image(top, right, bottom, left)
                    col.append(tile)
            new_tilemap.append(col)
        self.tilemap = new_tilemap



    def draw(self, offsetx):
        self.draw_background(offsetx)
        self.draw_tiles(offsetx)


    def draw_background(self, offsetx):
        for i in range(self.bg_num):
            posx = i * self.bg_img.get_width() - offsetx
            self.parent.blit(self.bg_img, (posx, 0))

    
    # draw the tilemap onto the screen
    def draw_tiles(self, offsetx):
        # topleft is the topleft corner of where the tiles start rendering relative to the topleft of the screen
        topleft = [-1*offsetx, 0]
        pos = topleft.copy()
        for col in self.tilemap:
            for tile in col:
                if tile.type == 1:
                    tile.draw(self.parent, pos)
                pos[1] += self.tile_size
            pos[1] = topleft[1]
            pos[0] += int(self.tile_size)
    

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
                    nearby_tiles.append(self.tilemap[t[0]+i][t[1]+k])
                except IndexError:
                    pass
        
        return nearby_tiles



