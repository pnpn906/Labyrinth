import pygame.image
from Config import Config
from pygame.sprite import Sprite
import random
from Tiles.HardTile import HardTile

class Enemy(Sprite):
    DIR_UP = 'up'
    DIR_DOWN = 'down'
    DIR_LEFT = 'left'
    DIR_RIGHT = 'right'

    DIRECTIONS = [DIR_UP, DIR_RIGHT, DIR_LEFT, DIR_DOWN]

    def __init__(self, texture, x, y, speed=1):
        super().__init__()
        self.__image = pygame.image.load(texture).convert_alpha()
        self.__screen = Config.get_Screen()
        self.__tileMap = Config.get_Map()
        
        self.rect = self.__image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.direction = random.choice(Enemy.DIRECTIONS)
        
    def ColliedWithHardTile(self):
        map = Config.get_Map()

        if map is not None:
            for tileMap in map.sprites():
                group = tileMap.group

                for tile in group.sprites():
                    if isinstance(tile, HardTile):
                        if self.rect.colliderect(tile.rect):
                            return True
        return False
        
    def update(self):
        # Сохраняем предыдущую позицию
        old_x = self.rect.x
        old_y = self.rect.y
        
        if self.direction == Enemy.DIR_LEFT:
            # Двигаемся влево
            self.rect.x -= self.speed
            # Проверяем коллизию
            if self.ColliedWithHardTile():
                self.rect.x = old_x
                self.direction =  random.choice(Enemy.DIRECTIONS)

        elif self.direction == Enemy.DIR_RIGHT:
            # Двигаемся вправо
            self.rect.x += self.speed
            # Проверяем коллизию
            if self.ColliedWithHardTile():
                self.rect.x = old_x
                self.direction =  random.choice(Enemy.DIRECTIONS)

        elif self.direction == Enemy.DIR_UP:
            # Двигаемся вверх
            self.rect.y -= self.speed
            # Проверяем коллизию
            if self.ColliedWithHardTile():
                self.rect.y = old_y
                self.direction =  random.choice(Enemy.DIRECTIONS)

        else:   # down
            # Двигаемся вниз
            self.rect.y += self.speed
            # Проверяем коллизию
            if self.ColliedWithHardTile():
                self.rect.y = old_y
                self.direction =  random.choice(Enemy.DIRECTIONS)


            


    def blit(self):
        self.__screen.blit(self.__image, self.rect)

if __name__ == "__main__":
    enemy = Enemy("../images/spider.png", 90, 90)