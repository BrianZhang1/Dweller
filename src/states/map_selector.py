import pygame as pg
from ..components import ui

class MapSelector:
    def __init__(self, parent, resources, maps, load_main_menu, load_game):
        self.parent = parent
        self.resources = resources
        self.load_main_menu = load_main_menu
        self.load_game = load_game

        screen_size = (self.parent.get_width(), self.parent.get_height())
        self.offsety = 0  # for up and down scrolling through map menu
        self.buttons = []

        # BACK BUTTON
        self.back_button = ui.Button(self.parent, resources["back_button.png"], (10, 10), self.load_main_menu)
        self.buttons.append(self.back_button)

        map_row_size = (screen_size[0]-20, 50)
        map_row_marginy = 10
        font = pg.font.Font(None, int(map_row_size[1]/2))
        self.map_rows = []
        i = 0
        for map in maps:
            map_row = MapRow(self.parent, resources, load_game, map, map_row_size, font)
            map_row.rect.centerx = screen_size[0]/2
            map_row.rect.top = i*(map_row_marginy + map_row_size[1]) + 100
            map_row.load_images()
            self.buttons.append(map_row.select_button)
            self.map_rows.append(map_row)
            i += 1


    def update(self):
        self.handle_events()
        self.draw()


    def handle_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
            
            if e.type == pg.MOUSEBUTTONDOWN:
                if e.button == 1:
                    for button in self.buttons:
                        button.check_click(e.pos)
                elif e.button == 4:
                    self.offsety += 20
                elif e.button == 5:
                    self.offsety -= 20

    
    def draw(self):
        self.parent.fill("black")
        for map_row in self.map_rows:
            map_row.draw(self.offsety)
        self.back_button.draw()


class MapRow:
    def __init__(self, parent, resources, load_game, map, size, font):
        self.parent = parent
        self.resources = resources
        self.map = map
        self.rect = pg.Rect((0, 0), size)
        self.font = font
        self.select_button = ui.Button(self.parent, self.resources["select_button.png"], (0, 0), lambda map=map: load_game(map))

        self.offsety = 0  # most recent offsety level
    

    def draw(self, offsety):
        self.update_offsety(offsety)
        pg.draw.rect(self.parent, "green", self.rect)
        self.parent.blit(self.name_text, self.name_rect)
        self.select_button.draw()


    def update_offsety(self, new_offsety):
        self.rect.y += new_offsety - self.offsety
        self.offsety = new_offsety
    

    def load_images(self):
        self.name_text = self.font.render(self.map["name"], True, "black")
        self.name_rect = self.name_text.get_rect()
        self.name_rect.centery = self.rect.centery
        self.name_rect.left = self.rect.left + 10
        self.select_button.rect.centery = self.rect.centery
        self.select_button.rect.right = self.rect.right-5
