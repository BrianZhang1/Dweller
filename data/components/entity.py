# base class for Enemy and Player
# controls basic functions
# see enemy.py and player.py

import pygame as pg
from . import healthbar

# objects that inherit from Entity MUST have a self.animation_ref dictionary containing all assets for animation before calling __init__ method of the Entity class
class Entity(pg.sprite.Sprite):
  def __init__(self, parent, resources, init_pos, animation_cooldown, health, speed, direction_offset, active_attack_frames):
    super().__init__()
    self.cur_time = pg.time.get_ticks()
    
    self.parent = parent
    self.resources = resources
    self.max_health = health
    self.health = health
    self.speed = speed
    self.direction_offset = direction_offset
    self.active_attack_frames = active_attack_frames

    self.pos = list(init_pos)

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
    self.move_direction = 0 # the direction the player is trying to move in.
    self.floor = 367 # y position of floor

    # state variables
    self.state = None  # set at end of __init__()
    self.last_change_state = 0 # the time of the last state change
    self.grounded = True  # whether entity is touching the ground

    # attack variables
    self.active_attack = False # whether attack hitbox should be active

    # auxiliary objects
    self.healthbar = healthbar.Healthbar(self.parent, self)

    # initially start on idle state
    self.change_state("idle")




  # called once per tick
  def update(self, cur_time):
    self.cur_time = cur_time
    
    self.handle_state()

    self.update_pos()
    self.handle_gravity()

    if self.cur_time - self.last_animation > self.animation_cooldown and not self.animation_paused:
      self.animate()




  # updates position depending on velocity values
  def update_pos(self):
    self.pos[0] += self.vel_x
    self.pos[1] -= self.vel_y
    
  


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
    # change state to run if state is idle
    if self.state == "idle":
      self.change_state("run")

    # if trying to move right, set velocity accordingly
    if self.move_direction == 1:
      self.vel_x = self.speed
      # if changing direction from right to left,
      if self.direction == 0:
        self.direction = 1
        self.pos[0] += self.direction_offset
        self.animate()
        
    # if trying to move left, set velocity accordingly
    elif self.move_direction == -1:
      self.vel_x = -self.speed
      if self.direction == 1:
        self.direction = 0
        self.pos[0] -= self.direction_offset
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
    if self.state == "idle" or self.state == "run":
      self.vel_y = 12
      self.change_state("jump")




  def handle_jump(self):
    if self.animation_step >= self.animation_ref["jump"][2]:
      self.change_state("fall")




  def handle_fall(self):
    if self.grounded:
      self.change_state("idle")




  def begin_attack(self):
    if self.state == "idle" or self.state == "run":
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
    if self.move_direction != 0:
      self.move()
    else:
      self.vel_x = 0
      if self.state == "run":
        self.change_state("idle")




  # handles when entity is in attack state
  def handle_attack(self):
    if self.animation_paused:
      if self.cur_time - self.pause_time > self.attack_recovery:
        self.unpause_animation()
        self.animate()
    else:
      if self.animation_step == self.animation_ref["attack"][2]-1:
        self.pause_animation()
      elif self.animation_step > self.animation_ref["attack"][2]:
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
    if self.pos[1] > self.floor:
      self.vel_y = 0
      self.pos[1] = self.floor
      self.grounded = True
    elif self.pos[1] < self.floor:
      self.vel_y -= 1
      self.grounded = False
    else:
      self.grounded = True

    if self.vel_y < 0 and (self.state == "idle" or self.state == "run"):
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
    
