import pygame
from Config import Config
from pygame.sprite import Sprite

class Tile(Sprite):
    #def __init__(self, texture,width=0,height=0,x=0,y=0):
    def __init__(self, **kwargs):   # TODO - также хранить абстрактные координаты!
        """
        Класс базового тайла.

        :param kwargs:
        - texture - путь к текстуре в формате png
        - width - ширина текстуры
        - height - высота текстуры
        - x - реальные координаты объекта
        - y - реальные координаты объекта
        """
        super().__init__()
        self.texture = kwargs["texture"]
        self.image = self.LoadImage(kwargs["texture"],kwargs.get("width", 0),kwargs.get("height",0))
        self.rect = self.image.get_rect()
        self.Pos(kwargs.get("x",0), kwargs.get("y",0))

    def Pos(self,x,y):
        self.rect.left = x
        self.rect.top = y

    def blit(self, func=None):
        f = self.rect
        if func is not None:
            f = func(self)


        Config.get_Screen().blit(self.image, f)

    def update(self):
        pass

    def UpdateParams(self, width=None, height=None, x=None, y=None):
        newWidth = Tile.GetParam(width, self.image.get_width())
        newHeight = Tile.GetParam(height, self.image.get_height())
        newX = Tile.GetParam(x,  self.rect.left)
        newY = Tile.GetParam(y, self.rect.top)
        self.image = self.LoadImage(self.texture, newWidth, newHeight)
        self.rect.width = newWidth
        self.rect.height = newHeight
        self.Pos(newX, newY)

    @staticmethod
    def GetParam(newParam, default):
        if newParam is None:
            return default
        return newParam

    def LoadImage(self, texture, width, height):
        image = pygame.image.load(f"images/{texture}").convert_alpha()
        image = pygame.transform.scale(image, (width, height))
        return image

    @staticmethod
    def Deserialize(data:dict):
        texture = data["texture"]
        x_abs = data["x"]
        y_abs = data["y"]
        tile = Tile(texture=texture, x=x_abs, y=y_abs)  # Передаем абстрактные координаты, т.к. мы не знаем ширину и
                                                # высоту абстрактной координатной сетки
        return tile