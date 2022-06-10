import pygame

class User_Interface:
  def __init__(self, parent, resources):
    self.parent = parent
    self.resources = resources

    self.centerx = self.parent.get_width()/2
    self.font1 = pygame.font.SysFont("dejavuserif", 50)
    self.font2 = pygame.font.SysFont("Arial", 25)
    
    # load resources into variables
    # Set resource variables from resources
    self.game_over_image = resources["game_over.png"]
    self.play_again_image = resources["play_again.png"]
    self.main_menu_image = resources["main_menu_button.png"]
    

  # processes clicks
  def process_click(self, pos):
    if self.play_again_pos.collidepoint(pos):
      return "start_new_game"
    elif self.main_menu_pos.collidepoint(pos):
      return "load_main_menu"
    else:
      return None


  # renders the score text
  def render_score(self, score):
    # create score/speed text objects
    score_text_content = "Score: " + str(score)
    score_text = self.font2.render(score_text_content, True, "black", "white")
    score_text_pos = score_text.get_rect()
    score_text_pos.right = self.parent.get_width() - 10
    score_text_pos.top = 10
    
    
    # draw objects
    self.parent.blit(score_text, score_text_pos)


  # must always be called before first call of render game over
  # positions everything
  def process_game_over(self, high_score):
    # position game_over/replay/high_score text
    self.game_over_pos = self.game_over_image.get_rect()
    self.game_over_pos.centerx = self.centerx
    self.game_over_pos.top = 100

    self.play_again_pos = self.play_again_image.get_rect()
    self.play_again_pos.centerx = self.centerx
    self.play_again_pos.top = 240

    self.main_menu_pos = self.main_menu_image.get_rect()
    self.main_menu_pos.centerx = self.centerx
    self.main_menu_pos.top = 310
    
    self.high_score_text = self.font2.render("High Score: " + str(high_score), True, "black", "white")
    self.high_score_pos = self.high_score_text.get_rect()
    self.high_score_pos.centerx = self.parent.get_width()/2
    self.high_score_pos.top = 200
    

  # draws everyting when game is over
  def render_game_over(self):
      self.parent.blit(self.game_over_image, self.game_over_pos)
      self.parent.blit(self.play_again_image, self.play_again_pos)
      self.parent.blit(self.main_menu_image, self.main_menu_pos)
      self.parent.blit(self.high_score_text, self.high_score_pos)
