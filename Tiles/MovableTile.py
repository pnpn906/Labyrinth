from Tiles.HardTile import HardTile

class MovableTile(HardTile):
    def __init__(self, **kwargs):
        """
               Класс базового тайла.

               :param kwargs:
               - texture - путь к текстуре в формате png
               - width - ширина текстуры
               - height - высота текстуры
               - x - реальные координаты объекта
               - y - реальные координаты объекта
       """
        super().__init__(**kwargs)
