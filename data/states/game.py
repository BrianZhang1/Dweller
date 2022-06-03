import random
import pygame as pg
from ..components import user_interface, player, enemy, terrain


# Controls the game screen
class Game:
    def __init__(self, parent, resources, start_new_game, load_main_menu, high_score, difficulty):
        self.cur_tile_rect = None

        self.parent = parent
        self.resources = resources
        self.start_new_game = start_new_game
        self.load_main_menu = load_main_menu
        self.high_score = high_score
        self.difficulty = difficulty

        # important variables
        self.cur_time = pg.time.get_ticks()
        self.screen_size = (parent.get_width(), parent.get_height())
        self.scroll_speed = 5  # speed the background scrolls
        self.score = 0
        self.game_over = False  # whether the game is over
        self.last_enemy = pg.time.get_ticks()  # time of last enemy spawn

        # change enemy spawn cooldown depending on game difficulty
        if self.difficulty == "easy":
            self.enemy_cooldown = 5000
        elif self.difficulty == "okay":
            self.enemy_cooldown = 4500
        elif self.difficulty == "hard":
            self.enemy_cooldown = 4000
        else:
            print("invalid difficulty")

        # create terrain handler
        self.terrain_h = terrain.Terrain_Handler(self.parent, self.resources)

        # create sprite groups
        self.all_sprites = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()

        # create initial objects and add to sprite groups
        self.ui = user_interface.User_Interface(self.parent, self.resources)
        self.player = player.Player(self.parent, self.resources, self.end_game)
        self.all_sprites.add(self.player)

        #self.background_image = resources["background.png"]
        #self.floor = obstacle.Obstacle(0, 0)
        self.offsetx = self.player.get_centerx() - self.screen_size[0] / 2

        # start music
        pg.mixer.music.rewind()
        pg.mixer.music.play(-1)

    # called once per tick by main.py
    def update(self):
        # the update function is called once per tick
        self.cur_time = pg.time.get_ticks()
        self.handle_events()

        if not self.game_over:
            self.player.update(self.cur_time)
            self.check_tile_collision(self.player)
            self.check_bounds()
            self.enemies.update(self.cur_time, self.player.get_centerx())
            self.check_collision()

            #if self.cur_time - self.last_enemy > self.enemy_cooldown:
            #  self.generate_enemy_rand_side()

        # blits everything on parent surface
        self.draw()

    # handles events
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

            if not self.game_over:
                # check for mouse clicks for attacks
                # keyboard input is handled in handle_keyboard method below
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.player.begin_attack()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_d:
                        self.player.move_direction += 1
                    elif event.key == pg.K_a:
                        self.player.move_direction -= 1
                    elif event.key == pg.K_SPACE:
                        self.player.jump()
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_d:
                        self.player.move_direction -= 1
                    elif event.key == pg.K_a:
                        self.player.move_direction += 1

            else:
                # check for click on replay or main menu button
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click_target = self.ui.process_click(event.pos)
                        if click_target:
                            if click_target == "start_new_game":
                                self.start_new_game(score=self.score)
                            elif click_target == "load_main_menu":
                                self.load_main_menu(score=self.score)

    # handles keyboard input to move player
    def handle_keyboard(self):
        if self.player.state == "idle" or self.player.state == "run":
            keys_pressed = pg.key.get_pressed()
            a_pressed = keys_pressed[pg.K_a]
            d_pressed = keys_pressed[pg.K_d]
            space_pressed = keys_pressed[pg.K_SPACE]
            if d_pressed and not a_pressed:
                self.player.move(1)
            elif a_pressed and not d_pressed:
                self.player.move(-1)
            else:
                self.player.move(0)
            if space_pressed:
                self.player.jump()

    # draws everything in the game
    def draw(self):
        self.scroll()  # update screen offset

        self.terrain_h.draw(self.offsetx)
        #self.parent.blit(self.background_image, (0-self.offsetx, 0))

        # update Rect position of all sprites to prepare to draw
        for sprite in self.all_sprites.sprites():
            sprite.update_rect(self.offsetx)
            sprite.healthbar.render()  # render healthbar of all sprites
        pg.draw.rect(self.parent, "red", self.player.get_rect())
        self.all_sprites.draw(
            self.parent)  # use pygame built-in draw function for sprite groups

        # render score text
        self.ui.render_score(self.score)

        if self.game_over:
            self.ui.render_game_over()

    # ends the game upon being called
    def end_game(self):
        pg.mixer.music.stop()

        # update high score if score is higher than high score
        if self.score > self.high_score:
            self.high_score = self.score
        self.ui.process_game_over(self.high_score)

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

    # check collisions between entities and nearby tiles
    def check_tile_collision(self, entity):
        grounded = False
        tile_size = self.terrain_h.tile_size
        if isinstance(entity, player.Player):
            rect = self.player.get_rect()
            nearby_tiles = self.terrain_h.get_nearby_tiles(self.player.get_center(), radius=2)
        else:
            print("not player")
        for tile in nearby_tiles:
            if tile.type == 1:
                tile_rect = pg.Rect((tile.pos[0] - self.offsetx, tile.pos[1]), (tile_size, tile_size))
                # FIX SNAPPING AND MAKE COMPATIBLE WITH ENEMY

                if rect.colliderect(tile_rect):
                    # if top of tile is between the bottom and center of the player, move the player to the top of the tile
                    if rect.bottom > tile_rect.top and tile_rect.top > rect.centery:
                        grounded = True
                        self.player.set_bottom(tile_rect.top + 1)
                        if self.player.vel_y < 0:
                            self.player.vel_y = 0
                    # if bottom of tile is between center and top player, move player top to the bottom of the tile
                    elif rect.centery > tile_rect.bottom and tile_rect.bottom > rect.top:
                        self.player.set_bottom(tile_rect.bottom+rect.height)
                        if self.player.vel_y > 0:
                            self.player.vel_y = 0
                    # if right of tile is between left and center, move player left to the right of the tile
                    elif rect.centerx > tile_rect.right and tile_rect.right > rect.left:
                        self.player.set_left(tile.pos[0]+self.terrain_h.tile_size-1)
                        if self.player.vel_x < 0:
                            self.player.vel_x = 0
                    # if left of tile is between center and right, move player right to the left of the tile
                    elif rect.right > tile_rect.left and tile_rect.left > rect.centerx:
                        self.player.set_left(tile.pos[0]-self.terrain_h.tile_size)
                        if self.player.vel_x > 0:
                            self.player.vel_x = 0
        self.player.grounded = grounded

    def generate_enemy_rand_side(self):
        side = random.randint(0, 1)
        if side:
            pos = (self.parent.get_width(), 367)
        else:
            pos = (-100, 367)
        self.generate_enemy(pos)

    # spawn new enemy
    def generate_enemy(self, pos):
        self.last_enemy = self.cur_time
        enemy_obj = enemy.Enemy(self.parent, self.resources, pos,
                                self.handle_enemy_death, self.difficulty)
        self.all_sprites.add(self.player, enemy_obj)
        self.enemies.add(enemy_obj)

    # handles death of an enemy
    def handle_enemy_death(self):
        self.score += 1  # +1 score per enemy killed

    # handles scrolling of camera when player moves
    def scroll(self):
        bg_w = self.terrain_h.bg_w
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
        elif self.player.get_centerx() > self.terrain_h.bg_w:
            self.player.set_centerx(self.terrain_h.bg_w)
