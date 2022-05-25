import pygame as pg

class Obstacle(pg.sprite.Sprite):
    def __init__(self, pos, image):
        self.pos = pos
        self.image = image

        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.pos
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        pass


    def update_rect(self, offsetx):
        self.rect.bottom = self.pos[1]
        self.rect.left = self.pos[0] - offsetx