from pygame.sprite import Group
class Serialization:

    @staticmethod
    def SerializeTile(tile): # указал явно что надо передавать
        return {"texture": tile.texture, "x": tile.rect.left, "y": tile.rect.top}

    @staticmethod
    def SerializeTileMap(tileMap):
        data = {}

        for el in tileMap.group.sprites():
            ser = Serialization.SerializeTile(el)
            ser["x"] = ser["x"] // tileMap.width
            ser["y"] = ser["y"] // tileMap.height

            tileType = el.__class__.__name__

            tilesOfType = data.get(tileType)

            if tilesOfType is None:
                tilesOfType = []
                data[tileType] = tilesOfType

            tilesOfType.append(ser)

        print(data)
        return data

    @staticmethod
    def SerializeMap(map:Group):
        data = {}

        tileMaps = map.sprites()

        for i in range(len(tileMaps)):
            tileMap = tileMaps[i]
            layerName = f"layer_{i}"
            ser = Serialization.SerializeTileMap(tileMap)
            data[layerName] = ser

        return data