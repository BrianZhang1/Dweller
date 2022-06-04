import pygame as pg

from . import entity, healthbar

class Player(entity.Entity):
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
    super().__init__(parent, resources, init_pos, 100, 3, 4, active_attack_frames, get_nearby_tiles)
    
    self.healthbar = healthbar.Healthbar(self.parent, self, player=True)

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



  # same as Entity.move, except it accounts for offset when flipping the image (since the player is not centered in the image)
  

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


  # gets rect of the actual player
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


  def set_bottom(self, bottom):
    self.pos[1] = bottom


  def set_left(self, left):
    if self.direction:
      self.pos[0] = left-14
    else:
      self.pos[0] = left-45
    


  # FIX WALL CLIMBING
  def update_pos(self, offsetx):
    newx = self.pos[0] + self.vel_x
    newy = self.pos[1] - self.vel_y
    new_bottomleft = (newx, newy)
    rect = self.get_rect(offsetx)
    new_rect = self.get_rect(offsetx, new_bottomleft)
    grounded = False
    x_changed = False

    tiles = self.get_nearby_tiles(self.get_center(), 3)
    tile_size = 32  # CHANGE TO VARIABLE
    for tile in tiles:
      if tile.type == 1:
        tile_rect = pg.Rect((tile.pos[0] - offsetx, tile.pos[1]), (tile_size, tile_size))
        if new_rect.colliderect(tile_rect):
          if rect.bottom <= tile_rect.top:
            print("yyy")
            newy = tile_rect.top
            grounded = True
            if self.vel_y < 0:
              self.vel_y = 0
          elif rect.top >= tile_rect.bottom:
            newy = tile_rect.bottom + rect.height
            if self.vel_y > 0:
              self.vel_y = 0
          elif rect.left >= tile_rect.right:
            print("xxx")
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
    self.grounded = grounded
    if x_changed:
      self.pos[1] = newy
    else:
      self.pos = [newx, newy]
      