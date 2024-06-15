
import pygame
from Config import Config
from UiElement import UIElement

class Text(UIElement):
    def __init__(self, text, size, color=(0,0,0), x=0,y = 0):
        super().__init__(0,0, color, x, y)

        self.font = pygame.font.SysFont("arial", size)
        self.btn_text = self.font.render(text, False, color)
        self.main_rect = self.btn_text.get_rect()

        self.main_rect.x = x
        self.main_rect.y = y

    def UpdateText(self, text):
        oldX = self.main_rect.x
        oldY = self.main_rect.y
        self.btn_text = self.font.render(text, False, self.main_rect_color)
        self.main_rect = self.btn_text.get_rect()

        self.main_rect.x = oldX
        self.main_rect.y = oldY

    def blit(self):
        Config.get_Screen().blit(self.btn_text, self.main_rect)

class SelectorListText(UIElement):
    def __init__(self, values:list, size, color=(0,0,0), x=0,y = 0, orientation="horizontal"):
        super().__init__(0, 0, x= x,y= y)
        self.ui_elements = pygame.sprite.Group()
        self.currentSelectedText = None

        if len(values) == 0:
            raise Exception("Values can not be empty.")

        for val in values:
            text = Text(val, size, color)
            self.ui_elements.add(text)

        # Orientation Block
        self.spacing = 30
        self.orientation = orientation  # не используется нигде, хотя должна

        if self.orientation == "horizontal":
            pass

    def blit(self):
        super().blit()

        for el in self.ui_elements.sprites():
            el.blit()

class Button(UIElement):
    def __init__(self,text, size, width, height, color=(0,0,0), x=0,y = 0):
        if size > width -5:
            width = size + 5

        if size > height -5:
            height = size + 5

        super().__init__(width, height, color, x,y)

        font = pygame.font.SysFont("arial", size)
        self.text = text
        self.btn_text = font.render(text, False, (0,0,0), self.main_rect_color)

        self.text_rect = self.btn_text.get_rect()
        self.RebuildFromMain()

    def RebuildFromMain(self):
        self.text_rect.center = self.main_rect.center
    def blit(self):
        super().blit()
        Config.get_Screen().blit(self.btn_text, self.text_rect)

