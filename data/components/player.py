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

    active_attack_frames = [3, 4]
    self.attack_recovery = 400 # time it takes to recover after finishing attack
    super().__init__(parent, resources, (100, 367), 100, 3, 4, 20, active_attack_frames)
    self.update_center()
    
    self.healthbar = healthbar.Healthbar(self.parent, self, player=True)

    # get sounds
    self.attack_sound = self.resources["axe1.mp3"]
    self.hurt_sound = resources["player_hurt.mp3"]
    self.death_sound = resources["game_over.mp3"]

    self.floor = 367 # y position of floor
    


  # called once per tick
  def update(self, cur_time):
    super().update(cur_time)

    self.update_center()
    
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
      
    # handle gravity
    self.vel_y -= 0.6
    if self.rect.bottom >= self.floor:
      self.vel_y = 0
      self.rect.bottom = self.floor
      self.grounded = True
    else:
      self.grounded = False
    if self.vel_y < 0 and (self.state == "idle" or self.state == "run"):
      self.change_state("fall")


  # ends game when when death animation ends
  def handle_dying(self):
    if self.animation_step >= self.animation_ref["dead"][2]:
      self.end_game()


  # the sprite is left aligned, so the self.centerx is the x position of the actual player section of the image rather than the entire image
  def update_center(self):
    if self.direction:
      self.centerx = self.rect.x + 33
    else:
      self.centerx = self.rect.x + 55

    
    
  