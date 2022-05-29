import pygame as pg

from . import entity, healthbar

class Player(entity.Entity):
  def __init__(self, parent, resources, end_game):

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
    super().__init__(parent, resources, init_pos, 100, 3, 4, active_attack_frames)
    
    self.healthbar = healthbar.Healthbar(self.parent, self, player=True)

    # get sounds
    self.attack_sound = self.resources["axe1.mp3"]
    self.hurt_sound = resources["player_hurt.mp3"]
    self.death_sound = resources["game_over.mp3"]



  # same as Entity.move, except it accounts for offset when flipping the image (since the player is not centered in the image)
  def move(self):
    # change state to run if state is idle
    if self.state == "idle":
      self.change_state("run")

    # if trying to move right, set velocity accordingly
    if self.move_direction == 1:
      self.vel_x = self.speed
      # if changing direction from right to left,
      if self.direction == 0:
        self.direction = 1
        self.pos[0] += 27 # account for uncentered sprite
        self.animate()
        
    # if trying to move left, set velocity accordingly
    elif self.move_direction == -1:
      self.vel_x = -self.speed
      if self.direction == 1:
        self.direction = 0
        self.pos[0] -= 27 # account for uncentered sprite
        self.animate()


  # ends game when when death animation ends
  def handle_dying(self):
    if self.animation_step >= self.animation_ref["dead"][2]:
      self.end_game()


  # the sprite is left aligned, so centerx is the x position of the actual player section of the image rather than the entire image
  # absolute=True means use absolute position to get the center
  # absolute=False means use position on screen to get the center
  # e.g., player may be at absolute position (500, 100), but they will always be at the center of the screen
  def get_centerx(self, absolute=True):
    if absolute:
      if self.direction:
        centerx = self.pos[0] + 33
      else:
        centerx = self.pos[0] + 62
    else:
      if self.direction:
        centerx = self.rect.x + 33
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
      self.pos[0] = posx - 33
    else:
      self.pos[0] = posx - 62



    
    
  