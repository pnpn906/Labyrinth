from pygame.sprite import Sprite
import pygame
class Level(Sprite):
    def __init__(self,lvl, player=None, map=None):
        super().__init__()
        self.player = player
        self.map = map
        self.lvl = lvl

    def handle_event(self, event):
        if self.player is not None:
            if event.type == pygame.KEYDOWN:
                self.player.moving(event.key, True)
            elif event.type == pygame.KEYUP:
                self.player.moving(event.key, False)

    def update(self, *args, **kwargs):
        if self.map is not None:
            for tileMap in self.map.sprites():  # TODO - переделать на общий апдейт
                tileMap.update()
        if self.player is not None:
            self.player.update()

    def blit(self):
        if self.map is not None:
            for tileMap in self.map.sprites():
                tileMap.blit()  # TODO - переделать на draw

        if self.player is not None:
            self.player.blit()