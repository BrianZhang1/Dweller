# This file contains the base class Entity, all its subclasses, and related classes.
# Subclasses of Entity include Player and Enemy.

import pygame as pg



# base class for all entities
# objects that inherit from Entity MUST have a self.animation_ref dictionary containing all assets for animation before calling __init__ method of the Entity class
class Entity(pg.sprite.Sprite):
  def __init__(self, parent, resources, init_pos, animation_cooldown, health, speed, active_attack_frames, get_nearby_tiles):
    super().__init__()
    self.cur_time = pg.time.get_ticks()
    
    self.parent = parent
    self.resources = resources
    self.active_attack_frames = active_attack_frames
    self.get_nearby_tiles = get_nearby_tiles # method to get tiles near this entity

    self.max_health = health
    self.health = health
    self.speed = speed

    self.pos = list(init_pos)  # bottom left pos

    # Sprite variables
    self.image = self.animation_ref["idle"][0][0]
    self.image_length = self.animation_ref["idle"][0][0].get_height()
    # rect controls the position of sprite when drawing
    self.rect = self.image.get_rect()
    # mask is for pixel perfect hitbox
    self.mask = pg.mask.from_surface(self.image)

    # animation variables
    self.animation_cooldown = animation_cooldown
    self.animation_step = 0 # current step of animation in animation loop
    self.last_animation = 0 # time of last animation step
    self.animation_paused = False # whether animation is paused
    self.pause_time = None # when pause began

    # velocity/movement variables
    self.vel_x = 0
    self.vel_y = 0
    self.direction = 1  # 1 = right, 0 = left
    self.move_direction = 0 # the direction the entity is trying to move in.
    self.floor = 390 # y position of floor

    # state variables
    self.state = None  # set at end of __init__()
    self.last_change_state = 0 # the time of the last state change
    self.grounded = True  # whether entity is touching the ground

    # attack variables
    self.active_attack = False # whether attack hitbox should be active

    # auxiliary objects
    self.healthbar = Healthbar(self.parent, self)

    # initially start on idle state
    self.change_state("idle")


  # called once per tick
  def update(self, cur_time, offsetx):
    self.cur_time = cur_time
    
    self.handle_state()

    self.update_pos(offsetx)
    self.handle_gravity()

    if self.cur_time - self.last_animation > self.animation_cooldown and not self.animation_paused:
      self.animate()


  # updates position depending on velocity values
  # also checks for collision with tiles
  def update_pos(self, offsetx):
    self.update_posy(offsetx)
    self.update_posx(offsetx)


  def update_posy(self, offsetx):
    newy = self.pos[1] - self.vel_y
    new_bottomleft = (self.pos[0], newy)
    rect = self.get_rect(offsetx)  # rect of current pos of player
    nrect = self.get_rect(offsetx, new_bottomleft)  # rect of new position of player
    grounded = False
    ychanged = False

    tiles = self.get_nearby_tiles(self.get_center(), 3)
    tile_size = 32  # CHANGE TO VARIABLE
    for tile in tiles:
      if tile.type == 1:
        tile_rect = pg.Rect((tile.pos[0] - offsetx, tile.pos[1]), (tile_size, tile_size))
        if nrect.colliderect(tile_rect):
          if rect.bottom <= tile_rect.top:
            ychanged = True
            self.set_bottom(tile_rect.top)
            grounded = True
            if self.vel_y < 0:
              self.vel_y = 0
          elif rect.top >= tile_rect.bottom:
            ychanged = True
            self.set_bottom(tile_rect.bottom + rect.height)
            if self.vel_y > 0:
              self.vel_y = 0
    self.grounded = grounded
    if not ychanged:
      self.pos[1] = newy


  def update_posx(self, offsetx):
    newx = self.pos[0] + self.vel_x
    new_bottomleft = (newx, self.pos[1])
    rect = self.get_rect(offsetx)  # rect of current pos of player
    nrect = self.get_rect(offsetx, new_bottomleft)  # rect of new position of player
    x_changed = False

    tiles = self.get_nearby_tiles(self.get_center(), 3)
    tile_size = 32  # CHANGE TO VARIABLE
    for tile in tiles:
      if tile.type == 1:
        tile_rect = pg.Rect((tile.pos[0] - offsetx, tile.pos[1]), (tile_size, tile_size))
        if nrect.colliderect(tile_rect):
          if rect.left >= tile_rect.right:
            x_changed = True
            new_left = tile_rect.right+offsetx
            self.set_left(new_left)
            if self.vel_x < 0:
              self.vel_x = 0
          elif rect.right <= tile_rect.left:
            x_changed = True
            new_left = tile_rect.left - rect.width + offsetx
            self.set_left(new_left)
            if self.vel_x > 0:
              self.vel_x = 0
    if not x_changed:
      self.pos = [newx, self.pos[1]]
  

  # returns the rect of this entity
  # usually overridden by subclasses
  def get_rect(self):
    return self.rect
  

  # sets the left position of this entity
  # usually overridden by subclasses
  def set_left(self, left):
    self.pos[0] = left
  

  # sets the bottom position of this entity
  # usually overridden by subclasses
  def set_bottom(self, bottom):
    self.pos[1] = bottom


  # updates the rectangle depending on self.pos
  def update_rect(self, offsetx):
    self.rect.bottom = self.pos[1]
    self.rect.left = self.pos[0] - offsetx


  # changes state of entity
  def change_state(self, new_state):
    self.unpause_animation()
    self.active_attack = False
    self.state = new_state
    self.last_change_state = self.cur_time
    self.animation_step = 0
    self.animate()
        

  # sets the x velocity of the player depending on what direction they are trying to move in
  # actual change in position is controlled in update_pos() method
  def move(self):

    # if trying to move right, set velocity accordingly
    if self.move_direction == 1:
      self.vel_x = self.speed
      # change state to run if state is idle
      if self.state == "idle":
        self.change_state("run")
        
    # if trying to move left, set velocity accordingly
    elif self.move_direction == -1:
      self.vel_x = -self.speed
      # change state to run if state is idle
      if self.state == "idle":
        self.change_state("run")

    elif self.move_direction == 0:
      self.vel_x = 0
      if self.state == "run":
        self.change_state("idle")
    
    self.try_change_direction(self.move_direction)
        

  # if changing direction, immediately move to next animation step (so there is no apparent lag in changing directions)
  def try_change_direction(self, new_direction):
    if new_direction != 0:
      if self.direction == 0 and new_direction == 1:
        self.direction = 1
        self.animate()
      elif self.direction == 1 and new_direction == -1:
        self.direction = 0
        self.animate()


  # moves to next step in animation loop
  def animate(self):
    self.last_animation = self.cur_time
      
    if self.direction:
      self.image = self.animation_ref[self.state][0][self.animation_step%self.animation_ref[self.state][2]]
      self.mask = pg.mask.from_surface(self.image)
    else:
      self.image = self.animation_ref[self.state][1][self.animation_step%self.animation_ref[self.state][2]]
      self.mask = pg.mask.from_surface(self.image)
    self.animation_step += 1
    

  def jump(self):
    self.grounded = False
    self.vel_y = 14
    self.change_state("jump")

  def begin_attack(self):
    self.change_state("attack")
    self.vel_x = 0
    self.attack_sound_played = False

    # create hitbox for attack
    hitbox_y = self.pos[1] + self.image_length*0.2
    hitbox_width = self.image_length*0.3
    hitbox_height = self.image_length*0.5
    if self.direction:
      hitbox_x = self.pos[0] + self.image_length*0.5
    else:
      hitbox_x = self.pos[0] - self.image_length*0.35
      
    self.attack_hitbox = pg.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)


  # handle states
  def handle_state(self):
    if self.state == "dead":
      self.handle_dying()
    elif self.state == "hurt":
      self.handle_hurt()
    elif self.state == "attack":
      self.handle_attack()
    elif self.state == "jump":
      self.handle_jump()
    elif self.state == "fall":
      self.handle_fall()
    else:
      self.handle_idle()


  def handle_idle(self):
    self.move()


  def handle_jump(self):
    self.move()
    if self.grounded:
      self.change_state("idle")
    if self.animation_step >= self.animation_ref["jump"][2]:
      self.change_state("fall")

  
  def handle_fall(self):
    self.move()
    if self.grounded:
      self.change_state("idle")

      
  # handles when entity is in attack state
  def handle_attack(self):
    if self.animation_step > self.animation_ref["attack"][2]:
      self.change_state("idle")
      
    if self.animation_step in self.active_attack_frames:
      if not self.attack_sound_played:
        self.attack_sound.play()
        self.attack_sound_played = True
      self.active_attack = True
      
    else:
      self.active_attack = False


  # handles when entity is in hurt state
  def handle_hurt(self):
    if self.animation_step > self.animation_ref["hurt"][2]:
      self.change_state("idle")
    
    
  # handles when entity is in dying state
  def handle_dying(self):
    if self.animation_step > self.animation_ref["dead"][2]:
      self.kill()


  # handle falling, gravity
  def handle_gravity(self):
    self.vel_y -= 1
    if not self.grounded and (self.state == "idle" or self.state == "run"):
      self.change_state("fall")


  # processes when entity gets attacked
  def receive_attack(self, damage):
    if self.state != "hurt" and self.state != "dead":
      self.health -= damage
      self.vel_x = 0
      if self.health <= 0:
        self.death_sound.play()
        self.change_state("dead")
      else:
        self.hurt_sound.play()
        self.change_state("hurt")


  def pause_animation(self):
    self.animation_paused = True
    self.pause_time = self.cur_time


  def unpause_animation(self):
    self.animation_paused = False
    self.pause_time = None


  # checks if this entity collides with tile type given
  def collide_type(self, offsetx, type):
    rect = self.get_rect(offsetx)  # rect of current pos of player
    tiles = self.get_nearby_tiles(self.get_center(), 3)

    # try to treat type as a list of types
    try:
      for tile in tiles:
        if tile.type in type:
          if rect.colliderect(tile.get_rect(offsetx)):
            return tile
    except TypeError:  # type is a single type, not a list
      for tile in tiles:
        if tile.type == type:
          if rect.colliderect(tile.get_rect(offsetx)):
            return tile
    
    return None # no tile found

    
  


# healthbar that appears above entities
# healthbar is drawn on parent, but attached to entity
class Healthbar:
  def __init__(self, parent, entity, player=False):
    self.parent = parent
    self.entity = entity
    self.player = player

    self.size = (80, 4)
    self.font = pg.font.Font(None, 20)
    

  # draw healthbar+text
  def render(self):
    self.render_bar()
    self.render_text()


  # render the bar
  def render_bar(self):
    y_margin = 4
    self.pos = pg.Rect((0, 0), self.size)
    if not self.player:
      self.pos.centerx = self.entity.rect.centerx
    else:
      self.pos.centerx = self.entity.get_centerx(absolute=False)
      
    self.pos.bottom = self.entity.rect.top + y_margin

    # percentage that the healthbar is filled
    try:
      percent_filled = self.entity.health / self.entity.max_health
    except ZeroDivisionError:
      percent_filled = 0
      
    healthbar_width = self.size[0]*percent_filled
    healthbar_pos = self.pos.copy()
    healthbar_pos.width = healthbar_width
    
    pg.draw.rect(self.parent, "black", self.pos)
    pg.draw.rect(self.parent, "green", healthbar_pos)


  # render the health text
  def render_text(self):
    health = self.entity.health
    if health < 0:
      health = 0
    text_content = str(health)
    text = self.font.render(text_content, True, "black")
    text_pos = text.get_rect(centerx=self.pos.centerx, bottom=self.pos.top+3)
    
    self.parent.blit(text, text_pos)




class Player(Entity):
  def __init__(self, parent, resources, end_game, get_nearby_tiles):

    # callback method when player dies to end the game
    self.end_game = end_game

    # animation_ref contains a tuple for each state
    # format -> state: (image, reverse image, frames)
    self.animation_ref = {
      "idle": (resources["woodcutter_idle"], resources["woodcutter_idle_reverse"], 4),
      "run": (resources["woodcutter_run"], resources["woodcutter_run_reverse"], 6),
      "attack": (resources["woodcutter_attack"], resources["woodcutter_attack_reverse"], 6),
      "hurt": (resources["woodcutter_hurt"], resources["woodcutter_hurt_reverse"], 3),
      "dead": (resources["woodcutter_death"], resources["woodcutter_death_reverse"], 6),
      "jump": (resources["woodcutter_jump"], resources["woodcutter_jump_reverse"], 4),
      "fall": (resources["woodcutter_fall"], resources["woodcutter_fall_reverse"], 1)
    }

    init_pos = (100, 367)
    active_attack_frames = [3, 4]
    self.attack_recovery = 400 # time it takes to recover after finishing attack
    self.jump_count = 0
    self.jump_ability = 1  # how many jumps the player can make in the air
    self.jump_power = 12 # how high the player can jump in 1 jump
    super().__init__(parent, resources, init_pos, 100, 3, 4, active_attack_frames, get_nearby_tiles)
    
    self.healthbar = Healthbar(self.parent, self, player=True)

    # get sounds
    self.attack_sound = self.resources["axe1.mp3"]
    self.hurt_sound = resources["player_hurt.mp3"]
    self.death_sound = resources["game_over.mp3"]

    # DISTANCE CONSTANTS
    # distance from side of image to side of actual sprite
    # e.g., left is distance from left of image to where the the left side of the sprite starts
    self.dist_consts = {
      "left": 14,
      "bottom": 0,
      "right": -45,
      "top": 32,
      "left_to_centerx": 34
    }


  def update(self, cur_time, offsetx):
    super().update(cur_time, offsetx)
    if self.grounded:
      self.jump_count = 0

  
  # override entity.jump so player can double jump
  def jump(self):
    if self.jump_count <= self.jump_ability:
      self.grounded = False
      self.vel_y = self.jump_power
      self.jump_count += 1
      self.change_state("jump")


  # checks if direction changed, then acts accordingly
  # new_direction = -1 | 0 | 1  ->  left | none | right  
  def try_change_direction(self, new_direction):
    if new_direction != 0:
      if self.direction == 0 and new_direction == 1:
        self.direction = 1
        self.pos[0] += 27 # account for uncentered sprite
        self.animate()
      elif self.direction == 1 and new_direction == -1:
        self.direction = 0
        self.pos[0] -= 27 # account for uncentered sprite
        self.animate()


  # ends game when when death animation ends
  def handle_dying(self):
    if self.animation_step >= self.animation_ref["dead"][2]:
      self.end_game()


  # gets rect of the actual player rather than entire sprite (sprite is a huge rectangle)
  def get_rect(self, offsetx, bottomleft=None):
    # default bottomleft is self.pos
    if bottomleft == None:
      bottomleft = self.pos.copy()
    
    bottomleft = (bottomleft[0]-offsetx, bottomleft[1])

    # rect position is different depending on which way the player is facing
    if self.direction:
      rect_bottomleft = (bottomleft[0]+14, bottomleft[1]) # (x, y)
      rect_size = (36, 64)
      rect = pg.Rect((0, 0), rect_size)
      rect.bottomleft = rect_bottomleft
    else:
      rect_bottomleft = (bottomleft[0]+45, bottomleft[1]) # (x, y)
      rect_size = (36, 64)
      rect = pg.Rect((0, 0), rect_size)
      rect.bottomleft = rect_bottomleft
      

    return rect
    


  # the sprite is left aligned, so centerx is the x position of the actual player section of the image rather than the entire image
  # absolute=True means use absolute position to get the center
  # absolute=False means use position on screen to get the center
  # e.g., player may be at absolute position (500, 100), but they will always be at the center of the screen
  def get_centerx(self, absolute=True):
    if absolute:
      if self.direction:
        centerx = self.pos[0] + 34
      else:
        centerx = self.pos[0] + 62
    else:
      if self.direction:
        centerx = self.rect.x + 34
      else:
        centerx = self.rect.x + 62

    return centerx
  
  def get_centery(self):
    return self.pos[1] - 32
  
  def get_center(self):
    return (self.get_centerx(), self.get_centery())
  

  # set centerx of player
  # see get_centerx() for more details
  def set_centerx(self, posx):
    if self.direction:
      self.pos[0] = posx - 34
    else:
      self.pos[0] = posx - 62


  def set_left(self, left):
    if self.direction:
      self.pos[0] = left-14
    else:
      self.pos[0] = left-45
  

  # override handle attack so player can attack and move at the same time
  def handle_attack(self):
    super().handle_attack()
    self.move()
  


class Enemy(Entity):
  def __init__(self, parent, resources, init_pos, death_callback, difficulty, get_nearby_tiles):

    self.death_callback = death_callback
    
    # animation_ref contains a tuple for each state
    # format -> state: (image, reverse image, frames)
    self.animation_ref = {
      "idle": (resources["golem_idle"], resources["golem_idle_reverse"], 12),
      "run": (resources["golem_walk"], resources["golem_walk_reverse"], 18),
      "attack": (resources["golem_attack"], resources["golem_attack_reverse"], 12),
      "hurt": (resources["golem_hurt"], resources["golem_hurt_reverse"], 12),
      "dead": (resources["golem_death"], resources["golem_death_reverse"], 15)
    }
    self.animation_ref["fall"] = self.animation_ref["idle"]

    active_attack_frames = [7, 8, 9] # which frames in attack animation is the attack hitbox actually active
    self.attack_recovery = 800 # time it takes to recover after finishing attack
    # health changes depending on difficulty
    if difficulty == "easy":
      health = 2
    elif difficulty == "okay":
      health = 3
    if difficulty == "hard":
      health = 4
    super().__init__(parent, resources, init_pos, 50, health, 2, active_attack_frames, get_nearby_tiles)

    # load sounds
    self.attack_sound = resources["swing.mp3"]
    self.hurt_sound = resources["enemy_hurt.mp3"]
    self.death_sound = resources["enemy_hurt.mp3"]


  # called once per tick
  def update(self, cur_time, offsetx, player_centerx):
    self.player_centerx = player_centerx
    super().update(cur_time, offsetx)


  def handle_idle(self):
    super().handle_idle()

    centerx = self.pos[0] + self.image.get_width()/2  # centerx of self
    distance = self.player_centerx - centerx

    if abs(distance) < 40:
      self.begin_attack()
    else:
      self.move_to_player(distance)
  


  # gets rect of the actual enemy rather than entire sprite (sprite is a huge rectangle)
  def get_rect(self, offsetx, bottomleft=None):
    # default bottomleft is self.pos
    if bottomleft == None:
      bottomleft = self.pos.copy()
    
    # change bottomleft to screen-relative position rather than absolute position
    bottomleft = (bottomleft[0]-offsetx, bottomleft[1])

    rect_bottomleft = (bottomleft[0]+41, bottomleft[1]-4) # (x, y)
    rect_size = (26, 53)
    rect = pg.Rect((0, 0), rect_size)
    rect.bottomleft = rect_bottomleft
      

    return rect
  


  def get_center(self):
    return (self.pos[0]+54, self.pos[1]-34)
  

  def set_left(self, left):
    self.pos[0] = left-41


  def set_bottom(self, bottom):
    self.pos[1] = bottom+4




  # moves towards the player's location
  def move_to_player(self, distance):
    if distance > 1:
      self.move_direction = 1
    elif distance < -1:
      self.move_direction = -1
    else:
      self.move_direction = 0


  # called upon death
  def kill(self):
    self.death_callback()
    super().kill()

    