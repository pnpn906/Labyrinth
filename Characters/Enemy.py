import pygame.image
from Config import Config
from pygame.sprite import Sprite
import random
from Tiles.HardTile import HardTile

class Enemy(Sprite):
    def __init__(self, texture, x, y, speed=2):
        super().__init__()
        self.__image = pygame.image.load(texture).convert_alpha()
        self.__screen = Config.get_Screen()
        self.__tileMap = Config.get_Map()
        
        self.rect = self.__image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.direction = random.choice(['left', 'right'])
        self.movement_counter = 0
        self.max_movement = 100  # Количество пикселей для движения в одном направлении
        
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
        
        if self.direction == 'left':
            # Двигаемся влево
            self.rect.x -= self.speed
            # Проверяем коллизию
            if self.ColliedWithHardTile():
                self.rect.x = old_x
                self.direction = 'right'
                self.movement_counter = 0
            else:
                self.movement_counter += self.speed
        else:
            # Двигаемся вправо
            self.rect.x += self.speed
            # Проверяем коллизию
            if self.ColliedWithHardTile():
                self.rect.x = old_x
                self.direction = 'left'
                self.movement_counter = 0
            else:
                self.movement_counter += self.speed
            
        if self.movement_counter >= self.max_movement:
            self.direction = 'right' if self.direction == 'left' else 'left'
            self.movement_counter = 0

    def blit(self):
        self.__screen.blit(self.__image, self.rect)

if __name__ == "__main__":
    enemy = Enemy("../images/spider.png", 10, 10)