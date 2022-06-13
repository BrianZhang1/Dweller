# MAIN FILE
# Controls switching between game states and higher level functions (high score, difficulty, loading assets, etc.)

import pygame
pygame.init()

from . import resource_handler, data_handler
from .states import game, main_menu, difficulty_change, map_creator



# called by start.py to start the program
def start():
  # Constants
  constants = {
    "TILE_SIZE": 32
  }
  Control(constants)
  

# This class controls the entire program.
class Control:
  def __init__(self, constants):
    self.constants = constants
    
    # Load resources and data
    self.resources = resource_handler.load_resources()
    self.data = data_handler.load_data(bg_size=(self.resources["bg.png"].get_size()), tile_size=self.constants["TILE_SIZE"])
    
    # Variables
    screen_size = (600, 400)
    self.state = None
    self.state_object = None
    self.high_score = 0
    self.difficulty = "easy"
    # difficulty = easy | okay | hard


    # Initialize PyGame Variables
    self.root = pygame.display.set_mode(screen_size)
    self.clock = pygame.time.Clock()

    self.load_main_menu() # initally start on main menu
    
    # starts game loop
    self.main()


  
  # This is the game loop.
  def main(self):
    while True:
      # update the current state object
      self.state_object.update()
    
      # update display and tick
      pygame.display.update()
      self.clock.tick(30)

      
  # loads main menu screen
  def load_main_menu(self, difficulty=None, score=None):
    self.state = "main_menu"
    self.state_object = main_menu.Main_Menu(self.root, self.resources, self.load_game, self.load_difficulty_change, self.load_map_creator)
    
    if difficulty:
      self.difficulty = difficulty

    # update highscore if applicable
    if score:
      if score > self.high_score:
        self.high_score = score
  

  # loads game screen
  def load_game(self, score=None):
    if score:
      if score > self.high_score:
        self.high_score = score
        
    self.state = "game"
    self.state_object = game.Game(self.root, self.resources, self.load_game, self.load_main_menu, self.high_score, self.difficulty, self.constants["TILE_SIZE"], self.data["maps"][1])


  # loads difficulty selection screen
  def load_difficulty_change(self):
    self.state = "difficulty_change"
    self.state_object = difficulty_change.Difficulty_Change(self.root, self.resources, self.load_main_menu, self.difficulty)
  

  def load_map_creator(self):
    self.state = "map_creator"
    self.state_object = map_creator.Map_Creator(self.root, self.resources, self.constants["TILE_SIZE"], self.data["maps"][0], data_handler.save_map)

