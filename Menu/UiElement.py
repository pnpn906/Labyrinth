import pygame
from pygame.sprite import Sprite
from Config import Config
class UIElement(Sprite):
    def __init__(self, width, height, color=(0,0,0), x=0,y=0):
        super().__init__()
        self.main_rect = pygame.rect.Rect(x, y, width, height)
        self.main_rect_color = color
        self.action = None

    def ChangeCoords(self, x_change, y_change):
        self.main_rect.x += x_change
        self.main_rect.y += y_change

        self.RebuildFromMain()

    def RebuildFromMain(self):
        pass

    def SetCoords(self, x, y):
        self.main_rect.x = x
        self.main_rect.y = y

        self.RebuildFromMain()

    def GetTop(self):
        return self.main_rect.top

    def GetBottom(self):
        return self.main_rect.bottom

    def GetRight(self):
        return self.main_rect.right

    def GetLeft(self):
        return self.main_rect.left

    def BindAction(self, action):
        self.action = action

    def Pressed(self):
        if self.action is not None:
            self.action()

    def CheckPressed(self, x, y):
        if self.main_rect.collidepoint(x,y):
            self.Pressed()

    def blit(self):
        pygame.draw.rect(Config.get_Screen(), self.main_rect_color, self.main_rect)

    def update(self, *args, **kwargs):
        pass

    def HandleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x,y = event.pos

            if self.CheckPressed(x,y):
                self.Pressed()
