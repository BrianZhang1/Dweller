import pygame

# controls the diffculty selection screen
class Difficulty_Change:
  def __init__(self, parent, resources, load_main_menu, difficulty):
    self.parent = parent
    self.resources = resources
    self.load_main_menu = load_main_menu

    self.screen_size = (parent.get_width(), parent.get_height())

    # assets for buttons
    self.easy_image = resources["easy.png"]
    self.okay_image = resources["okay.png"]
    self.hard_image = resources["hard.png"]


    # create current difficulty text
    self.font2 = pygame.font.SysFont("Arial", 25)
    self.cur_difficulty_content = "Current Difficulty: " + difficulty
    cur_difficulty_x = self.screen_size[0]/2 - self.font2.size(self.cur_difficulty_content)[0]/2
    cur_difficulty_y = 20
    self.cur_difficulty_pos = (cur_difficulty_x, cur_difficulty_y)
    self.cur_difficulty_text = self.font2.render(self.cur_difficulty_content, True, "black")
    
    # position buttons
    top_margin = 70
    y_between = 10  # length between buttons (vertically)
    button_height = self.easy_image.get_height()
    
    easy_x = self.screen_size[0]/2 - self.easy_image.get_width()/2
    easy_y = top_margin
    self.easy_pos = (easy_x, easy_y)
    self.easy_hitbox = self.easy_image.get_rect(topleft=self.easy_pos)

    okay_x = self.screen_size[0]/2 - self.okay_image.get_width()/2
    okay_y = easy_y + button_height + y_between
    self.okay_pos = (okay_x, okay_y)
    self.okay_hitbox = self.okay_image.get_rect(topleft=self.okay_pos)

    hard_x = self.screen_size[0]/2 - self.hard_image.get_width()/2
    hard_y = okay_y + button_height + y_between
    self.hard_pos = (hard_x, hard_y)
    self.hard_hitbox = self.hard_image.get_rect(topleft=self.hard_pos)


  # called once per tick by main.py
  def update(self):
    self.handle_events()
    self.render()


  # handles events (mostly button pressing)
  def handle_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()

      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          if self.easy_hitbox.collidepoint(event.pos):
            self.load_main_menu("easy")
          if self.okay_hitbox.collidepoint(event.pos):
            self.load_main_menu("okay")
          if self.hard_hitbox.collidepoint(event.pos):
            self.load_main_menu("hard")


  # draws everything on screen
  def render(self):
    self.parent.fill("burlywood1")
    self.parent.blit(self.cur_difficulty_text, self.cur_difficulty_pos)
    self.parent.blit(self.easy_image, self.easy_pos)
    self.parent.blit(self.okay_image, self.okay_pos)
    self.parent.blit(self.hard_image, self.hard_pos)
    