import datetime
import json
import pathlib

from Tiles.TileMap import TileMap
from Tiles.Tile import Tile
from Tiles.HardTile import HardTile
from Tiles.MovableTile import MovableTile
from Tiles.InteractiveTile import InteractiveTile
from Menu.Menu import Menu
from LevelLoader import LevelLoader
from Serialization import Serialization
from Game import Game
import pygame
import glob
from pygame.sprite import Group

# TODO - добавить слои (2)
# TODO - добавить предпросмотр тайла, которым рисуем
# TODO - добавить просмотр слоя, на котором рисуем

class MapGenerator:
    __currentTileMap: TileMap = None
    __map: Group = None
    __filePath = None
    __imgNames = []
    __tileTypes = (Tile, HardTile, InteractiveTile, MovableTile)
    __currentTextureIndex = 0
    __currentTileTypeIndex = 0
    __currentLayerIndex = 0
    __menu = None

    @staticmethod
    def Start():
        # MapGenerator.__map.sprites()[coord]
        # -1 - первый элемент с конца (последний)
        # При нажатии на какую-то кнопку менять слой __currentTileMap

        MapGenerator.InitImages()
        Game.InitializePygame()
        MapGenerator.__menu = Menu()
        MapGenerator.__map = MapGenerator.InitTileMap()
        Game.Initialize(tileMapsGroup=MapGenerator.__map, customEventHandler=MapGenerator.EventHandler)
        Game.customMenuHandler = MapGenerator.ShowMenu
        Game.Start()

    @staticmethod
    def InitTileMap():
        answer = input("Do you want to load exists map (y/n): ")
        MapGenerator.__filePath = input("Enter path to map: ")

        if answer == "y":
            map = LevelLoader.LoadLevel(MapGenerator.__filePath)
        else:
            map = Group()
            map.add(TileMap())
            map.add(TileMap())

        allTileMaps = map.sprites()

        if len(allTileMaps) == 0:
            print("There were no TileMaps in list. Two default TileMaps will be autogenerated.")
            map.add(TileMap())
            map.add(TileMap())

        MapGenerator.__currentTileMap = map.sprites()[0]

        return map
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
            MapGenerator.__menu.Update()
            MapGenerator.__menu.Blitme()

    @staticmethod
    def SaveMap():
        filePath = MapGenerator.__filePath

        # сериализовать тайлмэп
        serMap = Serialization.SerializeMap(MapGenerator.__map)

        # записать сериализованный тайлмэп в файл через библиотеку json
        with open(filePath, 'w') as file:
            json.dump(serMap, file)

        # вывести на экран сообщение с датой и временем, что произошло сохранение
        print(f"[{datetime.datetime.now()}] Map saved to {filePath}")

    @staticmethod
    def EventHandler(event):
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
            elif  event.button == 3:
                MapGenerator.__currentTileMap.RemoveTile(x_abs, y_abs)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                # [text1, text2, text3]
                #          ind
                if MapGenerator.__currentTextureIndex < len(MapGenerator.__imgNames) - 1:
                    MapGenerator.__currentTextureIndex += 1
                else:
                    MapGenerator.__currentTextureIndex = 0
            elif event.key == pygame.K_q:
                if MapGenerator.__currentTextureIndex > 0:
                    MapGenerator.__currentTextureIndex -= 1
            elif event.key == pygame.K_2:
                if MapGenerator.__currentTileTypeIndex < len(MapGenerator.__tileTypes) - 1:
                    MapGenerator.__currentTileTypeIndex += 1
                else:
                    MapGenerator.__currentTileTypeIndex = 0
            elif event.key == pygame.K_1:
                if MapGenerator.__currentTileTypeIndex > 0:
                    MapGenerator.__currentTileTypeIndex -= 1
            elif event.key == pygame.K_F5:
                MapGenerator.SaveMap()
            elif event.key == pygame.K_F1 or event.key == pygame.K_F2:
                if event.key == pygame.K_F1 and MapGenerator.__currentLayerIndex > 0:
                    MapGenerator.__currentLayerIndex -= 1
                elif event.key == pygame.K_F2 and MapGenerator.__currentLayerIndex < 4:  # TODO - сделать так, чтобы можно было управлять слоями через меню
                    MapGenerator.__currentLayerIndex += 1

                    if len(MapGenerator.__map.sprites()) < MapGenerator.__currentLayerIndex + 1:
                        MapGenerator.__map.add(TileMap())
                        print("New layer added.")

                MapGenerator.__currentTileMap = MapGenerator.__map.sprites()[MapGenerator.__currentLayerIndex]
            elif event.key == pygame.K_ESCAPE:
                MapGenerator.__menu.need_show = not MapGenerator.__menu.need_show


if __name__ == "__main__":
    MapGenerator.Start()