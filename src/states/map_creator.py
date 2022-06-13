from json import load
import pygame as pg
from ..components import terrain, button, textbox

class Map_Creator:
    def __init__(self, parent, resources, tile_size, default_map, save_map_callback, load_main_menu):
        self.parent = parent
        self.resources = resources
        self.tile_size = tile_size
        self.default_map = default_map
        self.save_map_callback = save_map_callback
        self.load_main_menu = load_main_menu

        # core variables
        self.terrainh = terrain.Terrain_Handler(self.parent, resources, tile_size, default_map["tilemap"], 1)
        self.offsetx = 0
        self.selected_tile_type = 1  # type of selected tile
        self.buttons = [] # list of all buttons

        # NAVIGATION BUTTONS -----------------------------------
        # buttons at side of screen to move screen
        self.nav_buttons = []
        screen_size = (self.parent.get_width(), self.parent.get_height())
        arrow_button_xmargin = 10

        # left navigation button
        self.left_button = button.Button(self.parent, self.resources["arrow_left.png"], (0, 0), lambda: self.move_screen(-100))
        self.left_button.rect.centery = screen_size[1]/2
        self.left_button.rect.left = arrow_button_xmargin
        self.nav_buttons.append(self.left_button)

        # right navigation button
        self.right_button = button.Button(self.parent, self.resources["arrow_right.png"], (0, 0), lambda: self.move_screen(100))
        self.right_button.rect.centery = screen_size[1]/2
        self.right_button.rect.right = screen_size[0]-arrow_button_xmargin
        self.nav_buttons.append(self.right_button)
        # add navigation buttons to buttons list
        for nav_button in self.nav_buttons:
            self.buttons.append(nav_button)
    
        # TILE PANEL ------------------------------------------------
        # create tile panel (where tiles can be selected)
        self.tpanel_bg_rect = pg.Rect(0, 0, 300, 60)
        self.tpanel_bg_rect.centerx = screen_size[0]/2
        self.tpanel_bg_color = (180, 180, 180)

        tile_images = [self.resources["remove.png"], self.resources["Tile_18.png"]]
        self.tpanel_tile_margin = 10
        self.tpanel_select_rect = pg.Rect(0, 0, len(tile_images)*(self.tpanel_tile_margin + tile_size), tile_size+20)
        self.tpanel_select_rect.center = self.tpanel_bg_rect.center
        self.tpanel_select_color = (150, 150, 150)

        self.tpanel_buttons = []
        pos = (self.tpanel_select_rect.left+5, self.tpanel_select_rect.centery-self.tile_size/2)
        for i in range(len(tile_images)):
            self.tpanel_buttons.append(button.Button(self.parent, tile_images[i], pos, lambda i=i: self.set_selected_tile_type(i)))
            pos = (pos[0]+self.tile_size+self.tpanel_tile_margin, pos[1])
        # add tile panel buttons to button list
        for tpanel_button in self.tpanel_buttons:
            self.buttons.append(tpanel_button)

        # SAVE BUTTON ------------------------------
        save_button_margin = 10
        self.save_button = button.Button(self.parent, self.resources["save_button.png"], (0, 0), self.show_tb)
        self.save_button.rect.right = screen_size[0]-save_button_margin
        self.save_button.rect.bottom = screen_size[1]-save_button_margin
        self.buttons.append(self.save_button)

        # TITLE MAP TEXT BOX
        self.show_tb = False
        self.title_tb = textbox.Textbox(self.parent, (300, 60))
        self.title_tb.rect.center = (screen_size[0]/2, screen_size[1]/2)
        self.title_tb.update_tb_pos()

    

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
                            tile.type = self.selected_tile_type
                            for tile in self.terrainh.get_nearby_tiles(tile.pos, radius=2):
                                tile.load_image(self.terrainh.map.tilemap)
            
            elif e.type == pg.KEYDOWN:
                if self.show_tb:
                    if e.key == pg.K_BACKSPACE:
                        self.title_tb.content = self.title_tb.content[:-1] # remove last character
                    elif e.key == pg.K_RETURN:
                        self.save_map()
                    else:
                        self.title_tb.content += e.unicode

    

    def draw(self):
        self.parent.fill("black")
        self.terrainh.draw(self.offsetx)
        for button in self.nav_buttons:
            button.draw()
        self.draw_tpanel()
        self.save_button.draw()
        if self.show_tb:
            self.title_tb.draw()


    def draw_tpanel(self):
        pg.draw.rect(self.parent, self.tpanel_bg_color, self.tpanel_bg_rect)
        pg.draw.rect(self.parent, self.tpanel_select_color, self.tpanel_select_rect)
        for button in self.tpanel_buttons:
            button.draw()
        
    
    def move_screen(self, amount):
        self.offsetx += amount


    def set_selected_tile_type(self, new_tile):
        self.selected_tile_type = new_tile
    

    def show_tb(self):
        self.show_tb = True  # make textbox for titling map appear
    

    # save the map
    def save_map(self):
        self.save_map_callback(self.title_tb.content, self.terrainh.map, self.terrainh.bg_num)
        self.load_main_menu()