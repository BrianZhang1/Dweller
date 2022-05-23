import pygame

# healthbar that appears above entities
# healthbar is drawn on parent, but attached to entity
class Healthbar:
  def __init__(self, parent, entity, player=False):
    self.parent = parent
    self.entity = entity
    self.player = player

    self.size = (80, 4)
    self.font = pygame.font.Font(None, 20)
    

  # draw healthbar+text
  def render(self):
    self.render_bar()
    self.render_text()


  # render the bar
  def render_bar(self):
    y_margin = 4
    self.pos = pygame.Rect((0, 0), self.size)
    if not self.player:
      self.pos.centerx = self.entity.rect.centerx
    else:
      self.pos.centerx = self.entity.centerx
      
    self.pos.bottom = self.entity.rect.top + y_margin

    # percentage that the healthbar is filled
    try:
      percent_filled = self.entity.health / self.entity.max_health
    except ZeroDivisionError:
      percent_filled = 0
      
    healthbar_width = self.size[0]*percent_filled
    healthbar_pos = self.pos.copy()
    healthbar_pos.width = healthbar_width
    
    pygame.draw.rect(self.parent, "black", self.pos)
    pygame.draw.rect(self.parent, "green", healthbar_pos)


  # render the health text
  def render_text(self):
    health = self.entity.health
    if health < 0:
      health = 0
    text_content = str(health)
    text = self.font.render(text_content, True, "black")
    text_pos = text.get_rect(centerx=self.pos.centerx, bottom=self.pos.top+3)
    
    self.parent.blit(text, text_pos)