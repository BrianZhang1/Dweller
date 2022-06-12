from email.policy import default
import pygame as pg
from ..components import terrain, button

class Map_Creator:
    def __init__(self, parent, resources, tile_size, default_map):
        self.parent = parent
        self.resources = resources

        self.terrainh = terrain.Terrain_Handler(self.parent, resources, tile_size, default_map["tilemap"], 1)
        self.offsetx = 0

        # buttons at side of screen to move screen
        self.buttons = []
        screen_size = (self.parent.get_width(), self.parent.get_height())
        arrow_button_xmargin = 10

        self.left_button = button.Button(self.parent, self.resources["arrow_left.png"], (0, 0), lambda: self.move_screen(-100))
        self.left_button.rect.centery = screen_size[1]/2
        self.left_button.rect.left = arrow_button_xmargin
        self.buttons.append(self.left_button)

        self.right_button = button.Button(self.parent, self.resources["arrow_right.png"], (0, 0), lambda: self.move_screen(100))
        self.right_button.rect.centery = screen_size[1]/2
        self.right_button.rect.right = screen_size[0]-arrow_button_xmargin
        self.buttons.append(self.right_button)
    
        self.bpanel_bg_rect = pg.Rect(0, 0, 300, 60)
        self.bpanel_bg_rect.centerx = screen_size[0]/2
        self.bpanel_bg_color = (180, 180, 180)

    

    def update(self):
        self.handle_events()
        self.draw()


    def handle_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
            
            elif e.type == pg.MOUSEBUTTONDOWN:
                if e.button == 1:
                    button_pressed = False
                    for button in self.buttons:
                        if button.check_click(e.pos):
                            button_pressed = True
                            break
                    
                    if not button_pressed:
                        tile = self.terrainh.get_tile((e.pos[0]+self.offsetx, e.pos[1]))
                        if tile != None:
                            tile.type = 2
    

    def draw(self):
        self.parent.fill("black")
        self.terrainh.draw(self.offsetx)
        for button in self.buttons:
            button.draw()
        pg.draw.rect(self.parent, self.bpanel_bg_color, self.bpanel_bg_rect)
    

    def move_screen(self, amount):
        self.offsetx += amount