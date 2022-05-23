import pygame

# main menu screen
class Main_Menu:
  def __init__(self, parent, resources, load_game, load_difficulty_change):
    
    self.parent = parent
    self.resources = resources
    self.load_game = load_game
    self.load_difficulty_change = load_difficulty_change

    self.screen_size = (parent.get_width(), parent.get_height())
    
    self.start_button_image = self.resources["start_button.png"]
    self.difficulty_button_image = self.resources["difficulty_button.png"]

    self.font = pygame.font.SysFont("Arial", 18)
    
    # position start button
    start_button_x = self.screen_size[0]/2 - self.start_button_image.get_width()/2
    start_button_y = 80
    self.start_button_pos = (start_button_x, start_button_y)
    self.start_hitbox = self.start_button_image.get_rect(topleft=self.start_button_pos)

    # position change difficulty button
    difficulty_x = self.screen_size[0]/2 - self.difficulty_button_image.get_width()/2
    difficulty_y = start_button_y + self.start_button_image.get_height() + 30
    self.difficulty_pos = (difficulty_x, difficulty_y)
    self.difficulty_hitbox = self.difficulty_button_image.get_rect(topleft=self.difficulty_pos)

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
          if self.start_hitbox.collidepoint(event.pos):
            self.load_game()

          elif self.difficulty_hitbox.collidepoint(event.pos):
            self.load_difficulty_change()
            

            
  # draws everything
  def render(self):
    self.parent.fill("burlywood1")
    self.parent.blit(self.start_button_image, self.start_button_pos)
    self.parent.blit(self.difficulty_button_image, self.difficulty_pos)
    self.parent.blit(self.sound_reminder_text, self.sound_reminder_pos)
    