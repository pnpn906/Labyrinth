import pygame
from Config import Config

class PuzzleTileMap:
    def __init__(self, width = 40, height = 40):
        self.width = width
        self.height = height
        self.group = pygame.sprite.Group()

    def AddPuzzleTile(self, tile, x, y):
        x = x * self.width
        y = y * self.height
        tile.UpdateParams(width=self.width,
                          height=self.height,
                          x=x, y=y)
        self.group.add(tile)

    def RemoveTilePuzzleTile(self, x_abs, y_abs):
        x = x_abs * self.width
        y = y_abs * self.height

        for tile in self.group.copy():
            if tile.rect.left == x and tile.rect.top == y:
                self.group.remove(tile)

    def GetGroup(self):
        return self.group

    def blit(self):
        self.group.draw(Config.get_Screen())

    def update(self):
        self.group.update()