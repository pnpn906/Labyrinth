import pygame
from Config import Config
from Tiles.TileMap import TileMap
from pygame.sprite import Group
from Tiles.Tile import Tile
from Characters.Player import Player
from Tiles.HardTile import HardTile
from UiElements.Menu import Menu
from UiElements.Button import Button

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
    mainMenu = None
    levelsMenu = None

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

        # Main menu

        menu = Menu("MAIN MENU", Game.screen.get_width(), Game.screen.get_height(), (60, 60, 60), 0, 0, alignment="center")

        btn1 = Button("продолжить", 20, 470, 40, (243, 243, 223))
        btn2 = Button("новая игра", 20, 470, 40, (243, 243, 223))
        btn3 = Button("выбор уровня", 20, 470, 40, (243, 243, 223))
        btn4 = Button("выход", 20, 470, 40, (243, 243, 223))


        menu.AddUiElemnt(btn1)
        menu.AddUiElemnt(btn2)
        menu.AddUiElemnt(btn3)
        menu.AddUiElemnt(btn4)

        Game.mainMenu = menu

        Game.initialized = True

    @staticmethod
    def DrawObjects():
        for tileMap in Game.map.sprites():
            tileMap.blit()  # TODO - переделать на draw

        Game.player.blit()

        Game.mainMenu.blit()

    @staticmethod
    def UpdateObjects():
        for tileMap in Game.map.sprites():  # TODO - переделать на общий апдейт
            tileMap.update()

        Game.player.update()

        Game.mainMenu.update()

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