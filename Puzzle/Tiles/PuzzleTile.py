import pygame
from Config import Config
from pygame.sprite import Sprite

class Tile(Sprite):
    def __init__(self, texture,width,height,x,y):
        super().__init__()
        self.__screen = Config.__screen
        self.texture = texture
        self.image = self.LoadImage(texture,width,height)
        self.rect = self.image.get_rect()
        self.Pos(x, y)

    def Pos(self,x,y):
        self.rect.left = x
        self.rect.top = y

    def Blitme(self):
       Config.get_Screen().blit(self.image,self.rect)

    def update(self):
        pass

    def LoadImage(self, texture, width, height):
        image = pygame.image.load(f"Images/{texture}").convert_alpha()
        image = pygame.transform.scale(image, (width, height))
        return image