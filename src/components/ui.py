from turtle import up
import pygame as pg



# class for clickable Buttons. Onclick, they run the "command" argument, which is a function
class Button:
    def __init__(self, parent, image, init_pos, command):
        self.parent = parent
        self.image = image
        self.rect = self.image.get_rect(topleft=init_pos)
        self.command = command
        self.offset = (0, 0)  # screen offset
    

    # draw the button
    def draw(self, offset=(0, 0)):
        self.update_offset(offset)
        self.parent.blit(self.image, self.rect)
    

    # update rect depending on difference between new offset and current offset
    def update_offset(self, new_offset):
        self.rect.x += new_offset[0] - self.offset[0]
        self.rect.y += new_offset[1] - self.offset[1]
        self.offset = new_offset


    # runs command if this button is clicked
    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.command()
            return True
        return False



# class for textboxes where user can enter text
# tb is short for textbox
class Textbox:
    def __init__(self, parent, size, title=None, init_content=""):
        self.parent = parent
        self.rect = pg.Rect((0, 0), size)
        self.content = init_content  # content in the textbox
        self.title = title
        self.margin = 5


        # title and entry area take up 30 and 70 percent of total textbox height respectively
        self.title_font = pg.font.Font(None, int(size[1]*0.3))
        self.content_font = pg.font.Font(None, int(size[1]*0.7)-2*self.margin)
        self.tb_bg_color = (100, 100, 100)

        # Entry box (where text appears when user types)
        self.entry_color = (255, 255, 255)
        if title != None:
            self.title_text = self.title_font.render(title, True, "black")
            self.entry_rect = pg.Rect(0, 0, size[0]-2*self.margin, int(size[1]*0.7)-2*self.margin)  # entry box
        else:
            self.entry_rect = pg.Rect(0, 0, size[0]-2*self.margin, size[1]-2*self.margin)  # entry box
        
        # handling errors with input
        self.error = None  
        self.error_start_time = None
        self.error_duration = None
    

    # called once per tick
    # turns off error message after error_duration has passed
    def update(self):
        if self.error != None:
            cur_time = pg.time.get_ticks()
            if cur_time - self.error_start_time >= self.error_duration:
                self.end_error()


    # draw the textbox
    def draw(self):
        pg.draw.rect(self.parent, self.tb_bg_color, self.rect)
        pg.draw.rect(self.parent, self.entry_color, self.entry_rect)
        self.parent.blit(self.title_text, self.title_rect)
        self.draw_entry_text()
    

    # draw the entrybox and content
    def draw_entry_text(self):
        if self.error == None:
            text = self.content_font.render(self.content, True, "black")
        else:
            text = self.content_font.render(self.error, True, "red")
        text_rect = text.get_rect()
        text_rect.center = self.entry_rect.center
        self.parent.blit(text, text_rect)


    # update position of tb components
    def update_tb_pos(self):
        if self.title != None:
            self.title_rect = self.title_text.get_rect(centerx=self.rect.centerx, top=self.rect.top+self.margin)
            self.entry_rect.centerx = self.rect.centerx
            self.entry_rect.top = self.title_rect.bottom+5
        else:
            self.entry_rect.center = self.rect.center
    

    # sets an error in the textbox
    def set_error(self, error, duration):
        self.error = error
        self.error_start_time = pg.time.get_ticks()
        self.error_duration = duration
    

    # ends textbox error
    def end_error(self):
        self.error = None
        self.error_start_time = None
        self.error_duration = None


# has up and down arrow buttons that can increment or decrement a value
# position_components() method must be called after positioning this widget
class Incrementer:
    def __init__(self, parent, resources, buttons, title, callback, init_value):
        self.parent = parent
        self.resources = resources
        self.title = title
        self.callback = callback
        
        # font and positioning
        self.title_font = pg.font.SysFont("Arial", 15)
        self.value_font = pg.font.SysFont("Arial", 12)
        self.margin = 5  # pixel margin separating the components of this widget
        self.value = init_value  # value of this widget

        # creating buttons
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
    

    # sets the value for the incrementer
    def set_value(self, new_value):
        self.value = new_value
        self.value_text = self.value_font.render(str(self.value), True, "black")
        self.position_components()

    
    # draws the incrementer
    def draw(self):
        pg.draw.rect(self.parent, "lightblue", self.rect)
        self.parent.blit(self.title_text, self.title_rect)
        self.increase_width_button.draw()
        self.parent.blit(self.value_text, self.value_rect)
        self.decrease_width_button.draw()
