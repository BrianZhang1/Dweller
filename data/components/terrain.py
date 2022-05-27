# File for general terrain handling

import pygame as pg

# class for an individual tile
class Tile:
    def __init__(self, resources, sur):
        # the sur argument is a tuple of 4 boolean values
        # it describes whether there are tiles surrounding this tile
        # it starts at the tile North of this tile and goes clockwise
        # e.g. (1, 0, 0, 1) means there is a tile above and to the left

        self.image = None
        self.load_image(resources, sur)

    
    
    # loads image for the tile depending on the tiles surrounding it
    def load_image(self, resources, sur):
        if sur[0] == 1:
            self.image = resources["Tile_04.png"]
        elif sur == (0, 0, 0, 0):
            self.image = resources["Tile_18.png"]
        elif sur == (0, 1, 1, 0):
            self.image = resources["Tile_01.png"]
        elif sur == (0, 0, 1, 1):
            self.image = resources["Tile_03.png"]
        elif sur == (0, 1, 1, 1):
            self.image = resources["Tile_01.png"]
        else:
            print("invalid sur argument for Tile")
    

    # draws this tile
    def draw(self, parent, pos):
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



    # tilemap argument is a 2d array of tiles
    # it loads the data from the tilemap into Tile objects and creates a new tilemap
    def load_tilemap(self, tilemap):
        new_tilemap = []
        for i in range(len(tilemap)):
            row = []
            for k in range(len(tilemap[i])):
                # if the tile is empty, append an empty tile
                if tilemap[i][k] == 0:
                    row.append(0)
                else:
                    top = False
                    right = False
                    bottom = False
                    left = False
                    if i != 0:
                        if tilemap[i-1][k] != 0:
                            top = True
                    if i != len(tilemap)-1:
                        if tilemap[i+1][k] != 0:
                            bottom = True
                    if k != 0:
                        if tilemap[i][k-1] != 0:
                            left = True
                    if k != len(tilemap[i])-1:
                        if tilemap[i][k+1] != 0:
                            right = True
                    sur = (top, right, bottom, left)
                    tile = Tile(self.resources, sur)
                    row.append(tile)
            new_tilemap.append(row)
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
        init_pos = [-1*offsetx, self.parent.get_height()-self.tile_size]
        pos = init_pos.copy()
        for row in self.tilemap:
            for tile in row:
                if tile:
                    tile.draw(self.parent, pos)
                pos[0] += self.tile_size
            pos[0] = init_pos[0]
            pos[1] -= int(self.tile_size)
    

