import pygame
from ..components import ui

# main menu screen
class Main_Menu:
  def __init__(self, parent, resources, load_map_selector, load_difficulty_change, load_map_creator):
    
    self.parent = parent
    self.resources = resources
    self.load_map_selector = load_map_selector
    self.load_difficulty_change = load_difficulty_change
    self.load_map_creator = load_map_creator

    self.screen_size = (parent.get_width(), parent.get_height())
    
    # images for buttons
    self.start_button_image = self.resources["start_button.png"]
    self.difficulty_button_image = self.resources["difficulty_button.png"]

    # set font
    self.font = pygame.font.SysFont("Arial", 18)
    
    self.buttons = []  # contains all buttons

    # position start button
    self.start_button = ui.Button(self.parent, self.resources["start_button.png"], (0, 0), self.load_map_selector)
    self.start_button.rect.centerx = self.screen_size[0]/2
    self.start_button.rect.top = 70
    self.buttons.append(self.start_button)

    # position change difficulty button
    self.difficulty_button = ui.Button(self.parent, self.resources["difficulty_button.png"], (0, 0), self.load_difficulty_change)
    self.difficulty_button.rect.centerx = self.screen_size[0]/2
    self.difficulty_button.rect.top = self.start_button.rect.bottom + 30
    self.buttons.append(self.difficulty_button)

    # create map creator button
    self.map_creator_button = ui.Button(self.parent, self.resources["map_creator_button.png"], (0, 0), self.load_map_creator)
    self.map_creator_button.rect.centerx = self.screen_size[0]/2
    self.map_creator_button.rect.top = self.difficulty_button.rect.bottom + 15
    self.buttons.append(self.map_creator_button)

    # reminder to turn on sound text
    sound_reminder_content = "Turn on sound for the best experience!"
    self.sound_reminder_text = self.font.render(sound_reminder_content, True, "black")
    self.sound_reminder_pos = self.sound_reminder_text.get_rect()
    self.sound_reminder_pos.centerx = self.screen_size[0]/2
    self.sound_reminder_pos.bottom = self.screen_size[1] - 30
    

  # called once per tick by main.py
  def update(self):
    self.handle_events()
    self.render()


    
  # handles events (mostly button press)
  def handle_events(self):
    # event handling
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        
      # handle clicks on buttons
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          for button in self.buttons:
            button.check_click(event.pos)
            

            
  # draws everything
  def render(self):
    self.parent.fill("burlywood1")
    for button in self.buttons:
      button.draw()
    self.parent.blit(self.sound_reminder_text, self.sound_reminder_pos)
    