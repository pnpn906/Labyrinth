
import pygame
from Config import Config
from UiElements.UiElement import UIElement

class Text(UIElement):
    def __init__(self, text, size, color=(0,0,0), x=0,y = 0):
        super().__init__(0,0, color, x, y)

        self.font = pygame.font.SysFont("arial", size)
        self.btn_text = self.font.render(text, False, color)
        self.root_text = text
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

    def high_light(self, hight_light=True):
        self.font.set_underline(hight_light)
        self.UpdateText(self.root_text)
        self.font.set_underline(False)

        print("HIGHTLIE")

    def blit(self):
        Config.get_Screen().blit(self.btn_text, self.main_rect)


    def CheckPressed(self, x, y, **args):
        args["text"] = self.root_text
        return super().CheckPressed(x, y, **args)

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
        self.additionalArgs = {}
        self.text_rect = self.btn_text.get_rect()
        self.RebuildFromMain()

    def Pressed(self, **args):
        super().Pressed(sender=self, **args)

    def RebuildFromMain(self):
        self.text_rect.center = self.main_rect.center
    def blit(self):
        super().blit()
        Config.get_Screen().blit(self.btn_text, self.text_rect)

