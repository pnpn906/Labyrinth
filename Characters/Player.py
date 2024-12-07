import pygame.image
from Config import Config
from pygame.sprite import Sprite

class Player(Sprite):
    def __init__(self, texture):
        super().__init__()
        self.__image = pygame.image.load(texture).convert_alpha()
        self.__screen = Config.get_Screen()

        self.__speed = 2

        self.__isLeft = False
        self.__isRight = False
        self.__isUp = False
        self.__isDown = False

        self.rect = self.__image.get_rect()

    def blit(self):
        self.__screen.blit(self.__image, self.rect)

    def update(self, *args, **kwargs):
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


    def moving(self, key, key_down=True):
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
                result = pg.sprite.spritecollideany(self, group)

                if result is not None:
                    print("Collided!")
                else:
                    print("Not collided")


                #for tileGroup in group.sprites():
                    #collision = pygame.sprite.spritecollideany(self, tileGroup)
                #    collision = self.rect.colliderect(tileGroup.rect)
                #    if collision:
                 #       print(collision)
                # Может быть несколько спрайтов в коллизии, проверяем каждый
                # нас интересуют только ХардТайлы
                # если хоть один хард тайл есть, то возвращаем тру


        return False

if __name__ == "__main__":
    player = Player("../images/traveler.png.png")