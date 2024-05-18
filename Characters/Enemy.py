import pygame.image
from Config import Config
from pygame.sprite import Sprite

class Enemy(Sprite):
    def __init__(self, texture):
        super().__init__()
        self.__image = pygame.image.load(texture).convert_alpha()
        self.__screen = Config.get_Screen()
        self.__tileMap = Config.get_Map()

        self.rect = self.__image.get_rect()

    def blit(self):
        self.__screen.blit(self.__image, self.rect)

if __name__ == "__main__":
    enemy = Enemy("../images/spider.png.png")