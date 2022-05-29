import pygame as pg
from . import entity

class Enemy(entity.Entity):
  def __init__(self, parent, resources, init_pos, death_callback, difficulty):

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
    super().__init__(parent, resources, init_pos, 50, health, 2, active_attack_frames)

    # load sounds
    self.attack_sound = resources["swing.mp3"]
    self.hurt_sound = resources["enemy_hurt.mp3"]
    self.death_sound = resources["enemy_hurt.mp3"]


  # called once per tick
  def update(self, cur_time, player_centerx):
    self.player_centerx = player_centerx
    super().update(cur_time)


  def handle_idle(self):
    super().handle_idle()

    centerx = self.pos[0] + self.image.get_width()/2  # centerx of self
    distance = self.player_centerx - centerx

    if abs(distance) < 40:
      self.begin_attack()
    else:
      self.move_to_player(distance)



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

    