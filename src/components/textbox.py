import pygame as pg

# class for textboxes where user can enter text
# tb is short for textbox
class Textbox:
    def __init__(self, parent, size):
        self.parent = parent
        self.rect = pg.Rect((0, 0), size)
        self.content = "sample"  # content in the textbox

        self.tb_bg_color = (100, 100, 100)

        # Entry box (where text appears when user types)
        self.entry_color = (255, 255, 255)
        entry_margin = 5
        self.entry_rect = pg.Rect(0, 0, size[0]-2*entry_margin, size[1]-2*entry_margin)  # entry box
        self.font = pg.font.Font(None, size[1]-2*entry_margin)


    def draw(self):
        pg.draw.rect(self.parent, self.tb_bg_color, self.rect)
        pg.draw.rect(self.parent, self.entry_color, self.entry_rect)
        self.draw_entry_text()
    

    def draw_entry_text(self):
        text = self.font.render(self.content, True, "black")
        text_rect = text.get_rect()
        text_rect.center = self.entry_rect.center
        self.parent.blit(text, text_rect)


    def update_tb_pos(self):
        self.entry_rect.center = self.rect.center