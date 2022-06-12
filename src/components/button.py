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