
import pygame
from Config import Config
from UiElement import UIElement

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