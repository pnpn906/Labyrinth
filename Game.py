import pygame
import sys
import LevelLoader
from Config import Config
from Tiles.TileMap import TileMap
from pygame.sprite import Group
from pygame.rect import Rect
from Tiles.Tile import Tile
from Characters.Player import Player
from Characters.Enemy import Enemy
from Tiles.HardTile import HardTile
from UiElements.Menu import Menu
from UiElements.PagedMenu import PagedMenu
from UiElements.Button import Button
from Levels.Level import Level
from camera import Camera

class Game:
    LEVEL_ARG = "levelArg"
    CUSTOM_EVENT_HANDLER_ARG = "customEventHandler"
    showMenu = True
    initialized = False
    pygameInitialized = False
    screen = None
    player = None
    eventHandler = None
    customMenuHandler = None
    currentMenu : PagedMenu = None
    inGameMenu: PagedMenu = None
    mainMenu: PagedMenu = None
    levelsMenu = None
    currentLevel : Level = None
    camera : Camera = None
    enemies : Group = Group()

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

        if kwargs.keys().__contains__(Game.LEVEL_ARG) and kwargs[Game.LEVEL_ARG] is not None:
            Game.__set_current_level(kwargs[Game.LEVEL_ARG])
        else:   
            Game.__set_current_level(Level(0))

        Game.player = Player("images/traveler.png")
        Game.currentLevel.player = Game.player
        Config.InternalSetPlayer(Game.player)

        # Создаем тестового врага
        enemy = Enemy("images/spider.png", 283, 200)
        Game.enemies.add(enemy)

        total_level_width = 50
        total_level_height = 50
        camera = Camera(Game.camera_configure, total_level_width, total_level_height)
        Game.currentLevel.camera = camera
        Game.camera = camera

        Game.showMenu = kwargs.get("showMenu", True)

        if Game.showMenu:

            # Menu in level

            inGameMenu = Menu("IN GAME MENU", Game.screen.get_width(), Game.screen.get_height(), (60, 60, 60), 0, 0, alignment="center")

            btn1 = Button("вернуться в главное меню", 20, 470, 40, (243, 243, 223))
            btn1.BindAction(Game.SubstitutionMenu)
            btn2 = Button("продолжить игру", 20, 470, 40, (243, 243, 223))
            btn2.BindAction(Game.GoToGameFromMenu)

            inGameMenu.AddUiElemnt(btn1)
            inGameMenu.AddUiElemnt(btn2)

            Game.inGameMenu = PagedMenu(inGameMenu)

            # Main menu

            menu = Menu("MAIN MENU", Game.screen.get_width(), Game.screen.get_height(), (60, 60, 60), 0, 0, alignment="center")

            btn1 = Button("продолжить", 20, 470, 40, (243, 243, 223))
            btn2 = Button("новая игра", 20, 470, 40, (243, 243, 223))
            btn3 = Button("выбор уровня", 20, 470, 40, (243, 243, 223))
            btn4 = Button("выход", 20, 470, 40, (243, 243, 223))

            btn4.BindAction(Game.Quit)

            menu.AddUiElemnt(btn1)
            menu.AddUiElemnt(btn2)
            menu.AddUiElemnt(btn3)
            menu.AddUiElemnt(btn4)

            menuLvl = Menu("LEVEL MENU", Game.screen.get_width(), Game.screen.get_height(), (60, 60, 60), 0, 0, alignment="center")
            menuLvlBtns = Menu("", Game.screen.get_width() - 100, Game.screen.get_height() - 200, (60,60,60), 0, 0, orientation="horizontal")
            menuLvl.AddUiElemnt(menuLvlBtns)

            # Вытащить из директории все файлы - это уровни

            # Пройти все файлы

            # Для каждого создать кнопку

            # Подгрузить через левел лоадер

            # Сделать бинд на кнопку, чтобы проставлялся текущий уровень при нажатии

            listOfLevels = LevelLoader.LevelLoader.GetListOfLevelMaps()
            for i in range(len(listOfLevels)):
                btnLvl = Button(f"{i+1}", 30, 119, 119, (243, 243, 223))
                btnLvl.BindAction(Game.LevelChoosed_Action)
                btnLvl.additionalArgs["filePath"] = listOfLevels[i]
                menuLvlBtns.AddUiElemnt(btnLvl)

            btnBackToMainMenu = Button("Back", 20, 470, 40, (243, 243, 223))

            menuLvl.AddUiElemnt(btnBackToMainMenu)

            Game.mainMenu =  PagedMenu(menu, menuLvl, back_bind = [btnBackToMainMenu], next_bind = [btn3])
            Game.currentMenu =  Game.mainMenu

        Game.initialized = True

    @staticmethod
    def LevelChoosed_Action(**kwargs):
        # TODO - level loader problem
        sender = kwargs.get("sender", None)

        if isinstance(sender, Button):
            filePath = sender.additionalArgs.get("filePath")
            if filePath is not None:
                Game.__set_current_level(LevelLoader.LevelLoader.LoadLevel(filePath, "Maps/" + filePath, Game.player, Game.enemies))
                Game.showMenu = False

    @staticmethod
    def SubstitutionMenu(**kwargs):
        Game.currentMenu = Game.mainMenu
        Game.currentLevel = Level(0)

    @staticmethod
    def GoToGameFromMenu(**kwargs):
        Game.showMenu = False

    @staticmethod
    def __set_current_level(level : Level):
        Game.currentLevel = level
        Game.currentLevel.camera = Game.camera
        Config.InternalSetTileMap(Game.currentLevel.map)

        if Game.currentLevel != None and Game.currentLevel.map is not None:
            Game.currentMenu = Game.inGameMenu
            pass

    @staticmethod
    def camera_configure(camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t = -l + Game.screen.get_width() / 2, -t + Game.screen.get_height() / 2

        l = min(0, l)  # Не выходим за левую границу
        l = max(-(camera.width - Game.screen.get_width()), l)  # Не выходим за правую границу
        t = max(-(camera.height - Game.screen.get_height()), t)  # Не выходим за нижнюю границу
        t = min(0, t)  # Не выходим за верхнюю границу

        return Rect(l, t, w, h)

    @staticmethod
    def DrawObjects():
        if Game.currentLevel is not None:
            Game.currentLevel.blit()

        if Game.currentMenu != None and Game.showMenu:
            Game.currentMenu.blit()

    @staticmethod
    def UpdateObjects():
        if Game.currentLevel is not None:
            Game.currentLevel.update()

        if Game.currentMenu != None and Game.showMenu:
            Game.currentMenu.update()

    @staticmethod
    def HandleEvents():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if not Game.showMenu:
                    Game.showMenu = True
                elif Game.currentLevel != None and Game.currentLevel.map is not None:
                    Game.showMenu = False

            # проверка нажатия
            if Game.currentLevel != None:
                Game.currentLevel.handle_event(event)

            if Game.currentMenu != None and Game.showMenu:
                Game.currentMenu.HandleEvent(event)

            if Game.currentLevel != None and Game.showMenu and Game.currentMenu is not None:
                Game.currentMenu.HandleEvent(event)

            if Game.eventHandler is not None:
                Game.eventHandler(event)

    @staticmethod
    def Quit(**kwargs):
        sys.exit()

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