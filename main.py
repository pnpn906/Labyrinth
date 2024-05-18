import pygame

import Characters.Enemy
from Tiles.TileMap import TileMap
from Tiles.Tile import Tile
import Characters.Player
from Config import Config

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
Config.Initialize(screen, None)
player = Characters.Player.Player("images/traveler.png")
tileMap = TileMap()
tileMap.AddTile(Tile(texture="fioor.png"), 2,3)
tileMap.AddTile(Tile(texture="fioor.png"), 3,3)
tileMap.AddTile(Tile(texture="fioor.png"), 3,4)

while True:
    screen.fill((33, 174, 233))

    for event in pygame.event.get():
        # проверка нажатия
        if event.type == pygame.KEYDOWN:
            player.moving(event.key, True)
        elif event.type == pygame.KEYUP:
            player.moving(event.key, False)

    tileMap.blit()
    player.update()
    player.blit()


    pygame.display.flip()