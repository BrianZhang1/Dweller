import pygame as pg
from ..components import ui, map

class Map_Creator:
    def __init__(self, parent, resources, data, tile_size, save_map_callback, load_main_menu):
        self.parent = parent
        self.resources = resources
        self.data = data
        self.tile_size = tile_size
        self.save_map_callback = save_map_callback
        self.load_main_menu = load_main_menu

        # core variables
        self.load_plain_map(1)  # loads the initial map
        self.offsetx = 0  # for moving screen horizontally
        self.selected_tile_type = 1  # type of selected tile
        self.buttons = [] # list of all buttons
        self.placing_tiles = False  # so user can click and drag to place multiple tiles
        self.portal = None  # location of the portal (ends level when player reaches this)

        # -------------------POSITIONING UI ELEMENTS--------------------------------
        # NAVIGATION BUTTONS -----------------------------------
        # buttons at side of screen to move screen
        self.nav_buttons = []
        screen_size = (self.parent.get_width(), self.parent.get_height())
        arrow_button_xmargin = 10

        # left navigation button
        self.left_button = ui.Button(self.parent, self.resources["arrow_left.png"], (0, 0), lambda: self.move_screen(-100))
        self.left_button.rect.centery = screen_size[1]/2
        self.left_button.rect.left = arrow_button_xmargin
        self.nav_buttons.append(self.left_button)

        # right navigation button
        self.right_button = ui.Button(self.parent, self.resources["arrow_right.png"], (0, 0), lambda: self.move_screen(100))
        self.right_button.rect.centery = screen_size[1]/2
        self.right_button.rect.right = screen_size[0]-arrow_button_xmargin
        self.nav_buttons.append(self.right_button)
        # add navigation buttons to buttons list
        for nav_button in self.nav_buttons:
            self.buttons.append(nav_button)
    
        # TILE PANEL ------------------------------------------------
        # create tile panel (where tiles can be selected)
        tile_images = [self.resources["remove.png"], self.resources["Tile_18.png"], self.resources["enemy_tile.png"], self.resources["portal_display.png"]]
        self.tpanel_tile_margin = 10
        self.tpanel_select_rect = pg.Rect(0, 0, len(tile_images)*(self.tpanel_tile_margin + tile_size), tile_size+20)
        self.tpanel_select_rect.centerx = screen_size[0]/2
        self.tpanel_select_color = (150, 150, 150)

        self.tpanel_bg_rect = pg.Rect(0, 0, self.tpanel_select_rect.width+10, self.tpanel_select_rect.height+10)
        self.tpanel_bg_rect.center = self.tpanel_select_rect.center
        self.tpanel_bg_color = (180, 180, 180)

        self.tpanel_buttons = []
        pos = (self.tpanel_select_rect.left+5, self.tpanel_select_rect.centery-self.tile_size/2)
        for i in range(len(tile_images)):
            self.tpanel_buttons.append(ui.Button(self.parent, tile_images[i], pos, lambda i=i: self.set_selected_tile_type(i)))
            pos = (pos[0]+self.tile_size+self.tpanel_tile_margin, pos[1])
        # add tile panel buttons to button list
        for tpanel_button in self.tpanel_buttons:
            self.buttons.append(tpanel_button)

        # SAVE BUTTON ------------------------------
        save_button_margin = 10
        self.save_button = ui.Button(self.parent, self.resources["save_button.png"], (0, 0), self.toggle_tb)
        self.save_button.rect.right = screen_size[0]-save_button_margin
        self.save_button.rect.bottom = screen_size[1]-save_button_margin
        self.buttons.append(self.save_button)

        # BACK BUTTON
        self.back_button = ui.Button(self.parent, resources["back_button.png"], (10, 10), self.load_main_menu)
        self.buttons.append(self.back_button)

        # TITLE MAP TEXT BOX
        self.show_tb = False
        self.title_tb = ui.Textbox(self.parent, (300, 60), "Map Title", "Map"+str(len(self.data["maps"])))
        self.title_tb.rect.center = (screen_size[0]/2, screen_size[1]/2)
        self.title_tb.update_tb_pos()
        self.enter_to_save_rect = self.resources["enter_to_save_text.png"].get_rect(centerx=screen_size[0]/2, top=self.title_tb.rect.bottom+20)

        # SETTINGS BUTTON
        self.show_settings = False
        self.settings_button = ui.Button(self.parent, self.resources["settings_gear.png"], (0, 0), self.toggle_settings)
        self.settings_button.rect.top = 10
        self.settings_button.rect.right = screen_size[0]-10
        self.buttons.append(self.settings_button)

        # SETTINGS PANEL
        self.settings_panel = pg.Rect(0, 0, 0, 0)
        self.settings_panel.top = self.settings_button.rect.bottom + 10
        self.settings_panel.right = screen_size[0] - 10

        # SETTINGS PANEL SET WIDTH VALUEINCREMENTER
        # callback for width_incrementer
        def width_incrementer_callback(value):
            new_width = self.map.width + value
            self.set_width(new_width)
            self.width_incrementer.set_value(new_width)

        self.width_incrementer = ui.Incrementer(self.parent, self.resources, self.buttons, "Map Width", width_incrementer_callback, self.map.width)
        self.width_incrementer.rect.topright = self.settings_panel.right-5, self.settings_panel.top+5
        self.width_incrementer.position_components()
        
        # update settings panel dimensions/position according to widgets it contains
        self.settings_panel.width = self.width_incrementer.rect.width + 10
        self.settings_panel.height = self.width_incrementer.rect.height + 10
        self.settings_panel.top = self.settings_button.rect.bottom + 10
        self.settings_panel.right = screen_size[0] - 10


    
    # called onced per tick
    def update(self):
        self.handle_events()
        self.check_place_tile()  # place a tile at mouse pos if self.placing_tiles is true
        self.title_tb.update()
        self.draw()


    # handles events
    def handle_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
            
            elif e.type == pg.MOUSEBUTTONDOWN:
                if e.button == 1:
                    # check clicks on buttons
                    button_pressed = False
                    for button in self.buttons:
                        if button.check_click(e.pos):
                            button_pressed = True
                            break
                    
                    # if the click wasn't for a button then place tiles
                    if not button_pressed:
                        self.placing_tiles = True
            
            # stop placing tiles when click released
            elif e.type == pg.MOUSEBUTTONUP:
                self.placing_tiles = False
            
            elif e.type == pg.KEYDOWN:
                if self.show_tb:
                    # TYPING IN TEXTBOX
                    if e.key == pg.K_BACKSPACE:
                        self.title_tb.content = self.title_tb.content[:-1] # remove last character
                    elif e.key == pg.K_ESCAPE:
                        self.show_tb = False  # close textbox
                    elif e.key == pg.K_RETURN:
                        self.save_map()
                    else:
                        self.title_tb.content += e.unicode
                else:
                    # MOVE SCREEN WITH A AND D KEYS
                    if e.key == pg.K_a:
                        self.move_screen(-100)
                    elif e.key == pg.K_d:
                        self.move_screen(100)

    

    # draws everything
    def draw(self):
        self.parent.fill("black")
        self.map.draw(self.offsetx)
        
        # draw tile panel
        pg.draw.rect(self.parent, self.tpanel_bg_color, self.tpanel_bg_rect)
        pg.draw.rect(self.parent, self.tpanel_select_color, self.tpanel_select_rect)
        for button in self.tpanel_buttons:
            button.draw()

        # draw buttons
        self.save_button.draw()
        self.settings_button.draw()
        self.back_button.draw()
        for button in self.nav_buttons:
            button.draw()

        # show menus
        if self.show_tb:
            self.title_tb.draw()
            self.parent.blit(self.resources["enter_to_save_text.png"], self.enter_to_save_rect)
        if self.show_settings:
            pg.draw.rect(self.parent, (160, 160, 160), self.settings_panel)
            self.width_incrementer.draw()
        
    
    # moves screen horizontally by amount argument
    def move_screen(self, amount):
        self.offsetx += amount


    # changes the selected tile type
    def set_selected_tile_type(self, new_tile):
        self.selected_tile_type = new_tile
    

    # title textbox for titling map
    def toggle_tb(self):
        if self.show_tb:
            self.show_tb = False
            self.save_button.image = self.resources["save_button.png"]
        else:
            self.show_tb = True 
            self.save_button.image = self.resources["close_save.png"]
    

    # toggles settings panel open/close
    def toggle_settings(self):
        if self.show_settings:
            self.show_settings = False
        else:
            self.show_settings = True
    

    # save the map
    def save_map(self):
        error = self.save_map_callback(self.title_tb.content, self.map)
        if error != 0:
            self.title_tb.set_error(error, 1000)
        else:
            self.load_main_menu()

    
    # place a tile at mouse pos if self.placing_tiles is true
    def check_place_tile(self):
        if self.placing_tiles:
            mouse_pos = pg.mouse.get_pos()
            tile = self.map.get_tile((mouse_pos[0]+self.offsetx, mouse_pos[1]))
            if tile != None:
                if self.selected_tile_type == 3:
                    self.place_portal(tile)
                else:
                    tile_changed = tile.change_type(self.selected_tile_type, self.map.tilemap)
                    if tile_changed:  # if new tile, update surrounding tile images
                        for tile in self.map.get_nearby_tiles(tile.pos, radius=2):
                            tile.load_image(self.map.tilemap)
    

    # generates a plain map with just a floor, given width
    # width is how many backgrounds wide the map is
    def load_plain_map(self, width):
        bg_width = self.resources["bg.png"].get_width()
        bg_height = self.resources["bg.png"].get_height()
        cols = int(bg_width*width/self.tile_size) + 1
        rows = int(bg_height/self.tile_size) + 1
        tilemap = []
        for i in range(cols):
            col = []
            for k in range(rows):
                if k == rows-1:
                    col.append(1)
                else:
                    col.append(0)
            tilemap.append(col)

        map_data = {
            "name": "plain",
            "tilemap": tilemap,
            "width": width
        }
        
        self.map = map.Map(self.parent, self.resources, self.tile_size, map_data)


    # set how many bg the width of the map is
    def set_width(self, new_width):
        if new_width < 1:
            new_width = 1
        self.load_plain_map(new_width)
    

    # places the portal to end level
    # the portal is 2x2 tiles
    # tile argument is the top left tile of the portal
    def place_portal(self, tile):
        tilemap = self.map.tilemap

        # first, check if space is available for portal
        if len(tilemap) - tile.list_pos[0] >= 2 and len(tilemap[0]) - tile.list_pos[1] >= 2:
            # remove old portal if it exists
            if self.portal != None:
                # change tiles of old portal to empty tiles
                tilemap[self.portal.list_pos[0]][self.portal.list_pos[1]].change_type(0, tilemap)
                tilemap[self.portal.list_pos[0]+1][self.portal.list_pos[1]].change_type(0, tilemap)
                tilemap[self.portal.list_pos[0]][self.portal.list_pos[1]+1].change_type(0, tilemap)
                tilemap[self.portal.list_pos[0]+1][self.portal.list_pos[1]+1].change_type(0, tilemap)
            self.portal = tile

            # change tiles to portal tiles
            tilemap[tile.list_pos[0]][tile.list_pos[1]].change_type(3, tilemap)
            tilemap[tile.list_pos[0]+1][tile.list_pos[1]].change_type(4, tilemap)
            tilemap[tile.list_pos[0]][tile.list_pos[1]+1].change_type(5, tilemap)
            tilemap[tile.list_pos[0]+1][tile.list_pos[1]+1].change_type(6, tilemap)
        else:
            print("Not enough space for portal.")

