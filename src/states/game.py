import pygame as pg
from ..components import entities, ui, map


# Controls the game screen
class Game:
    def __init__(self, parent, resources, start_new_game, load_main_menu, high_score, difficulty, tile_size, map_data):
        self.parent = parent
        self.resources = resources
        self.start_new_game = start_new_game
        self.load_main_menu = load_main_menu
        self.high_score = high_score
        self.difficulty = difficulty
        self.map_data = map_data

        # important variables
        self.cur_time = pg.time.get_ticks()
        self.screen_size = (parent.get_width(), parent.get_height())
        self.scroll_speed = 5  # speed the background scrolls
        self.enemies_defeated = 0  # how many enemies have been defeated
        self.game_over = False  # whether the game is over
        self.buttons = []  # list of all button objects for ui
        self.paused = False  # whether game is paused
        self.tick_count = 0 # used to track how long since the game has started
        self.music_on = True  # whether music is on

        # create map object
        self.map = map.Map(self.parent, self.resources, tile_size, self.map_data)

        # create sprite groups
        self.all_sprites = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()

        # create initial objects and add to sprite groups
        self.player = entities.Player(self.parent, self.resources, self.end_game, self.map.get_nearby_tiles)
        self.all_sprites.add(self.player)
        self.generate_map_enemies()  # generate an enemy for every enemy tile in map

        # for horizontal camera movement (tracks player movement)
        self.offsetx = self.player.get_centerx() - self.screen_size[0] / 2

        # start music
        pg.mixer.music.rewind()
        pg.mixer.music.play(-1)

        # fonts for text
        self.font1 = pg.font.SysFont("dejavuserif", 50)
        self.font2 = pg.font.SysFont("Arial", 25)

        # GAME OVER UI
        centerx = self.screen_size[0]/2

        self.play_again_button = ui.Button(self.parent, self.resources["play_again.png"], (0, 0), lambda: self.start_new_game(score=self.enemies_defeated, map=self.map_data))
        self.play_again_button.rect.centerx = centerx
        self.play_again_button.rect.top = 240

        self.main_menu_button = ui.Button(self.parent, self.resources["main_menu_button.png"], (0, 0), lambda: self.load_main_menu(score=self.enemies_defeated))
        self.main_menu_button.rect.centerx = centerx
        self.main_menu_button.rect.top = self.play_again_button.rect.bottom + 10

        self.game_over_buttons = [self.play_again_button, self.main_menu_button]
        self.buttons.extend(self.game_over_buttons)

        # PAUSE UI
        # Pause/Settings button
        self.settings_icon = ui.Button(self.parent, self.resources["settings_icon.png"], (0, 0), self.toggle_pause)
        self.settings_icon.rect.top = 10
        self.settings_icon.rect.right = self.screen_size[0]-10
        self.buttons.append(self.settings_icon)

        # dim screen
        self.screen_dimmer = pg.Surface(self.screen_size)
        self.screen_dimmer.set_alpha(128)
        self.screen_dimmer.fill("black")

        # Buttons for Pause Screen
        self.resume_icon = ui.Button(self.parent, self.resources["play_icon.png"], (0, 0,), self.toggle_pause)
        self.main_menu_icon = ui.Button(self.parent, self.resources["main_menu_icon.png"], (0, 0,), self.load_main_menu)
        self.mute_icon = ui.Button(self.parent, self.resources["mute_icon.png"], (0, 0,), self.toggle_music)
        self.paused_buttons = [self.resume_icon, self.main_menu_icon, self.mute_icon]
        self.buttons.extend(self.paused_buttons)
        button_count = len(self.paused_buttons)
        button_width = 60
        button_margin = 10
        centerx = self.screen_size[0]/2
        centery = self.screen_size[1]/2
        x = centerx - (button_count*(button_width+button_margin)-button_margin)/2
        for button in self.paused_buttons:
            button.rect.centery = centery
            button.rect.left = x
            x += button_width + button_margin



    # called once per tick by main.py
    def update(self):
        # the update function is called once per tick
        self.cur_time = pg.time.get_ticks()
        self.handle_events()

        # update player and enemy movements if the game is not paused and is still going
        if not self.game_over and not self.paused:
            self.player.update(self.cur_time, self.offsetx)
            self.check_bounds()
            self.enemies.update(self.cur_time, self.offsetx, self.player.get_centerx())
            self.check_collision()
            self.tick_count += 1

        # blits everything on parent surface
        self.draw()

    # handles events
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

            if not self.game_over:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.paused:
                            # CHECK CLICK ON PAUSED UI BUTTONS
                            for button in self.paused_buttons:
                                button.check_click(event.pos)
                        else:
                            # CHECK CLICK ON SETTINGS
                            if not self.settings_icon.check_click(event.pos):
                                # CHECK CLICK FOR ATTACK IF BUTTON NOT CLICKED
                                self.player.begin_attack()

                elif event.type == pg.KEYDOWN:
                    # ESC KEY PAUSES GAME
                    if event.key == pg.K_ESCAPE:
                        self.toggle_pause()
                    elif not self.paused:
                        # PLAYER MOVEMENT
                        if event.key == pg.K_d:
                            self.player.move_direction += 1
                        elif event.key == pg.K_a:
                            self.player.move_direction -= 1
                        elif event.key == pg.K_w:
                            self.player.jump()


                # stop player movement on keyup
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_d:
                        self.player.move_direction -= 1
                    elif event.key == pg.K_a:
                        self.player.move_direction += 1

            else:
                # check for click on game over ui buttons
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in self.game_over_buttons:
                            button.check_click(event.pos)


    # draws everything in the game
    def draw(self):
        self.scroll()  # update screen offset

        self.map.draw(self.offsetx)  # draw map (background + tiles)
        self.settings_icon.draw() 

        # update Rect position of all sprites to prepare to draw
        for sprite in self.all_sprites.sprites():
            sprite.update_rect(self.offsetx)
            sprite.healthbar.render()  # render healthbar of all sprites
        # draw all sprites
        self.all_sprites.draw(self.parent)  # use pygame built-in draw function for sprite groups

        # drawing ui when game is over
        if self.game_over:
            # draw different graphic depending on whether player won or lost
            if not self.win:
                self.parent.blit(self.resources["game_over.png"], self.game_over_rect)
            else:
                self.parent.blit(self.resources["level_complete.png"], self.level_complete_rect)

            # stats for game
            self.parent.blit(self.enemies_defeated_text, self.enemies_defeated_rect)
            self.parent.blit(self.time_text, self.time_rect)
            self.parent.blit(self.high_score_text, self.high_score_rect)
            # menu buttons
            self.play_again_button.draw()
            self.main_menu_button.draw()
        
        # PAUSE UI
        elif self.paused:
            self.parent.blit(self.screen_dimmer, (0, 0))
            for button in self.paused_buttons:
                button.draw()

    # ends the game upon being called
    def end_game(self, win=False):
        self.win = win
        pg.mixer.music.stop()

        # calculate score
        time = int(self.tick_count/30)
        score = self.enemies_defeated

        # update high score if score is higher than high score
        if score > self.high_score:
            self.high_score = score

        # positioning images for post-game ui
        centerx = self.screen_size[0]/2  # for positioning
        self.enemies_defeated_text = self.font2.render("Enemies Defeated: " + str(self.enemies_defeated), True, "black", "white")
        self.enemies_defeated_rect = self.enemies_defeated_text.get_rect()
        self.enemies_defeated_rect.centerx = centerx
        self.time_text = self.font2.render("Time: " + str(time) + " seconds", True, "black", "white")
        self.time_rect = self.time_text.get_rect()
        self.time_rect.centerx = centerx
        self.high_score_text = self.font2.render("High Score: " + str(self.high_score), True, "black", "white")
        self.high_score_rect = self.high_score_text.get_rect()
        self.high_score_rect.centerx = centerx
        if not win:
            self.game_over_rect = self.resources["game_over.png"].get_rect()
            self.game_over_rect.centerx = centerx
            self.game_over_rect.top = 50
            self.enemies_defeated_rect.top = self.game_over_rect.bottom + 10
        else:
            self.level_complete_rect = self.resources["level_complete.png"].get_rect()
            self.level_complete_rect.centerx = centerx
            self.level_complete_rect.top = 50
            self.enemies_defeated_rect.top = self.level_complete_rect.bottom + 10
        self.time_rect.top = self.enemies_defeated_rect.bottom
        self.high_score_rect.top = self.time_rect.bottom

        self.game_over = True

    # check for collisions
    def check_collision(self):
        # check collision between enemy/player
        for enemy_obj in pg.sprite.spritecollide(self.player, self.enemies, False, pg.sprite.collide_mask):
            # active_attack attribute means whether their attack hitbox is active
            if self.player.active_attack:
                enemy_obj.receive_attack(1)
            elif enemy_obj.active_attack:
                self.player.receive_attack(1)
        
        # check if player reaches portal to end level
        if self.player.collide_type(self.offsetx, [3, 4, 5, 6]):
            self.end_game(win=True)
    

    # generates an enemy for every enemy tile in the map
    def generate_map_enemies(self):
        for col in self.map.tilemap:
            for tile in col:
                if tile.type == 2:  # 2 is the type for enemy tile
                    self.generate_enemy(tile.pos)
                    tile.change_type(0, self.map.tilemap)


    # spawn new enemy
    def generate_enemy(self, pos):
        enemy_obj = entities.Enemy(self.parent, self.resources, pos, self.handle_enemy_death, self.difficulty, self.map.get_nearby_tiles)
        self.all_sprites.add(self.player, enemy_obj)
        self.enemies.add(enemy_obj)

    # handles death of an enemy
    def handle_enemy_death(self):
        self.enemies_defeated += 1  # +1 score per enemy killed

    # handles scrolling of camera when player moves
    def scroll(self):
        bg_w = self.map.pixel_width
        new_offsetx = self.player.get_centerx() - self.screen_size[0] / 2

        # the offset cannot be less than 0
        if new_offsetx < 0:
            self.offsetx = 0
        # the offset cannot go past the right side of the screen
        elif new_offsetx > bg_w - self.screen_size[0]:
            self.offsetx = bg_w - self.screen_size[0]
        # otherwise, center the screen on the player position
        else:
            self.offsetx = new_offsetx

    # stops player from going out of bounds
    def check_bounds(self):
        if self.player.get_centerx() < 0:
            self.player.set_centerx(0)
        elif self.player.get_centerx() > self.map.pixel_width:
            self.player.set_centerx(self.map.pixel_width)
    

    # renders the score text
    def draw_score(self, score):
        # create score/speed text objects
        score_text_content = "Score: " + str(score)
        score_text = self.font2.render(score_text_content, True, "black", "white")
        score_text_pos = score_text.get_rect()
        score_text_pos.left = 10
        score_text_pos.top = 10
        
        # draw objects
        self.parent.blit(score_text, score_text_pos)
    

    # toggles whether game is paused
    def toggle_pause(self):
        if self.paused == False:
            self.paused = True
            if self.music_on:
                pg.mixer.music.pause()
        else:
            self.paused = False
            if self.music_on:
                pg.mixer.music.unpause()
    

    # toggles music on/off
    def toggle_music(self):
        if self.music_on == True:
            self.music_on = False
        else:
            self.music_on = True


