import pygame
from ..components.button import Button

# main menu screen
class Main_Menu:
  def __init__(self, parent, resources, load_game, load_difficulty_change, load_map_creator):
    
    self.parent = parent
    self.resources = resources
    self.load_game = load_game
    self.load_difficulty_change = load_difficulty_change
    self.load_map_creator = load_map_creator

    self.screen_size = (parent.get_width(), parent.get_height())
    
    self.start_button_image = self.resources["start_button.png"]
    self.difficulty_button_image = self.resources["difficulty_button.png"]

    self.font = pygame.font.SysFont("Arial", 18)
    
    self.buttons = []
    # position start button
    self.start_button = Button(self.parent, self.resources["start_button.png"], (0, 0), self.load_game)
    self.start_button.rect.centerx = self.screen_size[0]/2
    self.start_button.rect.top = 80
    self.buttons.append(self.start_button)

    # position change difficulty button
    self.difficulty_button = Button(self.parent, self.resources["difficulty_button.png"], (0, 0), self.load_map_creator)
    self.difficulty_button.rect.centerx = self.screen_size[0]/2
    self.difficulty_button.rect.top = self.start_button.rect.bottom + 30
    self.buttons.append(self.difficulty_button)

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
        
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          for button in self.buttons:
            button.check_click(event.pos)
            

            
  # draws everything
  def render(self):
    self.parent.fill("burlywood1")
    for button in self.buttons:
      button.draw()
    