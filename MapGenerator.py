import datetime
import json
import pathlib

from UiElements.ItemSelector import ItemSelector
from Tiles.TileMap import TileMap
from Tiles.Tile import Tile
from Tiles.HardTile import HardTile
from Tiles.MovableTile import MovableTile
from Tiles.InteractiveTile import InteractiveTile
from UiElements.Menu import Menu
from UiElements.Button import Text, Button
from UiElements.Image import Image
from LevelLoader import LevelLoader
from Serialization import Serialization
from Game import Game
import pygame
import glob
from pygame.sprite import Group
from Levels.Level import Level

# TODO - добавить слои (2)
# TODO - добавить предпросмотр тайла, которым рисуем
# TODO - добавить просмотр слоя, на котором рисуем

class MapGenerator:
    __currentTileMap: TileMap = None
    __level: Level = None
    __filePath = None
    __imgNames = []
    __tileTypes = (Tile, HardTile, InteractiveTile, MovableTile)
    __currentTextureIndex = 0
    __currentTileTypeIndex = 0
    __currentLayerIndex = 0
    __menu = None

    __itemSelector : ItemSelector = None
    __typeSelector : ItemSelector = None

    @staticmethod
    def Start():
        # MapGenerator.__map.sprites()[coord]
        # -1 - первый элемент с конца (последний)
        # При нажатии на какую-то кнопку менять слой __currentTileMap

        MapGenerator.InitImages()
        Game.InitializePygame()
        MapGenerator.__menu = Menu("Creator Form", 500, 1000, (255,255,255), 1400,50)

        # <editor-fold desc="MENU BLOCK LAYER">

        # Создаем подменю для изменения слоя рисования, добавляем его в меню
        subMenuLayer = Menu("Layer selection", 400, 100, (0, 0, 255), orientation="horizontal")
        MapGenerator.__menu.AddUiElemnt(subMenuLayer)

        # Создаем текстовый блок (+,- и кнопку), добавляем их в подменю
        btnPlus = Button("+", 20, 20, 20, (243, 243, 243))
        btnPlus.BindAction(MapGenerator.IncrLayer)

        btnMenus = Button("-", 20, 20, 20, (243, 243, 243))
        btnMenus.BindAction(MapGenerator.DecrLayer)

        MapGenerator.__textQuantity = Text(str(MapGenerator.__currentLayerIndex), 20)

        subMenuLayer.AddUiElemnt(btnMenus)
        subMenuLayer.AddUiElemnt(MapGenerator.__textQuantity)
        subMenuLayer.AddUiElemnt(btnPlus)

        # </editor-fold>

        # <editor-fold desc="MENU BLOCK TILE">

        subMenuTile = Menu("Tile selection", 400, 150, (0, 0, 255), orientation="horizontal")
        MapGenerator.__menu.AddUiElemnt(subMenuTile)

        imgGroup = pygame.sprite.Group()

        for img in MapGenerator.__imgNames:
            imgObj = Image(f"images/{img}", (255, 0, 0), 30, 30)
            imgObj.BindAction(MapGenerator.__update_current_texture_index)
            imgGroup.add(imgObj)

        itemSelector = ItemSelector(imgGroup, 350, 250)
        subMenuTile.AddUiElemnt(itemSelector)
        MapGenerator.__itemSelector = itemSelector

        # </editor-fold>

        # <editor-fold desc="MENU BLOCK Type">

        subMenuType = Menu("Type selection", 400, 150, (0, 0, 255), orientation="horizontal")
        MapGenerator.__menu.AddUiElemnt(subMenuType)

        TextGroup = pygame.sprite.Group()

        for _type in MapGenerator.__tileTypes:
            textObj = Text(_type.__name__,20)
            textObj.BindAction(MapGenerator.__update_current_type_index)
            TextGroup.add(textObj)

        typeSelector = ItemSelector(TextGroup, 350, 250)
        subMenuType.AddUiElemnt(typeSelector)
        MapGenerator.__typeSelector = typeSelector

        # </editor-fold>

        MapGenerator.__level = MapGenerator.InitLevel()
        Game.Initialize(levelArg=MapGenerator.__level, customEventHandler=MapGenerator.EventHandler, showMenu = False)
        Game.customMenuHandler = MapGenerator.ShowMenu
        Game.Start()

    @staticmethod
    def IncrLayer():
        print("Incremented")
        if MapGenerator.__currentLayerIndex < 4:  # TODO - сделать так, чтобы можно было управлять слоями через меню
            MapGenerator.__currentLayerIndex += 1

            if len(MapGenerator.__level.map.sprites()) < MapGenerator.__currentLayerIndex + 1:
                MapGenerator.__level.map.add(TileMap())
                print("New layer added.")

            MapGenerator.__textQuantity.UpdateText(str(MapGenerator.__currentLayerIndex))

        MapGenerator.__currentTileMap = MapGenerator.__level.map.sprites()[MapGenerator.__currentLayerIndex]

    @staticmethod
    def DecrLayer():
        print("Decremented")
        if MapGenerator.__currentLayerIndex > 0:
            MapGenerator.__currentLayerIndex -= 1

            MapGenerator.__textQuantity.UpdateText(str(MapGenerator.__currentLayerIndex))

        MapGenerator.__currentTileMap = MapGenerator.__level.map.sprites()[MapGenerator.__currentLayerIndex]


    @staticmethod
    def InitLevel():
        answer = input("Do you want to load exists map (y/n): ")
        # answer = "n"
        MapGenerator.__filePath = "Maps\\" + input("Enter map file name: ")
        #MapGenerator.__filePath = "test.json"

        level = None

        if answer == "y":
            level = LevelLoader.LoadLevel(0, MapGenerator.__filePath)
        else:
            level = Level(0, None, Group())
            level.map.add(TileMap())
            level.map.add(TileMap())

        allTileMaps = level.map.sprites()

        if len(allTileMaps) == 0:
            print("There were no TileMaps in list. Two default TileMaps will be autogenerated.")
            level.map.add(TileMap())
            level.map.add(TileMap())

        MapGenerator.__currentTileMap = level.map.sprites()[0]

        return level
    @staticmethod
    def InitImages():
        for path in glob.glob("images/*.png"):
            imgName = pathlib.Path(path).name
            MapGenerator.__imgNames.append(imgName)
        print(MapGenerator.__imgNames)
    @staticmethod
    def ShowMenu():
        #texture = MapGenerator.__imgNames[MapGenerator.__currentTextureIndex]
        #tile = Tile(texture=texture, width=20,height=20,x=10,y=10)

        #tile.update()
        #tile.Blitme()
        if MapGenerator.__menu.need_show == True:
            MapGenerator.__menu.update()
            MapGenerator.__menu.blit()

    @staticmethod
    def SaveMap():
        filePath = MapGenerator.__filePath

        # сериализовать тайлмэп
        serMap = Serialization.SerializeMap(MapGenerator.__level.map)

        # записать сериализованный тайлмэп в файл через библиотеку json
        with open(filePath, 'w') as file:
            json.dump(serMap, file)

        # вывести на экран сообщение с датой и временем, что произошло сохранение
        print(f"[{datetime.datetime.now()}] Map saved to {filePath}")

    @staticmethod
    def __update_current_texture_index(**args):
        newTexturePath = args.get("texture", None)

        if newTexturePath is None:
            return

        for coord in range(len(MapGenerator.__imgNames)):
            if newTexturePath.endswith(MapGenerator.__imgNames[coord]): # TODO - endswith не надежно
                MapGenerator.__currentTextureIndex = coord
                return

    @staticmethod
    def __update_current_type_index(**args):
        newTextType = args.get("text", None)

        if newTextType is None:
            return

        for coord in range(len(MapGenerator.__tileTypes)):
            # Tile, HardTile, InteractiveTile, MovableTile
            if newTextType == MapGenerator.__tileTypes[coord].__name__:
                MapGenerator.__currentTileTypeIndex = coord
                return

    @staticmethod
    def HandleMapGenEvent(event):
        """
        Обработка события связанного с генерацией карты
        - простановка тайлов, удаление их и т.п.
        :param event:  Событие.
        :return: True в случае обработки, иначе False.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos  # (0,1) - кортеж, в х положится 0, в у положится 1
            x_abs = x // MapGenerator.__currentTileMap.width
            y_abs = y // MapGenerator.__currentTileMap.height

            if event.button == 1:
                texture = MapGenerator.__imgNames[MapGenerator.__currentTextureIndex]
                tileType = MapGenerator.__tileTypes[MapGenerator.__currentTileTypeIndex]
                tile = tileType(texture=texture)
                MapGenerator.__currentTileMap.RemoveTile(x_abs, y_abs)
                MapGenerator.__currentTileMap.AddTile(tile, x_abs, y_abs)

                return True
            elif event.button == 3:
                MapGenerator.__currentTileMap.RemoveTile(x_abs, y_abs)

                return True

        return False

    @staticmethod
    def HandleControlPanelEvent(event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                # [text1, text2, text3]
                #          ind
                # TODO - сделать так, чтобы не только карент текстур индекс менялся, но и выделение на селекторе
                if MapGenerator.__currentTextureIndex < len(MapGenerator.__imgNames) - 1:
                    MapGenerator.__currentTextureIndex += 1
                else:
                    MapGenerator.__currentTextureIndex = 0

                MapGenerator.__itemSelector.SelectItemByCoord(MapGenerator.__currentTextureIndex)
                return True
            elif event.key == pygame.K_q:
                if MapGenerator.__currentTextureIndex > 0:
                    MapGenerator.__currentTextureIndex -= 1

                    MapGenerator.__itemSelector.SelectItemByCoord(MapGenerator.__currentTextureIndex)

                    return True
            elif event.key == pygame.K_2:
                if MapGenerator.__currentTileTypeIndex < len(MapGenerator.__tileTypes) - 1:
                    MapGenerator.__currentTileTypeIndex += 1
                else:
                    MapGenerator.__currentTileTypeIndex = 0

                MapGenerator.__typeSelector.SelectItemByCoord(MapGenerator.__currentTileTypeIndex)
                return True
            elif event.key == pygame.K_1:
                if MapGenerator.__currentTileTypeIndex > 0:
                    MapGenerator.__currentTileTypeIndex -= 1
                    MapGenerator.__typeSelector.SelectItemByCoord(MapGenerator.__currentTileTypeIndex)

                    return True
            elif event.key == pygame.K_F5:
                MapGenerator.SaveMap()

                return True
            elif event.key == pygame.K_F1 or event.key == pygame.K_F2:
                if event.key == pygame.K_F1:
                    MapGenerator.DecrLayer()
                elif event.key == pygame.K_F2:  # TODO - сделать так, чтобы можно было управлять слоями через меню
                    MapGenerator.IncrLayer()
                else:
                    return False

                return True

            elif event.key == pygame.K_ESCAPE:
                MapGenerator.__menu.need_show = not MapGenerator.__menu.need_show
                return True

    @staticmethod
    def HandleMenuEvent(event):
        handled = False

        if (MapGenerator.__menu.need_show):
            handled = MapGenerator.__menu.HandleEvent(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos

                if MapGenerator.__menu.CheckPressed(x, y):
                    handled = True

        return handled

    @staticmethod
    def EventHandler(event):
        handled = MapGenerator.HandleMenuEvent(event)

        if not handled:
            MapGenerator.HandleMapGenEvent(event)

        MapGenerator.HandleControlPanelEvent(event)


if __name__ == "__main__":
    MapGenerator.Start()