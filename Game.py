import pygame
from Config import Config
from Tiles.TileMap import TileMap
from pygame.sprite import Group
from Tiles.Tile import Tile
from Characters.Player import Player
from Tiles.HardTile import HardTile

class Game:
    MAP_ARG = "tileMapsGroup"
    CUSTOM_EVENT_HANDLER_ARG = "customEventHandler"

    initialized = False
    pygameInitialized = False
    player = None
    map: Group = Group()
    screen = None
    eventHandler = None
    customMenuHandler = None

    @staticmethod
    def InitializePygame():
        pygame.init()
        Game.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        Game.pygameInitialized = True
        Config.InternalSetPyGame(pygame)

    @staticmethod
    def Initialize(**kwargs):
        if not Game.pygameInitialized:
            Game.InitializePygame()

        Config.Initialize(Game.screen)

        if kwargs.keys().__contains__(Game.CUSTOM_EVENT_HANDLER_ARG) and kwargs[Game.CUSTOM_EVENT_HANDLER_ARG] is not None:
            Game.eventHandler = kwargs[Game.CUSTOM_EVENT_HANDLER_ARG]

        if kwargs.keys().__contains__(Game.MAP_ARG) and kwargs[Game.MAP_ARG] is not None:
            Game.map = kwargs[Game.MAP_ARG]
        else:
            tileMap = TileMap()

            tileMap.AddTile(Tile(texture="fioor.png"), 2, 3)
            tileMap.AddTile(Tile(texture="fioor.png"), 3, 3)
            tileMap.AddTile(Tile(texture="fioor.png"), 3, 4)
            tileMap.AddTile(HardTile(texture="fioor.png"), 10, 4)
            tileMap.AddTile(HardTile(texture="fioor.png"), 10, 5)
            tileMap.AddTile(HardTile(texture="fioor.png"), 10, 6)

            Game.map.add(tileMap)

        # TODO - наверное, в генераторе лучше не проверять коллизии или вообще добавить какую-нибудь настройку
        Config.InternalSetTileMap(Game.map)

        Game.player = Player("images/traveler.png")


        Game.initialized = True

    @staticmethod
    def DrawObjects():
        for tileMap in Game.map.sprites():
            tileMap.blit()  # TODO - переделать на draw

        Game.player.blit()

    @staticmethod
    def UpdateObjects():
        for tileMap in Game.map.sprites():  # TODO - переделать на общий апдейт
            tileMap.update()

        Game.player.update()

    @staticmethod
    def HandleEvents():
        for event in pygame.event.get():
            # проверка нажатия
            if event.type == pygame.KEYDOWN:
                Game.player.moving(event.key, True)
            elif event.type == pygame.KEYUP:
                Game.player.moving(event.key, False)

            if Game.eventHandler is not None:
                Game.eventHandler(event)


    @staticmethod
    def Start():
        if not Game.initialized:
            Game.Initialize()

        while True:
            Game.screen.fill((33, 174, 233))
            Game.UpdateObjects()
            Game.DrawObjects()
            Game.HandleEvents()

            if Game.customMenuHandler is not None:
                Game.customMenuHandler()

            pygame.display.flip()


if __name__ == "__main__":
    Game.Start()