# MAIN FILE CONTROLLING HIGHER LEVEL FUNCTIONS
# Controls switching between game states and higher level functions (high score, difficulty, loading assets, etc.)

import pygame
pygame.init()

from . import resource_handler, data_handler
from .states import game, main_menu, difficulty_change, map_creator, map_selector



# called by start.py to start the program
def start():
  # Constants
  constants = {
    "SCREEN_SIZE": (600, 400),
    "TILE_SIZE": 32
  }

  Control(constants)
  

# This class controls the entire program.
class Control:
  def __init__(self, constants):
    pygame.display.set_caption("Dweller")
    self.constants = constants
    
    # Load resources and data
    self.resources = resource_handler.load_resources()
    self.datah = data_handler.DataHandler()  # data handler (loading, writing, etc.)
    if self.datah.load_data() == 1:  # load_data() returns 1 upon FileNotFoundError
      self.datah.create_default_data()
    
    # Variables
    self.state = None
    self.state_object = None
    self.high_score = 0
    self.difficulty = "easy"
    # difficulty = easy | okay | hard


    # Initialize PyGame Variables
    self.root = pygame.display.set_mode(self.constants["SCREEN_SIZE"])
    self.clock = pygame.time.Clock()

    # initally start on main menu
    self.load_main_menu() 
    
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
    self.state_object = main_menu.Main_Menu(self.root, self.resources, self.load_map_selector, self.load_difficulty_change, self.load_map_creator)
    
    if difficulty:
      self.difficulty = difficulty

    # update highscore if applicable
    if score:
      if score > self.high_score:
        self.high_score = score
  

  # loads game screen
  def load_game(self, map, score=None):
    # update highscore if applicable
    if score:
      if score > self.high_score:
        self.high_score = score
        
    self.state = "game"
    self.state_object = game.Game(self.root, self.resources, self.load_game, self.load_main_menu, self.high_score, self.difficulty, self.constants["TILE_SIZE"], map)


  # loads difficulty selection screen
  def load_difficulty_change(self):
    self.state = "difficulty_change"
    self.state_object = difficulty_change.Difficulty_Change(self.root, self.resources, self.load_main_menu, self.difficulty)
  

  # loads map creator
  def load_map_creator(self):
    self.state = "map_creator"
    self.state_object = map_creator.Map_Creator(self.root, self.resources, self.datah.data, self.constants["TILE_SIZE"], self.datah.save_map, self.load_main_menu)


  # loads map selector
  def load_map_selector(self):
    self.state = "map_selector"
    self.state_object = map_selector.MapSelector(self.root, self.resources, self.datah.data["maps"], self.load_main_menu, self.load_game)

