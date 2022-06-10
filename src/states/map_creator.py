import pygame as pg
from ..components import terrain

class Map_Creator:
    def __init__(self, parent, resources):
        self.parent = parent
        self.resources = resources

        self.terrainh = terrain.Terrain_Handler(self.parent, resources)
    

    def update(self):
        self.handle_events()
        self.draw()


    def handle_events(self):
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
    

    def draw(self):
        self.parent.fill("black")
        self.terrainh.draw(-100)