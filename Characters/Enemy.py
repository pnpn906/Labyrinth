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
    ShowDetection = True  # Флаг для отображения зоны обнаружения

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
        self.detected_player = False
        self.detection_area = None
        
    def check_player_detection(self):
        player = Config.get_Player()
        if player is None or not player.is_alive:
            return False
            
        # Создаем прямоугольник для проверки в направлении движения
        self.detection_area = self.rect.copy()
        check_distance = 100  # Дистанция проверки
        
        # Создаем прямоугольник, охватывающий всё пространство между врагом и точкой обнаружения
        if self.direction == Enemy.DIR_LEFT:
            self.detection_area.width += check_distance
            self.detection_area.left -= check_distance
        elif self.direction == Enemy.DIR_RIGHT:
            self.detection_area.width += check_distance
        elif self.direction == Enemy.DIR_UP:
            self.detection_area.height += check_distance
            self.detection_area.top -= check_distance
        else:  # DIR_DOWN
            self.detection_area.height += check_distance
            
        # Проверяем, находится ли игрок в зоне обнаружения
        return self.detection_area.colliderect(player.rect)
        
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
        
        # Проверяем обнаружение игрока
        was_detected = self.detected_player
        self.detected_player = self.check_player_detection()
        
        # Выводим сообщение только при изменении состояния обнаружения
        if self.detected_player and not was_detected:
            print(f"DETECTED! Enemy at ({self.rect.x}, {self.rect.y})")
        elif not self.detected_player and was_detected:
            print("Player lost from sight")
        
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
        # Отрисовка зоны обнаружения
        if Enemy.ShowDetection and self.detection_area is not None:
            surface = pygame.Surface((self.detection_area.width, self.detection_area.height), pygame.SRCALPHA)
            pygame.draw.rect(surface, (255, 0, 0, 50), surface.get_rect())
            self.__screen.blit(surface, self.detection_area)
        
        # Отрисовка самого врага
        self.__screen.blit(self.__image, self.rect)

if __name__ == "__main__":
    enemy = Enemy("../images/spider.png", 90, 90)