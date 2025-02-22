from pygame.sprite import Sprite
import pygame
class Level(Sprite):
    def __init__(self,lvl, player=None, map=None):
        super().__init__()
        self.player = player
        self.map = map
        self.lvl = lvl
        self.camera = None

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

            if self.camera is not None:
                self.camera.update(self.player)

    def camera_apply(self, obj):
        return self.camera.apply(obj)

    def blit(self):
        if self.map is not None:
            for tileMap in self.map.sprites():
                tileMap.blit(self.camera_apply)  # TODO - переделать на draw

        if self.player is not None:
            self.player.blit()