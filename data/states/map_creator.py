import pygame as pg

class Map_Creator:
    def __init__(self, parent, resources):
        self.parent = parent
        self.resources = resources
    

    def update(self):
        self.handle_events()
        self.draw()


    def handle_events(self):
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
    

    def draw(self):
        self.parent.fill("black")