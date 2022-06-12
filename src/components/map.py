import pygame as pg

class Map:
    def __init__(self, parent, resources, tile_size, tilemap=None):
        self.parent = parent
        self.resources = resources
        self.tile_size = tile_size
        self.tilemap = None
        if tilemap:
            self.load_tilemap(tilemap, resources)


    # tilemap argument is a 2d array of tiles
    # it loads the data from the tilemap into Tile objects and creates a new tilemap
    def load_tilemap(self, tilemap):
        # topleft is the topleft corner of where the tiles start rendering relative to the topleft of the screen
        topleft = [0, 0]
        pos = topleft.copy()

        new_tilemap = []
        for i in range(len(tilemap)):
            col = []
            for k in range(len(tilemap[i])):
                # if the tile is empty, append an empty tile
                if tilemap[i][k] == 0:
                    tile_type = 0
                else:
                    tile_type = 1
                tile = Tile(self.resources, type=tile_type, list_pos=(i, k), pos=(pos[0], pos[1]))
                tile.load_image(tilemap, init=True)
                col.append(tile)
                pos[1] += self.tile_size
            new_tilemap.append(col)
            pos[1] = topleft[1]
            pos[0] += int(self.tile_size)
        self.tilemap = new_tilemap


    # draw the tilemap onto the screen
    def draw(self, offsetx):
        for col in self.tilemap:
            for tile in col:
                tile.draw(self.parent, offsetx)



# class for an individual tile
class Tile:
    def __init__(self, resources, type, list_pos, pos):
        # top/right/bottom/left are boolean values that identify the tiles surrounding this tile
        # e.g., top = True means there is a tile above this one

        self.resources = resources
        self.type = type
        self.list_pos = list_pos # position of tile in tilemap
        self.pos = pos # absolute pos (topleft)

        self.image = None


    # loads image for the tile depending on the tiles surrounding it
    # init argument is for whether this is the initial loading of the image
    def load_image(self, tilemap, init=False):
        if self.type == 0:
            self.image = None
        
        else:
            surrounding_tiles = self.check_surrounding_tiles(tilemap, not init)
            top = surrounding_tiles[0]
            right = surrounding_tiles[1]
            bottom = surrounding_tiles[2]
            left = surrounding_tiles[3]
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
                    self.image = self.resources["Tile_18.png"]


    # checks whether tiles surrounding this tile are non-empty using given tilemap
    def check_surrounding_tiles(self, tilemap, tiles_are_objects):
        # False = empty, True = filled
        # e.g., top = False means there is no tile above this tile
        top = False
        right = False
        bottom = False
        left = False
        i = self.list_pos[0]
        k = self.list_pos[1]
        if tiles_are_objects:
            if i != 0:
                if tilemap[i-1][k].type != 0:
                    left = True
            if i != len(tilemap)-1:
                if tilemap[i+1][k].type != 0:
                    right = True
            if k != 0:
                if tilemap[i][k-1].type != 0:
                    top = True
            if k != len(tilemap[i])-1:
                if tilemap[i][k+1].type != 0:
                    bottom = True
        else:
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

        return (top, right, bottom, left)
    

    # draws this tile
    def draw(self, parent, offsetx):
        if self.type != 0:
            pos = (self.pos[0]-offsetx, self.pos[1])
            if self.type == 1:
                parent.blit(self.image, pos)
            elif self.type == 2:
                rect = pg.Rect(pos, (32, 32))
                pg.draw.rect(parent, "red", rect)
            else:
                print("Invalid tile type:", self.type)


