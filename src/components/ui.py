from turtle import up
import pygame as pg



# class for clickable Buttons. Onclick, they run the "command" argument, which is a function
class Button:
    def __init__(self, parent, image, init_pos, command):
        self.parent = parent
        self.image = image
        self.rect = self.image.get_rect(topleft=init_pos)
        self.command = command
    

    def draw(self):
        self.parent.blit(self.image, self.rect)


    # runs command if this button is clicked
    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.command()
            return True
        return False



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


# has up and down arrow buttons that can increment or decrement a value
# position_components() method must be called after positioning this widget
class Incrementer:
    def __init__(self, parent, resources, buttons, title, callback, init_value):
        self.parent = parent
        self.resources = resources
        self.title = title
        self.callback = callback
        
        self.title_font = pg.font.SysFont("Arial", 15)
        self.value_font = pg.font.SysFont("Arial", 12)
        self.margin = 5  # pixel margin separating the components of this widget
        self.value = init_value  # value of this widget

        self.title_text = self.title_font.render(str(title), True, "black")
        self.increase_width_button = Button(self.parent, self.resources["arrow_up.png"], (0, 0), lambda: self.callback(1))
        self.value_text = self.value_font.render(str(self.value), True, "black")
        self.decrease_width_button = Button(self.parent, self.resources["arrow_down.png"], (0, 0), lambda: self.callback(-1))
        buttons.append(self.increase_width_button)
        buttons.append(self.decrease_width_button)

        rect_width = max(self.title_text.get_width(), self.increase_width_button.rect.height, self.value_text.get_width(), self.decrease_width_button.rect.height)
        rect_width += 2*self.margin
        rect_height = self.title_text.get_height() + self.increase_width_button.rect.height + self.value_text.get_height() + self.decrease_width_button.rect.height + self.margin*5
        self.rect = pg.Rect(0, 0, rect_width, rect_height)

    
    # positions the rect of all components after self.rect is set
    def position_components(self):
        title_pos = (self.rect.left + 5, self.rect.top + 5)
        self.title_rect = self.title_text.get_rect(topleft=title_pos)

        self.increase_width_button.rect.centerx = self.title_rect.centerx
        self.increase_width_button.rect.top = self.title_rect.bottom + 5

        self.value_rect = self.value_text.get_rect(centerx=self.title_rect.centerx, top=self.increase_width_button.rect.bottom + 5)

        self.decrease_width_button.rect.centerx = self.title_rect.centerx
        self.decrease_width_button.rect.top = self.value_rect.bottom + 5
    

    def set_value(self, new_value):
        self.value = new_value
        self.value_text = self.value_font.render(str(self.value), True, "black")
        self.position_components()

    
    def draw(self):
        pg.draw.rect(self.parent, "lightblue", self.rect)
        self.parent.blit(self.title_text, self.title_rect)
        self.increase_width_button.draw()
        self.parent.blit(self.value_text, self.value_rect)
        self.decrease_width_button.draw()
