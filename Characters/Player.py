import pygame.image
from Config import Config
from pygame.sprite import Sprite
from Tiles.HardTile import HardTile

class Player(Sprite):
    def __init__(self, texture):
        super().__init__()
        self.__image = pygame.image.load(texture).convert_alpha()
        self.__image = pygame.transform.scale(self.__image, (20,20))

        self.__screen = Config.get_Screen()

        self.__speed = 2

        self.__isLeft = False
        self.__isRight = False
        self.__isUp = False
        self.__isDown = False

        self.rect = self.__image.get_rect()
        self.is_alive = True

    def blit(self):
        if self.is_alive:
            self.__screen.blit(self.__image, self.rect)

    def update(self, *args, **kwargs):
        if not self.is_alive:
            return

        if self.__isUp:
            self.rect.y -= self.__speed
        if self.__isDown:
            self.rect.y += self.__speed
        if self.__isRight:
            self.rect.x += self.__speed
        if self.__isLeft:
            self.rect.x -= self.__speed

        collided = self.ColliedWithHardTile()

        if collided:
            if self.__isUp:
                self.rect.y += self.__speed
            if self.__isDown:
                self.rect.y -= self.__speed
            if self.__isRight:
                self.rect.x -= self.__speed
            if self.__isLeft:
                self.rect.x += self.__speed

        if self.ColliedWithEnemy():
            self.is_alive = False

    def moving(self, key, key_down=True):
        if not self.is_alive:
            return
            
        if key == pygame.K_a:
            self.__isLeft = key_down
        elif key == pygame.K_d:
            self.__isRight = key_down
        elif key == pygame.K_w:
            self.__isUp = key_down
        elif key == pygame.K_s:
            self.__isDown = key_down

    def ColliedWithHardTile(self):
        map = Config.get_Map()

        if map is not None:
            for tileMap in map.sprites():
                group = tileMap.group
                pg = Config.get_pygame()

                for tile in group.sprites():
                    if isinstance(tile, HardTile):
                        if self.rect.colliderect(tile.rect):
                            return True

        return False

    def ColliedWithEnemy(self):
        from Game import Game
        for enemy in Game.enemies:
            if self.rect.colliderect(enemy.rect):
                return True
        return False

if __name__ == "__main__":
    player = Player("../images/traveler.png.png")