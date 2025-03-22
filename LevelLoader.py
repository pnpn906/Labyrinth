import pygame.sprite
from os import listdir

from Tiles.Tile import Tile
from Tiles.TileMap import TileMap
from Tiles.HardTile import HardTile
from Tiles.InteractiveTile import InteractiveTile
from Tiles.MovableTile import MovableTile
import json
from Levels.Level import Level

class LevelLoader:
    @staticmethod
    def __loadData(filePath):
        with open(filePath, "r") as file:
            return json.load(file)

    @staticmethod
    def __deserializeMapSection(section:dict):
        tileMap = TileMap()

        for type in section.keys():
            listOfTiles = section[type]

            for tileData in listOfTiles:
                texture = tileData["texture"]
                x = tileData["x"]
                y = tileData["y"]

                tile = None
                if type == HardTile.__name__:
                    tile = HardTile(texture=texture, x=x, y=y)
                elif type == MovableTile.__name__:
                    tile = MovableTile(texture=texture, x=x, y=y)
                elif type == InteractiveTile.__name__:
                    tile = InteractiveTile(texture=texture, x=x, y=y)
                else:
                    tile = Tile(texture=texture, x=x, y=y)

                tileMap.AddTile(tile, x, y)

        return tileMap

    @staticmethod
    def GetListOfLevelMaps():
        list = listdir("Maps")
        return list

    @staticmethod
    def LoadLevel(lvl, mapPath=None, player=None, en=None):
        """
        Подгруажет уровень.

        json format:
        {
            "layer_0":
            {
                "tile_type_0": [
                    {"texture": "path", "x": 0, "y": 0},
                    {"texture": "path", "x": 0, "y": 0},
                    {"texture": "path", "x": 0, "y": 0},
                    ...
                ],
                ...
            },
            ...
        }

        :param mapPath: Путь к файлу json с уровнем.
        :return: Группу с Tilemap.
        """

        result = Level(lvl, player = player)

        if en is not None:
            result.enemies = en

        tileMaps = pygame.sprite.Group()

        if mapPath is not None:
            data : dict = LevelLoader.__loadData(mapPath)

            for section, value in data.items():
                tileMap = LevelLoader.__deserializeMapSection(value)
                tileMaps.add(tileMap)

            result.map = tileMaps

        return result

if __name__ == "__main__":
    print(Tile.__name__)